from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from contexts.consumption.application.queries.get_lead_consumption_handler import (
    GetLeadConsumptionHandler,
)
from contexts.consumption.application.queries.get_lead_consumption_query import (
    GetLeadConsumptionQuery,
)
from contexts.consumption.application.queries.get_monthly_consumption_handler import (
    GetMonthlyConsumptionHandler,
)
from contexts.consumption.application.queries.get_monthly_consumption_query import (
    GetMonthlyConsumptionQuery,
)
from contexts.consumption.infrastructure.api.serializers import (
    ConsumptionRangeSerializer,
    LeadConsumptionItemSerializer,
    MonthlyConsumptionItemSerializer,
)


class LeadConsumptionView(APIView):
    """The door the consumption of each lead is read from."""

    get_lead_consumption: GetLeadConsumptionHandler = None  # type: ignore[assignment]

    def __init__(self, get_lead_consumption: GetLeadConsumptionHandler) -> None:
        self.get_lead_consumption = get_lead_consumption
        super().__init__()

    def get(self, request: Request) -> Response:
        form = ConsumptionRangeSerializer(data=request.query_params)
        form.is_valid(raise_exception=True)

        response = self.get_lead_consumption.execute(
            GetLeadConsumptionQuery(
                start=form.validated_data["start"],
                end=form.validated_data["end"],
            )
        )
        return Response(
            {"items": LeadConsumptionItemSerializer(response.items, many=True).data}
        )


class MonthlyConsumptionView(APIView):
    """The door the consumption of each month is read from."""

    get_monthly_consumption: GetMonthlyConsumptionHandler = None  # type: ignore[assignment]

    def __init__(self, get_monthly_consumption: GetMonthlyConsumptionHandler) -> None:
        self.get_monthly_consumption = get_monthly_consumption
        super().__init__()

    def get(self, request: Request) -> Response:
        form = ConsumptionRangeSerializer(data=request.query_params)
        form.is_valid(raise_exception=True)

        response = self.get_monthly_consumption.execute(
            GetMonthlyConsumptionQuery(
                start=form.validated_data["start"],
                end=form.validated_data["end"],
            )
        )
        return Response(
            {"items": MonthlyConsumptionItemSerializer(response.items, many=True).data}
        )


class HealthView(APIView):
    """The door whoever keeps the service running asks if it is up."""

    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        return Response({"status": "ok"})
