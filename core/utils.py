from typing import Optional

from django.conf import settings

from .models import ActivityLog


def log_activity(user: Optional[object], action: str, object_type: str = "", object_id: Optional[object] = None, extra: str = ""):
    """Create an ActivityLog entry if logging is enabled.

    `user` may be None for system actions. `object_id` will be stringified.
    """
    if not getattr(settings, "ACTIVITY_LOGGING", False):
        return None

    oid = str(object_id) if object_id is not None else ""
    entry = ActivityLog.objects.create(
        user=(user if hasattr(user, "is_authenticated") else None),
        action=action,
        object_type=object_type or "",
        object_id=oid,
        extra=extra or "",
    )
    return entry
