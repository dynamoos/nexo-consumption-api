from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class GetLeadConsumptionQuery:
    """A request for the consumption of every lead recorded in a span of days."""

    start: date
    end: date
