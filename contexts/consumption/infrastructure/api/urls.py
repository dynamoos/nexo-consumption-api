from typing import cast

from django.apps import apps
from django.urls import path

from contexts.consumption.apps import ConsumptionConfig

consumption = cast(ConsumptionConfig, apps.get_app_config("consumption"))

urlpatterns = [
    path("health", consumption.views["health"], name="health"),
    path("leads", consumption.views["get_lead_consumption"], name="lead-consumption"),
    path(
        "monthly",
        consumption.views["get_monthly_consumption"],
        name="monthly-consumption",
    ),
]
