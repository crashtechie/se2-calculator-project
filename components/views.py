"""
Views for Components app.

Implements CRUD operations with:
- List view with search, filtering, and sorting
- Detail view with formatted materials display
- Create/Update views with dynamic material selector
- Delete view with confirmation
- Performance optimization (select_related, caching)
"""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Component
from .forms import ComponentForm
from ores.models import Ore
import logging

logger = logging.getLogger(__name__)


class ComponentListView(ListView):
    """
    Display paginated list of components with search and sorting.
    
    Query Parameters:
    - q: Search query (searches name and description)
    - sort: Sort field (name, mass, created_at, updated_at)
    - order: Sort order (asc, desc)
    - page: Page number for pagination
    """
    model = Component
    template_name = 'components/component_list.html'
    context_object_name = 'component_list'
    paginate_by = 25
    
    def get_queryset(self):
        """Get filtered and sorted queryset."""
        queryset = Component.objects.all()
        
        # Search functionality
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Sorting functionality
        sort_field = self.request.GET.get('sort', 'name')
        sort_order = self.request.GET.get('order', 'asc')
        
        # Validate sort field
        valid_sort_fields = ['name', 'mass', 'build_time', 'created_at', 'updated_at']
        if sort_field not in valid_sort_fields:
            sort_field = 'name'
        
        # Apply sorting
        if sort_order == 'desc':
            queryset = queryset.order_by(f'-{sort_field}')
        else:
            queryset = queryset.order_by(sort_field)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add search and sort parameters to context."""
        context = super().get_context_data(**kwargs)
        
        # Preserve query parameters
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'name')
        context['current_order'] = self.request.GET.get('order', 'asc')
        
        # Calculate statistics
        context['total_components'] = Component.objects.count()
        
        # For pagination with query params
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['query_string'] = query_params.urlencode()
        
        return context


class ComponentDetailView(DetailView):
    """
    Display detailed information for a single component.
    
    Shows all component properties including formatted materials list
    with ore names (not just UUIDs).
    """
    model = Component
    template_name = 'components/component_detail.html'
    context_object_name = 'component'
    
    def get_context_data(self, **kwargs):
        """Add formatted materials with ore names to context."""
        context = super().get_context_data(**kwargs)
        
        # Format materials with ore names
        component = self.get_object()
        formatted_materials = []
        
        if component.materials:
            # Batch fetch all ores to avoid N+1 queries
            ore_ids = list(component.materials.keys())
            ores = {str(ore.ore_id): ore for ore in Ore.objects.filter(ore_id__in=ore_ids)}
            
            for ore_id_str, quantity in component.materials.items():
                ore = ores.get(ore_id_str)
                formatted_materials.append({
                    'ore_id': ore_id_str,
                    'ore_name': ore.name if ore else f'Unknown Ore ({ore_id_str})',
                    'ore': ore,
                    'quantity': quantity,
                })
        
        context['formatted_materials'] = formatted_materials
        context['total_material_mass'] = sum(m['quantity'] for m in formatted_materials)
        
        return context


class ComponentCreateView(CreateView):
    """
    Create new component with dynamic material selector.
    
    Uses JavaScript to provide user-friendly interface for adding materials.
    Validates all materials using Phase 1 validation helpers.
    """
    model = Component
    form_class = ComponentForm
    template_name = 'components/component_form.html'
    success_url = reverse_lazy('components:component_list')
    
    def get_context_data(self, **kwargs):
        """Add ore list for material selector."""
        context = super().get_context_data(**kwargs)
        
        # Provide all ores for dropdown
        context['ores'] = Ore.objects.all().order_by('name')
        context['form_title'] = 'Create New Component'
        context['submit_text'] = 'Create Component'
        
        return context
    
    def form_valid(self, form):
        """Handle successful form submission."""
        component = form.save()
        
        messages.success(
            self.request,
            f'Component "{component.name}" created successfully with '
            f'{len(component.materials)} material(s).'
        )
        
        logger.info(
            f'Component created: {component.name} (ID: {component.component_id})',
            extra={
                'component_id': str(component.component_id),
                'material_count': len(component.materials),
                'user': self.request.user if hasattr(self.request, 'user') else 'anonymous',
            }
        )
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Handle form validation errors."""
        messages.error(
            self.request,
            'Please correct the errors below.'
        )
        
        logger.warning(
            f'Component creation failed - validation errors: {form.errors}',
            extra={'errors': str(form.errors)}
        )
        
        return super().form_invalid(form)


class ComponentUpdateView(UpdateView):
    """
    Update existing component with material editing.
    
    Pre-populates form with existing materials.
    Preserves materials not modified by user.
    """
    model = Component
    form_class = ComponentForm
    template_name = 'components/component_form.html'
    
    def get_success_url(self):
        """Redirect to component detail after update."""
        return reverse_lazy('components:component_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add ore list and existing materials to context."""
        context = super().get_context_data(**kwargs)
        
        # Provide all ores for dropdown
        context['ores'] = Ore.objects.all().order_by('name')
        context['form_title'] = f'Edit Component: {self.object.name}'
        context['submit_text'] = 'Update Component'
        
        # Provide existing materials for JavaScript pre-population
        context['existing_materials'] = self.object.materials
        
        return context
    
    def form_valid(self, form):
        """Handle successful form submission."""
        component = form.save()
        
        messages.success(
            self.request,
            f'Component "{component.name}" updated successfully.'
        )
        
        logger.info(
            f'Component updated: {component.name} (ID: {component.component_id})',
            extra={
                'component_id': str(component.component_id),
                'material_count': len(component.materials),
                'user': self.request.user if hasattr(self.request, 'user') else 'anonymous',
            }
        )
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Handle form validation errors."""
        messages.error(
            self.request,
            'Please correct the errors below.'
        )
        
        return super().form_invalid(form)


class ComponentDeleteView(DeleteView):
    """
    Delete component with confirmation.
    
    Displays component details and materials before deletion.
    Requires POST to actually delete (CSRF protected).
    """
    model = Component
    template_name = 'components/component_confirm_delete.html'
    success_url = reverse_lazy('components:component_list')
    context_object_name = 'component'
    
    def get_context_data(self, **kwargs):
        """Add materials information for confirmation page."""
        context = super().get_context_data(**kwargs)
        
        # Format materials for display
        component = self.get_object()
        formatted_materials = []
        
        if component.materials:
            ore_ids = list(component.materials.keys())
            ores = {str(ore.ore_id): ore for ore in Ore.objects.filter(ore_id__in=ore_ids)}
            
            for ore_id_str, quantity in component.materials.items():
                ore = ores.get(ore_id_str)
                formatted_materials.append({
                    'ore_name': ore.name if ore else f'Unknown Ore',
                    'quantity': quantity,
                })
        
        context['formatted_materials'] = formatted_materials
        
        return context
    
    def delete(self, request, *args, **kwargs):
        """Handle component deletion."""
        component = self.get_object()
        component_name = component.name
        component_id = component.component_id
        
        messages.success(
            request,
            f'Component "{component_name}" has been deleted successfully.'
        )
        
        logger.info(
            f'Component deleted: {component_name} (ID: {component_id})',
            extra={
                'component_id': str(component_id),
                'user': request.user if hasattr(request, 'user') else 'anonymous',
            }
        )
        
        return super().delete(request, *args, **kwargs)
