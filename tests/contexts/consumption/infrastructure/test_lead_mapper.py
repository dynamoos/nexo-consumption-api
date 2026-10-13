from datetime import UTC, date, datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

import pytest

from contexts.consumption.domain.value_objects.lead_stage import LeadStage
from contexts.consumption.infrastructure.persistence.mappers.lead_mapper import (
    to_domain,
)
from contexts.consumption.infrastructure.persistence.models.lead_model import (
    LeadRecord,
)


def a_record() -> LeadRecord:
    return LeadRecord(
        id=uuid4(),
        status="lead",
        created_at=datetime(2026, 9, 30, 12, 0, tzinfo=UTC),
        conversation_id=uuid4(),
    )


def test_a_billable_lead_is_rebuilt_with_its_identities() -> None:
    record = a_record()

    lead = to_domain(record)

    assert lead is not None
    assert lead.lead_id == record.id
    assert lead.conversation_id == record.conversation_id
    assert lead.stage is LeadStage.LEAD
    assert lead.registered_at == record.created_at
    assert lead.day == date(2026, 9, 30)


def test_the_day_a_lead_belongs_to_is_its_utc_day() -> None:
    record = a_record()
    record.created_at = datetime(
        2026, 9, 30, 20, 0, tzinfo=timezone(timedelta(hours=-5))
    )

    lead = to_domain(record)

    assert lead is not None
    assert lead.day == date(2026, 10, 1)


@pytest.mark.parametrize(
    ("field", "value"),
    [("status", "otro"), ("created_at", None), ("conversation_id", None)],
)
def test_a_lead_that_cannot_be_billed_is_nothing(field: str, value: Any) -> None:
    record = a_record()
    setattr(record, field, value)

    assert to_domain(record) is None
