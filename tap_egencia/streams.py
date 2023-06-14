"""Stream type classes for tap-egencia."""

from __future__ import annotations

import requests

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_egencia.client import egenciaStream

from singer_sdk.typing import (
    PropertiesList,
    Property,
    StringType,
)

from typing import Any, Dict, Iterable, Optional

from tap_egencia.schemas.reporting import (
    linksObject,
    metadataObject,
    transactionsObject
)

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class TransactionsStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "transactions-api"
    schema = PropertiesList(
        Property("links", linksObject),
        Property("metadata", metadataObject),
        Property("report_id", StringType),
        Property("transactions", transactionsObject),
        ).to_dict()
    authenticator = None
    url_base = ""
    
    def get_records(self, *args, **kwargs) -> Iterable[Dict[str, Any]]:
        authenticator = super().authenticator
        url_base = super().url_base
        
        self.path = "/bi/api/v1/transactions"
        start_date = self.config['start_date']
        end_date = self.config['end_date']

        session = requests.Session()
        session.headers = authenticator.auth_headers

        transaction_request = session.prepare_request(
            requests.Request(
                method="POST",
                url=f"{url_base}{self.path}",
                json={
                    "format": "json",
                    "fields": {"start_date": f"{start_date}", "end_date": f"{end_date}"},
                },
            )
        )

        return session.send(transaction_request)