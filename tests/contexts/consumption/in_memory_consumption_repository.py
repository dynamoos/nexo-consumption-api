from contexts.consumption.domain.repositories.consumption_repository import (
    ConsumptionRepository,
)
from contexts.consumption.domain.value_objects.date_range import DateRange
from contexts.consumption.domain.value_objects.lead_consumption import (
    LeadConsumption,
)


class InMemoryConsumptionRepository(ConsumptionRepository):
    """Consumption kept in a list, for tests that have no database to read from."""

    def __init__(self, leads: list[LeadConsumption]) -> None:
        self._leads = leads

    def find_within(self, days: DateRange) -> list[LeadConsumption]:
        return [lead for lead in self._leads if days.start <= lead.day <= days.end]
