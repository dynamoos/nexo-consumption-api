from collections.abc import Callable

from django.apps import AppConfig
from django.http import HttpResponse


class ConsumptionConfig(AppConfig):
    """What Nexo's chatbot consumed, as billing needs to see it."""

    name = "contexts.consumption"
    verbose_name = "Consumption"

    views: dict[str, Callable[..., HttpResponse]]

    def ready(self) -> None:
        from contexts.consumption.infrastructure.di import build_views

        self.views = build_views()
