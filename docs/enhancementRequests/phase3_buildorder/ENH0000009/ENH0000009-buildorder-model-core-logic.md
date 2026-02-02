# Enhancement Request: Build Order Model & Core Logic

**Filename:** `ENH0000009-buildorder-model-core-logic.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000009  
**Status:** Planned  
**Priority:** High  
**Created Date:** 2026-02-01  
**Updated Date:** 2026-02-01  
**Completion Date:** (pending)  
**Assigned To:** (pending)  
**Estimated Effort:** 1 day  
**Actual Effort:** (pending)

---

## Summary

Create BuildOrder model with calculation methods for aggregating resource requirements across multiple blocks, including total mass, required components, required ores, and fabrication times.

---

## Description

Implement the core data model and business logic for the Build Order Calculator. The BuildOrder model stores a collection of blocks with quantities and provides methods to calculate total resource requirements by traversing the resource chain (Blocks → Components → Ores).

**Key Features:**
- UUIDv7 primary key (consistent with Phase 1 pattern)
- JSONField for blocks storage (dict format: {block_id: quantity})
- Validation methods following Phase 1 patterns
- Calculation methods as model methods (not separate utilities)
- Caching for expensive calculations
- Comprehensive test coverage including property-based tests

**Benefits:**
- Enables multi-block resource planning
- Provides accurate resource calculations
- Foundation for Phase 3 UI
- Reusable calculation logic
- Testable business logic

---

## Current Behavior

- No BuildOrder model exists
- No way to calculate resources for multiple blocks
- Users must manually calculate resource requirements
- No aggregation of components/ores across blocks

---

## Proposed Behavior

- BuildOrder model stores multiple blocks with quantities
- Automatic calculation of:
  - Total mass across all blocks
  - Aggregated component requirements
  - Aggregated ore requirements (traversing through components)
  - Fabrication time by fabricator type
- Validation ensures all block IDs reference valid blocks
- Calculations cached for performance
- Admin interface for management
- Full test coverage (50+ tests)

---

## Acceptance Criteria

- [ ] BuildOrder model created with UUIDv7 primary key
- [ ] JSONField `blocks` uses dict format {block_id: quantity}
- [ ] `validate_blocks()` method validates block IDs and quantities
- [ ] `get_block_objects()` method returns Block queryset
- [ ] `calculate_total_mass()` method returns correct total
- [ ] `calculate_required_components()` method aggregates components
- [ ] `calculate_required_ores()` method traverses to ores
- [ ] `calculate_fabricator_times()` method groups by fabricator type
- [ ] `get_calculation_summary()` method returns complete summary
- [ ] `clean()` and `save()` methods validate before saving
- [ ] Admin interface configured with JSON formatting
- [ ] Calculation results cached (5 minute TTL)
- [ ] Cache invalidated on save
- [ ] All tests pass (50+ tests)
- [ ] Test coverage ≥90% for buildorders app
- [ ] Property-based tests for calculations
- [ ] Documentation complete
- [ ] Code reviewed

---

## Technical Details

### Dependencies
- Django 6.0.1 (existing)
- uuid-utils (existing)
- No new packages required

### Affected Components
- New `buildorders` app
- `blocks` app (for block lookups)
- `components` app (for component lookups)
- `ores` app (for ore lookups)

### Files to Modify/Create

**New Files:**
- `buildorders/__init__.py`
- `buildorders/models.py` (BuildOrder model)
- `buildorders/admin.py` (admin configuration)
- `buildorders/apps.py` (app configuration)
- `buildorders/tests.py` (model tests)
- `buildorders/tests_calculations.py` (calculation tests)
- `buildorders/tests_property_based.py` (property-based tests)
- `buildorders/migrations/0001_initial.py` (auto-generated)

**Modified Files:**
- `se2CalcProject/settings.py` (add 'buildorders' to INSTALLED_APPS)

### Database Changes
- [x] Migrations required
- [x] New model: BuildOrder
- [ ] No schema changes to existing models

---

## Implementation Plan

### Step 1: Create BuildOrders App
```bash
cd app
uv run python manage.py startapp buildorders
```
- Create app structure
- Register in settings.py INSTALLED_APPS
- Create apps.py configuration

### Step 2: Implement BuildOrder Model
```python
# buildorders/models.py
from django.db import models
from uuid_utils import uuid7
from blocks.models import Block
from components.models import Component
from ores.models import Ore

def generate_uuid():
    return str(uuid7())

