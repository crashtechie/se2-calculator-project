---
inclusion: auto
fileMatchPattern: '**/views.py'
description: Django views patterns and best practices for Space Engineers 2 Calculator including CBVs, form handling, and template context
---

# Django Views Patterns

## Project Context

Space Engineers 2 Calculator uses Django's class-based views (CBVs) for CRUD operations on:
- Ores (base resources)
- Components (craftable items)
- Blocks (buildable structures)
- Build Orders (collections with calculations)

## Class-Based Views (CBVs)

### Standard CRUD Pattern

Use Django's generic views for standard CRUD operations.

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class BlockListView(ListView):
    model = Block
    template_name = 'blocks/block_list.html'
    context_object_name = 'blocks'
    paginate_by = 25
    
    def get_queryset(self):
        """Optimize queries and add filtering."""
        queryset = Block.objects.all()
        
        # Add search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add extra context for template."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class BlockDetailView(DetailView):
    model = Block
    template_name = 'blocks/block_detail.html'
    context_object_name = 'block'
    
    def get_context_data(self, **kwargs):
        """Add related data to context."""
        context = super().get_context_data(**kwargs)
        # Add component details
        context['component_requirements'] = self.object.iter_component_requirements()
        return context

class BlockCreateView(CreateView):
    model = Block
    form_class = BlockForm
    template_name = 'blocks/block_form.html'
    success_url = reverse_lazy('blocks:list')
    
    def form_valid(self, form):
        """Add custom logic on successful form submission."""
        response = super().form_valid(form)
        messages.success(self.request, f'Block "{self.object.name}" created successfully!')
        return response

class BlockUpdateView(UpdateView):
    model = Block
    form_class = BlockForm
    template_name = 'blocks/block_form.html'
    
    def get_success_url(self):
        """Redirect to detail view after update."""
        return reverse_lazy('blocks:detail', kwargs={'pk': self.object.pk})

class BlockDeleteView(DeleteView):
    model = Block
    template_name = 'blocks/block_confirm_delete.html'
    success_url = reverse_lazy('blocks:list')
    
    def delete(self, request, *args, **kwargs):
        """Add message on successful deletion."""
        block_name = self.get_object().name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Block "{block_name}" deleted successfully!')
        return response
```

### When to Use CBVs vs FBVs

**Use Class-Based Views (CBVs) when:**
- Standard CRUD operations
- Need to reuse view logic
- Want to use mixins
- Following Django conventions

**Use Function-Based Views (FBVs) when:**
- Complex custom logic
- Multiple forms on one page
- Unusual workflows
- Simpler to understand for specific case

## View Mixins

### Authentication Mixins

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class BlockCreateView(LoginRequiredMixin, CreateView):
    """Require login to create blocks."""
    model = Block
    form_class = BlockForm
    login_url = '/login/'

class BlockDeleteView(PermissionRequiredMixin, DeleteView):
    """Require specific permission to delete."""
    model = Block
    permission_required = 'blocks.delete_block'
    
    def handle_no_permission(self):
        """Custom handling for permission denied."""
        messages.error(self.request, "You don't have permission to delete blocks.")
        return redirect('blocks:list')
```

### Custom Mixins

```python
class SearchMixin:
    """Add search functionality to list views."""
    search_fields = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        
        if search and self.search_fields:
            from django.db.models import Q
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f'{field}__icontains': search})
            queryset = queryset.filter(query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class BlockListView(SearchMixin, ListView):
    model = Block
    search_fields = ['name', 'description']
```

## Form Handling

### Form Validation in Views

```python
class BlockCreateView(CreateView):
    model = Block
    form_class = BlockForm
    
    def form_valid(self, form):
        """Called when form is valid."""
        # Add custom validation
        if form.cleaned_data['mass'] > 1000000:
            form.add_error('mass', 'Mass is unrealistically high')
            return self.form_invalid(form)
        
        # Add user tracking
        form.instance.created_by = self.request.user
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Called when form is invalid."""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
```

### Multiple Forms in One View

```python
from django.views.generic import FormView

class BuildOrderCreateView(FormView):
    template_name = 'buildorders/create.html'
    
    def get(self, request, *args, **kwargs):
        """Display empty forms."""
        context = {
            'order_form': BuildOrderForm(),
            'block_formset': BlockFormSet(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        """Process both forms."""
        order_form = BuildOrderForm(request.POST)
        block_formset = BlockFormSet(request.POST)
        
        if order_form.is_valid() and block_formset.is_valid():
            # Save order
            order = order_form.save()
            
            # Save blocks
            blocks = block_formset.save(commit=False)
            for block in blocks:
                block.build_order = order
                block.save()
            
            messages.success(request, 'Build order created!')
            return redirect('buildorders:detail', pk=order.pk)
        
        # Re-render with errors
        context = {
            'order_form': order_form,
            'block_formset': block_formset,
        }
        return render(request, self.template_name, context)
```

## Template Context

### Adding Context Data

```python
class BlockDetailView(DetailView):
    model = Block
    
    def get_context_data(self, **kwargs):
        """Add extra data to template context."""
        context = super().get_context_data(**kwargs)
        
        # Add related objects
        context['component_requirements'] = self.object.iter_component_requirements()
        
        # Add calculations
        context['total_component_mass'] = self.object.calculate_component_mass()
        
        # Add metadata
        context['page_title'] = f'Block: {self.object.name}'
        
        return context
```

### Context Processors

For data needed across all templates, use context processors.

```python
# context_processors.py
def site_settings(request):
    """Add site-wide settings to all templates."""
    return {
        'site_name': 'SE2 Calculator',
        'version': '0.7.0-alpha',
    }

# settings.py
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            # ... default processors
            'app.context_processors.site_settings',
        ],
    },
}]
```

## Query Optimization in Views

