---
inclusion: auto
fileMatchPattern: '**/models.py'
description: Database design principles including schema design, normalization, indexing, and PostgreSQL-specific optimizations
---

# Database Design Best Practices

## Project Database Architecture

### Technology Stack
- **Production**: PostgreSQL (via Docker)
- **Development**: SQLite (fallback)
- **Primary Keys**: UUIDv7 (time-ordered UUIDs)
- **Relationships**: JSONField for flexible associations
- **Caching**: Redis (5-minute TTL for calculations)

### Data Model Hierarchy

```
Ores (base resources)
  ↓ materials (JSONField)
Components (craftable items)
  ↓ components (JSONField)
Blocks (buildable structures)
  ↓ blocks (JSONField)
Build Orders (collections with calculations)
```

## Schema Design Principles

### 1. Choose Appropriate Primary Keys

**Project Standard: UUIDv7**

```python
from uuid_utils import uuid7

def generate_uuid():
    """Generate UUIDv7 string for primary key."""
    return str(uuid7())

class MyModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=generate_uuid,
        editable=False,
        help_text="UUIDv7 primary key"
    )
```

**Why UUIDv7 over other options:**

| Type | Pros | Cons | Use Case |
|------|------|------|----------|
| Auto-increment | Simple, compact | Not distributed-safe | Single database |
| UUIDv4 | Globally unique | Random (poor index performance) | Distributed systems |
| **UUIDv7** | Time-ordered + unique | Slightly larger than int | **Our choice** |

**UUIDv7 Benefits:**
- Time-ordered (better B-tree index performance)
- Globally unique (no coordination needed)
- Compatible with distributed systems
- Better than UUIDv4 for database performance

### 2. Field Type Selection

```python
# Text Fields
name = models.CharField(max_length=100)  # Fixed max length
description = models.TextField()  # Unlimited text

# Numeric Fields
mass = models.FloatField()  # Floating point
quantity = models.IntegerField()  # Whole numbers
price = models.DecimalField(max_digits=10, decimal_places=2)  # Money

# Boolean
is_active = models.BooleanField(default=True)

# Dates
created_at = models.DateTimeField(auto_now_add=True)  # Set once
updated_at = models.DateTimeField(auto_now=True)  # Update on save

# JSON (PostgreSQL optimized)
components = models.JSONField(default=dict)

# UUID
block_id = models.UUIDField(primary_key=True, default=generate_uuid)
```

**Field Type Guidelines:**
- Use `CharField` for short text with known max length
- Use `TextField` for long text without length limit
- Use `DecimalField` for money (not FloatField)
- Use `JSONField` for flexible/dynamic data
- Always set `default` for non-nullable fields

### 3. Null vs Blank

```python
# null=True: Database allows NULL
# blank=True: Form validation allows empty

# Optional text field
description = models.TextField(blank=True)  # Empty string, not NULL

# Optional foreign key
category = models.ForeignKey(
    Category,
    null=True,  # Database NULL
    blank=True,  # Form can be empty
    on_delete=models.SET_NULL
)

# Optional number
tier = models.IntegerField(null=True, blank=True)

# Required field with default
is_active = models.BooleanField(default=True)  # Not nullable
```

**Guidelines:**
- Text fields: Use `blank=True`, not `null=True`
- Foreign keys: Use both `null=True` and `blank=True`
- Numbers: Use `null=True` for truly optional values
- Booleans: Use `default=True/False`, not nullable

### 4. Relationships

#### Foreign Keys (One-to-Many)

```python
# Standard foreign key
class Block(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,  # Delete blocks when category deleted
        related_name='blocks',  # Access via category.blocks.all()
    )

# Optional foreign key
class Block(models.Model):
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # Keep block if user deleted
    )
```

**on_delete Options:**
- `CASCADE`: Delete this object when referenced object deleted
- `SET_NULL`: Set to NULL (requires null=True)
- `PROTECT`: Prevent deletion of referenced object
- `SET_DEFAULT`: Set to default value
- `DO_NOTHING`: No action (can cause integrity errors)

#### Many-to-Many

