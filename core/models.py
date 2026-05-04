from django.conf import settings
from django.db import models


class ActivityLog(models.Model):
    """Simple activity log for auditing important actions.

    Fields:
    - user: the Django user who performed the action (nullable for system actions)
    - action: short verb describing the action (created, updated, deleted, status_changed, etc.)
    - object_type: content type as a short string, e.g. 'Job', 'Customer'
    - object_id: integer id of the affected object (nullable)
    - extra: optional free-text details
    - timestamp: when the event happened
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=80)
    object_type = models.CharField(max_length=80, blank=True)
    object_id = models.CharField(max_length=64, blank=True)
    extra = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        who = self.user.username if self.user else "system"
        if self.object_type and self.object_id:
            return f"{self.timestamp.isoformat()} | {who} | {self.action} {self.object_type}#{self.object_id}"
        return f"{self.timestamp.isoformat()} | {who} | {self.action}"
