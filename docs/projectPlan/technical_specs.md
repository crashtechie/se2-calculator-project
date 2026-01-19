# Technical Specifications

## Data Structures

### JSONField Formats

#### Component.material
```json
[
  {
    "ore_id": "uuid-string",
    "ore_name": "Iron Ore",
    "quantity": 10.5
  },
  {
    "ore_id": "uuid-string",
    "ore_name": "Silicon Ore",
    "quantity": 5.0
  }
]
```

#### Block.components
```json
[
  {
    "component_id": "uuid-string",
    "component_name": "Steel Plate",
    "quantity": 25
  },
  {
    "component_id": "uuid-string",
    "component_name": "Construction Component",
    "quantity": 10
  }
]
```

#### BuildOrder.blocks
```json
[
  {
    "block_id": "uuid-string",
    "block_name": "Large Reactor",
    "quantity": 2
  },
  {
    "block_id": "uuid-string",
    "block_name": "Small Reactor",
    "quantity": 5
  }
]
```

## Database Schema

### Ores Table
```sql
CREATE TABLE ores (
    object_id UUID PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    mass FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### Components Table
```sql
CREATE TABLE components (
    object_id UUID PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    mass FLOAT NOT NULL,
    material JSONB NOT NULL,
    fabricator VARCHAR(255) NOT NULL,
    crafting_time FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### Blocks Table
```sql
CREATE TABLE blocks (
    object_id UUID PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    mass FLOAT NOT NULL,
    components JSONB NOT NULL,
    health FLOAT NOT NULL,
    pcu INTEGER NOT NULL,
    snap_size FLOAT NOT NULL,
    input_mass INTEGER NOT NULL,
    output_mass INTEGER NOT NULL,
    consumer_type VARCHAR(255),
    consumer_rate FLOAT DEFAULT 0,
    producer_type VARCHAR(255),
    producer_rate FLOAT DEFAULT 0,
    storage_capacity FLOAT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### BuildOrders Table
```sql
CREATE TABLE buildorders (
    order_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    blocks JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

## Calculation Algorithms

### Total Mass Calculation
```python
def calculate_total_mass(blocks_data):
    """
    Calculate total mass of all blocks in build order.
    
    Args:
        blocks_data: List of dicts with block_id and quantity
    
    Returns:
        float: Total mass in kg
    """
    total = 0
    for item in blocks_data:
        block = Block.objects.get(object_id=item['block_id'])
        total += block.mass * item['quantity']
    return total
```

### Component Aggregation
```python
def calculate_required_components(blocks_data):
    """
    Aggregate all components needed for build order.
    
    Args:
        blocks_data: List of dicts with block_id and quantity
    
    Returns:
        dict: {component_id: {name, quantity, fabricator, crafting_time}}
    """
    components = {}
    for item in blocks_data:
        block = Block.objects.get(object_id=item['block_id'])
        for comp in block.components:
            comp_id = comp['component_id']
            qty = comp['quantity'] * item['quantity']
            
            if comp_id in components:
                components[comp_id]['quantity'] += qty
            else:
                component = Component.objects.get(object_id=comp_id)
                components[comp_id] = {
                    'name': component.name,
                    'quantity': qty,
                    'fabricator': component.fabricator,
                    'crafting_time': component.crafting_time
                }
    return components
```

### Ore Aggregation
```python
def calculate_required_ores(components_data):
    """
    Aggregate all ores needed from components.
    
    Args:
        components_data: Dict of component_id: {quantity, ...}
    
    Returns:
        dict: {ore_id: {name, quantity}}
    """
    ores = {}
    for comp_id, comp_data in components_data.items():
        component = Component.objects.get(object_id=comp_id)
        for material in component.material:
            ore_id = material['ore_id']
            qty = material['quantity'] * comp_data['quantity']
            
            if ore_id in ores:
                ores[ore_id]['quantity'] += qty
            else:
                ore = Ore.objects.get(object_id=ore_id)
                ores[ore_id] = {
                    'name': ore.name,
                    'quantity': qty
                }
    return ores
```

### Fabricator Time Calculation
```python
def calculate_fabricator_times(components_data):
    """
    Calculate total crafting time by fabricator type.
    
    Args:
        components_data: Dict of component_id: {quantity, fabricator, crafting_time}
    
    Returns:
        dict: {fabricator_type: total_seconds}
    """
    fabricators = {}
    for comp_data in components_data.values():
        fab = comp_data['fabricator']
        time = comp_data['crafting_time'] * comp_data['quantity']
        
        if fab in fabricators:
            fabricators[fab] += time
        else:
            fabricators[fab] = time
    return fabricators
```

## Model Validators

### JSONField Structure Validators
```python
from django.core.exceptions import ValidationError
import json

def validate_material_structure(value):
    """Validate Component.material JSONField structure."""
    if not isinstance(value, list):
        raise ValidationError("Material must be a list")
    
    for item in value:
        if not isinstance(item, dict):
            raise ValidationError("Each material item must be a dict")
        
        required_keys = ['ore_id', 'ore_name', 'quantity']
        if not all(key in item for key in required_keys):
            raise ValidationError(f"Material must have keys: {required_keys}")
        
        if not isinstance(item['quantity'], (int, float)) or item['quantity'] <= 0:
            raise ValidationError("Quantity must be positive number")

def validate_components_structure(value):
    """Validate Block.components JSONField structure."""
    if not isinstance(value, list):
        raise ValidationError("Components must be a list")
    
    for item in value:
        if not isinstance(item, dict):
            raise ValidationError("Each component item must be a dict")
        
        required_keys = ['component_id', 'component_name', 'quantity']
        if not all(key in item for key in required_keys):
            raise ValidationError(f"Component must have keys: {required_keys}")
        
        if not isinstance(item['quantity'], int) or item['quantity'] <= 0:
            raise ValidationError("Quantity must be positive integer")
```

## URL Patterns

```python
# Main urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('ores/', include('ores.urls')),
    path('components/', include('components.urls')),
    path('blocks/', include('blocks.urls')),
]

# ores/urls.py
app_name = 'ores'
urlpatterns = [
    path('', OreListView.as_view(), name='list'),
    path('<uuid:pk>/', OreDetailView.as_view(), name='detail'),
    path('create/', OreCreateView.as_view(), name='create'),
    path('<uuid:pk>/update/', OreUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', OreDeleteView.as_view(), name='delete'),
]

# Similar patterns for components and blocks
```

## Dependencies

### Python Packages
```toml
[project.dependencies]
django = ">=6.0.1"
psycopg2-binary = ">=2.9.0"
uuid-utils = ">=0.9.0"  # For UUIDv7 support

[project.optional-dependencies]
test = [
    "pytest>=8.0.0",
    "pytest-django>=4.8.0",
    "pytest-cov>=4.1.0",
    "factory-boy>=3.3.0",
    "faker>=22.0.0",
]
```

## Performance Considerations

### Database Indexes
```python
class Meta:
    indexes = [
        models.Index(fields=['name']),
        models.Index(fields=['mass']),
        models.Index(fields=['created_at']),
    ]
```

### Query Optimization
- Use select_related() for foreign key lookups
- Use prefetch_related() for JSONField data
- Cache calculation results for build orders
- Add pagination to list views (25 items per page)

## Security Considerations

- Validate all JSONField data before saving
- Use Django's CSRF protection on all forms
- Sanitize user input in search/filter fields
- Use parameterized queries (Django ORM handles this)
- Implement rate limiting for API endpoints (if added)

## Future Enhancements

- User authentication and authorization
- Export build orders to CSV/PDF
- Import data from CSV files
- API for external integrations
- Real-time calculation updates with WebSockets
- Build order templates
- Sharing build orders between users
- Version history for objects
