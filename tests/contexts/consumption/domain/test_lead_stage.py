import pytest

from contexts.consumption.domain.value_objects.conversation_type import (
    ConversationType,
)
from contexts.consumption.domain.value_objects.lead_stage import LeadStage


@pytest.mark.parametrize(
    ("recorded", "expected"),
    [
        ("inicial", LeadStage.INITIAL),
        ("prelead", LeadStage.PRELEAD),
        ("pre lead", LeadStage.PRELEAD),
        ("pre_lead", LeadStage.PRELEAD),
        ("PRE-Lead", LeadStage.PRELEAD),
        ("lead", LeadStage.LEAD),
        ("lead enriquecido", LeadStage.ENRICHED_LEAD),
        ("Lead_Enriquecido", LeadStage.ENRICHED_LEAD),
    ],
)
def test_a_recorded_status_names_its_stage(recorded: str, expected: LeadStage) -> None:
    assert LeadStage.parse(recorded) is expected


@pytest.mark.parametrize("recorded", ["", " lead", "lead\n", "pre  lead", "otro"])
def test_a_status_that_names_no_stage_is_nothing(recorded: str) -> None:
    assert LeadStage.parse(recorded) is None


@pytest.mark.parametrize(
    ("stage", "expected"),
    [
        (LeadStage.INITIAL, ConversationType.STARTED),
        (LeadStage.PRELEAD, ConversationType.PARTIAL),
        (LeadStage.LEAD, ConversationType.COMPLETE),
        (LeadStage.ENRICHED_LEAD, ConversationType.COMPLETE),
    ],
)
def test_each_stage_is_charged_as_one_type_of_conversation(
    stage: LeadStage, expected: ConversationType
) -> None:
    assert stage.conversation_type is expected
