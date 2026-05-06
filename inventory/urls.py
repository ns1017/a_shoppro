from django.urls import path

from . import views

urlpatterns = [
    path("", views.PartListView.as_view(), name="part_list"),
    path("add/", views.PartCreateView.as_view(), name="part_add"),
    path("<int:pk>/edit/", views.PartUpdateView.as_view(), name="part_edit"),
    path("<int:pk>/delete/", views.PartDeleteView.as_view(), name="part_delete"),
]
