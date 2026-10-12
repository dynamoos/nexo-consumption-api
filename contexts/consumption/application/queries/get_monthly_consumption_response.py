from dataclasses import dataclass


@dataclass(frozen=True)
class MonthlyConsumptionItem:
    """What was used in one month, in one stage of the funnel."""

    month: str
    stage: str
    conversation_type: str
    quantity: int


@dataclass(frozen=True)
class GetMonthlyConsumptionResponse:
    """The consumption of the span asked for, summed by month."""

    items: list[MonthlyConsumptionItem]
