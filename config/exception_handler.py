"""What a broken rule looks like once it has left the service."""

import logging
from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf

from contexts.consumption.domain.errors.date_range_errors import InvalidDateRangeError
from contexts.consumption.domain.errors.domain_error import DomainError

logger = logging.getLogger(__name__)

ANSWERS: dict[type[DomainError], int] = {
    InvalidDateRangeError: status.HTTP_400_BAD_REQUEST,
}


def problem(title: str, detail: str, code: int) -> Response:
    """Say what went wrong the way RFC 7807 asks for it."""
    return Response(
        {"title": title, "detail": detail, "status": code},
        status=code,
        content_type="application/problem+json",
    )


def handle(error: Exception, context: dict[str, Any]) -> Response:
    """Answer a broken rule with the code that names it.

    A rule broken by what the caller sent is the caller's doing. Only what
    the service itself got wrong deserves a 500.
    """
    answered = drf(error, context)
    if answered is not None:
        return answered

    if isinstance(error, DomainError):
        return problem(
            "Refused",
            str(error),
            ANSWERS.get(type(error), status.HTTP_400_BAD_REQUEST),
        )

    logger.exception("nothing here knows what to do with this")
    return problem(
        "Unknown error",
        "Something here broke, and it is not your doing.",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
