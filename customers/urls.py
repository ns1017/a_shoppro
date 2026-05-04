from django.urls import path

from . import views

urlpatterns = [
    path("", views.CustomerListView.as_view(), name="customer_list"),
    path("add/", views.CustomerCreateView.as_view(), name="customer_add"),
    path("<int:pk>/", views.CustomerDetailView.as_view(), name="customer_detail"),
    path("<int:pk>/edit/", views.CustomerUpdateView.as_view(), name="customer_edit"),
    path("vehicles/", views.VehicleListView.as_view(), name="vehicle_list"),
    path("vehicles/add/", views.VehicleCreateView.as_view(), name="vehicle_add"),
    path("vehicles/<int:pk>/edit/", views.VehicleUpdateView.as_view(), name="vehicle_edit"),
]
