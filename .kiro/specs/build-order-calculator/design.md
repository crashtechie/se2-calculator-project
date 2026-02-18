# Design Document: Build Order Calculator

## Overview

The Build Order Calculator feature provides a complete web interface for managing BuildOrder objects in the SE2 Calculator application. This design leverages the existing BuildOrder model (completed in ENH-0000009) and follows the established patterns from Phase 2 (ores, components, blocks apps).

### Key Design Principles

1. **Consistency**: Follow the exact patterns established in blocks app (ENH-0000007)
2. **Reusability**: Leverage existing calculation methods in BuildOrder model
3. **Performance**: Utilize caching and query optimization
4. **User Experience**: Provide intuitive, responsive interface with real-time feedback
5. **Maintainability**: Use Django best practices and comprehensive testing

### Architecture Overview

The feature consists of three main layers:

1. **View Layer**: Django class-based views (ListView, DetailView, CreateView, UpdateView, DeleteView)
2. **Form Layer**: BuildOrderForm handling JSONField blocks with dynamic JavaScript selector
3. **Template Layer**: Bootstrap 5 responsive templates with JavaScript for dynamic interactions

### Dependencies

- BuildOrder model (already implemented)
- Block, Component, Ore models (Phase 1)
- Django 6.0.1 class-based views
- Bootstrap 5 for styling
- JavaScript (vanilla or minimal jQuery) for dynamic selector
- Django cache framework for calculation results

## Architecture

### URL Structure

Following RESTful conventions and Django best practices:

```
/buildorders/                    → BuildOrderListView
/buildorders/create/             → BuildOrderCreateView
/buildorders/<uuid:pk>/          → BuildOrderDetailView
/buildorders/<uuid:pk>/update/   → BuildOrderUpdateView
/buildorders/<uuid:pk>/delete/   → BuildOrderDeleteView
```

### View Architecture

All views inherit from Django's generic class-based views:


```python
BuildOrderListView(ListView)
  - Paginate by 10 items
  - Search by name/description
  - Sort by name, created_at, updated_at
  - Filter queryset based on query parameters

BuildOrderDetailView(DetailView)
  - Display BuildOrder with all fields
  - Show calculation summary (cached)
  - Display blocks with quantities
  - Show component breakdown
  - Show ore breakdown
  - Display fabrication times

BuildOrderCreateView(CreateView)
  - Use BuildOrderForm
  - Provide block selection interface
  - Validate form data
  - Redirect to detail view on success

BuildOrderUpdateView(UpdateView)
  - Pre-populate form with existing data
  - Pre-populate blocks in JavaScript
  - Invalidate cache on save
  - Redirect to detail view on success

BuildOrderDeleteView(DeleteView)
  - Show confirmation page
  - Display BuildOrder details
  - Redirect to list view on success
```

### Data Flow

1. **List View**: Query BuildOrders → Apply filters/sorting → Paginate → Render
2. **Detail View**: Get BuildOrder → Check cache → Calculate if needed → Render
3. **Create View**: Display form → Validate input → Save BuildOrder → Redirect
4. **Update View**: Get BuildOrder → Pre-populate form → Validate → Save → Invalidate cache → Redirect
5. **Delete View**: Get BuildOrder → Confirm → Delete → Redirect

### Caching Strategy


The BuildOrder model already implements caching via `get_cached_calculation_summary()`:

- **Cache Key**: `buildorder_calc_{order_id}`
- **TTL**: 5 minutes (300 seconds)
- **Invalidation**: Automatic on BuildOrder.save()
- **Usage**: Detail view uses cached calculations

## Components and Interfaces

### BuildOrderForm

Handles the complex JSONField blocks data structure, converting between form representation and database storage.

**Form Fields:**
- `name`: CharField (required, max 200 characters)
- `description`: TextField (optional)
- `blocks_json`: HiddenInput (carries JSON payload from JavaScript)

**Validation Logic:**
1. Validate name is not empty and unique
2. Parse blocks_json from hidden field
3. Validate JSON structure is dict of {block_uuid: quantity}
4. Validate each block UUID exists in database
5. Validate each quantity is positive integer
6. Use BuildOrder.validate_blocks() helper method

**JavaScript Integration:**
- Form includes hidden field `blocks_json`
- JavaScript populates this field with selected blocks
- Format: `{"block_uuid": quantity, "block_uuid": quantity}`

