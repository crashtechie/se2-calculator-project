# Database Query Optimization

## When to Activate This Skill

- Investigating slow database queries
- Optimizing Django ORM queries
- Reducing N+1 query problems
- Analyzing query execution plans
- Improving application performance
- Working with large datasets

## Identifying Query Problems

### Django Debug Toolbar
```python
# settings.py (development only)
INSTALLED_APPS = [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
```

### Query Counting in Tests
```python
from django.test import TestCase
from django.test.utils import override_settings
from django.db import connection

class QueryOptimizationTest(TestCase):
    def test_list_view_query_count(self):
        """Ensure view doesn't cause N+1 queries"""
        # Create test data
        for i in range(10):
            Block.objects.create(name=f'Block {i}')
        
        with self.assertNumQueries(1):
            # Should use select_related/prefetch_related
            list(Block.objects.select_related('component').all())
```

### Logging Queries
```python
# settings.py (development)
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Common Query Problems

### N+1 Query Problem
```python
# Bad: Causes N+1 queries (1 for blocks + N for each component)
blocks = Block.objects.all()
for block in blocks:
    print(block.component.name)  # Separate query each time

# Good: Use select_related for foreign keys
blocks = Block.objects.select_related('component').all()
for block in blocks:
    print(block.component.name)  # No additional queries

# Good: Use prefetch_related for many-to-many and reverse foreign keys
blocks = Block.objects.prefetch_related('materials').all()
for block in blocks:
    for material in block.materials.all():  # No additional queries
        print(material.name)
```

### Over-fetching Data
```python
# Bad: Fetches all fields when only need a few
blocks = Block.objects.all()
names = [block.name for block in blocks]

# Good: Use only() to fetch specific fields
blocks = Block.objects.only('name', 'id')
names = [block.name for block in blocks]

# Good: Use values() for dictionaries
names = Block.objects.values('name', 'id')

# Good: Use values_list() for tuples
names = Block.objects.values_list('name', flat=True)
```

### Unnecessary Queries
```python
# Bad: Checks existence with count()
if Block.objects.filter(name='Test').count() > 0:
    pass

# Good: Use exists() for boolean checks
if Block.objects.filter(name='Test').exists():
    pass

# Bad: Fetches all objects to count
total = len(Block.objects.all())

# Good: Use count() for counting
total = Block.objects.count()
```

## Django ORM Optimization Techniques

### select_related() - SQL JOIN
```python
# Use for ForeignKey and OneToOneField
# Performs SQL JOIN to fetch related objects in single query

# Single level
blocks = Block.objects.select_related('component')

# Multiple levels
blocks = Block.objects.select_related('component__category')

# Multiple relations
blocks = Block.objects.select_related('component', 'created_by')
```

### prefetch_related() - Separate Queries
```python
# Use for ManyToManyField and reverse ForeignKey
# Performs separate queries and joins in Python

# Basic usage
blocks = Block.objects.prefetch_related('materials')

# Nested prefetch
blocks = Block.objects.prefetch_related('materials__ore')

# Custom prefetch
from django.db.models import Prefetch

blocks = Block.objects.prefetch_related(
    Prefetch(
        'materials',
        queryset=Material.objects.filter(is_active=True).select_related('ore')
    )
)
```

### Combining Optimizations
```python
# Optimize complex queries
blocks = (
    Block.objects
    .select_related('component', 'created_by')  # ForeignKeys
    .prefetch_related('materials', 'tags')       # ManyToMany
    .only('id', 'name', 'component__name')       # Specific fields
    .filter(is_active=True)
    .order_by('-created_at')
)
```

## Query Analysis

### EXPLAIN Query Plans
```python
# View query execution plan
queryset = Block.objects.select_related('component').filter(name__startswith='Iron')
print(queryset.explain())

# Detailed analysis
print(queryset.explain(verbose=True, analyze=True))
```

### Raw SQL When Needed
```python
from django.db import connection

def complex_aggregation():
    """Use raw SQL for complex queries"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT b.name, COUNT(m.id) as material_count
            FROM blocks_block b
            LEFT JOIN blocks_materials m ON b.id = m.block_id
            GROUP BY b.id, b.name
            HAVING COUNT(m.id) > 5
            ORDER BY material_count DESC
        """)
        return cursor.fetchall()

# Or use raw() for model instances
blocks = Block.objects.raw("""
    SELECT * FROM blocks_block
    WHERE created_at > %s
""", [start_date])
```

## Aggregation and Annotation

### Efficient Aggregations
```python
from django.db.models import Count, Sum, Avg, Max, Min, F, Q

# Count related objects
blocks_with_counts = Block.objects.annotate(
    material_count=Count('materials'),
    total_mass=Sum('materials__mass')
)

# Filter on annotations
popular_blocks = Block.objects.annotate(
    usage_count=Count('buildorders')
).filter(usage_count__gt=10)

# Complex annotations
blocks = Block.objects.annotate(
    total_cost=Sum(F('materials__quantity') * F('materials__unit_price'))
)
```

### Conditional Aggregation
```python
from django.db.models import Case, When, IntegerField

blocks = Block.objects.annotate(
    active_materials=Count(
        Case(
            When(materials__is_active=True, then=1),
            output_field=IntegerField()
        )
    )
)
```

## Bulk Operations

### Bulk Create
```python
# Bad: Multiple INSERT queries
for i in range(1000):
    Block.objects.create(name=f'Block {i}')

# Good: Single INSERT query
blocks = [Block(name=f'Block {i}') for i in range(1000)]
Block.objects.bulk_create(blocks, batch_size=100)
```

### Bulk Update
```python
# Bad: Multiple UPDATE queries
blocks = Block.objects.all()
for block in blocks:
    block.is_active = True
    block.save()

