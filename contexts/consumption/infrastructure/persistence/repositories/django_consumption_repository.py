from datetime import UTC, datetime, time, timedelta

from contexts.consumption.domain.repositories.consumption_repository import (
    ConsumptionRepository,
)
from contexts.consumption.domain.value_objects.date_range import DateRange
from contexts.consumption.domain.value_objects.lead_consumption import (
    LeadConsumption,
)
from contexts.consumption.infrastructure.persistence.mappers.lead_mapper import (
    to_domain,
)
from contexts.consumption.infrastructure.persistence.models.lead_model import (
    LeadRecord,
)


class DjangoConsumptionRepository(ConsumptionRepository):
    """Reads consumption straight from the leads Nexo's chatbot recorded."""

    def find_within(self, days: DateRange) -> list[LeadConsumption]:
        starts_at = datetime.combine(days.start, time.min, tzinfo=UTC)
        ends_before = datetime.combine(
            days.end + timedelta(days=1), time.min, tzinfo=UTC
        )

        records = (
            LeadRecord.objects.filter(
                conversation_id__isnull=False,
                created_at__gte=starts_at,
                created_at__lt=ends_before,
            )
            .only("id", "conversation_id", "status", "created_at")
            .order_by("created_at", "id")
        )

        consumption = (to_domain(record) for record in records)
        return [lead for lead in consumption if lead is not None]
