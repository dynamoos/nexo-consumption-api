import hmac

from django.conf import settings
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


class ServiceCaller:
    """The internal service on the other end of a request."""

    is_authenticated = True


class ServiceTokenAuthentication(BaseAuthentication):
    """Lets in only whoever presents the token this service gave its callers."""

    keyword = "Bearer"

    def authenticate(self, request: Request) -> tuple[ServiceCaller, None] | None:
        header = get_authorization_header(request).split()
        if not header or header[0].lower() != self.keyword.lower().encode():
            return None
        if len(header) != 2:
            raise AuthenticationFailed("Malformed authorization header.")

        expected = settings.SERVICE_TOKEN.encode()
        if not hmac.compare_digest(header[1], expected):
            raise AuthenticationFailed("Invalid token.")
        return ServiceCaller(), None

    def authenticate_header(self, request: Request) -> str:
        return self.keyword
