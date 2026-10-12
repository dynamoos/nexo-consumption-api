"""Where each context answers."""

from django.urls import URLPattern, URLResolver, include, path

urlpatterns: list[URLPattern | URLResolver] = [
    path("api/consumption/", include("contexts.consumption.infrastructure.api.urls")),
]
