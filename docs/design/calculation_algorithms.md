# Build Order Calculation Algorithms

**Document Version:** 1.0  
**Last Updated:** 2026-02-02  
**Related Enhancement:** ENH-0000009

---

## Overview

This document describes the calculation algorithms used by the BuildOrder model to compute resource requirements, fabrication times, and mass totals for multi-block build orders in the Space Engineers 2 Calculator.

The calculation system follows a hierarchical resource chain:
```
Build Order → Blocks → Components → Ores
```

---

## Core Algorithms

### 1. Total Mass Calculation

**Method:** `calculate_total_mass()`

**Purpose:** Calculate the total mass of all blocks in the build order.

**Algorithm:**
```
total_mass = 0
for each (block_id, quantity) in build_order.blocks:
    block = get_block(block_id)
    total_mass += block.mass × quantity
return total_mass
```

**Example:**
```python
# Build Order:
# - Armor Block (150 kg) × 10
# - Light Armor Block (50 kg) × 20

total_mass = (150 × 10) + (50 × 20)
total_mass = 1500 + 1000
total_mass = 2500 kg
```

**Complexity:** O(n) where n = number of unique blocks

**Properties:**
- Commutative: Order of blocks doesn't affect result
- Linear scaling: Doubling quantities doubles mass
- Non-negative: Always returns ≥ 0

---

### 2. Required Components Calculation

**Method:** `calculate_required_components()`

**Purpose:** Aggregate all component requirements across all blocks.

**Algorithm:**
```
components = {}
for each (block_id, block_quantity) in build_order.blocks:
    block = get_block(block_id)
    for each (component_id, component_quantity) in block.components:
        if component_id in components:
            components[component_id] += component_quantity × block_quantity
        else:
            components[component_id] = component_quantity × block_quantity
return components
```

**Example:**
```python
# Build Order:
# - Block A (requires 5 Steel Plates, 2 Motors) × 3
# - Block B (requires 3 Steel Plates, 1 Computer) × 2

# Steel Plates: (5 × 3) + (3 × 2) = 15 + 6 = 21
# Motors: (2 × 3) = 6
# Computer: (1 × 2) = 2

components = {
    'steel_plate_id': 21,
    'motor_id': 6,
    'computer_id': 2
}
```

**Complexity:** O(n × m) where n = blocks, m = avg components per block

**Properties:**
- Aggregates shared components across different blocks
- Linear scaling with block quantities
- Handles empty component lists gracefully

---

### 3. Required Ores Calculation

**Method:** `calculate_required_ores()`

**Purpose:** Traverse through components to calculate total ore requirements.

**Algorithm:**
```
ores = {}
components = calculate_required_components()

for each (component_id, component_quantity) in components:
    component = get_component(component_id)
    for each (ore_id, ore_quantity) in component.materials:
        if ore_id in ores:
            ores[ore_id] += ore_quantity × component_quantity
        else:
            ores[ore_id] = ore_quantity × component_quantity
return ores
```

**Example:**
```python
# From previous example, we have:
# - 21 Steel Plates (each requires 7 Iron)
# - 6 Motors (each requires 3 Iron, 2 Nickel)
# - 2 Computers (each requires 1 Iron, 2 Silicon)

# Iron: (21 × 7) + (6 × 3) + (2 × 1) = 147 + 18 + 2 = 167
# Nickel: (6 × 2) = 12
# Silicon: (2 × 2) = 4

ores = {
    'iron_id': 167,
    'nickel_id': 12,
    'silicon_id': 4
}
```

**Complexity:** O(n × m × p) where n = blocks, m = components, p = ores per component

**Properties:**
- Traverses full resource chain
- Aggregates same ore from different components
- Handles multiple ore types per component

---

### 4. Fabricator Times Calculation

**Method:** `calculate_fabricator_times()`

**Purpose:** Calculate total fabrication time grouped by fabricator type.

**Algorithm:**
```
fabricators = {}
components = calculate_required_components()

for each (component_id, component_quantity) in components:
    component = get_component(component_id)
    fabricator_type = component.fabricator_type
    crafting_time = component.crafting_time × component_quantity
    
    if fabricator_type in fabricators:
        fabricators[fabricator_type] += crafting_time
    else:
        fabricators[fabricator_type] = crafting_time
return fabricators
```

**Example:**
```python
# From previous example:
# - 21 Steel Plates (Assembler, 2 sec each)
# - 6 Motors (Refinery, 8 sec each)
# - 2 Computers (Assembler, 5 sec each)

# Assembler: (21 × 2) + (2 × 5) = 42 + 10 = 52 seconds
# Refinery: (6 × 8) = 48 seconds

fabricators = {
    'Assembler': 52,
    'Refinery': 48
}
```

