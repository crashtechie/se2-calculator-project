"""
Views for Blocks app.

Implements CRUD operations with:
- List view with search, filtering, and sorting
- Detail view with formatted components display and resource chain
- Create/Update views with dynamic component selector
- Delete view with confirmation
- Resource chain calculation (Block → Components → Ores)
- Performance optimization (select_related, caching)

Pattern follows ENH-0000005 (Ores) and ENH-0000006 (Components).
"""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.cache import cache
from .models import Block
from .forms import BlockForm
from components.models import Component
from ores.models import Ore
import logging
import json

logger = logging.getLogger(__name__)


class BlockListView(ListView):
    """
    Display paginated list of blocks with search and sorting.
    
    Query Parameters:
    - q: Search query (searches name and description)
    - sort: Sort field (name, mass, pcu, created_at, updated_at)
    - order: Sort order (asc, desc)
    - page: Page number for pagination
    """
    model = Block
    template_name = 'blocks/block_list.html'
    context_object_name = 'block_list'
    paginate_by = 25
    
    def get_queryset(self):
        """Get filtered and sorted queryset."""
        queryset = Block.objects.all()
        
        # Search functionality
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Sorting
        sort_by = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')
        
        # Validate sort field
        valid_sort_fields = ['name', 'mass', 'pcu', 'created_at', 'updated_at']
        if sort_by not in valid_sort_fields:
            sort_by = 'name'
        
        # Apply sorting
        if order == 'desc':
            queryset = queryset.order_by(f'-{sort_by}')
        else:
            queryset = queryset.order_by(sort_by)
        
        logger.debug(f"BlockListView query: search='{search_query}', sort={sort_by}, order={order}, count={queryset.count()}")
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add search and sorting context."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'name')
        context['current_order'] = self.request.GET.get('order', 'asc')
        
        # Build query string for pagination
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['query_string'] = query_params.urlencode()
        
        return context


class BlockDetailView(DetailView):
    """
    Display detailed block information including resource chain.
    
    Shows:
    - All block properties
    - Formatted components list with quantities
    - Full resource chain (Block → Components → Ores)
    - Statistics (total mass, component count, ore breakdown)
    """
    model = Block
    template_name = 'blocks/block_detail.html'
    context_object_name = 'block'
    pk_url_kwarg = 'pk'
    
    def get_object(self, queryset=None):
        """Override get_object to use block_id field instead of pk."""
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(queryset, block_id=pk)
    
    def get_context_data(self, **kwargs):
        """Add components and resource chain data."""
        context = super().get_context_data(**kwargs)
        block = self.object
        
        # Calculate resource chain
        resource_chain = self._calculate_resource_chain(block)
        context['resource_chain'] = resource_chain
        
        # Calculate statistics
        context['stats'] = self._calculate_stats(block, resource_chain)
        
        logger.info(f"BlockDetailView: {block.name} with {len(block.components or {})} components")
        return context
    
    def _calculate_resource_chain(self, block):
        """
        Calculate full resource chain: Block → Components → Ores
        
        Args:
            block: Block instance
        
        Returns:
            dict: Resource chain data structure
        """
        if not block.components:
            return {'components': [], 'ores': {}, 'total_ore_mass': 0}
        
        # Check cache first
        cache_key = f'resource_chain_{block.block_id}'
        cached_chain = cache.get(cache_key)
        if cached_chain:
            logger.debug(f"Using cached resource chain for {block.name}")
            return cached_chain
        
        components_data = []
        ore_totals = {}
        
        # Iterate through block components
        for comp_id, quantity in block.components.items():
            try:
                component = Component.objects.get(component_id=comp_id)
                
                comp_data = {
                    'id': str(component.component_id),
                    'name': component.name,
                    'quantity': quantity,
                    'mass_per_unit': float(component.mass),
                    'total_mass': float(component.mass) * quantity,
                    'materials': []
                }
                
                # Get component's materials (ores)
                if component.materials:
                    for ore_id, ore_quantity in component.materials.items():
                        try:
                            ore = Ore.objects.get(ore_id=ore_id)
                            
                            # Calculate total ore needed for this component quantity
                            total_ore_qty = ore_quantity * quantity
                            
                            ore_data = {
                                'id': str(ore.ore_id),
                                'name': ore.name,
                                'quantity_per_component': ore_quantity,
                                'total_quantity': total_ore_qty,
                                'mass_per_unit': float(ore.mass)
                            }
                            
                            comp_data['materials'].append(ore_data)
                            
                            # Add to total ore count
                            ore_key = str(ore.ore_id)
                            if ore_key not in ore_totals:
                                ore_totals[ore_key] = {
                                    'name': ore.name,
                                    'quantity': 0,
                                    'mass': float(ore.mass)
                                }
                            ore_totals[ore_key]['quantity'] += total_ore_qty
                            
                        except Ore.DoesNotExist:
                            logger.warning(f"Ore {ore_id} not found for component {component.name}")
                
                components_data.append(comp_data)
                
            except Component.DoesNotExist:
                logger.warning(f"Component {comp_id} not found in database")
        
        # Calculate total ore mass
        total_ore_mass = sum(ore['quantity'] * ore['mass'] for ore in ore_totals.values())
        
        resource_chain = {
            'components': components_data,
            'ores': ore_totals,
            'total_ore_mass': total_ore_mass
        }
        
        # Cache for 5 minutes
        cache.set(cache_key, resource_chain, 300)
        
        return resource_chain
    
    def _calculate_stats(self, block, resource_chain):
        """Calculate block statistics."""
        return {
            'component_count': len(block.components or {}),
            'total_component_quantity': sum(block.components.values()) if block.components else 0,
            'ore_type_count': len(resource_chain['ores']),
            'total_ore_mass': resource_chain['total_ore_mass'],
        }


