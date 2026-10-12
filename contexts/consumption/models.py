"""The one module Django imports to find this context's tables."""

from contexts.consumption.infrastructure.persistence.models.lead_model import (
    LeadRecord,
)

__all__ = ["LeadRecord"]
