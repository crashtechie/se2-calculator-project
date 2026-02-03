# Phase 3: Build Order Calculator

**Duration:** 2-3 days  
**Priority:** High  
**Dependencies:** Phase 1 & 2 complete

## Objectives
- Create build order model and views
- Implement multi-block selection interface
- Calculate total resources required
- Display component, fabricator, and ore breakdowns

## Tasks

### 3.1 Build Order Model
**File:** `blocks/models.py` (or new `buildorders` app)

Model: BuildOrder
- order_id (UUIDv7, primary key)
- name (CharField)
- blocks (JSONField) - Format: [{"block_id": "uuid", "quantity": int}]
- created_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)

- [ ] Define BuildOrder model
- [ ] Add calculation methods (total_mass, required_components, required_ores)
- [ ] Add __str__ method
- [ ] Create and run migrations

### 3.2 Calculation Logic
**File:** `blocks/utils.py` or `blocks/calculators.py`

Functions needed:
- calculate_total_mass(blocks_list)
- calculate_required_components(blocks_list)
- calculate_required_ores(components_list)
- calculate_fabricator_times(components_list)

- [ ] Implement mass calculation
- [ ] Implement component aggregation (sum quantities)
- [ ] Implement ore aggregation (traverse component materials)
- [ ] Implement fabricator time calculation
- [ ] Add error handling for missing data
- [ ] Write unit tests for calculations

### 3.3 Build Order Views
**File:** `blocks/views.py`

Views to implement:
- BuildOrderListView
- BuildOrderDetailView (with full breakdown)
- BuildOrderCreateView (block selection interface)
- BuildOrderUpdateView
- BuildOrderDeleteView

- [ ] Implement BuildOrderListView
- [ ] Implement BuildOrderDetailView with calculations
- [ ] Implement BuildOrderCreateView with multi-select
- [ ] Implement BuildOrderUpdateView
- [ ] Implement BuildOrderDeleteView

### 3.4 Block Selection Interface
**File:** `blocks/templates/blocks/buildorder_form.html`

Features:
- Search/filter blocks
- Add blocks with quantity input
- Display selected blocks in cart
- Remove blocks from selection
- Show live preview of totals

- [ ] Create block search/filter interface
- [ ] Add quantity input for each block
- [ ] Create "cart" display for selected blocks
- [ ] Add remove button for each selected block
- [ ] Implement live calculation preview (optional)

### 3.5 Build Order Detail Template
**File:** `blocks/templates/blocks/buildorder_detail.html`

Sections to display:
1. Build Order Info (name, created date)
2. Selected Blocks (with quantities and individual mass)
3. Total Mass
4. Required Components (aggregated with quantities)
5. Required Ores (aggregated with quantities)
6. Fabricator Breakdown (by fabricator type with total time)

- [ ] Display build order metadata
- [ ] Display blocks table with quantities
- [ ] Display total mass calculation
- [ ] Display components breakdown table
- [ ] Display ores breakdown table
- [ ] Display fabricator times by type
- [ ] Add export functionality (CSV/PDF - optional)

### 3.6 JavaScript for Dynamic Selection
**File:** `static/js/buildorder.js`

Features:
- Dynamic block addition/removal
- Quantity updates
- Client-side calculation preview
- Form validation

- [ ] Implement block search functionality
- [ ] Handle add/remove block actions
- [ ] Update quantities dynamically
- [ ] Calculate and display preview totals
- [ ] Validate form before submission

### 3.7 URL Configuration
**File:** `blocks/urls.py`

- [ ] Add buildorder list URL
- [ ] Add buildorder detail URL
- [ ] Add buildorder create URL
- [ ] Add buildorder update URL
- [ ] Add buildorder delete URL

### 3.8 API Endpoints (Optional)
**File:** `blocks/api.py` or use Django REST Framework

Endpoints:
- GET /api/blocks/ - List blocks for selection
- POST /api/buildorder/calculate/ - Calculate resources without saving

- [ ] Create block list API endpoint
- [ ] Create calculation API endpoint
- [ ] Add CSRF protection
- [ ] Return JSON responses

## Deliverables
- BuildOrder model with calculation methods
- Block selection interface
- Resource calculation engine
- Detailed breakdown display
- Full CRUD for build orders

## Testing Checklist
- [ ] Can create build order with multiple blocks
- [ ] Can update quantities in build order
- [ ] Total mass calculates correctly
- [ ] Component aggregation works (multiple blocks using same component)
- [ ] Ore aggregation works (traverse through components)
- [ ] Fabricator times calculate correctly
- [ ] Can view detailed breakdown
- [ ] Can update and delete build orders
- [ ] Edge cases handled (missing data, zero quantities)

## Calculation Example

**Input:**
- 2x Block A (requires 3x Component X, 2x Component Y)
- 1x Block B (requires 1x Component X, 4x Component Z)

**Expected Output:**
- Components:
  - Component X: 7 (2×3 + 1×1)
  - Component Y: 4 (2×2)
  - Component Z: 4 (1×4)
- Ores: (aggregate from all components)
- Fabricators: (group by fabricator type, sum times)

## URL Structure
```
/buildorders/                    - Build order list
/buildorders/<uuid>/             - Build order detail
/buildorders/create/             - Create build order
/buildorders/<uuid>/update/      - Update build order
/buildorders/<uuid>/delete/      - Delete build order
```

## Notes
- Consider caching calculation results for performance
- Add validation to prevent circular dependencies
- Consider adding "save as template" feature
- May want to add user authentication for saved orders
- Consider adding print-friendly view

---

## Recommendations from Phase 1 & 2 Completion

**Date Added:** February 1, 2026  
**Based on:** Phase 1 & 2 validation and lessons learned

### Architecture Recommendations

#### 1. Model Design Pattern
**Recommendation:** Follow the established UUIDv7 pattern from Phase 1

