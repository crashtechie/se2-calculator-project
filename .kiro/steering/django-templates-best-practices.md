---
inclusion: auto
fileMatchPattern: '**/*.html'
description: Django template best practices including template inheritance, template tags, filters, and Bootstrap 5 patterns
---

# Django Templates Best Practices

## Project Context

Space Engineers 2 Calculator uses:
- **Django Template Language** (DTL)
- **Bootstrap 5.3.2** for UI framework
- **Bootstrap Icons 1.11.3** for iconography
- **Template inheritance** with `base.html`
- **Custom template tags** and filters
- **Responsive design** (mobile-first)

## Template Structure

### Base Template Pattern

```django
{# base.html - Main layout template #}
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}SE2 Calculator{% endblock %}</title>
    
    <!-- CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'partials/navbar.html' %}
    
    {% if messages %}
        {% include 'partials/messages.html' %}
    {% endif %}
    
    <main class="container my-4">
        {% block content %}{% endblock %}
    </main>
    
    {% include 'partials/footer.html' %}
    
    <!-- JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Child Template Pattern

```django
{# blocks/block_list.html #}
{% extends 'base.html' %}
{% load static %}

{% block title %}Blocks - SE2 Calculator{% endblock %}

{% block extra_css %}
<style>
    /* Page-specific styles */
</style>
{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h1><i class="bi bi-bricks"></i> Blocks</h1>
        <!-- Content here -->
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Page-specific JavaScript
</script>
{% endblock %}
```

## Template Inheritance

### Block Organization

```django
{# Common blocks to define in base.html #}
{% block title %}{% endblock %}          {# Page title #}
{% block meta %}{% endblock %}            {# Meta tags #}
{% block extra_css %}{% endblock %}       {# Additional CSS #}
{% block content %}{% endblock %}         {# Main content #}
{% block extra_js %}{% endblock %}        {# Additional JavaScript #}
{% block breadcrumbs %}{% endblock %}     {# Breadcrumb navigation #}
```

### Multi-Level Inheritance

```django
{# base.html - Root template #}
{% block content %}{% endblock %}

{# base_list.html - List view base #}
{% extends 'base.html' %}
{% block content %}
    <div class="list-header">
        {% block list_header %}{% endblock %}
    </div>
    <div class="list-content">
        {% block list_content %}{% endblock %}
    </div>
    <div class="list-pagination">
        {% block pagination %}{% endblock %}
    </div>
{% endblock %}

{# blocks/block_list.html - Specific list #}
{% extends 'base_list.html' %}
{% block list_header %}
    <h1>Blocks</h1>
{% endblock %}
```

## Template Tags and Filters

### Built-in Template Tags

```django
{# Conditionals #}
{% if block_list %}
    <!-- Show blocks -->
{% elif search_query %}
    <!-- No results -->
{% else %}
    <!-- Empty state -->
{% endif %}

{# Loops #}
{% for block in block_list %}
    <div class="card">{{ block.name }}</div>
{% empty %}
    <p>No blocks found</p>
{% endfor %}

{# URL generation #}
<a href="{% url 'blocks:block_detail' block.block_id %}">View</a>
<a href="{% url 'blocks:block_update' pk=block.block_id %}">Edit</a>

{# Static files #}
<link rel="stylesheet" href="{% static 'css/main.css' %}">
<img src="{% static 'images/logo.png' %}" alt="Logo">

{# Include partials #}
{% include 'partials/navbar.html' %}
{% include 'partials/card.html' with title="Block" %}

{# Comments #}
{# This is a comment #}
{% comment %}
    Multi-line comment
    Not rendered in HTML
{% endcomment %}
```

### Built-in Filters

```django
{# String filters #}
{{ block.name|title }}                    {# Title Case #}
{{ block.description|truncatewords:20 }}  {# Truncate to 20 words #}
{{ block.name|lower }}                    {# lowercase #}
{{ block.name|upper }}                    {# UPPERCASE #}
{{ block.description|default:"No description" }}

{# Number filters #}
{{ block.mass|floatformat:2 }}            {# 2 decimal places #}
{{ total|floatformat }}                   {# Auto decimal places #}

{# Date filters #}
{{ block.created_at|date:"Y-m-d H:i" }}   {# 2026-01-20 14:30 #}
{{ block.created_at|date:"F j, Y" }}      {# January 20, 2026 #}
{{ block.created_at|timesince }}          {# "2 days ago" #}

{# List filters #}
{{ block.components|length }}             {# Count items #}
{{ block_list|first }}                    {# First item #}
{{ block_list|last }}                     {# Last item #}

{# Safe HTML #}
{{ block.description|safe }}              {# Don't escape HTML #}
{{ block.description|linebreaks }}        {# Convert newlines to <p> #}
```

### Custom Template Tags

```python
# blocks/templatetags/block_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply value by arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary."""
    return dictionary.get(key)

@register.simple_tag
def calculate_total_mass(components):
    """Calculate total mass of components."""
    total = 0
    for comp_id, quantity in components.items():
        # Calculation logic
        pass
    return total
```

```django
{# Use custom filters #}
{% load block_filters %}

{{ ore.quantity|multiply:ore.mass }}
{{ components|get_item:comp_id }}
{% calculate_total_mass components as total %}
<p>Total: {{ total }} kg</p>
```

## Bootstrap 5 Patterns

### Grid System

```django
{# Responsive grid #}
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">
        <!-- Full width on mobile, half on tablet, third on desktop -->
    </div>
</div>

{# Common layouts #}
<div class="row">
    <div class="col-md-8">Main content</div>
    <div class="col-md-4">Sidebar</div>
</div>

<div class="row g-3">  {# g-3 = gap between columns #}
    {% for block in block_list %}
    <div class="col-md-6 col-lg-4">
        <div class="card">{{ block.name }}</div>
    </div>
    {% endfor %}
</div>
```

### Cards (Project Standard)

```django
{# Basic card #}
<div class="card">
    <div class="card-header">
        <h5><i class="bi bi-box"></i> Block Details</h5>
    </div>
    <div class="card-body">
        <p class="card-text">{{ block.description }}</p>
    </div>
    <div class="card-footer">
        <a href="#" class="btn btn-primary">View</a>
    </div>
</div>

{# Card with colored header (project pattern) #}
<div class="card">
    <div class="card-header bg-primary text-white">
        <h5 class="mb-0"><i class="bi bi-info-circle"></i> Details</h5>
    </div>
    <div class="card-body">
        <dl class="row">
            <dt class="col-sm-4">Name:</dt>
            <dd class="col-sm-8">{{ block.name }}</dd>
        </dl>
    </div>
</div>

{# Card grid (project pattern) #}
<div class="row">
    {% for block in block_list %}
    <div class="col-md-6 col-lg-4 mb-4">
        <div class="card h-100">  {# h-100 = equal height #}
            <div class="card-body">
                <h5 class="card-title">{{ block.name }}</h5>
                <p class="card-text">{{ block.description|truncatewords:20 }}</p>
            </div>
            <div class="card-footer bg-transparent">
                <a href="{% url 'blocks:block_detail' block.block_id %}" 
                   class="btn btn-sm btn-outline-primary">
                    <i class="bi bi-eye"></i> View
                </a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
```

### Forms

```django
{# Bootstrap form #}
<form method="post">
    {% csrf_token %}
    
    <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input type="text" 
               class="form-control {% if form.name.errors %}is-invalid{% endif %}" 
               id="name" 
               name="name" 
               value="{{ form.name.value|default:'' }}">
        {% if form.name.errors %}
            <div class="invalid-feedback">
                {{ form.name.errors.0 }}
            </div>
        {% endif %}
    </div>
    
    <button type="submit" class="btn btn-primary">
        <i class="bi bi-save"></i> Save
    </button>
</form>

{# Django form rendering #}
<form method="post">
    {% csrf_token %}
    
    {% for field in form %}
    <div class="mb-3">
        <label for="{{ field.id_for_label }}" class="form-label">
            {{ field.label }}
        </label>
        {{ field }}
        {% if field.errors %}
            <div class="invalid-feedback d-block">
                {{ field.errors.0 }}
            </div>
        {% endif %}
        {% if field.help_text %}
            <div class="form-text">{{ field.help_text }}</div>
        {% endif %}
    </div>
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Buttons (Project Pattern)

```django
{# Button styles #}
<a href="#" class="btn btn-primary">
    <i class="bi bi-plus-circle"></i> Create
</a>

<a href="#" class="btn btn-outline-primary">
    <i class="bi bi-eye"></i> View
</a>

<a href="#" class="btn btn-outline-secondary">
    <i class="bi bi-pencil"></i> Edit
</a>

<a href="#" class="btn btn-outline-danger">
    <i class="bi bi-trash"></i> Delete
</a>

{# Button group #}
<div class="btn-group" role="group">
    <a href="#" class="btn btn-sm btn-outline-primary">View</a>
    <a href="#" class="btn btn-sm btn-outline-secondary">Edit</a>
    <a href="#" class="btn btn-sm btn-outline-danger">Delete</a>
</div>
```

### Alerts and Messages

```django
{# Django messages (project pattern) #}
{% if messages %}
<div class="container mt-3">
    {% for message in messages %}
    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
        {{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    {% endfor %}
</div>
{% endif %}

{# Static alerts #}
<div class="alert alert-info">
    <i class="bi bi-info-circle"></i> Information message
</div>

<div class="alert alert-success">
    <i class="bi bi-check-circle"></i> Success message
</div>

<div class="alert alert-warning">
    <i class="bi bi-exclamation-triangle"></i> Warning message
</div>

<div class="alert alert-danger">
    <i class="bi bi-x-circle"></i> Error message
</div>
```

### Tables

```django
{# Responsive table #}
<div class="table-responsive">
    <table class="table table-striped table-hover">
        <thead>
            <tr>
                <th>Name</th>
                <th>Mass</th>
                <th>PCU</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for block in block_list %}
            <tr>
                <td>{{ block.name }}</td>
                <td>{{ block.mass }} kg</td>
                <td>{{ block.pcu }}</td>
                <td>
                    <a href="{% url 'blocks:block_detail' block.block_id %}" 
                       class="btn btn-sm btn-outline-primary">
                        View
                    </a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
```

### Pagination (Project Pattern)

```django
{% if is_paginated %}
<nav aria-label="Page navigation">
    <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page=1{% if query_string %}&{{ query_string }}{% endif %}">
                    <i class="bi bi-chevron-double-left"></i> First
                </a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if query_string %}&{{ query_string }}{% endif %}">
                    <i class="bi bi-chevron-left"></i> Previous
                </a>
            </li>
        {% endif %}

        <li class="page-item active">
            <span class="page-link">
                Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
            </span>
        </li>

        {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if query_string %}&{{ query_string }}{% endif %}">
                    Next <i class="bi bi-chevron-right"></i>
                </a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% if query_string %}&{{ query_string }}{% endif %}">
                    Last <i class="bi bi-chevron-double-right"></i>
                </a>
            </li>
        {% endif %}
    </ul>
</nav>
{% endif %}
```

## Common Patterns

### List View with Search and Filters

```django
{# Search and filter form #}
<div class="card mb-4">
    <div class="card-body">
        <form method="get" class="row g-3">
            <div class="col-md-6">
                <label for="search" class="form-label">Search</label>
                <input type="text" 
                       class="form-control" 
                       id="search" 
                       name="q" 
                       value="{{ search_query }}"
                       placeholder="Search...">
            </div>
            <div class="col-md-3">
                <label for="sort" class="form-label">Sort By</label>
                <select class="form-select" id="sort" name="sort">
                    <option value="name" {% if current_sort == 'name' %}selected{% endif %}>Name</option>
                    <option value="mass" {% if current_sort == 'mass' %}selected{% endif %}>Mass</option>
                </select>
            </div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">
                    <i class="bi bi-search"></i> Search
                </button>
                <a href="{% url 'blocks:block_list' %}" class="btn btn-secondary">
                    <i class="bi bi-x-circle"></i> Clear
                </a>
            </div>
        </form>
    </div>
</div>
```

### Empty State

```django
{% if block_list %}
    <!-- Show list -->
{% else %}
    <div class="alert alert-info text-center">
        <i class="bi bi-info-circle fs-1"></i>
        <h4 class="mt-3">No Blocks Found</h4>
        <p>
            {% if search_query %}
                No blocks match your search criteria.
                <a href="{% url 'blocks:block_list' %}">Clear search</a>
            {% else %}
                Get started by creating your first block!
            {% endif %}
        </p>
        <a href="{% url 'blocks:block_create' %}" class="btn btn-primary">
            <i class="bi bi-plus-circle"></i> Create First Block
        </a>
    </div>
{% endif %}
```

### Detail View Layout

```django
<div class="row">
    <!-- Header with actions -->
    <div class="col-md-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1><i class="bi bi-box"></i> {{ object.name }}</h1>
            <div>
                <a href="{% url 'blocks:block_update' object.block_id %}" 
                   class="btn btn-primary">
                    <i class="bi bi-pencil"></i> Edit
                </a>
                <a href="{% url 'blocks:block_delete' object.block_id %}" 
                   class="btn btn-danger">
                    <i class="bi bi-trash"></i> Delete
                </a>
                <a href="{% url 'blocks:block_list' %}" 
                   class="btn btn-secondary">
                    <i class="bi bi-arrow-left"></i> Back
                </a>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <!-- Details cards -->
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">Details</h5>
            </div>
            <div class="card-body">
                <dl class="row">
                    <dt class="col-sm-4">Name:</dt>
                    <dd class="col-sm-8">{{ object.name }}</dd>
                </dl>
            </div>
        </div>
    </div>
</div>
```

### Confirmation Modal

```django
{# Delete confirmation #}
<div class="modal fade" id="deleteModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Confirm Delete</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete <strong>{{ object.name }}</strong>?</p>
                <p class="text-danger">This action cannot be undone.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                    Cancel
                </button>
                <form method="post" style="display: inline;">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-danger">
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
```

## Performance Optimization

### Template Fragment Caching

```django
{% load cache %}

{# Cache expensive template fragment #}
{% cache 600 block_detail block.block_id %}
    <div class="resource-chain">
        <!-- Expensive rendering -->
    </div>
{% endcache %}

{# Cache with multiple variables #}
{% cache 300 block_list page_obj.number search_query %}
    <!-- List content -->
{% endcache %}
```

### Minimize Database Queries

```django
{# BAD: N+1 queries #}
{% for block in block_list %}
    {{ block.category.name }}  {# Query per block! #}
{% endfor %}

{# GOOD: Prefetch in view #}
{# View: blocks = Block.objects.select_related('category') #}
{% for block in block_list %}
    {{ block.category.name }}  {# No additional query #}
{% endfor %}
```

## Accessibility

### Semantic HTML

```django
{# Use semantic elements #}
<header>
    <nav><!-- Navigation --></nav>
</header>

<main>
    <article><!-- Main content --></article>
    <aside><!-- Sidebar --></aside>
</main>

<footer><!-- Footer --></footer>
```

### ARIA Labels

```django
{# Add ARIA labels for screen readers #}
<button type="button" 
        class="btn-close" 
        data-bs-dismiss="alert" 
        aria-label="Close">
</button>

<nav aria-label="Page navigation">
    <ul class="pagination"><!-- Pagination --></ul>
</nav>

<form role="search">
    <input type="search" aria-label="Search blocks">
</form>
```

### Form Labels

```django
{# Always associate labels with inputs #}
<label for="block-name" class="form-label">Block Name</label>
<input type="text" 
       class="form-control" 
       id="block-name" 
       name="name">

{# Or use aria-label #}
<input type="search" 
       class="form-control" 
       aria-label="Search blocks" 
       placeholder="Search...">
```

## Template Checklist

### Structure
- [ ] Extend base.html
- [ ] Define title block
- [ ] Load required template tags
- [ ] Use semantic HTML
- [ ] Include CSRF token in forms

### Bootstrap
- [ ] Use responsive grid (col-md-*, col-lg-*)
- [ ] Add appropriate spacing (mb-*, mt-*, p-*)
- [ ] Use Bootstrap components (cards, buttons, alerts)
- [ ] Include Bootstrap Icons
- [ ] Make tables responsive

### Content
- [ ] Handle empty states
- [ ] Show loading states
- [ ] Display error messages
- [ ] Add pagination for lists
- [ ] Include breadcrumbs

### Accessibility
- [ ] Add alt text to images
- [ ] Use semantic HTML elements
- [ ] Include ARIA labels
- [ ] Associate labels with inputs
- [ ] Ensure keyboard navigation

### Performance
- [ ] Cache expensive fragments
- [ ] Minimize template logic
- [ ] Use template inheritance
- [ ] Optimize images
- [ ] Defer non-critical JS
