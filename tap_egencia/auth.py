"""Auth0 Authentication."""

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


class Auth0Authenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Auth0."""

    @property
    def domain(self) -> str:
        return self.config["egencia_base_url"]

    @property
    def auth_endpoint(self) -> str:
        return f"{self.domain}/auth/v1/token"

    @property
    def client_id(self) -> str:
        return self.config["client_id"]

    @property
    def client_secret(self) -> str:
        return self.config["client_secret"]

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Auth0 API."""

        return {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

    @classmethod
    def create_for_stream(cls, stream) -> "Auth0Authenticator":
        return cls(
            stream=stream,
        )