```python
# buildorders/models.py
from uuid_utils import uuid7

def generate_uuid():
    return str(uuid7())

class BuildOrder(models.Model):
    order_id = models.UUIDField(
        primary_key=True,
        default=generate_uuid,
        editable=False,
        help_text="UUIDv7 primary key"
    )
    # ... rest of fields
```

**Why:** Consistent with existing models, provides time-ordered UUIDs, avoids migration serialization issues.

#### 2. JSONField Structure
**Recommendation:** Use dict format for blocks (not list)

```python
# Recommended format
blocks = models.JSONField(
    default=dict,
    blank=True,
    help_text="JSON object mapping block IDs to quantities"
)
# Format: {"block_id_1": quantity, "block_id_2": quantity}
```

**Why:** 
- Consistent with Component.materials and Block.components patterns
- Easier to update quantities (direct key access)
- Simpler validation logic
- Better performance for lookups

**Alternative (if order matters):**
```python
# If you need to preserve block order
blocks = models.JSONField(
    default=list,
    blank=True,
    help_text="Ordered list of blocks"
)
# Format: [{"block_id": "uuid", "quantity": int, "order": int}]
```

#### 3. Validation Methods
**Recommendation:** Add validation methods like existing models

```python
class BuildOrder(models.Model):
    # ... fields ...
    
    def validate_blocks(self):
        """Validate that all block_ids reference valid Blocks."""
        if not self.blocks:
            return True, []
        
        errors = []
        for block_id, quantity in self.blocks.items():
            if not isinstance(quantity, (int, float)) or quantity <= 0:
                errors.append(f"Invalid quantity for block {block_id}")
                continue
            
            try:
                Block.objects.get(block_id=block_id)
            except Block.DoesNotExist:
                errors.append(f"Block with ID {block_id} does not exist")
        
        return len(errors) == 0, errors
    
    def get_block_objects(self):
        """Get all Block objects referenced in this order."""
        if not self.blocks:
            return Block.objects.none()
        
        block_ids = list(self.blocks.keys())
        return Block.objects.filter(block_id__in=block_ids)
    
    def clean(self):
        """Validate model before saving."""
        from django.core.exceptions import ValidationError
        
        is_valid, errors = self.validate_blocks()
        if not is_valid:
            raise ValidationError(f"Blocks validation failed: {', '.join(errors)}")
    
    def save(self, *args, **kwargs):
        """Override save to validate before saving."""
        self.clean()
        super().save(*args, **kwargs)
```

**Why:** Consistent with Component and Block models, prevents invalid data.

### Calculation Logic Recommendations

#### 4. Calculation Methods Location
**Recommendation:** Add calculation methods directly to BuildOrder model

```python
class BuildOrder(models.Model):
    # ... fields and validation ...
    
    def calculate_total_mass(self):
        """Calculate total mass of all blocks in this order."""
        total = 0.0
        for block in self.get_block_objects():
            quantity = self.blocks.get(str(block.block_id), 0)
            total += block.mass * quantity
        return total
    
    def calculate_required_components(self):
        """
        Aggregate all components required across all blocks.
        Returns: dict mapping component_id -> total_quantity
        """
        component_totals = {}
        
        for block in self.get_block_objects():
            block_quantity = self.blocks.get(str(block.block_id), 0)
            
            # Aggregate components from this block
            for comp_id, comp_qty in (block.components or {}).items():
                total_needed = comp_qty * block_quantity
                component_totals[comp_id] = component_totals.get(comp_id, 0) + total_needed
        
        return component_totals
    
    def calculate_required_ores(self):
        """
        Aggregate all ores required by traversing components.
        Returns: dict mapping ore_id -> total_quantity
        """
        ore_totals = {}
        component_totals = self.calculate_required_components()
        
        # Get all required components
        component_ids = list(component_totals.keys())
        components = Component.objects.filter(component_id__in=component_ids)
        
        for component in components:
            comp_quantity = component_totals.get(str(component.component_id), 0)
            
            # Aggregate ores from this component
            for ore_id, ore_qty in (component.materials or {}).items():
                total_needed = ore_qty * comp_quantity
                ore_totals[ore_id] = ore_totals.get(ore_id, 0) + total_needed
        
        return ore_totals
    
    def calculate_fabricator_times(self):
        """
        Calculate total fabrication time grouped by fabricator type.
        Returns: dict mapping fabricator_type -> total_seconds
        """
        fabricator_times = {}
        component_totals = self.calculate_required_components()
        
        component_ids = list(component_totals.keys())
        components = Component.objects.filter(component_id__in=component_ids)
        
        for component in components:
            comp_quantity = component_totals.get(str(component.component_id), 0)
            
            if component.fabricator_type:
                total_time = component.crafting_time * comp_quantity
                fabricator_times[component.fabricator_type] = \
                    fabricator_times.get(component.fabricator_type, 0) + total_time
        
        return fabricator_times
    
    def get_calculation_summary(self):
        """
        Get complete calculation summary for display.
        Returns: dict with all calculations and resolved objects
        """
        return {
            'total_mass': self.calculate_total_mass(),
            'components': self._get_components_with_details(),
            'ores': self._get_ores_with_details(),
            'fabricators': self.calculate_fabricator_times(),
        }
    
    def _get_components_with_details(self):
        """Helper to get components with names and details."""
        component_totals = self.calculate_required_components()
        component_ids = list(component_totals.keys())
        components = Component.objects.filter(component_id__in=component_ids)
        
        return [
            {
                'component': comp,
                'quantity': component_totals.get(str(comp.component_id), 0),
                'total_mass': comp.mass * component_totals.get(str(comp.component_id), 0),
                'total_time': comp.crafting_time * component_totals.get(str(comp.component_id), 0),
            }
            for comp in components
        ]
    
    def _get_ores_with_details(self):
        """Helper to get ores with names and details."""
        ore_totals = self.calculate_required_ores()
        ore_ids = list(ore_totals.keys())
        ores = Ore.objects.filter(ore_id__in=ore_ids)
        
        return [
            {
                'ore': ore,
                'quantity': ore_totals.get(str(ore.ore_id), 0),
                'total_mass': ore.mass * ore_totals.get(str(ore.ore_id), 0),
            }
            for ore in ores
        ]
```

