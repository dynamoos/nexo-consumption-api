from contexts.consumption.domain.repositories.consumption_repository import (
    ConsumptionRepository,
)
from contexts.consumption.domain.value_objects.date_range import DateRange

from .get_lead_consumption_query import GetLeadConsumptionQuery
from .get_lead_consumption_response import (
    GetLeadConsumptionResponse,
    LeadConsumptionItem,
)


class GetLeadConsumptionHandler:
    """Answers what each lead used within a span of days."""

    def __init__(self, consumption: ConsumptionRepository) -> None:
        self._consumption = consumption

    def execute(self, query: GetLeadConsumptionQuery) -> GetLeadConsumptionResponse:
        days = DateRange(query.start, query.end)
        return GetLeadConsumptionResponse(
            items=[
                LeadConsumptionItem(
                    day=row.day,
                    conversation_id=str(row.conversation_id),
                    lead_id=str(row.lead_id),
                    stage=row.stage.value,
                    conversation_type=row.conversation_type.value,
                )
                for row in self._consumption.find_within(days)
            ]
        )