### Dynamic Block Selector (JavaScript)

**Component Structure:**
```javascript
BlockSelector {
  availableBlocks: Array<Block>
  selectedBlocks: Map<UUID, {block: Block, quantity: number}>
  
  methods:
    - searchBlocks(query): Filter available blocks
    - addBlock(blockId): Add block to selection
    - removeBlock(blockId): Remove block from selection
    - updateQuantity(blockId, quantity): Update block quantity
    - getBlocksJSON(): Return JSON for form submission
    - validateQuantities(): Ensure all quantities > 0
}
```

**User Interface Elements:**
- Search/autocomplete input for block selection
- Selected blocks list with quantity inputs
- Remove buttons for each selected block
- Visual feedback for validation errors



### Live Preview Component (JavaScript)

**Component Structure:**
```javascript
LivePreview {
  currentBlocks: Map<UUID, quantity>
  
  methods:
    - calculateTotals(): Make AJAX request to get calculations
    - updateDisplay(summary): Update UI with calculation results
    - showLoading(): Display loading indicator
    - showError(message): Display error message
    - debounce(func, delay): Prevent excessive API calls
}
```

**AJAX Endpoint:**
- URL: `/buildorders/calculate/` (POST)
- Request: `{blocks: {uuid: quantity, ...}}`
- Response: `{total_mass, component_count, ore_count, fabricator_times}`

**Display Elements:**
- Total mass
- Total block count
- Unique component count
- Unique ore count
- Loading spinner during calculation

### Template Structure

Following the blocks app pattern:

```
buildorders/
├── buildorder_list.html          # List view with search/sort/pagination
├── buildorder_detail.html        # Detail view with calculations
├── buildorder_form.html          # Create/Update form with dynamic selector
└── buildorder_confirm_delete.html # Delete confirmation
```

**Template Inheritance:**
- All templates extend `base.html`
- Use Bootstrap 5 components (cards, tables, forms, buttons)
- Include CSRF tokens in all forms
- Use Django template tags for URLs ({% url 'buildorders:...' %})

## Data Models

The BuildOrder model is already implemented. This design uses it as-is:

**BuildOrder Model:**
```python
class BuildOrder(models.Model):
    order_id: UUIDField (primary key, UUIDv7)
    name: CharField(max_length=200)
    description: TextField(blank=True)
    blocks: JSONField (dict of {block_uuid: quantity})
    created_at: DateTimeField(auto_now_add=True)
    updated_at: DateTimeField(auto_now=True)
    
    methods:
        - validate_blocks(): Validate block UUIDs and quantities
        - get_block_objects(): Return list of (Block, quantity) tuples
        - calculate_total_mass(): Sum of block masses * quantities
        - calculate_required_components(): Aggregate components across blocks
        - calculate_required_ores(): Traverse to ores through components
        - calculate_fabricator_times(): Group by fabricator type
        - get_calculation_summary(): Complete summary dict
        - get_cached_calculation_summary(): Cached version with 5min TTL
```

**No database migrations needed** - BuildOrder model is complete.



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, I've identified the following consolidations to eliminate redundancy:

**Consolidations:**
- Form validation properties (8.1-8.8) can be consolidated into comprehensive validation properties
- Cache-related properties (2.7, 4.6, 11.1, 11.2) can be consolidated into cache behavior properties
- Display properties for detail view (2.1-2.6) can be consolidated into a comprehensive rendering property
- JavaScript interaction properties (3.4, 3.5, 6.3, 6.6, 15.2, 15.3, 15.4) can be consolidated
- Update properties (4.3, 4.4, 4.5) can be consolidated into comprehensive update behavior

### Core Properties

**Property 1: List View Pagination**
*For any* set of BuildOrders, when displayed in the list view, the results should be paginated with 10 items per page and navigation should allow access to all pages.
**Validates: Requirements 1.1**

**Property 2: Search Filtering**
*For any* search query and set of BuildOrders, the filtered results should contain only BuildOrders whose name or description contains the search query (case-insensitive).
**Validates: Requirements 1.2**

**Property 3: List Sorting**
*For any* sort field (name, created_at, updated_at) and sort order (asc, desc), the list view should return BuildOrders ordered correctly by that field and order.
**Validates: Requirements 1.3**