### Prefetch Related Objects

```python
class BlockListView(ListView):
    model = Block
    
    def get_queryset(self):
        """Optimize queries for list view."""
        # Get all blocks
        queryset = Block.objects.all()
        
        # Prefetch components
        component_ids = set()
        for block in queryset:
            component_ids.update(block.components.keys())
        
        # Cache components
        components = {
            str(c.component_id): c
            for c in Component.objects.filter(component_id__in=component_ids)
        }
        
        # Attach to blocks
        for block in queryset:
            block._cached_components = components
        
        return queryset
```

### Select Related for Foreign Keys

```python
class BuildOrderDetailView(DetailView):
    model = BuildOrder
    
    def get_queryset(self):
        """Optimize with select_related."""
        return BuildOrder.objects.select_related('created_by', 'updated_by')
```

## Pagination

### Basic Pagination

```python
class BlockListView(ListView):
    model = Block
    paginate_by = 25
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add pagination info
        context['total_blocks'] = self.get_queryset().count()
        
        return context
```

### Custom Pagination

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def block_list(request):
    blocks = Block.objects.all()
    paginator = Paginator(blocks, 25)
    
    page = request.GET.get('page')
    try:
        blocks_page = paginator.page(page)
    except PageNotAnInteger:
        blocks_page = paginator.page(1)
    except EmptyPage:
        blocks_page = paginator.page(paginator.num_pages)
    
    return render(request, 'blocks/list.html', {
        'blocks': blocks_page,
        'paginator': paginator,
    })
```

## AJAX Views

### JSON Response Views

```python
from django.http import JsonResponse
from django.views import View

class BlockSearchView(View):
    """AJAX endpoint for block search."""
    
    def get(self, request):
        search = request.GET.get('q', '')
        
        blocks = Block.objects.filter(name__icontains=search)[:10]
        
        results = [
            {
                'id': str(block.block_id),
                'name': block.name,
                'mass': block.mass,
            }
            for block in blocks
        ]
        
        return JsonResponse({'results': results})
```

### AJAX Form Submission

```python
class BlockCreateAjaxView(View):
    """Handle AJAX form submission."""
    
    def post(self, request):
        form = BlockForm(request.POST)
        
        if form.is_valid():
            block = form.save()
            return JsonResponse({
                'success': True,
                'block_id': str(block.block_id),
                'message': 'Block created successfully!'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
```

## Error Handling

### Custom Error Views

```python
# views.py
def handler404(request, exception):
    """Custom 404 page."""
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """Custom 500 page."""
    return render(request, 'errors/500.html', status=500)

# urls.py
handler404 = 'app.views.handler404'
handler500 = 'app.views.handler500'
```

### Try-Except in Views

```python
class BlockDetailView(DetailView):
    model = Block
    
    def get_object(self, queryset=None):
        """Handle missing objects gracefully."""
        try:
            return super().get_object(queryset)
        except Block.DoesNotExist:
            messages.error(self.request, 'Block not found.')
            raise Http404("Block does not exist")
```

## Messages Framework

### Adding Messages

```python
from django.contrib import messages

class BlockCreateView(CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Block "{self.object.name}" created!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

# Different message levels
messages.debug(request, 'Debug message')
messages.info(request, 'Info message')
messages.success(request, 'Success message')
messages.warning(request, 'Warning message')
messages.error(request, 'Error message')
```

## Redirects

### Redirect Patterns

```python
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

class BlockCreateView(CreateView):
    # Static redirect
    success_url = reverse_lazy('blocks:list')
    
    # Dynamic redirect
    def get_success_url(self):
        return reverse('blocks:detail', kwargs={'pk': self.object.pk})
    
    # Conditional redirect
    def form_valid(self, form):
        response = super().form_valid(form)
        
        if 'save_and_add' in self.request.POST:
            return redirect('blocks:create')
        elif 'save_and_continue' in self.request.POST:
            return redirect('blocks:update', pk=self.object.pk)
        else:
            return redirect('blocks:detail', pk=self.object.pk)
```

## View Testing

### Testing CBVs

```python
def test_block_list_view(client):
    """Test block list view."""
    Block.objects.create(name="Test Block", mass=10.0)
    
    response = client.get(reverse('blocks:list'))
    
    assert response.status_code == 200
    assert 'blocks' in response.context
    assert len(response.context['blocks']) == 1

def test_block_create_view(client):
    """Test block creation."""
    data = {
        'name': 'New Block',
        'mass': 15.0,
        'description': 'Test block'
    }
    
    response = client.post(reverse('blocks:create'), data)
    
    assert response.status_code == 302  # Redirect
    assert Block.objects.filter(name='New Block').exists()

def test_block_detail_view_not_found(client):
    """Test 404 for missing block."""
    response = client.get(reverse('blocks:detail', kwargs={'pk': 'invalid-uuid'}))
    assert response.status_code == 404
```

## Views Checklist

### List Views
- [ ] Add pagination
- [ ] Implement search/filtering
- [ ] Optimize queries (prefetch)
- [ ] Add sorting options
- [ ] Show total count

### Detail Views
- [ ] Prefetch related objects
- [ ] Add breadcrumbs
- [ ] Show related data
- [ ] Add edit/delete links
- [ ] Handle missing objects

### Create/Update Views
- [ ] Use appropriate form class
- [ ] Add form validation
- [ ] Show success messages
- [ ] Handle errors gracefully
- [ ] Redirect appropriately

### Delete Views
- [ ] Require confirmation
- [ ] Check permissions
- [ ] Show what will be deleted
- [ ] Add success message
- [ ] Handle cascade deletes

### General
- [ ] Add authentication where needed
- [ ] Check permissions
- [ ] Optimize database queries
- [ ] Add appropriate messages
- [ ] Test all views
