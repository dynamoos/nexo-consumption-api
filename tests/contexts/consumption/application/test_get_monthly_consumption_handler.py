from datetime import date
from uuid import uuid4

import pytest

from contexts.consumption.application.queries.get_monthly_consumption_handler import (
    GetMonthlyConsumptionHandler,
)
from contexts.consumption.application.queries.get_monthly_consumption_query import (
    GetMonthlyConsumptionQuery,
)
from contexts.consumption.application.queries.get_monthly_consumption_response import (
    MonthlyConsumptionItem,
)
from contexts.consumption.domain.errors.date_range_errors import InvalidDateRangeError
from contexts.consumption.domain.value_objects.lead_consumption import (
    LeadConsumption,
)
from contexts.consumption.domain.value_objects.lead_stage import LeadStage
from tests.contexts.consumption.in_memory_consumption_repository import (
    InMemoryConsumptionRepository,
)


def a_lead(day: date, stage: LeadStage) -> LeadConsumption:
    return LeadConsumption(
        day=day, conversation_id=uuid4(), lead_id=uuid4(), stage=stage
    )


def monthly(
    leads: list[LeadConsumption], start: date, end: date
) -> list[MonthlyConsumptionItem]:
    handler = GetMonthlyConsumptionHandler(
        consumption=InMemoryConsumptionRepository(leads)
    )
    return handler.execute(GetMonthlyConsumptionQuery(start=start, end=end)).items


def test_leads_are_counted_by_month_and_stage() -> None:
    items = monthly(
        [
            a_lead(date(2026, 9, 3), LeadStage.INITIAL),
            a_lead(date(2026, 9, 15), LeadStage.INITIAL),
            a_lead(date(2026, 9, 15), LeadStage.LEAD),
            a_lead(date(2026, 10, 2), LeadStage.INITIAL),
        ],
        date(2026, 9, 1),
        date(2026, 10, 31),
    )

    assert [(i.month, i.stage, i.conversation_type, i.quantity) for i in items] == [
        ("2026-09", "inicial", "iniciada", 2),
        ("2026-09", "lead", "completa", 1),
        ("2026-10", "inicial", "iniciada", 1),
    ]


def test_leads_outside_the_range_are_left_out() -> None:
    items = monthly(
        [
            a_lead(date(2026, 8, 31), LeadStage.INITIAL),
            a_lead(date(2026, 9, 1), LeadStage.INITIAL),
            a_lead(date(2026, 9, 30), LeadStage.INITIAL),
            a_lead(date(2026, 10, 1), LeadStage.INITIAL),
        ],
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    assert [(i.month, i.quantity) for i in items] == [("2026-09", 2)]


def test_a_span_with_no_leads_is_empty() -> None:
    assert monthly([], date(2026, 9, 1), date(2026, 9, 30)) == []


def test_a_range_that_ends_before_it_begins_is_refused() -> None:
    with pytest.raises(InvalidDateRangeError):
        monthly([], date(2026, 9, 30), date(2026, 9, 1))
