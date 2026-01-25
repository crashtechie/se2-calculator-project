from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Ore
from .forms import OreForm

class OreListView(ListView):
    """
    Display paginated list of ores with filtering and sorting capabilities.
    
    URL: /ores/
    Template: ores/ore_list.html
    Context:
        - ore_list: Queryset of Ore objects
        - search_query: Current search term
        - sort_by: Current sort field
        - sort_order: Current sort order (asc/desc)
    """
    model = Ore
    template_name = 'ores/ore_list.html'
    context_object_name = 'ore_list'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Ore.objects.all()
        
        # search filtering
        search_query = self.request.GET.get('search','').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            
        # Sorting
        sort_by = self.request.GET.get('sort_by', 'name')
        sort_order = self.request.GET.get('sort_order', 'asc')
        
        # Validate sort_by parameter
        valid_sort_fields = ['name', 'mass', 'created_at', 'updated_at']
        if sort_by not in valid_sort_fields:
            sort_by = 'name'
            
        # Apply sorting
        if sort_order == 'desc':
            queryset = queryset.order_by(f'-{sort_by}')
        else:
            queryset = queryset.order_by(sort_by)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort_by', 'name')
        context['sort_order'] = self.request.GET.get('order', 'asc')
        
        # Add total count
        context['total_count'] = self.get_queryset().count()
        
        return context


class OreDetailView(DetailView):
    """
    Display detailed information for a single ore.
    
    URL: /ores/<uuid:pk>/
    Template: ores/ore_detail.html
    Context:
        - ore: Ore object instance
    """
    model = Ore
    template_name = 'ores/ore_detail.html'
    context_object_name = 'ore'
    
    def get_context_data(self, **kwargs):
        """Add additional context for the detail view."""
        context = super().get_context_data(**kwargs)
        
        # Add previous/next navigation
        current_ore = self.get_object()
        all_ores = Ore.objects.all().order_by('name')
        ore_list = list(all_ores)
        
        try:
            current_index = ore_list.index(current_ore)
            context['previous_ore'] = ore_list[current_index - 1] if current_index > 0 else None
            context['next_ore'] = ore_list[current_index + 1] if current_index < len(ore_list) - 1 else None
        except (ValueError, IndexError):
            context['previous_ore'] = None
            context['next_ore'] = None
        
        return context


class OreCreateView(SuccessMessageMixin, CreateView):
    """
    Create a new ore instance.
    
    URL: /ores/create/
    Template: ores/ore_form.html
    Redirects to: ore_detail on success
    """
    model = Ore
    form_class = OreForm
    template_name = 'ores/ore_form.html'
    success_message = "Ore '%(name)s' was created successfully!"
    
    def get_success_url(self):
        """Redirect to the detail page of the newly created ore."""
        return reverse_lazy('ores:ore_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add form action context."""
        context = super().get_context_data(**kwargs)
        context['form_action'] = 'Create'
        return context


class OreUpdateView(SuccessMessageMixin, UpdateView):
    """
    Update an existing ore instance.
    
    URL: /ores/<uuid:pk>/update/
    Template: ores/ore_form.html
    Redirects to: ore_detail on success
    """
    model = Ore
    form_class = OreForm
    template_name = 'ores/ore_form.html'
    success_message = "Ore '%(name)s' was updated successfully!"
    
    def get_success_url(self):
        """Redirect to the detail page of the updated ore."""
        return reverse_lazy('ores:ore_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add form action context."""
        context = super().get_context_data(**kwargs)
        context['form_action'] = 'Update'
        return context


class OreDeleteView(DeleteView):
    """
    Delete an ore instance with confirmation.
    
    URL: /ores/<uuid:pk>/delete/
    Template: ores/ore_confirm_delete.html
    Redirects to: ore_list on success
    """
    model = Ore
    template_name = 'ores/ore_confirm_delete.html'
    success_url = reverse_lazy('ores:ore_list')
    
    def delete(self, request, *args, **kwargs):
        """Override delete to add success message."""
        ore = self.get_object()
        messages.success(request, f"Ore '{ore.name}' was deleted successfully!")
        return super().delete(request, *args, **kwargs)