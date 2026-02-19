---
inclusion: manual
description: Performance optimization guide covering database queries, caching strategies, profiling, and load testing
---

# Performance Optimization Guide

## Performance Philosophy

### Optimization Rules
1. **Don't optimize prematurely** - Profile first, optimize second
2. **Measure everything** - Use metrics to guide decisions
3. **Focus on bottlenecks** - 80/20 rule applies
4. **Maintain readability** - Don't sacrifice clarity for minor gains

## Database Performance

### Query Optimization

#### N+1 Query Problem
```python
# BAD: N+1 queries
blocks = Block.objects.all()
for block in blocks:
    print(block.component.name)  # Queries database each iteration

# GOOD: Use select_related
blocks = Block.objects.select_related('component').all()
for block in blocks:
    print(block.component.name)  # No additional queries
```

#### Prefetch Related
```python
# BAD: Multiple queries for many-to-many
components = Component.objects.all()
for component in components:
    for ore in component.ores.all():  # Query per component
        print(ore.name)

# GOOD: Use prefetch_related
components = Component.objects.prefetch_related('ores').all()
for component in components:
    for ore in component.ores.all():  # Uses prefetched data
        print(ore.name)
```

#### Only Fetch What You Need
```python
# BAD: Fetch all fields
blocks = Block.objects.all()

# GOOD: Use only() for specific fields
blocks = Block.objects.only('id', 'name', 'mass')

# GOOD: Use values() for dictionaries
blocks = Block.objects.values('id', 'name')

# GOOD: Use values_list() for tuples
block_names = Block.objects.values_list('name', flat=True)
```

### Database Indexes

#### When to Add Indexes
- Fields used in WHERE clauses frequently
- Fields used in ORDER BY
- Foreign keys (Django adds these automatically)
- Fields used in JOIN operations

#### Index Examples
```python
class Block(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # Single field
    
    class Meta:
        indexes = [
            models.Index(fields=['name', 'mass']),  # Composite index
            models.Index(fields=['-created_at']),   # Descending order
        ]
```

#### Index Considerations
- Indexes speed up reads but slow down writes
- Don't over-index (each index has overhead)
- Monitor index usage in production
- Consider partial indexes for filtered queries

### Query Analysis

#### Django Debug Toolbar
```python
# settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# Shows:
# - Number of queries
# - Query execution time
# - Duplicate queries
# - Query explain plans
```

#### Manual Query Analysis
```python
from django.db import connection
from django.test.utils import override_settings

# Log all queries
with override_settings(DEBUG=True):
    # Your code here
    print(len(connection.queries))
    for query in connection.queries:
        print(query['sql'])
        print(query['time'])
```

#### PostgreSQL EXPLAIN
```python
# Get query execution plan
queryset = Block.objects.filter(mass__gt=100)
print(queryset.explain())

# Detailed analysis
print(queryset.explain(analyze=True, verbose=True))
```

## Caching Strategies

### Django Cache Framework

#### Cache Configuration
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'se2calc',
        'TIMEOUT': 300,  # 5 minutes
    }
}
```

#### View Caching
```python
from django.views.decorators.cache import cache_page

# Cache view for 5 minutes
@cache_page(60 * 5)
def block_list(request):
    blocks = Block.objects.all()
    return render(request, 'blocks/list.html', {'blocks': blocks})
```

#### Template Fragment Caching
```django
{% load cache %}

{% cache 500 sidebar %}
    <!-- Expensive sidebar rendering -->
    {% for block in blocks %}
        {{ block.name }}
    {% endfor %}
{% endcache %}
```

#### Low-Level Caching
```python
from django.core.cache import cache

# Set cache
cache.set('my_key', 'my_value', timeout=300)

# Get cache
value = cache.get('my_key')

# Get or set
value = cache.get_or_set('my_key', expensive_function, timeout=300)

# Delete cache
cache.delete('my_key')

# Clear all cache
cache.clear()
```

### Cache Invalidation

#### Time-Based Expiration
```python
# Cache for 5 minutes
cache.set('block_list', blocks, timeout=300)
```

#### Event-Based Invalidation
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Block)
def invalidate_block_cache(sender, instance, **kwargs):
    cache.delete('block_list')
    cache.delete(f'block_{instance.id}')
```

#### Cache Versioning
```python
# Increment version when data structure changes
CACHE_VERSION = 2
cache.set('my_key', value, version=CACHE_VERSION)
value = cache.get('my_key', version=CACHE_VERSION)
```

## Python Performance

### List Comprehensions vs Loops
```python
# GOOD: List comprehension (faster)
squares = [x**2 for x in range(1000)]

# SLOWER: Traditional loop
squares = []
for x in range(1000):
    squares.append(x**2)

# BEST: Generator for large datasets
squares = (x**2 for x in range(1000000))
```

