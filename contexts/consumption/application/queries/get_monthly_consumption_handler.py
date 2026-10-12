from collections import Counter

from contexts.consumption.domain.repositories.consumption_repository import (
    ConsumptionRepository,
)
from contexts.consumption.domain.value_objects.date_range import DateRange

from .get_monthly_consumption_query import GetMonthlyConsumptionQuery
from .get_monthly_consumption_response import (
    GetMonthlyConsumptionResponse,
    MonthlyConsumptionItem,
)


class GetMonthlyConsumptionHandler:
    """Answers what was used each month, stage by stage."""

    def __init__(self, consumption: ConsumptionRepository) -> None:
        self._consumption = consumption

    def execute(
        self, query: GetMonthlyConsumptionQuery
    ) -> GetMonthlyConsumptionResponse:
        days = DateRange(query.start, query.end)
        totals = Counter(
            (row.day.strftime("%Y-%m"), row.stage)
            for row in self._consumption.find_within(days)
        )

        return GetMonthlyConsumptionResponse(
            items=[
                MonthlyConsumptionItem(
                    month=month,
                    stage=stage.value,
                    conversation_type=stage.conversation_type.value,
                    quantity=quantity,
                )
                for (month, stage), quantity in sorted(totals.items())
            ]
        )
