from typing import Any

import pytest
from pytest_django import Settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from contexts.consumption.infrastructure.api.authentication import (
    ServiceCaller,
    ServiceTokenAuthentication,
)

TOKEN = "a-service-token"


@pytest.fixture(autouse=True)
def service_token(settings: Settings) -> None:
    settings.SERVICE_TOKEN = TOKEN


def authenticate(**headers: Any) -> tuple[ServiceCaller, None] | None:
    request = Request(APIRequestFactory().get("/", **headers))
    return ServiceTokenAuthentication().authenticate(request)


@pytest.mark.parametrize("scheme", ["Bearer", "BEARER", "bearer"])
def test_the_right_token_lets_the_caller_in(scheme: str) -> None:
    result = authenticate(HTTP_AUTHORIZATION=f"{scheme} {TOKEN}")

    assert result is not None
    caller, _ = result
    assert caller.is_authenticated


@pytest.mark.parametrize("headers", [{}, {"HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNz"}])
def test_a_request_without_a_bearer_token_is_not_for_this_authentication(
    headers: dict[str, str],
) -> None:
    assert authenticate(**headers) is None


@pytest.mark.parametrize(
    "header", ["Bearer wrong", f"Bearer {TOKEN}x", f"Bearer {TOKEN[:-1]}"]
)
def test_a_wrong_token_is_refused(header: str) -> None:
    with pytest.raises(AuthenticationFailed):
        authenticate(HTTP_AUTHORIZATION=header)


@pytest.mark.parametrize("header", ["Bearer", f"Bearer {TOKEN} extra"])
def test_a_malformed_header_is_refused(header: str) -> None:
    with pytest.raises(AuthenticationFailed):
        authenticate(HTTP_AUTHORIZATION=header)


def test_a_refusal_asks_for_a_bearer_token() -> None:
    request = Request(APIRequestFactory().get("/"))

    assert ServiceTokenAuthentication().authenticate_header(request) == "Bearer"
