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
        data = response.json()
        if 'next' in data['_links']:
            return data['_links']['next']['href']
        else:
            return None

class egenciaStream(RESTStream):
    """egencia stream class."""

    report_id = ""
    records_jsonpath = "$[transactions][*]"

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
    
    def get_report_id(self,context):

        session = requests.Session()
        session.headers = self.authenticator.auth_headers
        session.headers["Accept"] = "application/hal+json"
        session.headers["Content-Type"] = "application/json"

        self.start_date = self.get_starting_timestamp(context)
        self.start_date = self.start_date.strftime("%Y-%m-%d %H:%M:%S")

        today = datetime.datetime.now()
        self.end_date = today.strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f'start_date: {self.start_date}, end_date {self.end_date}')
        self.body = {"start_date": f"{self.start_date}", "end_date": f"{self.end_date}"}

        post_transaction_request = session.prepare_request(
            requests.Request(method="POST", url=self.url_base + self.path, json=self.body)
        )
        post_transaction_response = self._request(post_transaction_request, None)

        if post_transaction_response.status_code != 201:
            raise Exception(f'Report was not created successfully. Status Code {post_transaction_response.status_code}')
        report_id = post_transaction_response.json()["report_id"]

        return report_id

    def get_url(self, context: Context | None) -> str:

        url = "".join([self.url_base, self.path or ""])
        self.logger.info(f"report_id: {self.report_id}")
        if self.report_id == "":
            self.report_id = self.get_report_id(context)
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