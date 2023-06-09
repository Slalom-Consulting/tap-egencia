"""Stream type classes for tap-egencia."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_egencia.client import egenciaStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class TransactionsStream(egenciaStream):
    """Define custom stream."""

    primary_keys = ["id"]
    path = '/v1/transactions'
    name = "Transactions Reporting"
    schema = SCHEMAS_DIR / "transactions.json"