from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.JobBoardView.as_view(), name="job_board"),
    path("add/", views.JobCreateView.as_view(), name="job_create"),
    path("list/", views.JobListView.as_view(), name="job_list"),
    path("api/vehicles-by-customer/", views.get_vehicles_by_customer, name="get_vehicles_by_customer"),
    path("<int:pk>/", views.JobDetailView.as_view(), name="job_detail"),
    path("<int:pk>/edit/", views.JobUpdateView.as_view(), name="job_edit"),
    path("<int:pk>/delete/", views.JobDeleteView.as_view(), name="job_delete"),
    path("<int:pk>/status/", views.update_job_status, name="job_update_status"),
    path("<int:pk>/attachment/<int:attachment_id>/delete/", views.delete_job_attachment, name="delete_attachment"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