**Why:** 
- Encapsulates business logic with the model
- Easier to test
- Reusable across views and APIs
- Consistent with Django best practices

#### 5. Performance Optimization
**Recommendation:** Use select_related and prefetch_related

```python
# In views
def get_queryset(self):
    return BuildOrder.objects.all().order_by('-created_at')

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Prefetch related objects to avoid N+1 queries
    blocks = self.object.get_block_objects().prefetch_related(
        Prefetch('get_component_objects', 
                 queryset=Component.objects.prefetch_related('get_material_ores'))
    )
    
    context['calculation_summary'] = self.object.get_calculation_summary()
    return context
```

**Why:** Prevents N+1 query problems when displaying resource chains.

### View & Template Recommendations

#### 6. Follow Established View Patterns
**Recommendation:** Use the same view structure as Phase 2

```python
# buildorders/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

class BuildOrderListView(ListView):
    model = BuildOrder
    template_name = 'buildorders/buildorder_list.html'
    context_object_name = 'buildorders'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset.order_by('-created_at')

class BuildOrderDetailView(DetailView):
    model = BuildOrder
    template_name = 'buildorders/buildorder_detail.html'
    context_object_name = 'buildorder'
    pk_url_kwarg = 'order_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calculation_summary'] = self.object.get_calculation_summary()
        context['blocks_with_details'] = self._get_blocks_with_details()
        return context
    
    def _get_blocks_with_details(self):
        """Get blocks with quantities and calculated values."""
        blocks = self.object.get_block_objects()
        return [
            {
                'block': block,
                'quantity': self.object.blocks.get(str(block.block_id), 0),
                'total_mass': block.mass * self.object.blocks.get(str(block.block_id), 0),
            }
            for block in blocks
        ]

class BuildOrderCreateView(SuccessMessageMixin, CreateView):
    model = BuildOrder
    template_name = 'buildorders/buildorder_form.html'
    fields = ['name', 'blocks']
    success_message = "Build order '%(name)s' created successfully!"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_blocks'] = Block.objects.all().order_by('name')
        return context
    
    def get_success_url(self):
        return reverse_lazy('buildorders:detail', kwargs={'order_id': self.object.order_id})
```

**Why:** Consistent with existing codebase, proven patterns from Phase 2.

#### 7. JavaScript Pattern
**Recommendation:** Follow the component-selector.js pattern

```javascript
// static/js/buildorder-selector.js
class BuildOrderSelector {
    constructor() {
        this.selectedBlocks = {};
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadExistingBlocks();
    }
    
    setupEventListeners() {
        // Block search
        document.getElementById('block-search')?.addEventListener('input', (e) => {
            this.filterBlocks(e.target.value);
        });
        
        // Add block buttons
        document.querySelectorAll('.add-block-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const blockId = e.target.dataset.blockId;
                this.addBlock(blockId);
            });
        });
    }
    
    addBlock(blockId) {
        if (!this.selectedBlocks[blockId]) {
            this.selectedBlocks[blockId] = 1;
        } else {
            this.selectedBlocks[blockId]++;
        }
        this.updateDisplay();
        this.updateHiddenField();
    }
    
    removeBlock(blockId) {
        delete this.selectedBlocks[blockId];
        this.updateDisplay();
        this.updateHiddenField();
    }
    
    updateQuantity(blockId, quantity) {
        if (quantity > 0) {
            this.selectedBlocks[blockId] = parseInt(quantity);
        } else {
            delete this.selectedBlocks[blockId];
        }
        this.updateDisplay();
        this.updateHiddenField();
    }
    
    updateHiddenField() {
        const hiddenField = document.getElementById('id_blocks');
        if (hiddenField) {
            hiddenField.value = JSON.stringify(this.selectedBlocks);
        }
    }
    
    updateDisplay() {
        // Update the selected blocks display
        const container = document.getElementById('selected-blocks-container');
        // ... render selected blocks with quantities
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    new BuildOrderSelector();
});
```

**Why:** Proven pattern from blocks/components forms, familiar to developers.

### Testing Recommendations

#### 8. Comprehensive Test Coverage
**Recommendation:** Aim for same coverage as Phase 2 (87%+)

