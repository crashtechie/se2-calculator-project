---
inclusion: auto
fileMatchPattern: '**/models.py'
description: Django backend architecture patterns for Space Engineers 2 Calculator including models, business logic, and data relationships
---

# Django Backend Architecture

## Project-Specific Context

This is the Space Engineers 2 Calculator backend, a Django application that models the resource chain:
- **Ores** → **Components** → **Blocks** → **Build Orders**

### Core Models
- `Ore`: Base resources (iron, silicon, etc.)
- `Component`: Craftable items made from ores (steel plates, circuits, etc.)
- `Block`: Buildable structures made from components (reactors, thrusters, etc.)
- `BuildOrder`: Collections of blocks with resource calculations

### Key Design Decisions
- **UUIDv7 Primary Keys**: All models use UUIDv7 for better distributed system compatibility
- **JSONField for Relationships**: Component/material requirements stored as JSON for flexibility
- **Calculation Caching**: BuildOrder calculations cached with 5-minute TTL
- **Validation in Models**: Business logic lives in models (fat models, thin views)

## Model Design Patterns

### UUIDv7 Primary Keys

All models use UUIDv7 as primary keys for better performance and distributed compatibility.

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

**Why UUIDv7?**
- Time-ordered (better database performance than UUIDv4)
- Globally unique (no coordination needed)
- Compatible with distributed systems
- Better index performance than random UUIDs

### JSONField for Flexible Relationships

Use JSONField for dynamic relationships where the structure may vary.

```python
class Block(models.Model):
    # Store component requirements as JSON
    components = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON object mapping component IDs to quantities"
    )
    
    def validate_components(self):
        """Validate that all component_ids reference valid Components."""
        if not self.components:
            return True, []
        
        errors = []
        for component_id, quantity in self.components.items():
            # Validate quantity
            if not isinstance(quantity, (int, float)) or quantity <= 0:
                errors.append(f"Invalid quantity for {component_id}: {quantity}")
            
            # Validate component exists
            try:
                Component.objects.get(component_id=component_id)
            except Component.DoesNotExist:
                errors.append(f"Component {component_id} does not exist")
        
        return len(errors) == 0, errors
```

**When to use JSONField:**
- Dynamic relationships (varying number of items)
- Flexible data structures
- Performance over strict relational integrity
- When you need to store metadata

**When NOT to use JSONField:**
- Fixed relationships (use ForeignKey)
- Need database-level constraints
- Complex queries on nested data
- Strict referential integrity required

### Model Validation Pattern

Always validate data in the model's `clean()` method and call it from `save()`.

```python
class BuildOrder(models.Model):
    blocks = models.JSONField(default=dict)
    
    def validate_blocks(self):
        """Validate block references and quantities."""
        errors = []
        for block_id, quantity in self.blocks.items():
            try:
                block = Block.objects.get(block_id=block_id)
                if quantity <= 0:
                    errors.append(f"Invalid quantity for {block.name}: {quantity}")
            except Block.DoesNotExist:
                errors.append(f"Block {block_id} does not exist")
        return errors
    
    def clean(self):
        """Validate model before saving."""
        errors = self.validate_blocks()
        if errors:
            raise ValidationError("Validation errors: " + "; ".join(errors))
    
    def save(self, *args, **kwargs):
        """Override save to validate."""
        self.full_clean()  # Calls clean()
        super().save(*args, **kwargs)
```

**Validation Best Practices:**
- Validate in `clean()` method
- Call `full_clean()` in `save()`
- Return structured errors (list of messages)
- Validate relationships exist
- Validate business rules
- Test validation thoroughly

## Business Logic in Models

Keep business logic in models, not views. This follows Django's "fat models, thin views" philosophy.

### Calculation Methods

```python
class BuildOrder(models.Model):
    def calculate_total_mass(self):
        """Calculate total mass of all blocks."""
        total_mass = 0.0
        for block_id, quantity in self.blocks.items():
            try:
                block = Block.objects.get(block_id=block_id)
                total_mass += block.mass * quantity
            except Block.DoesNotExist:
                continue
        return total_mass
    
    def calculate_required_components(self):
        """Aggregate components across all blocks."""
        components = {}
        for block_id, quantity in self.blocks.items():
            try:
                block = Block.objects.get(block_id=block_id)
                for comp_id, comp_qty in block.components.items():
                    components[comp_id] = components.get(comp_id, 0) + comp_qty * quantity
            except Block.DoesNotExist:
                continue
        return components
    
    def calculate_required_ores(self):
        """Traverse component tree to calculate ore requirements."""
        ores = {}
        components = self.calculate_required_components()
        for comp_id, comp_qty in components.items():
            try:
                component = Component.objects.get(component_id=comp_id)
                for ore_id, ore_qty in component.materials.items():
                    ores[ore_id] = ores.get(ore_id, 0) + ore_qty * comp_qty
            except Component.DoesNotExist:
                continue
        return ores
```

