from django.urls import path

from .views import dashboard, calendar_events

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("calendar/events/", calendar_events, name="calendar_events"),
]