**Property 4: List Display Completeness**
*For any* BuildOrder in the list view, the rendered HTML should contain the BuildOrder's name, description, block count, and creation date.
**Validates: Requirements 1.5**

**Property 5: Detail View Calculation Display**
*For any* BuildOrder, the detail view should display all calculation results including total mass, all required components with quantities, all required ores with quantities, and fabrication times grouped by type.
**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**

**Property 6: Cache Behavior**
*For any* BuildOrder, when calculation results are requested multiple times within 5 minutes without updates, the second and subsequent requests should retrieve data from cache; when the BuildOrder is updated, the cache should be invalidated.
**Validates: Requirements 2.7, 4.6, 11.1, 11.2**


**Property 7: Form Validation Completeness**
*For any* form submission, if the name is empty, or blocks are empty, or any quantity is less than 1, or any quantity is non-integer, or any block UUID doesn't exist, then validation should fail and display appropriate error messages; if all validation passes, the BuildOrder should be saved successfully.
**Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.8, 12.1, 12.2**

**Property 8: Form State Preservation**
*For any* form submission that fails validation, the form should be re-rendered with all user input preserved and validation errors displayed next to the relevant fields.
**Validates: Requirements 8.6, 8.7**

**Property 9: Create Operation Success**
*For any* valid BuildOrder data (name, description, blocks with quantities), when submitted via the create form, a new BuildOrder should be created in the database and the user should be redirected to the detail view.
**Validates: Requirements 3.6, 3.8**

**Property 10: Update Operation Success**
*For any* existing BuildOrder and valid changes to name, description, or blocks, when submitted via the update form, the BuildOrder should be updated in the database with the new values and the user should be redirected to the detail view.
**Validates: Requirements 4.3, 4.4, 4.5, 4.8**

**Property 11: Update Form Pre-population**
*For any* existing BuildOrder, when the update form is loaded, all fields (name, description) and the Dynamic_Selector should be pre-populated with the current BuildOrder data.
**Validates: Requirements 4.1, 4.2**

**Property 12: Delete Operation Success**
*For any* BuildOrder, when deletion is confirmed, the BuildOrder should be removed from the database and the user should be redirected to the list view; when deletion is cancelled, the BuildOrder should remain in the database and the user should be redirected to the detail view.
**Validates: Requirements 5.3, 5.4, 5.5**

**Property 13: Dynamic Selector Block Addition**
*For any* block selection, when a user adds a block via the Dynamic_Selector, the block should appear in the selected blocks list with a quantity input defaulting to 1, and the same block should not be addable again.
**Validates: Requirements 3.4, 6.3, 6.4, 6.5**

**Property 14: Dynamic Selector Block Removal**
*For any* selected block, when a user clicks remove, the block should be removed from the selected blocks list and become available for selection again.
**Validates: Requirements 3.5, 6.6**

**Property 15: Dynamic Selector Search Filtering**
*For any* search query in the Dynamic_Selector, the available blocks should be filtered to show only blocks whose name contains the query (case-insensitive).
**Validates: Requirements 3.3, 6.2**

**Property 16: Dynamic Selector Quantity Validation**
*For any* quantity input in the Dynamic_Selector, only positive integers should be accepted; non-integers and values less than 1 should be rejected with validation feedback.
**Validates: Requirements 6.7**

**Property 17: Live Preview Updates**
*For any* change to selected blocks or quantities, the Live_Preview should update to display the current total mass, total block count, unique component count, and unique ore count via AJAX without page reload.
**Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.6**

**Property 18: Live Preview Error Handling**
*For any* calculation error during live preview, an error message should be displayed to the user.
**Validates: Requirements 7.8**

**Property 19: JavaScript Interaction Without Reload**
*For any* block addition, removal, or quantity change in the Dynamic_Selector, the operation should complete without triggering a page reload.
**Validates: Requirements 15.2, 15.3, 15.4**

**Property 20: AJAX Debouncing**
*For any* rapid sequence of changes to selected blocks or quantities, the Live_Preview should debounce AJAX requests to avoid excessive server calls (maximum one request per 500ms).
**Validates: Requirements 15.6**

**Property 21: Success Message Display**
*For any* successful create, update, or delete operation, a success message should be displayed to the user.
**Validates: Requirements 10.4**

