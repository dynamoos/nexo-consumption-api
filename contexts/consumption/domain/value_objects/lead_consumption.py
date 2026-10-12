from dataclasses import dataclass
from datetime import date
from uuid import UUID

from contexts.consumption.domain.value_objects.conversation_type import (
    ConversationType,
)
from contexts.consumption.domain.value_objects.lead_stage import LeadStage


@dataclass(frozen=True)
class LeadConsumption:
    """What one lead of a conversation used, on the day it was recorded."""

    day: date
    conversation_id: UUID
    lead_id: UUID
    stage: LeadStage

    @property
    def conversation_type(self) -> ConversationType:
        return self.stage.conversation_type
