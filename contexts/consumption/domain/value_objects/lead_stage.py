import re
from enum import StrEnum

from contexts.consumption.domain.value_objects.conversation_type import (
    ConversationType,
)


class LeadStage(StrEnum):
    """Where a lead stands in Nexo's funnel, and so what it is billed as."""

    INITIAL = "inicial"
    PRELEAD = "prelead"
    LEAD = "lead"
    ENRICHED_LEAD = "lead enriquecido"

    @classmethod
    def parse(cls, recorded: str) -> LeadStage | None:
        """The stage a recorded status names, or nothing if it names none."""
        for stage, spelling in _SPELLINGS.items():
            if spelling.fullmatch(recorded):
                return stage
        return None

    @property
    def conversation_type(self) -> ConversationType:
        """The kind of conversation this stage is charged as."""
        match self:
            case LeadStage.INITIAL:
                return ConversationType.STARTED
            case LeadStage.PRELEAD:
                return ConversationType.PARTIAL
            case LeadStage.LEAD | LeadStage.ENRICHED_LEAD:
                return ConversationType.COMPLETE


_SPELLINGS = {
    LeadStage.INITIAL: re.compile(r"inicial", re.IGNORECASE),
    LeadStage.PRELEAD: re.compile(r"pre[\s_-]?lead", re.IGNORECASE),
    LeadStage.LEAD: re.compile(r"lead", re.IGNORECASE),
    LeadStage.ENRICHED_LEAD: re.compile(r"lead[\s_-]?enriquecido", re.IGNORECASE),
}