**Why in models?**
- Reusable across views, APIs, management commands
- Testable in isolation
- Encapsulates business logic
- Follows single responsibility principle

### Helper Methods for Views

Provide helper methods that return data in view-friendly formats.

```python
class BuildOrder(models.Model):
    def _get_components_with_details(self):
        """Get components with full details for templates."""
        components = self.calculate_required_components()
        result = []
        for comp_id, qty in components.items():
            try:
                comp = Component.objects.get(component_id=comp_id)
                result.append({
                    'component': comp,
                    'quantity': qty,
                    'total_mass': comp.mass * qty
                })
            except Component.DoesNotExist:
                continue
        return result
    
    def get_calculation_summary(self):
        """Return complete summary for views."""
        return {
            'total_mass': self.calculate_total_mass(),
            'required_components': self.calculate_required_components(),
            'required_ores': self.calculate_required_ores(),
            'fabricator_times': self.calculate_fabricator_times(),
        }
```

## Caching Strategy

### Model-Level Caching

Cache expensive calculations at the model level.

```python
from django.core.cache import cache

class BuildOrder(models.Model):
    def get_cached_calculation_summary(self, use_cache=True):
        """Get calculation summary with caching."""
        cache_key = f"buildorder_calc_{self.order_id}"
        
        if use_cache:
            cached_result = cache.get(cache_key)
            if cached_result:
                return cached_result
        
        summary = self.get_calculation_summary()
        cache.set(cache_key, summary, 300)  # 5 minute TTL
        return summary
    
    def save(self, *args, **kwargs):
        """Invalidate cache on save."""
        super().save(*args, **kwargs)
        cache_key = f"buildorder_calc_{self.order_id}"
        cache.delete(cache_key)
```

**Caching Best Practices:**
- Cache expensive operations (complex calculations, aggregations)
- Use descriptive cache keys (include model ID)
- Set appropriate TTL (5 minutes for calculations)
- Invalidate cache on model changes
- Make caching optional for testing (`use_cache` parameter)

### Cache Key Patterns

```python
# Model instance cache
f"model_{model_name}_{instance_id}"

# Calculation cache
f"{model_name}_calc_{instance_id}"

# List cache
f"{model_name}_list_{filter_params}"

# User-specific cache
f"user_{user_id}_{resource_type}"
```

## Query Optimization

### Avoid N+1 Queries

```python
# BAD: N+1 queries
def get_blocks_with_components():
    blocks = Block.objects.all()
    for block in blocks:
        for comp_id in block.components.keys():
            component = Component.objects.get(component_id=comp_id)  # Query per component!

# GOOD: Prefetch related objects
def get_blocks_with_components():
    blocks = Block.objects.all()
    # Get all component IDs
    component_ids = set()
    for block in blocks:
        component_ids.update(block.components.keys())
    
    # Single query for all components
    components = {
        str(c.component_id): c 
        for c in Component.objects.filter(component_id__in=component_ids)
    }
    
    # Use cached components
    for block in blocks:
        block._cached_components = {
            comp_id: components.get(comp_id)
            for comp_id in block.components.keys()
        }
```

### Bulk Operations

```python
# BAD: Multiple queries
for data in items:
    Block.objects.create(**data)

# GOOD: Bulk create
Block.objects.bulk_create([
    Block(**data) for data in items
])

# BAD: Multiple updates
for block in blocks:
    block.mass = new_mass
    block.save()

# GOOD: Bulk update
Block.objects.filter(id__in=block_ids).update(mass=new_mass)
```

## Model Meta Options

### Essential Meta Settings

```python
class BuildOrder(models.Model):
    class Meta:
        ordering = ['-created_at']  # Default ordering
        verbose_name = 'Build Order'
        verbose_name_plural = 'Build Orders'
        db_table = 'buildorders_buildorder'  # Explicit table name
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
```

**Meta Options to Use:**
- `ordering`: Default sort order
- `verbose_name`: Human-readable name
- `db_table`: Explicit table name (prevents migration issues)
- `indexes`: Database indexes for performance
- `constraints`: Database-level constraints

