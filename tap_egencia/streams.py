"""Stream type classes for tap-egencia."""

from __future__ import annotations

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

    name = "tap-egencia"
    # url_base = '' may not need this
    path = '/bi/api/v1/transactions'
    primary_keys = ["id"]
    schema = PropertiesList(
        property("links", linksObject),
        property("metadata", metadataObject),
        property("report_id", StringType),
        property("transactions", transactionsObject),
    ).to_dict()