**Complexity:** O(n × m) where n = blocks, m = components per block

**Properties:**
- Groups by fabricator type
- Sums times for same fabricator type
- Useful for production planning

---

## Calculation Summary

**Method:** `get_calculation_summary()`

**Purpose:** Return all calculations in a single comprehensive summary.

**Algorithm:**
```
return {
    'total_mass': calculate_total_mass(),
    'required_components': calculate_required_components(),
    'required_ores': calculate_required_ores(),
    'fabricator_times': calculate_fabricator_times()
}
```

**Caching:** Results are cached for 5 minutes with key `buildorder_calc_{order_id}`

---

## Helper Methods

### Component Details

**Method:** `_get_components_with_details()`

**Purpose:** Enrich component data with component objects and calculated totals.

**Returns:**
```python
[
    {
        'component': Component object,
        'quantity': int,
        'total_mass': float  # component.mass × quantity
    },
    ...
]
```

### Ore Details

**Method:** `_get_ores_with_details()`

**Purpose:** Enrich ore data with ore objects.

**Returns:**
```python
[
    {
        'ore': Ore object,
        'quantity': float
    },
    ...
]
```

---

## Performance Considerations

### Caching Strategy

**Implementation:**
- Cache key: `buildorder_calc_{order_id}`
- TTL: 5 minutes (300 seconds)
- Invalidation: Automatic on save()
- Bypass: `use_cache=False` parameter

**Benefits:**
- Reduces database queries for repeated calculations
- Improves response time for large build orders
- Automatic invalidation ensures data consistency

### Query Optimization

**Current Approach:**
- Individual queries per block/component/ore
- Suitable for typical build orders (< 100 blocks)

**Future Optimization (if needed):**
- Use `select_related()` for foreign key lookups
- Use `prefetch_related()` for many-to-many relationships
- Batch queries for large build orders

---

## Mathematical Properties

### Linearity

All calculations scale linearly with quantities:
```
calc(n × quantity) = n × calc(quantity)
```

**Proof by example:**
- If 1 block requires 5 components
- Then 10 blocks require 50 components
- calc(10 blocks) = 10 × calc(1 block)

### Commutativity

Block order doesn't affect results:
```
calc([A, B, C]) = calc([C, A, B])
```

**Reason:** Addition is commutative, and we're summing quantities.

### Non-negativity

All results are non-negative:
```
∀ calculations: result ≥ 0
```

**Guaranteed by:**
- Validation rejects negative/zero quantities
- All base values (mass, quantities) are positive
- Multiplication and addition preserve non-negativity

### Determinism

Same input always produces same output:
```
calc(order) = calc(order)  ∀ calls
```

**Ensured by:**
- No random elements
- No time-dependent calculations
- Consistent database state

---

## Error Handling

### Invalid Block IDs

**Detection:** `validate_blocks()` checks all block IDs exist
**Handling:** Raises `ValidationError` before calculation
**Prevention:** Called automatically in `clean()` and `save()`

### Missing Components

**Detection:** Try/except blocks in calculation methods
**Handling:** Skip missing components, continue calculation
**Logging:** Silent skip (component may have been deleted)

### Non-numeric Quantities

**Detection:** Type checking during validation
**Handling:** Raises `ValidationError` or `TypeError`
**Prevention:** JSONField validation + custom validation

---

## Usage Examples

### Basic Usage

```python
from buildorders.models import BuildOrder

# Create build order
order = BuildOrder.objects.create(
    name="Small Base",
    blocks={
        'armor_block_id': 50,
        'window_block_id': 10
    }
)

# Get calculations
summary = order.get_calculation_summary()
print(f"Total mass: {summary['total_mass']} kg")
print(f"Components needed: {len(summary['required_components'])}")
print(f"Ores needed: {len(summary['required_ores'])}")
```

### With Caching

```python
# First call - calculates and caches
summary1 = order.get_cached_calculation_summary()

# Second call - returns cached result (fast)
summary2 = order.get_cached_calculation_summary()

# Bypass cache for testing
summary3 = order.get_cached_calculation_summary(use_cache=False)
```

### Detailed Component Info

```python
# Get component details
components = order._get_components_with_details()
for item in components:
    print(f"{item['component'].name}: {item['quantity']} units")
    print(f"  Total mass: {item['total_mass']} kg")
```

---

## Testing

All algorithms are tested with:
- **Unit tests:** Verify individual calculations
- **Property-based tests:** Verify mathematical properties
- **Integration tests:** Verify end-to-end workflows

See `buildorders/tests.py` for complete test suite (52 tests).

---

## References

- **Enhancement:** ENH-0000009
- **Model:** `buildorders/models.py`
- **Tests:** `buildorders/tests.py`
- **Admin:** `buildorders/admin.py`

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-02 | Initial documentation |
