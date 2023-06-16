"""egencia tap class."""

from __future__ import annotations

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers


from tap_egencia.streams import (
    TransactionsStream,
)

STREAM_TYPES = [
    TransactionsStream,
]

class TapEgencia(Tap):
    """egencia tap class."""

    name = "tap-egencia"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The start record date to sync",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            description="The end record date to sync",
        ),
        th.Property(
            "egencia_base_url",
            th.StringType,
            description="The url for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[Stream]:  
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]    

if __name__ == "__main__":
    TapEgencia.cli()
