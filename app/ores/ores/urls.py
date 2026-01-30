"""
URL configuration for the Ores app.
Maps URLs to corresponding view classes for CRUD operations.
"""
from django.urls import path
from . import views

app_name = 'ores'

urlpatterns = [
    # List view - /ores/
    path('', views.OreListView.as_view(), name='ore_list'),
    
    # Detail view - /ores/<uuid>/
    path('<uuid:pk>/', views.OreDetailView.as_view(), name='ore_detail'),
    
    # Create view - /ores/create/
    path('create/', views.OreCreateView.as_view(), name='ore_create'),
    
    # Update view - /ores/<uuid>/update/
    path('<uuid:pk>/update/', views.OreUpdateView.as_view(), name='ore_update'),
    
    # Delete view - /ores/<uuid>/delete/
    path('<uuid:pk>/delete/', views.OreDeleteView.as_view(), name='ore_delete'),
]