"""Stream type classes for tap-egencia."""

from __future__ import annotations

import os

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_egencia.client import egenciaStream

from singer_sdk.typing import (
    PropertiesList,
    Property,
    StringType,
)

from tap_egencia.schemas.reporting import (
    linksObject,
    metadataObject,
    transactionsObject
)

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class TransactionsStream(egenciaStream):
    """Define custom stream."""
    @property
    def egencia_base_url(self) -> str:
        return self.config['egencia_base_url']

    name = "transactions-api"
    url_base = egencia_base_url
    path = '/bi/api/v1/transactions'
    schema = PropertiesList(
        Property("links", linksObject),
        Property("metadata", metadataObject),
        Property("report_id", StringType),
        Property("transactions", transactionsObject),
        ).to_dict()