**Property 22: Error Message Display**
*For any* failed operation, an error message should be displayed to the user.
**Validates: Requirements 10.5**

**Property 23: Query Optimization**
*For any* detail view request, the number of database queries should be minimized using select_related and prefetch_related to avoid N+1 query problems.
**Validates: Requirements 11.3, 11.4**

**Property 24: Performance Thresholds**
*For any* list view with up to 100 BuildOrders, the page should load in under 2 seconds; for any detail view with up to 50 blocks, the page should load in under 3 seconds.
**Validates: Requirements 11.5, 11.6**

**Property 25: Model Validation Integration**
*For any* BuildOrder save operation, the model's clean() method should be called to perform validation before saving to the database.
**Validates: Requirements 12.3**

**Property 26: Transaction Atomicity**
*For any* BuildOrder save operation, if any part of the save fails, the entire operation should be rolled back to maintain database consistency.
**Validates: Requirements 12.5**

**Property 27: Database Error Handling**
*For any* database error during an operation, the error should be caught and a user-friendly message should be displayed instead of exposing technical details.
**Validates: Requirements 12.6**

**Property 28: Template Inheritance**
*For any* BuildOrder view template, it should extend base.html to maintain consistent layout and styling across the application.
**Validates: Requirements 14.1**

**Property 29: Consistent Styling**
*For any* BuildOrder view, buttons should use consistent Bootstrap classes (btn-primary, btn-secondary, btn-danger), tables should use consistent table classes, and cards should use consistent card classes.
**Validates: Requirements 14.4, 14.5, 14.6**

**Property 30: Page Structure Consistency**
*For any* BuildOrder view, the page should include a title, heading, and consistent navigation elements.
**Validates: Requirements 14.7**

**Property 31: Progressive Enhancement**
*For any* form submission, the form should work correctly even when JavaScript is disabled, falling back to standard form submission.
**Validates: Requirements 15.7**

**Property 32: JavaScript Feedback**
*For any* JavaScript interaction (block add, remove, quantity change), clear visual feedback should be provided to the user.
**Validates: Requirements 15.8**

**Property 33: Test Coverage Threshold**
*For the* buildorders app, the test suite should achieve at least 85% code coverage.
**Validates: Requirements 16.1**

**Property 34: Test Completeness**
*For the* buildorders app, the test suite should include unit tests for all view classes, integration tests for the complete CRUD workflow, form validation tests for all error conditions, JavaScript functionality tests, cache invalidation tests, and pagination/search/sorting tests.
**Validates: Requirements 16.2, 16.3, 16.4, 16.5, 16.6, 16.7**



## Error Handling

### Form Validation Errors

**Client-Side (JavaScript):**
- Validate quantities are positive integers before form submission
- Validate at least one block is selected
- Display inline error messages next to invalid fields
- Prevent form submission if validation fails

**Server-Side (Django):**
- Validate name is not empty and unique
- Validate blocks_json is valid JSON
- Validate all block UUIDs exist in database
- Validate all quantities are positive integers
- Use BuildOrder.validate_blocks() for comprehensive validation
- Display field-specific errors using Django's form error system
- Preserve user input on validation failure

### Database Errors

**Connection Errors:**
- Catch database connection exceptions
- Display user-friendly message: "Unable to connect to database. Please try again."
- Log technical details for debugging

**Integrity Errors:**
- Catch unique constraint violations
- Display: "A build order with this name already exists."
- Catch foreign key violations
- Display: "One or more blocks no longer exist. Please refresh and try again."

**Transaction Errors:**
- Wrap save operations in transactions
- Rollback on any error
- Display: "An error occurred while saving. Please try again."

### AJAX Errors

**Network Errors:**
- Catch fetch/AJAX failures
- Display: "Unable to calculate totals. Please check your connection."
- Retry with exponential backoff (optional)

**Server Errors (500):**
- Display: "Calculation failed. Please try again later."
- Log error details for debugging

**Validation Errors (400):**
- Parse error response
- Display specific validation messages

### Cache Errors

**Cache Unavailable:**
- Gracefully degrade to direct calculation
- Log warning but don't fail request
- Continue normal operation without caching

### JavaScript Disabled

**Graceful Degradation:**
- Form submission works via standard POST
- No live preview, but form validation still works
- Display message: "Enable JavaScript for enhanced features"

