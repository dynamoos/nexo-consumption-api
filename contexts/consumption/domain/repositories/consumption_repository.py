from abc import ABC, abstractmethod

from contexts.consumption.domain.value_objects.date_range import DateRange
from contexts.consumption.domain.value_objects.lead_consumption import (
    LeadConsumption,
)


class ConsumptionRepository(ABC):
    """Where Nexo's recorded consumption is read from."""

    @abstractmethod
    def find_within(self, days: DateRange) -> list[LeadConsumption]:
        """The consumption of every lead recorded in the days, billable stages only."""
