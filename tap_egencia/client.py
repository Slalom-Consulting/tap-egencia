"""REST client handling, including egenciaStream base class."""

from __future__ import annotations

from pathlib import Path
from singer_sdk.streams import RESTStream

from tap_egencia.auth import Auth0Authenticator

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class egenciaStream(RESTStream):
    """egencia stream class."""

    @property
    def url_base(self) -> str:
        domain = self.config["egencia_base_url"]
        return domain

    @property
    def authenticator(self) -> Auth0Authenticator:
        """Return a new authenticator object."""
        return Auth0Authenticator.create_for_stream(self)
