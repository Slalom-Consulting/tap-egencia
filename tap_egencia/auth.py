"""egencia Authentication."""

from __future__ import annotations

from tap_egencia.secret import secret 

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta

class egenciaAuthenticator(OAuthAuthenticator):
    """Authenticator class for egencia."""

    @property
    def domain(self) -> str:
        return self.config["domain"]
    
    @property
    def auth_endpoint():
        baseUrl = secret.get_secret('egenciaBaseUrl')
        return f"{baseUrl}/auth/v1/token"

    @property
    def oauth_request_body() -> dict:
        clientId = secret.get_secret('egenciaClientId')
        clientSecret = secret.get_secret('egenciaClientSecret')
  
        return {
            'client_id': clientId,
            'client_secret': clientSecret,
            "grant_type": "client_credentials",
        }

    @classmethod
    def create_for_stream(cls, stream) -> "egenciaAuthenticator":
        return cls(
            stream=stream,
        )