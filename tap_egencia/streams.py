"""Stream type classes for tap-egencia."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_egencia.client import egenciaStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


# TODO: - Rename Stream to appropriately capture the dataStream and path. 
#       - Override `UsersStream` and `GroupsStream` with your own stream definition.
class UsersStream(egenciaStream):
    """Define custom stream."""

    primary_keys = ["id"]
    path = '/comments'
    name = "comments"
    schema = th.PropertiesList(
        th.Property("postId", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("email", th.StringType),
        th.Property("body", th.StringType),
    ).to_dict()
