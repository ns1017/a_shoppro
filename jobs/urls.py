from django.urls import path

from . import views

urlpatterns = [
    path("", views.JobBoardView.as_view(), name="job_board"),
    path("add/", views.JobCreateView.as_view(), name="job_create"),
    path("list/", views.JobListView.as_view(), name="job_list"),
    path("<int:pk>/", views.JobDetailView.as_view(), name="job_detail"),
    path("<int:pk>/edit/", views.JobUpdateView.as_view(), name="job_edit"),
    path("<int:pk>/delete/", views.JobDeleteView.as_view(), name="job_delete"),
    path("<int:pk>/status/", views.update_job_status, name="job_update_status"),
]