## Model Methods Best Practices

### Method Naming Conventions

```python
class Block(models.Model):
    # Validation methods: validate_*
    def validate_components(self):
        pass
    
    # Calculation methods: calculate_*
    def calculate_total_mass(self):
        pass
    
    # Getter methods: get_*
    def get_component_objects(self):
        pass
    
    # Iterator methods: iter_*
    def iter_component_requirements(self):
        pass
    
    # Private helpers: _*
    def _get_components_with_details(self):
        pass
```

### Return Types

```python
# Validation methods return (bool, list)
def validate_components(self):
    """Returns: tuple: (is_valid: bool, errors: list)"""
    return True, []

# Calculation methods return primitive types
def calculate_total_mass(self):
    """Returns: float: Total mass in kg"""
    return 0.0

# Getter methods return QuerySets or lists
def get_component_objects(self):
    """Returns: QuerySet: Component objects"""
    return Component.objects.none()

# Summary methods return dicts
def get_calculation_summary(self):
    """Returns: dict: Complete calculation summary"""
    return {}
```

## Error Handling

### Model-Level Exceptions

```python
from django.core.exceptions import ValidationError

class BuildOrder(models.Model):
    def clean(self):
        """Raise ValidationError for invalid data."""
        errors = []
        
        # Collect all validation errors
        block_errors = self.validate_blocks()
        if block_errors:
            errors.extend(block_errors)
        
        # Raise single ValidationError with all errors
        if errors:
            raise ValidationError({
                'blocks': errors
            })
```

### Graceful Degradation

```python
def calculate_required_components(self):
    """Continue processing even if some blocks are missing."""
    components = {}
    for block_id, quantity in self.blocks.items():
        try:
            block = Block.objects.get(block_id=block_id)
            # Process block
        except Block.DoesNotExist:
            # Log error but continue
            logger.warning(f"Block {block_id} not found, skipping")
            continue
    return components
```

## Testing Backend Logic

### Model Tests

```python
def test_build_order_calculate_total_mass():
    """Test mass calculation."""
    ore = Ore.objects.create(name="Iron", mass=1.0)
    component = Component.objects.create(
        name="Steel Plate",
        mass=2.0,
        materials={str(ore.ore_id): 3}
    )
    block = Block.objects.create(
        name="Light Armor",
        mass=5.0,
        components={str(component.component_id): 10}
    )
    build_order = BuildOrder.objects.create(
        name="Test Order",
        blocks={str(block.block_id): 5}
    )
    
    total_mass = build_order.calculate_total_mass()
    assert total_mass == 25.0  # 5 kg * 5 blocks
```

### Validation Tests

```python
def test_build_order_validation_with_invalid_quantity():
    """Test that zero quantity raises ValidationError."""
    block = Block.objects.create(name="Test Block", mass=10.0)
    
    with pytest.raises(ValidationError):
        BuildOrder.objects.create(
            name="Invalid Order",
            blocks={str(block.block_id): 0}  # Invalid!
        )
```

## Performance Monitoring

### Log Slow Queries

```python
import logging
import time

logger = logging.getLogger(__name__)

def calculate_required_ores(self):
    """Calculate ores with performance logging."""
    start_time = time.time()
    
    ores = {}
    # Calculation logic
    
    duration = time.time() - start_time
    if duration > 1.0:  # Log if > 1 second
        logger.warning(
            f"Slow ore calculation for BuildOrder {self.order_id}: {duration:.2f}s"
        )
    
    return ores
```

## Backend Checklist

### Model Design
- [ ] Use UUIDv7 for primary keys
- [ ] Add help_text to all fields
- [ ] Implement `__str__()` method
- [ ] Set appropriate Meta options
- [ ] Add database indexes for queried fields

### Validation
- [ ] Implement `clean()` method
- [ ] Call `full_clean()` in `save()`
- [ ] Validate JSONField contents
- [ ] Validate relationships exist
- [ ] Test all validation paths

### Business Logic
- [ ] Keep logic in models, not views
- [ ] Use descriptive method names
- [ ] Document return types
- [ ] Handle missing relationships gracefully
- [ ] Add helper methods for views

### Performance
- [ ] Cache expensive calculations
- [ ] Invalidate cache on changes
- [ ] Avoid N+1 queries
- [ ] Use bulk operations
- [ ] Add database indexes

### Testing
- [ ] Test model creation
- [ ] Test validation (valid and invalid)
- [ ] Test calculations
- [ ] Test edge cases
- [ ] Test cache invalidation
