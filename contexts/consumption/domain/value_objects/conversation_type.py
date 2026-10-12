from enum import StrEnum


class ConversationType(StrEnum):
    """How far a conversation went, which is what Nexo's billing charges for."""

    STARTED = "iniciada"
    PARTIAL = "parcial"
    COMPLETE = "completa"
