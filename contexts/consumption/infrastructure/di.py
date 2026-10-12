"""Where this context's pieces are put together, once, at startup."""

from collections.abc import Callable

from django.http import HttpResponse

from contexts.consumption.application.queries.get_lead_consumption_handler import (
    GetLeadConsumptionHandler,
)
from contexts.consumption.application.queries.get_monthly_consumption_handler import (
    GetMonthlyConsumptionHandler,
)

from .api.views import HealthView, LeadConsumptionView, MonthlyConsumptionView
from .persistence.repositories.django_consumption_repository import (
    DjangoConsumptionRepository,
)


def build_views() -> dict[str, Callable[..., HttpResponse]]:
    """Wire every view this context serves."""
    consumption = DjangoConsumptionRepository()

    return {
        "health": HealthView.as_view(),
        "get_lead_consumption": LeadConsumptionView.as_view(
            get_lead_consumption=GetLeadConsumptionHandler(consumption=consumption)
        ),
        "get_monthly_consumption": MonthlyConsumptionView.as_view(
            get_monthly_consumption=GetMonthlyConsumptionHandler(
                consumption=consumption
            )
        ),
    }