### Use Built-in Functions
```python
# GOOD: Built-in sum (C implementation)
total = sum(numbers)

# SLOWER: Manual loop
total = 0
for num in numbers:
    total += num
```

### Avoid Repeated Attribute Lookups
```python
# BAD: Repeated lookups
for i in range(len(items)):
    items[i].process()

# GOOD: Cache attribute
process = items.process
for item in items:
    process()
```

### Use Sets for Membership Testing
```python
# BAD: List membership (O(n))
if item in large_list:
    pass

# GOOD: Set membership (O(1))
if item in large_set:
    pass
```

## Frontend Performance

### Static File Optimization

#### Compression
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',  # Add at top
    # ... other middleware
]
```

#### Static File Caching
```nginx
# nginx.conf
location /static/ {
    alias /path/to/static/;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Template Optimization

#### Avoid Complex Logic in Templates
```python
# BAD: Complex logic in template
{% for block in blocks %}
    {% if block.calculate_total_mass > 1000 %}
        <!-- Heavy calculation in loop -->
    {% endif %}
{% endfor %}

# GOOD: Pre-calculate in view
def block_list(request):
    blocks = Block.objects.all()
    heavy_blocks = [b for b in blocks if b.calculate_total_mass() > 1000]
    return render(request, 'blocks/list.html', {'heavy_blocks': heavy_blocks})
```

#### Use Template Fragment Caching
```django
{% load cache %}
{% cache 600 block_detail block.id %}
    <!-- Expensive rendering -->
{% endcache %}
```

## Pagination

### Always Paginate Large Datasets
```python
from django.core.paginator import Paginator

def block_list(request):
    blocks = Block.objects.all()
    paginator = Paginator(blocks, 25)  # 25 items per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blocks/list.html', {'page_obj': page_obj})
```

### Cursor-Based Pagination (for APIs)
```python
# Better for large datasets
from rest_framework.pagination import CursorPagination

class BlockCursorPagination(CursorPagination):
    page_size = 25
    ordering = '-created_at'
```

## Async and Concurrency

### Async Views (Django 4.1+)
```python
async def async_block_list(request):
    blocks = await Block.objects.all().aiterator()
    return render(request, 'blocks/list.html', {'blocks': blocks})
```

### Background Tasks
```python
# Use Celery for long-running tasks
from celery import shared_task

@shared_task
def calculate_complex_build_order(build_order_id):
    # Long-running calculation
    pass

# Trigger from view
def create_build_order(request):
    build_order = BuildOrder.objects.create(...)
    calculate_complex_build_order.delay(build_order.id)
    return redirect('build_order_detail', pk=build_order.id)
```

## Profiling Tools

### Django Silk
```python
# Install: pip install django-silk
# settings.py
INSTALLED_APPS += ['silk']
MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

# Access profiling UI at /silk/
```

### cProfile
```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Code to profile
    expensive_function()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions
```

### Memory Profiling
```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    large_list = [i for i in range(1000000)]
    return sum(large_list)
```

## Performance Monitoring

### Application Performance Monitoring (APM)
- New Relic
- DataDog
- Sentry Performance
- Scout APM

### Key Metrics to Track
- Response time (p50, p95, p99)
- Database query time
- Cache hit rate
- Error rate
- Memory usage
- CPU usage

### Django Logging for Performance
```python
import logging
import time

logger = logging.getLogger(__name__)

def timed_view(request):
    start_time = time.time()
    
    # View logic
    response = render(request, 'template.html')
    
    duration = time.time() - start_time
    logger.info(f"View execution time: {duration:.2f}s")
    
    return response
```

## Load Testing

### Using Locust
```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def view_blocks(self):
        self.client.get("/blocks/")
    
    @task(3)  # 3x more frequent
    def view_block_detail(self):
        self.client.get("/blocks/1/")
```

### Run Load Test
```bash
locust -f locustfile.py --host=http://localhost:8000
```

## Performance Checklist

### Before Optimization
- [ ] Profile to identify bottlenecks
- [ ] Measure current performance
- [ ] Set performance goals
- [ ] Prioritize high-impact optimizations

### Database
- [ ] Eliminate N+1 queries
- [ ] Add appropriate indexes
- [ ] Use select_related/prefetch_related
- [ ] Optimize complex queries
- [ ] Implement pagination

### Caching
- [ ] Cache expensive computations
- [ ] Cache database queries
- [ ] Cache template fragments
- [ ] Implement cache invalidation

### Code
- [ ] Use efficient data structures
- [ ] Avoid premature optimization
- [ ] Profile hot paths
- [ ] Optimize algorithms

### Frontend
- [ ] Compress static files
- [ ] Enable browser caching
- [ ] Minimize HTTP requests
- [ ] Optimize images

### Monitoring
- [ ] Set up APM
- [ ] Track key metrics
- [ ] Set up alerts
- [ ] Regular performance reviews
