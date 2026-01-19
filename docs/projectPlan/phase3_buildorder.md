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
