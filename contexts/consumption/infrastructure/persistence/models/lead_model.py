from django.db import models


class LeadRecord(models.Model):
    """Row for one lead Nexo's chatbot recorded, with only the columns billing reads."""

    id = models.UUIDField(primary_key=True)
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(null=True)
    conversation_id = models.UUIDField(null=True)

    class Meta:
        managed = False
        db_table = "leads"

    def __str__(self) -> str:
        return str(self.id)