class BlockCreateView(CreateView):
    """
    Create new block with component selection.
    
    Uses dynamic JavaScript component selector for adding/removing components.
    """
    model = Block
    form_class = BlockForm
    template_name = 'blocks/block_form.html'
    success_url = reverse_lazy('blocks:block_list')
    
    def get_context_data(self, **kwargs):
        """Add components list for dropdown."""
        context = super().get_context_data(**kwargs)
        context['components_list'] = Component.objects.all().order_by('name')
        context['available_components'] = context['components_list']  # Alias for templates
        context['form_title'] = 'Create Block'
        context['button_text'] = 'Create Block'
        return context
    
    def form_valid(self, form):
        """Handle successful form submission."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Block "{self.object.name}" created successfully!'
        )
        logger.info(f"Created block: {self.object.name} (ID: {self.object.block_id})")
        return response
    
    def form_invalid(self, form):
        """Handle form validation errors."""
        messages.error(
            self.request,
            'Error creating block. Please check the form for errors.'
        )
        logger.warning(f"Block creation failed: {form.errors}")
        return super().form_invalid(form)


class BlockUpdateView(UpdateView):
    """
    Update existing block with pre-populated components.
    
    Components are pre-filled in the form for editing.
    """
    model = Block
    form_class = BlockForm
    template_name = 'blocks/block_form.html'
    pk_url_kwarg = 'pk'
    
    def get_object(self, queryset=None):
        """Override get_object to use block_id field instead of pk."""
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(queryset, block_id=pk)
    
    def get_success_url(self):
        """Redirect to detail view after update."""
        return reverse_lazy('blocks:block_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add components list and existing components."""
        context = super().get_context_data(**kwargs)
        context['components_list'] = Component.objects.all().order_by('name')
        context['available_components'] = context['components_list']  # Alias for templates
        context['form_title'] = f'Update Block: {self.object.name}'
        context['button_text'] = 'Update Block'
        
        # Pre-populate existing components for JavaScript
        if self.object.components:
            context['existing_components'] = json.dumps(self.object.components)
        
        return context
    
    def form_valid(self, form):
        """Handle successful update."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Block "{self.object.name}" updated successfully!'
        )
        logger.info(f"Updated block: {self.object.name} (ID: {self.object.block_id})")
        return response
    
    def form_invalid(self, form):
        """Handle update validation errors."""
        messages.error(
            self.request,
            'Error updating block. Please check the form for errors.'
        )
        logger.warning(f"Block update failed for {self.object.name}: {form.errors}")
        return super().form_invalid(form)


class BlockDeleteView(DeleteView):
    """
    Delete block with confirmation.
    
    Shows block details and components before deletion.
    """
    model = Block
    template_name = 'blocks/block_confirm_delete.html'
    success_url = reverse_lazy('blocks:block_list')
    context_object_name = 'delete_block'
    pk_url_kwarg = 'pk'
    
    def get_object(self, queryset=None):
        """Override get_object to use block_id field instead of pk."""
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(queryset, block_id=pk)
    
    def get_context_data(self, **kwargs):
        """Add component count for display."""
        context = super().get_context_data(**kwargs)
        context['component_count'] = len(self.object.components or {})
        return context
    
    def form_valid(self, form):
        """Handle successful deletion."""
        block_name = self.object.name
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Block "{block_name}" deleted successfully!'
        )
        logger.info(f"Deleted block: {block_name}")
        return response
