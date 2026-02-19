"""
URL configuration for buildorders app.

This module defines URL patterns for BuildOrder CRUD operations.
All URLs use the 'buildorders:' namespace and 'pk' parameter for consistency
with Phase 2 patterns.
"""

from django.urls import path

from . import views

app_name = "buildorders"

urlpatterns = [
    path("", views.BuildOrderListView.as_view(), name="list"),
    path("<uuid:pk>/", views.BuildOrderDetailView.as_view(), name="detail"),
    path("create/", views.BuildOrderCreateView.as_view(), name="create"),
    path("<uuid:pk>/update/", views.BuildOrderUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete/", views.BuildOrderDeleteView.as_view(), name="delete"),
]
