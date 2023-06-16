"""Stream type classes for tap-egencia."""

from __future__ import annotations

import requests

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from singer_sdk.helpers.jsonpath import extract_jsonpath

from tap_egencia.client import egenciaStream

from singer_sdk.typing import (
    PropertiesList,
    Property,
    StringType
)

from typing import Any, Dict, Iterable, Optional


from tap_egencia.schemas.get_transactions import (
    metadataObject,
    transactionsObject
)

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class TransactionsStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "transactions-api"
    schema = PropertiesList(
        Property("report_id", StringType),
        Property("metadata", metadataObject),
        Property("transactions", transactionsObject),
        ).to_dict()
    authenticator = None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        return [] if response.status_code == 400 else super().parse_response(response)
    
    def get_records(self, *args, **kwargs) -> Iterable[Dict[str, Any]]:
        authenticator = super().authenticator
        url_base = super().url_base
        
        self.path = "/bi/api/v1/transactions"
        start_date = self.config['start_date']
        end_date = self.config['end_date']

        session = requests.Session()
        session.headers = authenticator.auth_headers
        session.headers["Accept"] = "application/hal+json"
        session.headers["Content-Type"] = "application/json"

        self.body = {"start_date": f"{start_date}", "end_date": f"{end_date}"}

        post_transaction_request = session.prepare_request(
            requests.Request(
                method="POST",
                url= url_base + self.path,
                json=self.body
            )
        )

        post_transaction_response = self._request(post_transaction_request, None)
        report_id = post_transaction_response.json()["report_id"]
        total_pages = post_transaction_response.json()["metadata"]["total_pages"]

        self.path = f"/bi/api/v1/transactions/{report_id}?page={total_pages}"

        get_transaction_request = session.prepare_request(
            requests.Request(
                "GET",
                url_base + self.path,
            ),
        )

        get_transaction_response = self._request(get_transaction_request, None)
        
        return super().parse_response(get_transaction_response) 
