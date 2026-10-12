from datetime import date
from uuid import uuid4

import pytest
from pytest_django import Settings
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from contexts.consumption.application.queries.get_lead_consumption_handler import (
    GetLeadConsumptionHandler,
)
from contexts.consumption.domain.repositories.consumption_repository import (
    ConsumptionRepository,
)
from contexts.consumption.domain.value_objects.date_range import DateRange
from contexts.consumption.domain.value_objects.lead_consumption import (
    LeadConsumption,
)
from contexts.consumption.domain.value_objects.lead_stage import LeadStage
from contexts.consumption.infrastructure.api.views import (
    HealthView,
    LeadConsumptionView,
)
from tests.contexts.consumption.in_memory_consumption_repository import (
    InMemoryConsumptionRepository,
)

TOKEN = "a-service-token"
SEPTEMBER = {"start": "2026-09-01", "end": "2026-09-30"}


class BrokenConsumptionRepository(ConsumptionRepository):
    def find_within(self, days: DateRange) -> list[LeadConsumption]:
        raise RuntimeError("the database is gone")


@pytest.fixture(autouse=True)
def service_token(settings: Settings) -> None:
    settings.SERVICE_TOKEN = TOKEN


def ask(
    repository: ConsumptionRepository,
    params: dict[str, str],
    token: str | None = TOKEN,
) -> Response:
    view = LeadConsumptionView.as_view(
        get_lead_consumption=GetLeadConsumptionHandler(consumption=repository)
    )
    headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"} if token else {}
    response = view(APIRequestFactory().get("/", params, **headers))
    response.render()
    return response


def test_a_caller_without_the_token_is_unauthorized() -> None:
    response = ask(InMemoryConsumptionRepository([]), SEPTEMBER, token=None)

    assert response.status_code == 401


def test_a_valid_request_answers_with_each_lead() -> None:
    lead = LeadConsumption(date(2026, 9, 3), uuid4(), uuid4(), LeadStage.LEAD)

    response = ask(InMemoryConsumptionRepository([lead]), SEPTEMBER)

    assert response.status_code == 200
    assert response.data == {
        "items": [
            {
                "day": "2026-09-03",
                "conversation_id": str(lead.conversation_id),
                "lead_id": str(lead.lead_id),
                "stage": "lead",
                "conversation_type": "completa",
            }
        ]
    }


def test_a_missing_date_is_a_bad_request() -> None:
    response = ask(InMemoryConsumptionRepository([]), {"start": "2026-09-01"})

    assert response.status_code == 400
    assert "end" in response.data


def test_a_range_that_ends_before_it_begins_is_refused() -> None:
    response = ask(
        InMemoryConsumptionRepository([]),
        {"start": "2026-09-30", "end": "2026-09-01"},
    )

    assert response.status_code == 400
    assert response["Content-Type"] == "application/problem+json"


def test_a_failure_of_the_service_is_not_the_callers_doing() -> None:
    response = ask(BrokenConsumptionRepository(), SEPTEMBER)

    assert response.status_code == 500
    assert response["Content-Type"] == "application/problem+json"
    assert "the database is gone" not in str(response.data)


def test_the_service_says_it_is_up_without_asking_for_the_token() -> None:
    response = HealthView.as_view()(APIRequestFactory().get("/"))

    assert response.status_code == 200
    assert response.data == {"status": "ok"}
