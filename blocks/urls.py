"""
URL configuration for Blocks app.

Provides CRUD endpoints for Block model with UUID-based routing.
Follows ENH-0000005 (Ores) and ENH-0000006 (Components) URL pattern conventions.
"""
from django.urls import path
from . import views

app_name = 'blocks'

urlpatterns = [
    # List view - paginated with search and sorting
    path('', views.BlockListView.as_view(), name='block_list'),
    
    # Detail view - display individual block with components and resource chain
    path('<uuid:pk>/', views.BlockDetailView.as_view(), name='block_detail'),
    
    # Create view - dynamic component selection
    path('create/', views.BlockCreateView.as_view(), name='block_create'),
    
    # Update view - modify existing block with pre-populated components
    path('<uuid:pk>/update/', views.BlockUpdateView.as_view(), name='block_update'),
    
    # Delete view - confirmation before deletion
    path('<uuid:pk>/delete/', views.BlockDeleteView.as_view(), name='block_delete'),
]
