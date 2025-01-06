"""Stream type classes for tap-egencia."""

from __future__ import annotations

from pathlib import Path
import json

from tap_egencia.client import egenciaStream

from singer_sdk import typing as th 

from typing import Any, Dict, Iterable

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class AirTransactionsStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "transactions-api"
    path = "/bi/api/v1/transactions/air"
    replication_key = "last_extracted_date"
    schema = th.PropertiesList(
        th.Property("last_extracted_date", th.DateTimeType),
        th.Property("traveler", 
                    th.ObjectType(
                    th.Property("name", th.StringType)
                    ),
        th.Property("line_of_business", th.StringType)
        )
    ).to_dict()
