"""
URL configuration for Components app.

Provides CRUD endpoints for Component model with UUID-based routing.
Follows ENH-0000005 (Ores) URL pattern conventions.
"""
from django.urls import path
from . import views

app_name = 'components'

urlpatterns = [
    # List view - paginated with search and sorting
    path('', views.ComponentListView.as_view(), name='component_list'),
    
    # Detail view - display individual component with materials
    path('<uuid:pk>/', views.ComponentDetailView.as_view(), name='component_detail'),
    
    # Create view - form with dynamic material selector
    path('create/', views.ComponentCreateView.as_view(), name='component_create'),
    
    # Update view - edit existing component and materials
    path('<uuid:pk>/update/', views.ComponentUpdateView.as_view(), name='component_update'),
    
    # Delete view - confirmation before deletion
    path('<uuid:pk>/delete/', views.ComponentDeleteView.as_view(), name='component_delete'),
]
