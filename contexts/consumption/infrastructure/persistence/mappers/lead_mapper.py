from datetime import UTC

from contexts.consumption.domain.value_objects.lead_consumption import (
    LeadConsumption,
)
from contexts.consumption.domain.value_objects.lead_stage import LeadStage
from contexts.consumption.infrastructure.persistence.models.lead_model import (
    LeadRecord,
)


def to_domain(record: LeadRecord) -> LeadConsumption | None:
    """Rebuild what a lead used, or nothing when it cannot be billed."""
    stage = LeadStage.parse(record.status)
    if stage is None or record.created_at is None or record.conversation_id is None:
        return None

    return LeadConsumption(
        day=record.created_at.astimezone(UTC).date(),
        conversation_id=record.conversation_id,
        lead_id=record.id,
        stage=stage,
    )