```python
# buildorders/tests.py
from django.test import TestCase
from decimal import Decimal

class BuildOrderCalculationTests(TestCase):
    """Test calculation accuracy."""
    
    def setUp(self):
        # Create test data
        self.ore1 = Ore.objects.create(name="Iron", mass=1.0)
        self.ore2 = Ore.objects.create(name="Silicon", mass=0.5)
        
        self.comp1 = Component.objects.create(
            name="Steel Plate",
            mass=5.0,
            materials={str(self.ore1.ore_id): 3},
            fabricator_type="Basic Assembler",
            crafting_time=10.0
        )
        
        self.block1 = Block.objects.create(
            name="Armor Block",
            mass=50.0,
            health=100,
            pcu=1,
            snap_size=1.0,
            components={str(self.comp1.component_id): 5}
        )
        
        self.buildorder = BuildOrder.objects.create(
            name="Test Order",
            blocks={str(self.block1.block_id): 2}
        )
    
    def test_calculate_total_mass(self):
        """Test total mass calculation."""
        expected = 50.0 * 2  # 2 blocks at 50kg each
        self.assertEqual(self.buildorder.calculate_total_mass(), expected)
    
    def test_calculate_required_components(self):
        """Test component aggregation."""
        components = self.buildorder.calculate_required_components()
        expected_qty = 5 * 2  # 5 components per block, 2 blocks
        self.assertEqual(components[str(self.comp1.component_id)], expected_qty)
    
    def test_calculate_required_ores(self):
        """Test ore aggregation through components."""
        ores = self.buildorder.calculate_required_ores()
        # 2 blocks × 5 components × 3 ores = 30 ores
        expected_qty = 2 * 5 * 3
        self.assertEqual(ores[str(self.ore1.ore_id)], expected_qty)
    
    def test_calculate_fabricator_times(self):
        """Test fabricator time calculation."""
        times = self.buildorder.calculate_fabricator_times()
        # 2 blocks × 5 components × 10 seconds = 100 seconds
        expected_time = 2 * 5 * 10.0
        self.assertEqual(times["Basic Assembler"], expected_time)
    
    def test_multiple_blocks_same_component(self):
        """Test aggregation when multiple blocks use same component."""
        # Create second block using same component
        block2 = Block.objects.create(
            name="Another Block",
            mass=30.0,
            health=50,
            pcu=1,
            snap_size=1.0,
            components={str(self.comp1.component_id): 3}
        )
        
        self.buildorder.blocks[str(block2.block_id)] = 1
        self.buildorder.save()
        
        components = self.buildorder.calculate_required_components()
        # Block1: 2 × 5 = 10, Block2: 1 × 3 = 3, Total: 13
        expected_qty = (2 * 5) + (1 * 3)
        self.assertEqual(components[str(self.comp1.component_id)], expected_qty)

class BuildOrderViewTests(TestCase):
    """Test view functionality."""
    
    def test_create_view_renders(self):
        """Test create view renders with block list."""
        response = self.client.get(reverse('buildorders:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('all_blocks', response.context)
    
    def test_detail_view_shows_calculations(self):
        """Test detail view includes calculation summary."""
        # ... test implementation
```

**Why:** Calculations are critical - need comprehensive testing to ensure accuracy.

#### 9. Property-Based Testing for Calculations
**Recommendation:** Consider using Hypothesis for calculation testing

```python
from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase

class BuildOrderPropertyTests(HypothesisTestCase):
    """Property-based tests for calculations."""
    
    @given(
        block_quantity=st.integers(min_value=1, max_value=100),
        component_quantity=st.integers(min_value=1, max_value=50),
        ore_quantity=st.floats(min_value=0.1, max_value=100.0)
    )
    def test_ore_calculation_scales_linearly(self, block_quantity, component_quantity, ore_quantity):
        """Test that ore requirements scale linearly with block quantity."""
        # Property: doubling blocks should double ore requirements
        # ... implementation
```

**Why:** Catches edge cases and ensures calculation properties hold across all inputs.

### Admin Interface Recommendations

#### 10. Admin Configuration
**Recommendation:** Follow the same admin pattern as Phase 1

```python
# buildorders/admin.py
from django.contrib import admin
from django.utils.html import mark_safe
import json

@admin.register(BuildOrder)
class BuildOrderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'blocks_count',
        'total_mass_display',
        'created_at',
        'updated_at'
    )
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = (
        'order_id',
        'created_at',
        'updated_at',
        'blocks_formatted',
        'calculation_summary_display',
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name',)
        }),
        ('Blocks', {
            'fields': ('blocks', 'blocks_formatted'),
            'description': 'Define blocks as JSON: {"block_id": quantity, ...}'
        }),
        ('Calculations', {
            'fields': ('calculation_summary_display',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('order_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def blocks_count(self, obj):
        """Display number of unique blocks."""
        return len(obj.blocks) if obj.blocks else 0
    blocks_count.short_description = 'Blocks'
    
    def total_mass_display(self, obj):
        """Display calculated total mass."""
        try:
            mass = obj.calculate_total_mass()
            return f"{mass:.2f} kg"
        except Exception as e:
            return mark_safe(f'<span style="color: red;">Error: {e}</span>')
    total_mass_display.short_description = 'Total Mass'
    
    def blocks_formatted(self, obj):
        """Display blocks as formatted JSON."""
        if not obj.blocks:
            return mark_safe('<em>No blocks</em>')
        
        formatted = json.dumps(obj.blocks, indent=2)
        return mark_safe(
            f'<pre style="background-color: #f5f5f5; padding: 10px; '
            f'border-radius: 5px; overflow-x: auto;">{formatted}</pre>'
        )
    blocks_formatted.short_description = 'Blocks (Formatted)'
    
    def calculation_summary_display(self, obj):
        """Display full calculation summary."""
        try:
            summary = obj.get_calculation_summary()
            
            html = f"<strong>Total Mass:</strong> {summary['total_mass']:.2f} kg<br><br>"
            
            html += "<strong>Components:</strong><br>"
            for item in summary['components']:
                html += f"• {item['component'].name}: {item['quantity']} units<br>"
            
            html += "<br><strong>Ores:</strong><br>"
            for item in summary['ores']:
                html += f"• {item['ore'].name}: {item['quantity']:.2f} units<br>"
            
            html += "<br><strong>Fabricator Times:</strong><br>"
            for fab_type, time in summary['fabricators'].items():
                html += f"• {fab_type}: {time:.2f} seconds<br>"
            
            return mark_safe(html)
        except Exception as e:
            return mark_safe(f'<span style="color: red;">Error: {e}</span>')
    calculation_summary_display.short_description = 'Calculation Summary'
```

**Why:** Consistent admin experience, helpful for debugging calculations.

### Documentation Recommendations

#### 11. Document Calculation Algorithms
**Recommendation:** Create detailed calculation documentation

