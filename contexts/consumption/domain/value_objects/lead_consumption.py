from dataclasses import dataclass
from datetime import UTC, date, datetime
from uuid import UUID

from contexts.consumption.domain.value_objects.conversation_type import (
    ConversationType,
)
from contexts.consumption.domain.value_objects.lead_stage import LeadStage


@dataclass(frozen=True)
class LeadConsumption:
    """What one lead of a conversation used, from the moment it was recorded."""

    registered_at: datetime
    conversation_id: UUID
    lead_id: UUID
    stage: LeadStage

    @property
    def day(self) -> date:
        return self.registered_at.astimezone(UTC).date()

    @property
    def conversation_type(self) -> ConversationType:
        return self.stage.conversation_type