# Good: Single UPDATE query
Block.objects.all().update(is_active=True)

# Good: Bulk update with different values
blocks = Block.objects.all()
for block in blocks:
    block.updated_at = timezone.now()
Block.objects.bulk_update(blocks, ['updated_at'], batch_size=100)
```

### Bulk Delete
```python
# Efficient deletion
Block.objects.filter(is_active=False).delete()

# Be careful with cascading deletes
# Use select_related to understand impact
blocks_to_delete = Block.objects.filter(
    is_active=False
).select_related('component').prefetch_related('materials')
```

## Database Indexes

### Adding Indexes
```python
from django.db import models

class Block(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name', 'created_at']),
            models.Index(fields=['-created_at']),  # Descending
            models.Index(
                fields=['component', 'is_active'],
                name='block_component_active_idx'
            ),
        ]
```

### Partial Indexes (PostgreSQL)
```python
from django.contrib.postgres.indexes import Index as PostgresIndex
from django.db.models import Q

class Block(models.Model):
    class Meta:
        indexes = [
            PostgresIndex(
                fields=['name'],
                name='active_blocks_idx',
                condition=Q(is_active=True)
            ),
        ]
```

## Caching Strategies

### QuerySet Caching
```python
from django.core.cache import cache

def get_popular_blocks():
    """Cache expensive query results"""
    cache_key = 'popular_blocks'
    blocks = cache.get(cache_key)
    
    if blocks is None:
        blocks = list(
            Block.objects
            .annotate(usage_count=Count('buildorders'))
            .filter(usage_count__gt=10)
            .select_related('component')
            [:20]
        )
        cache.set(cache_key, blocks, timeout=300)  # 5 minutes
    
    return blocks
```

### Per-Object Caching
```python
from django.utils.functional import cached_property

class Block(models.Model):
    @cached_property
    def total_mass(self):
        """Cache expensive calculation"""
        return self.materials.aggregate(
            total=Sum(F('quantity') * F('mass'))
        )['total'] or 0
```

## Query Optimization Checklist

### Before Optimization
- [ ] Identify slow queries using Django Debug Toolbar
- [ ] Log query counts in critical views
- [ ] Use EXPLAIN to understand query plans
- [ ] Measure baseline performance

### Optimization Steps
- [ ] Add select_related() for ForeignKey relationships
- [ ] Add prefetch_related() for ManyToMany relationships
- [ ] Use only() or values() to limit fields
- [ ] Replace count() > 0 with exists()
- [ ] Use bulk operations for multiple inserts/updates
- [ ] Add database indexes for frequently queried fields
- [ ] Cache expensive query results
- [ ] Consider denormalization for read-heavy data

### After Optimization
- [ ] Verify query count reduction
- [ ] Measure performance improvement
- [ ] Test with realistic data volumes
- [ ] Update tests to prevent regression

## Advanced Techniques

### Database Functions
```python
from django.db.models.functions import Lower, Upper, Concat, Coalesce

# Case-insensitive search
blocks = Block.objects.annotate(
    lower_name=Lower('name')
).filter(lower_name='iron ore')

# String concatenation
blocks = Block.objects.annotate(
    full_description=Concat('name', models.Value(' - '), 'description')
)
```

### Subqueries
```python
from django.db.models import OuterRef, Subquery

# Get latest build order for each block
latest_orders = BuildOrder.objects.filter(
    block=OuterRef('pk')
).order_by('-created_at')

blocks = Block.objects.annotate(
    latest_order_date=Subquery(latest_orders.values('created_at')[:1])
)
```

### Window Functions (PostgreSQL)
```python
from django.db.models import Window, F
from django.db.models.functions import RowNumber, Rank

# Rank blocks by usage within each category
blocks = Block.objects.annotate(
    rank=Window(
        expression=Rank(),
        partition_by=[F('component__category')],
        order_by=F('usage_count').desc()
    )
)
```

## Monitoring and Profiling

### Django Silk
```python
# settings.py
INSTALLED_APPS = [
    'silk',
]

MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
]

# Access at /silk/ to see request profiling
```

### Custom Query Logging
```python
import time
from django.db import connection

class QueryLogger:
    """Context manager for query logging"""
    
    def __enter__(self):
        self.start_queries = len(connection.queries)
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        num_queries = len(connection.queries) - self.start_queries
        duration = end_time - self.start_time
        
        print(f"Queries: {num_queries}, Time: {duration:.3f}s")
        
        if num_queries > 10:
            print("WARNING: High query count!")

# Usage
with QueryLogger():
    blocks = list(Block.objects.select_related('component').all())
```

## Best Practices

- Always use select_related() for ForeignKey relationships in list views
- Use prefetch_related() for ManyToMany and reverse ForeignKey
- Add indexes for fields used in WHERE, ORDER BY, and JOIN clauses
- Use exists() instead of count() for boolean checks
- Cache expensive queries that don't change frequently
- Use bulk operations for multiple database writes
- Profile queries in development before deploying
- Monitor query performance in production
- Set query timeouts to prevent long-running queries
- Use database connection pooling in production

## Common Mistakes

- Accessing related objects in loops without select_related()
- Using count() when exists() is sufficient
- Not using indexes on frequently queried fields
- Fetching all fields when only a few are needed
- Not using bulk operations for multiple inserts
- Caching querysets instead of lists (querysets are lazy)
- Ignoring database-specific optimizations (PostgreSQL features)
- Not testing with production-like data volumes

## Resources

- [Django Database Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