class BuildOrder(models.Model):
    order_id = models.UUIDField(
        primary_key=True,
        default=generate_uuid,
        editable=False,
        help_text="UUIDv7 primary key"
    )
    
    name = models.CharField(
        max_length=200,
        help_text="Name of the build order"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Optional description"
    )
    
    blocks = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON object mapping block IDs to quantities"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Build Order'
        verbose_name_plural = 'Build Orders'
        db_table = 'buildorders_buildorder'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.name
```

### Step 3: Implement Validation Methods
- `validate_blocks()` - validate block IDs and quantities
- `get_block_objects()` - return Block queryset
- `clean()` - validate before saving
- `save()` - override to call clean() and invalidate cache

### Step 4: Implement Calculation Methods
- `calculate_total_mass()` - sum block masses × quantities
- `calculate_required_components()` - aggregate components across blocks
- `calculate_required_ores()` - traverse components to ores
- `calculate_fabricator_times()` - group by fabricator type
- `get_calculation_summary()` - return complete summary with caching
- `_get_components_with_details()` - helper for component details
- `_get_ores_with_details()` - helper for ore details

### Step 5: Implement Caching
- Cache calculation results with 5 minute TTL
- Cache key: `buildorder_calc_{order_id}`
- Invalidate cache on save
- Optional `use_cache` parameter for testing

### Step 6: Create Migrations
```bash
uv run python manage.py makemigrations buildorders
uv run python manage.py migrate
```

### Step 7: Configure Admin Interface
- Register BuildOrder with admin
- Add list_display: name, blocks_count, total_mass, created_at
- Add readonly_fields: order_id, timestamps, formatted blocks, calculation summary
- Add fieldsets with collapsible sections
- Add custom methods for display (blocks_count, total_mass_display)

### Step 8: Write Tests
**Model Tests (20 tests):**
- Model creation
- Field validation
- UUID generation
- Timestamps
- String representation
- Meta configuration

**Validation Tests (10 tests):**
- validate_blocks() with valid data
- validate_blocks() with invalid block IDs
- validate_blocks() with negative quantities
- validate_blocks() with zero quantities
- get_block_objects() returns correct queryset
- clean() raises ValidationError for invalid data

**Calculation Tests (15 tests):**
- calculate_total_mass() with single block
- calculate_total_mass() with multiple blocks
- calculate_required_components() with single block
- calculate_required_components() with multiple blocks using same component
- calculate_required_ores() traverses correctly
- calculate_fabricator_times() groups correctly
- get_calculation_summary() returns complete data

**Property-Based Tests (5 tests):**
- Ore requirements scale linearly with block quantity
- Component requirements scale linearly
- Mass calculation is commutative (order doesn't matter)
- Adding zero blocks doesn't change totals
- Doubling all quantities doubles all results

**Caching Tests (5 tests):**
- Cache stores calculation results
- Cache returns stored results
- Cache invalidates on save
- use_cache=False bypasses cache

---

## Testing Requirements

### Unit Tests (Minimum 50)

**Model Creation Tests (5):**
- [ ] Create BuildOrder with minimal fields
- [ ] Create BuildOrder with all fields
- [ ] UUID auto-generated
- [ ] Timestamps auto-populated
- [ ] String representation returns name

**Validation Tests (10):**
- [ ] validate_blocks() accepts valid blocks
- [ ] validate_blocks() rejects invalid block IDs
- [ ] validate_blocks() rejects negative quantities
- [ ] validate_blocks() rejects zero quantities
- [ ] validate_blocks() rejects non-numeric quantities
- [ ] get_block_objects() returns correct blocks
- [ ] get_block_objects() returns empty queryset for no blocks
- [ ] clean() raises ValidationError for invalid blocks
- [ ] save() calls clean()
- [ ] save() invalidates cache

**Calculation Tests (20):**
- [ ] calculate_total_mass() with 1 block
- [ ] calculate_total_mass() with multiple blocks
- [ ] calculate_total_mass() with zero blocks returns 0
- [ ] calculate_required_components() with 1 block
- [ ] calculate_required_components() with multiple blocks
- [ ] calculate_required_components() aggregates same component
- [ ] calculate_required_components() with zero blocks returns empty dict
- [ ] calculate_required_ores() traverses to ores
- [ ] calculate_required_ores() aggregates same ore
- [ ] calculate_required_ores() handles multiple components
- [ ] calculate_required_ores() with zero blocks returns empty dict
- [ ] calculate_fabricator_times() groups by type
- [ ] calculate_fabricator_times() sums times correctly
- [ ] calculate_fabricator_times() with zero blocks returns empty dict
- [ ] get_calculation_summary() returns all data
- [ ] get_calculation_summary() includes component details
- [ ] get_calculation_summary() includes ore details
- [ ] get_calculation_summary() includes fabricator times
- [ ] _get_components_with_details() returns correct format
- [ ] _get_ores_with_details() returns correct format

**Property-Based Tests (10):**
- [ ] Ore requirements scale linearly with quantity
- [ ] Component requirements scale linearly
- [ ] Mass calculation is commutative
- [ ] Adding zero blocks doesn't change results
- [ ] Doubling quantities doubles results
- [ ] Calculation results are deterministic
- [ ] No negative results ever produced
- [ ] Component totals ≥ 0
- [ ] Ore totals ≥ 0
- [ ] Fabrication times ≥ 0

**Caching Tests (5):**
- [ ] Cache stores results
- [ ] Cache returns stored results on second call
- [ ] Cache invalidates on save
- [ ] use_cache=False bypasses cache
- [ ] Cache key includes order_id

### Integration Tests (Minimum 5)
- [ ] Create order → Calculate → Results match manual calculation
- [ ] Update order → Cache invalidates → New calculation correct
- [ ] Multiple blocks with shared components → Aggregation correct
- [ ] Complex order (10+ blocks) → All calculations correct
- [ ] Order with fixture data → Calculations match expected values

---

## Deliverables

- [ ] Working BuildOrder model with all methods
- [ ] Database migrations created and applied
- [ ] Admin interface configured
- [ ] Automated test suite (50+ tests, all passing)
- [ ] Property-based tests implemented
- [ ] Test coverage ≥90% for buildorders app
- [ ] Calculation algorithm documentation
- [ ] Deployment guide completed
- [ ] Code comments and docstrings
- [ ] CHANGELOG.md updated

---

## Documentation Updates

- [ ] Create `docs/design/calculation_algorithms.md`
- [ ] Document each calculation method with examples
- [ ] Add docstrings to all model methods
- [ ] Create ENH-0000009 deployment guide
- [ ] Update CHANGELOG.md
- [ ] Add inline code comments for complex logic

---

## Risks and Considerations

**Risk 1: Calculation Performance**
- **Impact:** Medium
- **Likelihood:** Low (with caching)
- **Mitigation:**
  - Implement caching (5 minute TTL)
  - Use select_related/prefetch_related
  - Test with 100+ blocks
  - Monitor query count

**Risk 2: Circular Dependencies**
- **Impact:** Low (not possible with current data model)
- **Likelihood:** Very Low
- **Mitigation:**
  - Current model doesn't allow circular references
  - Blocks → Components → Ores is one-way

**Risk 3: Floating Point Precision**
- **Impact:** Low
- **Likelihood:** Low
- **Mitigation:**
  - Use Decimal for currency if needed later
  - Document precision limits
  - Test edge cases

**Risk 4: Cache Invalidation**
- **Impact:** Low
- **Likelihood:** Low
- **Mitigation:**
  - Invalidate on save
  - Short TTL (5 minutes)
  - use_cache parameter for testing

---

## Alternatives Considered

### Alternative 1: Separate Calculation Service
**Rejected:** Over-engineering. Model methods are simpler and more Django-idiomatic.

### Alternative 2: Celery for All Calculations
**Rejected:** Premature optimization. Add async only if performance issues arise.

### Alternative 3: List Format for Blocks JSONField
**Rejected:** Dict format is more efficient for lookups and consistent with Phase 1.

### Alternative 4: Separate BuildOrderBlock Model
**Rejected:** Adds complexity. JSONField is sufficient and matches Phase 1 pattern.

---

## Related Issues/Enhancements

- **Depends On:** ENH-0000001 (Ores Model) - ✅ Completed
- **Depends On:** ENH-0000002 (Components Model) - ✅ Completed
- **Depends On:** ENH-0000003 (Blocks Model) - ✅ Completed
- **Enables:** ENH-0000010 (Build Order Views)
- **Enables:** ENH-0000011 (Dynamic Block Selector)
- **Enables:** Phase 3 Build Order Calculator

---

## Notes

- Follow UUIDv7 pattern from Phase 1
- Use dict format for blocks JSONField (consistent with Component.materials and Block.components)
- Implement calculations as model methods (not separate utilities)
- Cache results for performance
- Write property-based tests for calculation properties
- Document calculation algorithms thoroughly
- Test with fixture data (15 blocks available)
- Consider adding helper methods for common queries
- Admin interface should display calculation summary

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Planned | Initial creation for Phase 3 |

---

## Sign-off

**Reviewed By:** (pending)  
**Approved By:** (pending)  
**Completed By:** (pending)  
**Completion Date:** (pending)