```python
# Simple many-to-many
class Block(models.Model):
    tags = models.ManyToManyField('Tag', blank=True)

# Many-to-many with extra fields
class Block(models.Model):
    components = models.ManyToManyField(
        'Component',
        through='BlockComponent',
    )

class BlockComponent(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    class Meta:
        unique_together = [['block', 'component']]
```

#### JSONField Relationships (Project Pattern)

```python
# Flexible relationships using JSONField
class Block(models.Model):
    components = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON object mapping component IDs to quantities"
    )
    # Format: {"component_uuid": quantity, ...}
    
    def validate_components(self):
        """Validate component references."""
        for comp_id, quantity in self.components.items():
            # Validate component exists
            try:
                Component.objects.get(component_id=comp_id)
            except Component.DoesNotExist:
                raise ValidationError(f"Component {comp_id} not found")
```

**When to use JSONField vs ForeignKey:**

| Use JSONField when: | Use ForeignKey when: |
|---------------------|----------------------|
| Flexible structure | Fixed relationship |
| Performance over integrity | Need referential integrity |
| Denormalized data | Normalized data |
| Dynamic relationships | Static relationships |

## Normalization

### Normal Forms

**1NF (First Normal Form):**
- Atomic values (no arrays in columns)
- Each column has unique name
- Order doesn't matter

```python
# GOOD: 1NF compliant
class Block(models.Model):
    name = models.CharField(max_length=100)
    mass = models.FloatField()

# BAD: Not 1NF (comma-separated values)
class Block(models.Model):
    tags = models.CharField(max_length=200)  # "tag1,tag2,tag3"
```

**2NF (Second Normal Form):**
- Must be in 1NF
- No partial dependencies

```python
# GOOD: 2NF compliant
class Component(models.Model):
    name = models.CharField(max_length=100)
    mass = models.FloatField()

class ComponentMaterial(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    ore = models.ForeignKey(Ore, on_delete=models.CASCADE)
    quantity = models.IntegerField()
```

**3NF (Third Normal Form):**
- Must be in 2NF
- No transitive dependencies

```python
# GOOD: 3NF compliant
class Block(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=50)
    tier = models.IntegerField()

# BAD: Not 3NF (tier depends on category, not block)
class Block(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    tier = models.IntegerField()  # Depends on category
```

### Denormalization (When Appropriate)

```python
# Denormalize for performance
class BuildOrder(models.Model):
    name = models.CharField(max_length=200)
    blocks = models.JSONField(default=dict)
    
    # Denormalized calculated field (cached)
    total_mass = models.FloatField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Update denormalized field
        self.total_mass = self.calculate_total_mass()
        super().save(*args, **kwargs)
```

**When to denormalize:**
- Expensive calculations accessed frequently
- Read-heavy workloads
- Performance is critical
- Data doesn't change often

**Denormalization trade-offs:**
- ✅ Faster reads
- ✅ Simpler queries
- ❌ Data duplication
- ❌ Update complexity
- ❌ Potential inconsistency

## Indexing Strategy

### When to Add Indexes

```python
class Block(models.Model):
    # Index on frequently queried fields
    name = models.CharField(max_length=100, db_index=True)
    
    # Foreign keys (Django adds indexes automatically)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            # Single field index
            models.Index(fields=['name']),
            
            # Composite index (order matters!)
            models.Index(fields=['category', 'tier']),
            
            # Descending index (for ORDER BY -created_at)
            models.Index(fields=['-created_at']),
            
            # Named index
            models.Index(fields=['name'], name='blocks_name_idx'),
        ]
```

**Index Guidelines:**
- Index fields used in WHERE clauses
- Index fields used in ORDER BY
- Index foreign keys (Django does this automatically)
- Index fields used in JOIN operations
- Don't over-index (each index has overhead)

### Composite Indexes

```python
# Order matters in composite indexes!
class Meta:
    indexes = [
        # Good for: WHERE category=X AND tier=Y
        # Good for: WHERE category=X
        # NOT good for: WHERE tier=Y (only)
        models.Index(fields=['category', 'tier']),
    ]
```

**Composite Index Rules:**
- Most selective field first
- Fields used together in queries
- Can be used for prefix queries
- Order matters for query optimization

### Index Monitoring

