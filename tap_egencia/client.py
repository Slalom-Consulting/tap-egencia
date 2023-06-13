"""REST client handling, including egenciaStream base class."""

from __future__ import annotations

import sys
import json
from pathlib import Path
from typing import Any, Callable, Iterable

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.streams import RESTStream

# from tap_egencia.auth import egenciaAuthenticator
from tap_egencia.auth import get_new_token

if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class egenciaStream(RESTStream):
    """egencia stream class."""

    @property
    def domain(self) -> str:
        return self.config.get["egencia_base_url"]
 
    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.next_page"  # Or override `get_next_page_token`.

    # @property
    # def authenticator(self) -> BearerTokenAuthenticator:
    #     """Return a new authenticator object."""
    #     access_token = get_new_token()
    #     return BearerTokenAuthenticator(self, access_token)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        token = get_new_token()

        headers['Authorization'] = f'Bearer {token}'
        headers['Accept'] = 'application/hal+json'
        headers['Content-Type'] = 'application/json'
        return headers
    
    def prepare_request_payload(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict | None:
        """Prepare the data payload for the REST API request."""
        
        body = {}
        body['start_date'] = self.config.get('start_date')
        body['end_date'] = self.config.get('end_date')
 
        return json.dumps(body)
        
    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())
        
    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.
        return row