"""REST client handling, including egenciaStream base class."""

from __future__ import annotations
import json
from typing import Any, Dict, Iterable

import typing as t
import requests
import datetime
from urllib.parse import parse_qsl

from singer_sdk.helpers.jsonpath import extract_jsonpath
from pathlib import Path
from singer_sdk.streams import RESTStream
from singer_sdk.pagination import BaseHATEOASPaginator 

from tap_egencia.auth import Auth0Authenticator

if t.TYPE_CHECKING:
    import requests
    from singer_sdk_helpers.types import Auth, Context

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class HATEOASPaginator(BaseHATEOASPaginator):
    def get_next_url(self,response):
        # A missing _links block means there is no next page. Indexing it
        # directly turns a final page into a KeyError, which aborts the stream
        # and leaves the state file empty.
        links = response.json().get('_links', {})
        if 'next' in links:
            return links['next']['href']
        else:
            return None

class egenciaStream(RESTStream):
    """egencia stream class."""

    report_id = ""
    records_jsonpath = "$[transactions][*]"

    # Egencia rejects any report request spanning more than a year with a 400.
    # Clamping here keeps a stream recoverable after state loss: without it, a
    # blank state file falls back to the config start_date and every subsequent
    # run fails, because tapdance rewrites the state file empty on each crash.
    max_window_days = 364

    # Streams whose records only become available after an out-of-band
    # reconciliation lag cannot derive their window from the bookmark: the
    # bookmark tracks wall-clock extract time, so the next window sits in the
    # not-yet-reconciled future and always comes back empty. Those streams set
    # a rolling lookback instead of using the bookmark.
    lookback_days: int | None = None

    @property
    def url_base(self) -> str:
        return self.config["egencia_base_url"]

    @property
    def authenticator(self) -> Auth0Authenticator:
        """Return a new authenticator object."""
        return Auth0Authenticator.create_for_stream(self)

    def get_new_paginator(self) -> BaseHATEOASPaginator:
        return HATEOASPaginator()
    
    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        headers["accept"] = "application/hal+json"
        headers["Content-Type"] = "application/json"

        return headers
    
    def get_url_params(self, context, next_page_token) -> dict:

        params: dict = {}

        if next_page_token:
            self.logger.info(f'next_page_token: {next_page_token}')
            return dict(parse_qsl(next_page_token.query))
        else:
            self.logger.info('First Time Run')
            params['page'] = 1
        self.logger.info(f'PARAMS:{params}')
        return params
    
    def get_window(self, context) -> tuple[str, str]:
        """Return the (start_date, end_date) to request, clamped to the API's limit."""
        # Naive UTC throughout. The API and the bookmark both carry naive UTC, so
        # a naive local now() would skew the window by the container's offset -
        # invisible in prod only because that container happens to run in UTC.
        end = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

        if self.lookback_days is not None:
            start = end - datetime.timedelta(days=self.lookback_days)
        else:
            # Falls back to the config start_date, and is None when neither a
            # bookmark nor a start_date is set - start_date is not a required
            # setting. The bookmark is naive UTC on the wire, so drop the tzinfo
            # the SDK adds to keep it comparable with the naive end above.
            bookmark = self.get_starting_timestamp(context)
            start = bookmark.replace(tzinfo=None) if bookmark is not None else None

        earliest_allowed = end - datetime.timedelta(days=self.max_window_days)
        if start is None:
            self.logger.warning(
                f'No bookmark or start_date to sync from; requesting the widest '
                f'window the API allows ({self.max_window_days} days).'
            )
            start = earliest_allowed
        elif start < earliest_allowed:
            self.logger.warning(
                f'Requested start_date {start:%Y-%m-%d %H:%M:%S} is outside the API\'s '
                f'{self.max_window_days}-day window; clamping to '
                f'{earliest_allowed:%Y-%m-%d %H:%M:%S}.'
            )
            start = earliest_allowed

        return start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")

    def get_report_id(self,context) -> str | None:
        """Create a report and return its id, or None when it holds no records."""

        session = requests.Session()
        session.headers = self.authenticator.auth_headers
        session.headers["Accept"] = "application/hal+json"
        session.headers["Content-Type"] = "application/json"

        self.start_date, self.end_date = self.get_window(context)
        self.logger.info(f'start_date: {self.start_date}, end_date: {self.end_date}, lob: {self.lob}')
        self.body = {"start_date": f"{self.start_date}", "end_date": f"{self.end_date}"}
        if self.reconciled_records_only:
            self.body['reconciled_records_only'] = 'true'
        post_transaction_request = session.prepare_request(
            requests.Request(method="POST", url=self.url_base + self.path + self.lob, json=self.body)
        )
        post_transaction_response = self._request(post_transaction_request, None)

        # An empty report is a normal outcome, not a failure. Raising here used to
        # abort the stream, which left the bookmark wiped and forced the next run
        # into a full-history pull.
        if post_transaction_response.status_code == 204:
            self.logger.info(
                f'No {self.lob} records for {self.start_date} - {self.end_date}'
                f'{" (reconciled only)" if self.reconciled_records_only else ""}; '
                'nothing to sync.'
            )
            return None

        if post_transaction_response.status_code != 201:
            raise Exception(
                f'Report was not created successfully. Status Code '
                f'{post_transaction_response.status_code}: {post_transaction_response.text}'
            )

        self.logger.info(f'report metadata: {post_transaction_response.json().get("metadata")}')
        report_id = post_transaction_response.json()["report_id"]

        return report_id

    def get_records(self, context: Context | None) -> t.Iterable[dict]:
        """Yield records for this stream, or nothing when the report is empty."""
        report_id = self.get_report_id(context)
        if report_id is None:
            return

        self.report_id = report_id
        yield from super().get_records(context)

    def validate_response(self, response: requests.Response) -> None:
        """Log the API's error body before the SDK turns the status into an exception.

        Egencia explains its 4xx rejections in the body only, so without this the
        reason never reaches the container logs.
        """
        if 400 <= response.status_code < 500:
            self.logger.error(
                f'{response.status_code} from {response.request.url}: {response.text[:1000]}'
            )
        super().validate_response(response)

    def get_url(self, context: Context | None) -> str:

        url = "".join([self.url_base, self.path or ""])
        self.logger.info(f"report_id: {self.report_id}")
        url = f"{url}/{self.report_id}"
        self.logger.info(f'URL: {url}')
        return url
    
    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(
            self,
            row: dict,
            context: Context | None = None,  # noqa: ARG002
        ) -> dict | None:
            """As needed, append or transform raw data to match expected structure.

            Args:
                row: An individual record from the stream.
                context: The stream context.

            Returns:
                The updated record dictionary, or ``None`` to skip the record.
            """
            row['last_extracted_date'] = self.end_date
            return row