from typing import Any

from rest_framework import serializers


class ConsumptionRangeSerializer(serializers.Serializer[None]):
    """What a request for consumption has to say before it is trusted."""

    start = serializers.DateField()
    end = serializers.DateField()


class LeadConsumptionItemSerializer(serializers.Serializer[Any]):
    """What a browse of consumption shows about one lead."""

    day = serializers.DateField()
    conversation_id = serializers.CharField()
    lead_id = serializers.CharField()
    stage = serializers.CharField()
    conversation_type = serializers.CharField()


class MonthlyConsumptionItemSerializer(serializers.Serializer[Any]):
    """What a monthly summary shows about one stage of the funnel."""

    month = serializers.CharField()
    stage = serializers.CharField()
    conversation_type = serializers.CharField()
    quantity = serializers.IntegerField()