Create `docs/design/calculation_algorithms.md`:
```markdown
# Build Order Calculation Algorithms

## Overview
This document describes the algorithms used to calculate resource requirements
for build orders in the SE2 Calculator.

## Algorithm 1: Component Aggregation
**Purpose:** Calculate total components needed across all blocks

**Input:** BuildOrder with blocks dict
**Output:** Dict mapping component_id -> total_quantity

**Steps:**
1. For each block in the order:
   a. Get block quantity from order
   b. For each component in block:
      - Multiply component quantity by block quantity
      - Add to running total for that component
2. Return aggregated component totals

**Time Complexity:** O(B × C) where B = blocks, C = avg components per block
**Space Complexity:** O(U) where U = unique components

## Algorithm 2: Ore Aggregation
... (continue with other algorithms)
```

**Why:** Complex calculations need clear documentation for maintenance.

### CI/CD Recommendations

#### 12. Add Phase 3 to CI Pipeline
**Recommendation:** Extend test automation to include build order tests

```yaml
# .github/workflows/test.yml (if implementing CI)
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install --system -e .
      - name: Run tests
        run: uv run pytest --cov --cov-report=xml
      - name: Check coverage threshold
        run: |
          coverage report --fail-under=85
      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

**Why:** Prevent regressions in calculation logic, maintain quality standards.

### Migration Strategy

#### 13. Incremental Development Approach
**Recommendation:** Build Phase 3 in stages

**Stage 1: Model & Basic CRUD (Day 1)**
- Create BuildOrder model
- Add basic validation
- Implement simple CRUD views
- Basic templates (no calculations yet)
- Write model tests

**Stage 2: Calculation Logic (Day 2)**
- Implement calculation methods
- Add calculation tests
- Update detail view to show calculations
- Add calculation summary to templates

**Stage 3: Advanced UI (Day 3)**
- Implement dynamic block selector
- Add JavaScript for live updates
- Polish templates
- Add export functionality (optional)
- Integration testing

**Why:** Reduces risk, allows for testing at each stage, easier to debug.

### Performance Considerations

#### 14. Caching Strategy
**Recommendation:** Cache calculation results

```python
from django.core.cache import cache

class BuildOrder(models.Model):
    # ... fields ...
    
    def get_calculation_summary(self, use_cache=True):
        """Get calculation summary with optional caching."""
        cache_key = f'buildorder_calc_{self.order_id}'
        
        if use_cache:
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        summary = {
            'total_mass': self.calculate_total_mass(),
            'components': self._get_components_with_details(),
            'ores': self._get_ores_with_details(),
            'fabricators': self.calculate_fabricator_times(),
        }
        
        if use_cache:
            cache.set(cache_key, summary, timeout=300)  # 5 minutes
        
        return summary
    
    def save(self, *args, **kwargs):
        """Clear cache on save."""
        super().save(*args, **kwargs)
        cache_key = f'buildorder_calc_{self.order_id}'
        cache.delete(cache_key)
```

**Why:** Calculations can be expensive with many blocks/components/ores.

### Summary of Key Recommendations

1. ✅ Use dict format for blocks JSONField (consistent with Phase 1)
2. ✅ Add validation methods to BuildOrder model
3. ✅ Implement calculations as model methods
4. ✅ Follow Phase 2 view patterns (ListView, DetailView, etc.)
5. ✅ Use JavaScript pattern from component-selector.js
6. ✅ Aim for 85%+ test coverage
7. ✅ Add property-based tests for calculations
8. ✅ Configure admin interface like Phase 1
9. ✅ Document calculation algorithms
10. ✅ Build incrementally in 3 stages
11. ✅ Implement caching for performance
12. ✅ Use prefetch_related to avoid N+1 queries

---

## Additional Improvements for Phase 3

### User Experience Enhancements

#### 15. Live Calculation Preview
**Recommendation:** Add real-time calculation preview in create/update forms

```javascript
// static/js/buildorder-calculator.js
class BuildOrderCalculator {
    constructor() {
        this.blocks = {};
        this.previewContainer = document.getElementById('calculation-preview');
        this.init();
    }
    
