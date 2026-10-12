from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class LeadConsumptionItem:
    """One lead of a conversation, and what it is billed as."""

    day: date
    conversation_id: str
    lead_id: str
    stage: str
    conversation_type: str


@dataclass(frozen=True)
class GetLeadConsumptionResponse:
    """The consumption of every lead recorded in the span asked for."""

    items: list[LeadConsumptionItem]
