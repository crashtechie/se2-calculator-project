# Resource Chain & Data Model

## Data Flow Architecture

```
Ores → Components → Blocks → Build Orders
```

Each level depends on the previous, creating a hierarchical resource chain.

## Model Relationships

### Ores (Base Level)
- **Primary Key**: UUIDv7
- **Fields**: name, mass, description
- **No Dependencies**: Foundation of the resource chain
- **Used By**: Components (via JSONField materials)

### Components (Level 2)
- **Primary Key**: UUIDv7
- **Fields**: name, mass, description, materials (JSONField)
- **Dependencies**: Ores
- **Materials Format**:
  ```json
  {
    "ore_uuid": quantity,
    "ore_uuid": quantity
  }
  ```
- **Used By**: Blocks (via JSONField components)

### Blocks (Level 3)
- **Primary Key**: UUIDv7
- **Fields**: name, mass, description, components (JSONField)
- **Dependencies**: Components
- **Components Format**:
  ```json
  {
    "component_uuid": quantity,
    "component_uuid": quantity
  }
  ```
- **Used By**: BuildOrders (via JSONField blocks)

### BuildOrders (Level 4)
- **Primary Key**: UUIDv7
- **Fields**: name, description, blocks (JSONField), created_at, updated_at
- **Dependencies**: Blocks
- **Blocks Format**:
  ```json
  {
    "block_uuid": quantity,
    "block_uuid": quantity
  }
  ```

## Calculation Methods

### Component-to-Ore Calculation
```python
def calculate_total_ores(self):
    """Recursively calculate ore requirements from components."""
    # Aggregate all component requirements
    # For each component, multiply by quantity
    # Sum ore requirements across all components
    # Return {ore_uuid: total_quantity}
```

### Block-to-Component Calculation
```python
def calculate_total_components(self):
    """Calculate component requirements from blocks."""
    # Aggregate all block requirements
    # For each block, multiply components by quantity
    # Return {component_uuid: total_quantity}
```

### Full Chain Calculation
```python
def calculate_full_chain(self):
    """Calculate complete resource chain: Blocks → Components → Ores."""
    # Get component totals
    # For each component, get ore requirements
    # Multiply by component quantity
    # Aggregate all ore requirements
```

## Caching Strategy

### Cache Keys
- `buildorder_{uuid}_components`: Component totals (5 min TTL)
- `buildorder_{uuid}_ores`: Ore totals (5 min TTL)

### Cache Invalidation
- On BuildOrder save/update
- On related Block/Component/Ore changes (future enhancement)

## Validation Rules

### JSONField Validation
- All UUIDs must reference existing objects
- Quantities must be positive integers
- No circular dependencies
- No duplicate entries

### Data Integrity
- Validate on model `clean()` method
- Raise `ValidationError` for invalid data
- Check in admin interface before save
- Test thoroughly in unit tests

## Query Optimization

### Avoiding N+1 Queries
```python
# Bad: N+1 queries
for block_uuid in build_order.blocks.keys():
    block = Block.objects.get(id=block_uuid)  # Query per block

# Good: Single query with prefetch
block_uuids = build_order.blocks.keys()
blocks = Block.objects.filter(id__in=block_uuids)
```

### Bulk Operations
- Use `bulk_create()` for multiple inserts
- Use `update()` for multiple updates
- Minimize database round trips

## Future Enhancements

### Planned Features
- Real-time cache invalidation on related model changes
- Optimized calculation algorithms
- Materialized views for common queries
- GraphQL API for flexible querying
- Export/import functionality for build orders