    async updatePreview() {
        if (Object.keys(this.blocks).length === 0) {
            this.showEmptyState();
            return;
        }
        
        try {
            // Fetch calculation from API endpoint
            const response = await fetch('/api/buildorder/calculate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ blocks: this.blocks })
            });
            
            const data = await response.json();
            this.renderPreview(data);
        } catch (error) {
            console.error('Preview calculation failed:', error);
            this.showError();
        }
    }
    
    renderPreview(data) {
        const html = `
            <div class="card border-info">
                <div class="card-header bg-info text-white">
                    <h6 class="mb-0">
                        <i class="bi bi-calculator"></i> Live Preview
                    </h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3">
                            <div class="text-center">
                                <h4>${data.total_mass.toFixed(2)}</h4>
                                <small class="text-muted">Total Mass (kg)</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center">
                                <h4>${data.component_count}</h4>
                                <small class="text-muted">Components</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center">
                                <h4>${data.ore_count}</h4>
                                <small class="text-muted">Ore Types</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center">
                                <h4>${this.formatTime(data.total_fabrication_time)}</h4>
                                <small class="text-muted">Fabrication Time</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        this.previewContainer.innerHTML = html;
    }
    
    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else if (minutes > 0) {
            return `${minutes}m ${secs}s`;
        } else {
            return `${secs}s`;
        }
    }
}
```

**Why:** Immediate feedback improves UX, helps users understand resource requirements before saving.

#### 16. Block Search with Autocomplete
**Recommendation:** Add autocomplete/typeahead for block search

```javascript
// Use a library like typeahead.js or implement custom autocomplete
class BlockAutocomplete {
    constructor(inputElement, resultsElement) {
        this.input = inputElement;
        this.results = resultsElement;
        this.blocks = [];
        this.selectedIndex = -1;
        
        this.init();
    }
    
    async init() {
        // Fetch all blocks once
        this.blocks = await this.fetchBlocks();
        
        // Set up event listeners
        this.input.addEventListener('input', this.handleInput.bind(this));
        this.input.addEventListener('keydown', this.handleKeydown.bind(this));
        document.addEventListener('click', this.handleClickOutside.bind(this));
    }
    
    async fetchBlocks() {
        const response = await fetch('/api/blocks/');
        return await response.json();
    }
    
    handleInput(e) {
        const query = e.target.value.toLowerCase().trim();
        
        if (query.length < 2) {
            this.hideResults();
            return;
        }
        
        const matches = this.blocks.filter(block => 
            block.name.toLowerCase().includes(query) ||
            (block.description && block.description.toLowerCase().includes(query))
        ).slice(0, 10); // Limit to 10 results
        
        this.showResults(matches);
    }
    
    showResults(matches) {
        if (matches.length === 0) {
            this.results.innerHTML = '<div class="p-2 text-muted">No blocks found</div>';
            this.results.classList.remove('d-none');
            return;
        }
        
        const html = matches.map((block, index) => `
            <div class="autocomplete-item p-2 ${index === this.selectedIndex ? 'active' : ''}" 
                 data-block-id="${block.block_id}"
                 data-index="${index}">
                <strong>${this.highlightMatch(block.name, this.input.value)}</strong>
                <br>
                <small class="text-muted">
                    Mass: ${block.mass} kg | PCU: ${block.pcu}
                </small>
            </div>
        `).join('');
        
        this.results.innerHTML = html;
        this.results.classList.remove('d-none');
        
        // Add click handlers
        this.results.querySelectorAll('.autocomplete-item').forEach(item => {
            item.addEventListener('click', () => this.selectBlock(item.dataset.blockId));
        });
    }
    
    highlightMatch(text, query) {
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
}
```

**Why:** Faster block selection, better UX for large block lists, reduces errors.

#### 17. Drag-and-Drop Block Ordering
**Recommendation:** Allow users to reorder blocks in build order

```javascript
// Use SortableJS or implement custom drag-and-drop
import Sortable from 'sortablejs';

class BlockOrderManager {
    constructor(containerElement) {
        this.container = containerElement;
        this.initSortable();
    }
    
    initSortable() {
        Sortable.create(this.container, {
            animation: 150,
            handle: '.drag-handle',
            ghostClass: 'sortable-ghost',
            onEnd: (evt) => {
                this.updateBlockOrder();
            }
        });
    }
    
    updateBlockOrder() {
        const blocks = [];
        this.container.querySelectorAll('.block-item').forEach((item, index) => {
            blocks.push({
                block_id: item.dataset.blockId,
                quantity: parseInt(item.querySelector('.quantity-input').value),
                order: index
            });
        });
        
        // Update hidden field or send to server
        this.saveBlockOrder(blocks);
    }
}
```

**Why:** Allows users to organize blocks logically (e.g., by build priority), improves planning workflow.

### Data Visualization Enhancements

#### 18. Resource Breakdown Charts
**Recommendation:** Add visual charts for resource distribution

```javascript
// Use Chart.js for visualization
class ResourceCharts {
    constructor(data) {
        this.data = data;
    }
    
    renderComponentPieChart(canvasId) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        const components = this.data.components;
        const labels = components.map(c => c.component.name);
        const quantities = components.map(c => c.quantity);
        
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: quantities,
                    backgroundColor: this.generateColors(components.length)
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Component Distribution'
                    },
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }
    
    renderFabricatorBarChart(canvasId) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        const fabricators = Object.entries(this.data.fabricators);
        const labels = fabricators.map(([type, _]) => type);
        const times = fabricators.map(([_, time]) => time / 60); // Convert to minutes
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Fabrication Time (minutes)',
                    data: times,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Time (minutes)'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Fabrication Time by Type'
                    }
                }
            }
        });
    }
}
```

**Template Integration:**
```django
{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const chartData = {{ calculation_summary|safe }};
    const charts = new ResourceCharts(chartData);
    
    charts.renderComponentPieChart('component-chart');
    charts.renderFabricatorBarChart('fabricator-chart');
});
</script>
{% endblock %}
```

**Why:** Visual representation helps users quickly understand resource distribution and bottlenecks.

#### 19. Export Functionality
**Recommendation:** Add export to CSV, PDF, and JSON

```python
# buildorders/views.py
from django.http import HttpResponse, JsonResponse
import csv
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class BuildOrderExportView(DetailView):
    """Export build order in various formats."""
    model = BuildOrder
    pk_url_kwarg = 'order_id'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        format_type = request.GET.get('format', 'csv')
        
        if format_type == 'csv':
            return self.export_csv()
        elif format_type == 'json':
            return self.export_json()
        elif format_type == 'pdf':
            return self.export_pdf()
        else:
            return HttpResponse('Invalid format', status=400)
    
    def export_csv(self):
        """Export as CSV file."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="buildorder_{self.object.order_id}.csv"'
        
        writer = csv.writer(response)
        
        # Header
        writer.writerow(['Build Order:', self.object.name])
        writer.writerow(['Created:', self.object.created_at])
        writer.writerow([])
        
        # Blocks
        writer.writerow(['Blocks'])
        writer.writerow(['Block Name', 'Quantity', 'Mass per Unit', 'Total Mass'])
        for block in self.object.get_block_objects():
            qty = self.object.blocks.get(str(block.block_id), 0)
            writer.writerow([block.name, qty, block.mass, block.mass * qty])
        
        writer.writerow([])
        
        # Components
        summary = self.object.get_calculation_summary()
        writer.writerow(['Required Components'])
        writer.writerow(['Component Name', 'Quantity', 'Mass per Unit', 'Total Mass', 'Crafting Time'])
        for comp_data in summary['components']:
            writer.writerow([
                comp_data['component'].name,
                comp_data['quantity'],
                comp_data['component'].mass,
                comp_data['total_mass'],
                comp_data['total_time']
            ])
        
        writer.writerow([])
        
        # Ores
        writer.writerow(['Required Ores'])
        writer.writerow(['Ore Name', 'Quantity', 'Mass per Unit', 'Total Mass'])
        for ore_data in summary['ores']:
            writer.writerow([
                ore_data['ore'].name,
                ore_data['quantity'],
                ore_data['ore'].mass,
                ore_data['total_mass']
            ])
        
        return response
    
    def export_json(self):
        """Export as JSON file."""
        summary = self.object.get_calculation_summary()
        
        data = {
            'build_order': {
                'id': str(self.object.order_id),
                'name': self.object.name,
                'created_at': self.object.created_at.isoformat(),
            },
            'blocks': [
                {
                    'id': str(block.block_id),
                    'name': block.name,
                    'quantity': self.object.blocks.get(str(block.block_id), 0),
                    'mass': float(block.mass)
                }
                for block in self.object.get_block_objects()
            ],
            'summary': {
                'total_mass': summary['total_mass'],
                'components': [
                    {
                        'name': c['component'].name,
                        'quantity': c['quantity'],
                        'total_mass': c['total_mass'],
                        'total_time': c['total_time']
                    }
                    for c in summary['components']
                ],
                'ores': [
                    {
                        'name': o['ore'].name,
                        'quantity': o['quantity'],
                        'total_mass': o['total_mass']
                    }
                    for o in summary['ores']
                ],
                'fabricators': summary['fabricators']
            }
        }
        
        response = JsonResponse(data, json_dumps_params={'indent': 2})
        response['Content-Disposition'] = f'attachment; filename="buildorder_{self.object.order_id}.json"'
        return response
    
    def export_pdf(self):
        """Export as PDF file."""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="buildorder_{self.object.order_id}.pdf"'
        
        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"Build Order: {self.object.name}", styles['Title'])
        elements.append(title)
        
        # Add tables for blocks, components, ores
        # ... (implementation details)
        
        doc.build(elements)
        return response
```

**URL Configuration:**
```python
# buildorders/urls.py
path('<uuid:order_id>/export/', BuildOrderExportView.as_view(), name='export'),
```

**Template Button:**
```django
<div class="btn-group">
    <button type="button" class="btn btn-secondary dropdown-toggle" data-bs-toggle="dropdown">
        <i class="bi bi-download"></i> Export
    </button>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="{% url 'buildorders:export' object.order_id %}?format=csv">
            <i class="bi bi-file-earmark-spreadsheet"></i> CSV
        </a></li>
        <li><a class="dropdown-item" href="{% url 'buildorders:export' object.order_id %}?format=json">
            <i class="bi bi-file-earmark-code"></i> JSON
        </a></li>
        <li><a class="dropdown-item" href="{% url 'buildorders:export' object.order_id %}?format=pdf">
            <i class="bi bi-file-earmark-pdf"></i> PDF
        </a></li>
    </ul>
</div>
```

**Why:** Users can share build orders, import into spreadsheets, or print for reference.

### Advanced Features

#### 20. Build Order Templates
**Recommendation:** Allow saving build orders as reusable templates

```python
# buildorders/models.py
class BuildOrderTemplate(models.Model):
    """Reusable build order template."""
    template_id = models.UUIDField(primary_key=True, default=generate_uuid, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    blocks = models.JSONField(default=dict)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def create_build_order(self, name=None):
        """Create a BuildOrder from this template."""
        return BuildOrder.objects.create(
            name=name or f"{self.name} (from template)",
            blocks=self.blocks.copy()
        )
```

**Views:**
```python
class BuildOrderFromTemplateView(CreateView):
    """Create build order from template."""
    model = BuildOrder
    template_name = 'buildorders/from_template.html'
    fields = ['name']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['templates'] = BuildOrderTemplate.objects.filter(
            Q(is_public=True) | Q(created_by=self.request.user)
        )
        return context
    
    def form_valid(self, form):
        template_id = self.request.POST.get('template_id')
        template = get_object_or_404(BuildOrderTemplate, template_id=template_id)
        
        self.object = template.create_build_order(name=form.cleaned_data['name'])
        messages.success(self.request, f'Build order created from template "{template.name}"')
        return redirect(self.get_success_url())
```

**Why:** Saves time for common builds, enables sharing of optimized build orders.

#### 21. Comparison View
**Recommendation:** Compare multiple build orders side-by-side

```python
class BuildOrderCompareView(TemplateView):
    """Compare multiple build orders."""
    template_name = 'buildorders/compare.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get order IDs from query params
        order_ids = self.request.GET.getlist('orders')
        orders = BuildOrder.objects.filter(order_id__in=order_ids)
        
        # Calculate summaries for each
        comparisons = []
        for order in orders:
            summary = order.get_calculation_summary()
            comparisons.append({
                'order': order,
                'summary': summary
            })
        
        context['comparisons'] = comparisons
        return context
```

**Template:**
```django
<table class="table table-bordered">
    <thead>
        <tr>
            <th>Metric</th>
            {% for comp in comparisons %}
            <th>{{ comp.order.name }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Total Mass</strong></td>
            {% for comp in comparisons %}
            <td>{{ comp.summary.total_mass|floatformat:2 }} kg</td>
            {% endfor %}
        </tr>
        <tr>
            <td><strong>Component Types</strong></td>
            {% for comp in comparisons %}
            <td>{{ comp.summary.components|length }}</td>
            {% endfor %}
        </tr>
        <!-- More comparison rows -->
    </tbody>
</table>
```

**Why:** Helps users choose between different build strategies, optimize resource usage.

#### 22. Batch Operations
**Recommendation:** Add bulk actions for build orders

```python
class BuildOrderBulkActionView(View):
    """Handle bulk actions on build orders."""
    
    def post(self, request):
        action = request.POST.get('action')
        order_ids = request.POST.getlist('order_ids')
        
        if action == 'delete':
            count = BuildOrder.objects.filter(order_id__in=order_ids).delete()[0]
            messages.success(request, f'Deleted {count} build orders')
        
        elif action == 'export_all':
            # Export multiple orders to single file
            return self.export_multiple(order_ids)
        
        elif action == 'duplicate':
            # Duplicate selected orders
            for order_id in order_ids:
                original = BuildOrder.objects.get(order_id=order_id)
                BuildOrder.objects.create(
                    name=f"{original.name} (Copy)",
                    blocks=original.blocks.copy()
                )
            messages.success(request, f'Duplicated {len(order_ids)} build orders')
        
        return redirect('buildorders:list')
```

**Why:** Improves efficiency when managing many build orders.

### Performance & Scalability

#### 23. Database Indexing
**Recommendation:** Add database indexes for common queries

```python
# buildorders/models.py
class BuildOrder(models.Model):
    # ... fields ...
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['created_at', 'name']),
        ]
```

**Why:** Improves query performance for list views and searches.

#### 24. Async Calculation for Large Orders
**Recommendation:** Use Celery for expensive calculations

```python
# buildorders/tasks.py
from celery import shared_task

@shared_task
def calculate_build_order_async(order_id):
    """Calculate build order resources asynchronously."""
    order = BuildOrder.objects.get(order_id=order_id)
    summary = order.get_calculation_summary(use_cache=False)
    
    # Cache the result
    cache_key = f'buildorder_calc_{order_id}'
    cache.set(cache_key, summary, timeout=3600)  # 1 hour
    
    return summary

# In views
class BuildOrderDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if calculation is in progress
        task_id = cache.get(f'buildorder_task_{self.object.order_id}')
        if task_id:
            context['calculation_pending'] = True
        else:
            # Try to get cached result
            summary = cache.get(f'buildorder_calc_{self.object.order_id}')
            if not summary:
                # Start async calculation
                task = calculate_build_order_async.delay(str(self.object.order_id))
                cache.set(f'buildorder_task_{self.object.order_id}', task.id, timeout=300)
                context['calculation_pending'] = True
            else:
                context['calculation_summary'] = summary
        
        return context
```

**Why:** Prevents timeouts for build orders with hundreds of blocks.

### Testing Enhancements

#### 25. Snapshot Testing for Calculations
**Recommendation:** Use snapshot testing to catch calculation regressions

```python
# buildorders/tests.py
import json
from pathlib import Path

class BuildOrderSnapshotTests(TestCase):
    """Snapshot tests for calculation results."""
    
    def setUp(self):
        self.snapshot_dir = Path(__file__).parent / 'snapshots'
        self.snapshot_dir.mkdir(exist_ok=True)
    
    def test_complex_build_order_snapshot(self):
        """Test that complex build order calculations match snapshot."""
        # Create complex test data
        order = self.create_complex_build_order()
        
        # Calculate
        summary = order.get_calculation_summary()
        
        # Serialize for comparison
        snapshot_data = {
            'total_mass': summary['total_mass'],
            'components': [
                {
                    'name': c['component'].name,
                    'quantity': c['quantity'],
                    'total_mass': c['total_mass']
                }
                for c in summary['components']
            ],
            'ores': [
                {
                    'name': o['ore'].name,
                    'quantity': o['quantity']
                }
                for o in summary['ores']
            ]
        }
        
        snapshot_file = self.snapshot_dir / 'complex_build_order.json'
        
        if snapshot_file.exists():
            # Compare with existing snapshot
            with open(snapshot_file) as f:
                expected = json.load(f)
            self.assertEqual(snapshot_data, expected)
        else:
            # Create new snapshot
            with open(snapshot_file, 'w') as f:
                json.dump(snapshot_data, f, indent=2)
            self.fail('Created new snapshot - review and commit')
```

**Why:** Catches unintended changes to calculation logic, provides regression protection.

### Summary of Additional Improvements

15. ✅ Live calculation preview with AJAX
16. ✅ Block search with autocomplete
17. ✅ Drag-and-drop block ordering
18. ✅ Resource breakdown charts (Chart.js)
19. ✅ Export to CSV, JSON, PDF
20. ✅ Build order templates
21. ✅ Comparison view for multiple orders
22. ✅ Batch operations (delete, duplicate, export)
23. ✅ Database indexing for performance
24. ✅ Async calculation for large orders (Celery)
25. ✅ Snapshot testing for calculations

### Priority Matrix

| Feature | Priority | Complexity | Impact | Implement In |
|---------|----------|------------|--------|--------------|
| Live Preview (#15) | High | Medium | High | Stage 3 |
| Export (#19) | High | Low | High | Stage 3 |
| Autocomplete (#16) | Medium | Medium | Medium | Stage 3 (optional) |
| Charts (#18) | Medium | Low | Medium | Stage 3 (optional) |
| Templates (#20) | Low | Medium | Medium | Post-Phase 3 |
| Comparison (#21) | Low | Medium | Low | Post-Phase 3 |
| Drag-Drop (#17) | Low | Medium | Low | Post-Phase 3 |
| Batch Ops (#22) | Low | Low | Low | Post-Phase 3 |
| Indexing (#23) | High | Low | High | Stage 1 |
| Async Calc (#24) | Low | High | Medium | Post-Phase 3 |
| Snapshots (#25) | Medium | Low | High | Stage 2 |

### Success Criteria

Phase 3 will be considered complete when:
- ✅ All calculation tests pass (unit + property-based)
- ✅ Test coverage ≥ 85%
- ✅ All CRUD operations functional
- ✅ Calculations accurate for complex scenarios
- ✅ UI responsive and intuitive
- ✅ Admin interface functional
- ✅ Documentation complete
- ✅ No performance issues with 100+ blocks
- ✅ Live preview working (if implemented)
- ✅ Export functionality working (if implemented)
- ✅ Database indexes in place