```sql
-- PostgreSQL: Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan ASC;

-- Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname
FROM pg_stat_user_indexes
WHERE idx_scan = 0
    AND indexname NOT LIKE 'pg_toast%';
```

## Constraints

### Database-Level Constraints

```python
class Block(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mass = models.FloatField()
    
    class Meta:
        constraints = [
            # Check constraint
            models.CheckConstraint(
                check=models.Q(mass__gte=0),
                name='block_mass_positive'
            ),
            
            # Unique together
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_block_per_category'
            ),
            
            # Partial unique constraint (PostgreSQL)
            models.UniqueConstraint(
                fields=['name'],
                condition=models.Q(is_active=True),
                name='unique_active_block_name'
            ),
        ]
```

**Constraint Types:**
- `unique=True`: Single field uniqueness
- `UniqueConstraint`: Multi-field uniqueness
- `CheckConstraint`: Value validation
- `unique_together`: Legacy multi-field uniqueness

## PostgreSQL-Specific Features

### JSONField Queries

```python
# Query JSON data
blocks = Block.objects.filter(
    components__has_key='component_uuid'
)

# Query nested JSON
blocks = Block.objects.filter(
    metadata__settings__enabled=True
)

# JSON array contains
blocks = Block.objects.filter(
    tags__contains=['armor', 'heavy']
)
```

### Full-Text Search

```python
from django.contrib.postgres.search import SearchVector, SearchQuery

# Add search vector
class Block(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        indexes = [
            # GIN index for full-text search
            models.Index(
                fields=['name', 'description'],
                name='block_search_idx',
                opclasses=['gin_trgm_ops', 'gin_trgm_ops']
            ),
        ]

# Search
blocks = Block.objects.annotate(
    search=SearchVector('name', 'description')
).filter(search=SearchQuery('reactor'))
```

### Array Fields (PostgreSQL)

```python
from django.contrib.postgres.fields import ArrayField

class Block(models.Model):
    tags = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        default=list
    )

# Query arrays
blocks = Block.objects.filter(tags__contains=['armor'])
blocks = Block.objects.filter(tags__overlap=['armor', 'heavy'])
```

## Performance Optimization

### Query Optimization

```python
# Use select_related for foreign keys
blocks = Block.objects.select_related('category').all()

# Use prefetch_related for many-to-many
blocks = Block.objects.prefetch_related('tags').all()

# Only fetch needed fields
blocks = Block.objects.only('id', 'name', 'mass')

# Defer large fields
blocks = Block.objects.defer('description')

# Count efficiently
count = Block.objects.count()  # Not len(Block.objects.all())

# Exists check
exists = Block.objects.filter(name='Reactor').exists()
```

### Bulk Operations

```python
# Bulk create
Block.objects.bulk_create([
    Block(name='Block 1', mass=10.0),
    Block(name='Block 2', mass=20.0),
])

# Bulk update
Block.objects.filter(category='armor').update(tier=2)

# Bulk delete
Block.objects.filter(is_active=False).delete()
```

### Database Connection Pooling

```python
# settings.py (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Connection pooling (10 minutes)
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

## Database Design Checklist

### Schema Design
- [ ] Use UUIDv7 for primary keys
- [ ] Choose appropriate field types
- [ ] Set appropriate null/blank settings
- [ ] Add help_text to all fields
- [ ] Use explicit table names (db_table)

### Relationships
- [ ] Choose appropriate relationship type
- [ ] Set correct on_delete behavior
- [ ] Add related_name for reverse relations
- [ ] Validate JSONField relationships

### Constraints
- [ ] Add unique constraints where needed
- [ ] Add check constraints for validation
- [ ] Use database-level constraints
- [ ] Test constraint violations

### Indexes
- [ ] Index frequently queried fields
- [ ] Add composite indexes for common queries
- [ ] Index foreign keys (automatic)
- [ ] Monitor index usage

### Performance
- [ ] Use select_related/prefetch_related
- [ ] Add database indexes
- [ ] Consider denormalization for hot paths
- [ ] Use bulk operations
- [ ] Enable connection pooling

### Documentation
- [ ] Document schema design decisions
- [ ] Add field help_text
- [ ] Document relationships
- [ ] Maintain ER diagrams
