from datetime import UTC, date, datetime, time
from uuid import UUID, uuid4

import pytest

from contexts.consumption.application.queries.get_lead_consumption_handler import (
    GetLeadConsumptionHandler,
)
from contexts.consumption.application.queries.get_lead_consumption_query import (
    GetLeadConsumptionQuery,
)
from contexts.consumption.application.queries.get_lead_consumption_response import (
    LeadConsumptionItem,
)
from contexts.consumption.domain.errors.date_range_errors import InvalidDateRangeError
from contexts.consumption.domain.value_objects.lead_consumption import (
    LeadConsumption,
)
from contexts.consumption.domain.value_objects.lead_stage import LeadStage
from tests.contexts.consumption.in_memory_consumption_repository import (
    InMemoryConsumptionRepository,
)


def a_lead(
    day: date,
    stage: LeadStage,
    conversation_id: UUID | None = None,
    registered_at: datetime | None = None,
) -> LeadConsumption:
    return LeadConsumption(
        registered_at=registered_at or datetime.combine(day, time(12), tzinfo=UTC),
        conversation_id=conversation_id or uuid4(),
        lead_id=uuid4(),
        stage=stage,
    )


def per_lead(
    leads: list[LeadConsumption], start: date, end: date
) -> list[LeadConsumptionItem]:
    handler = GetLeadConsumptionHandler(
        consumption=InMemoryConsumptionRepository(leads)
    )
    return handler.execute(GetLeadConsumptionQuery(start=start, end=end)).items


def test_each_lead_of_a_conversation_is_its_own_line() -> None:
    conversation = uuid4()
    leads = [
        a_lead(date(2026, 9, 3), LeadStage.INITIAL, conversation),
        a_lead(date(2026, 9, 3), LeadStage.LEAD, conversation),
        a_lead(date(2026, 9, 3), LeadStage.ENRICHED_LEAD, conversation),
    ]

    items = per_lead(leads, date(2026, 9, 1), date(2026, 9, 30))

    assert {item.conversation_id for item in items} == {str(conversation)}
    assert [item.lead_id for item in items] == [str(lead.lead_id) for lead in leads]


def test_each_line_says_its_stage_and_what_it_is_billed_as() -> None:
    items = per_lead(
        [
            a_lead(date(2026, 9, 3), LeadStage.INITIAL),
            a_lead(date(2026, 9, 3), LeadStage.PRELEAD),
            a_lead(date(2026, 9, 3), LeadStage.ENRICHED_LEAD),
        ],
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    assert [(i.stage, i.conversation_type) for i in items] == [
        ("inicial", "iniciada"),
        ("prelead", "parcial"),
        ("lead enriquecido", "completa"),
    ]


def test_each_line_says_the_moment_it_was_registered() -> None:
    late_in_lima = datetime(2026, 9, 1, 0, 12, 5, tzinfo=UTC)

    items = per_lead(
        [a_lead(date(2026, 9, 1), LeadStage.INITIAL, registered_at=late_in_lima)],
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    assert items[0].registered_at == late_in_lima
    assert items[0].day == date(2026, 9, 1)


def test_leads_outside_the_range_are_left_out() -> None:
    inside = a_lead(date(2026, 9, 1), LeadStage.INITIAL)

    items = per_lead(
        [a_lead(date(2026, 8, 31), LeadStage.INITIAL), inside],
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    assert [item.lead_id for item in items] == [str(inside.lead_id)]


def test_a_span_with_no_leads_is_empty() -> None:
    assert per_lead([], date(2026, 9, 1), date(2026, 9, 30)) == []


def test_a_range_that_ends_before_it_begins_is_refused() -> None:
    with pytest.raises(InvalidDateRangeError):
        per_lead([], date(2026, 9, 30), date(2026, 9, 1))
