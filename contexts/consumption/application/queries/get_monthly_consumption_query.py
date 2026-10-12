from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class GetMonthlyConsumptionQuery:
    """A request for the consumption of a span of days, summed by month."""

    start: date
    end: date
