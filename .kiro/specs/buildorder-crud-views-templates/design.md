# Design Document: BuildOrder CRUD Views and Templates

## Overview

This design document specifies the implementation of complete CRUD (Create, Read, Update, Delete) views and templates for the BuildOrder model in the EVE Online manufacturing calculator. The feature provides a user-facing web interface at `/buildorders/` URLs, enabling users to manage build orders with calculation summary displays.

### Purpose

The BuildOrder CRUD interface serves as the primary user interaction layer for manufacturing planning. Users can:
- Browse and search existing build orders
- View detailed calculation summaries (mass, components, ores, fabrication times)
- Create new build orders with block configurations
- Update existing build orders
- Delete build orders with confirmation

### Context

This feature builds directly on ENH-0000009 (BuildOrder Model), which provides:
- UUIDv7-based BuildOrder model with blocks JSONField
- Calculation methods: `calculate_total_mass()`, `calculate_required_components()`, `calculate_required_ores()`, `calculate_fabricator_times()`
- Helper methods: `_get_components_with_details()`, `_get_ores_with_details()`
- Caching: `get_cached_calculation_summary()` with 5-minute TTL
- Validation: `validate_blocks()` method
- Admin interface (already implemented)

The implementation follows established Phase 2 patterns from the blocks, components, and ores apps, ensuring consistency across the application.

### Key Design Decisions

1. **URL Parameter Naming**: Use `pk` (not `order_id`) for consistency with Phase 2 patterns
2. **Caching Strategy**: Leverage existing BuildOrder model caching for calculation summaries
3. **Form Handling**: Hide blocks_json field (JavaScript selector comes in ENH-0000011)
4. **Validation**: Reuse BuildOrder.validate_blocks() method
5. **Logging**: Comprehensive logging at debug, info, and warning levels
6. **URL Namespace**: Use `buildorders:` for all routes
7. **Template Framework**: Bootstrap 5 responsive design
8. **Messages**: Django messages framework for user feedback
9. **Pagination**: 25 items per page (consistent with Phase 2)
10. **Testing**: Property-based tests for calculations, pagination, search, sorting

## Architecture

### High-Level Architecture

The BuildOrder CRUD interface follows Django's MVT (Model-View-Template) architecture with a layered approach:

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Django URL Router                        │
│                  (buildorders/urls.py)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      View Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  ListView    │  │ DetailView   │  │ CreateView   │      │
│  │  (List/      │  │ (Display     │  │ (Form        │      │
│  │   Search/    │  │  Calcs)      │  │  Handling)   │      │
│  │   Sort)      │  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ UpdateView   │  │ DeleteView   │                        │
│  │ (Form        │  │ (Confirm)    │                        │
│  │  Handling)   │  │              │                        │
│  └──────────────┘  └──────────────┘                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Form Layer                              │
│                  (BuildOrderForm)                            │
│  - Field validation                                          │
│  - blocks_json processing                                    │
│  - Cross-field validation                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Model Layer                             │
│                  (BuildOrder Model)                          │
│  - Data persistence                                          │
│  - Calculation methods                                       │
│  - Validation logic                                          │
│  - Cache invalidation                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data/Cache Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │  Django      │  │  Related     │      │
│  │  Database    │  │  Cache       │  │  Models      │      │
│  │              │  │  (5min TTL)  │  │  (Block,     │      │
│  │              │  │              │  │   Component, │      │
│  │              │  │              │  │   Ore)       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

#### List View Flow
```
User Request → URL Router → BuildOrderListView
                              ↓
                         QuerySet Building
                         (filter, sort, paginate)
                              ↓
                         Database Query
                              ↓
                         Template Rendering
                         (buildorder_list.html)
                              ↓
                         HTTP Response
```

#### Detail View Flow
```
User Request → URL Router → BuildOrderDetailView
                              ↓
                         Get BuildOrder (404 if not found)
                              ↓
                         get_cached_calculation_summary()
                              ↓
                         Cache Hit? ──Yes→ Return Cached Data
                              │
                              No
                              ↓
                         Calculate Summary
                         (mass, components, ores, times)
                              ↓
                         Cache Result (5min TTL)
                              ↓
                         Template Rendering
                         (buildorder_detail.html)
                              ↓
                         HTTP Response
```

#### Create/Update Flow
```
User Request → URL Router → CreateView/UpdateView
                              ↓
                         GET: Display Form
                              ↓
                         POST: Validate Form
                              ↓
                         BuildOrderForm.clean()
                         - Parse blocks_json
                         - Validate structure
                         - Call validate_blocks()
                              ↓
                         Valid? ──No→ Display Errors
                              │
                              Yes
                              ↓
                         Save BuildOrder
                         (triggers cache invalidation)
                              ↓
                         Success Message
                              ↓
                         Redirect to Detail View
```

### Design Patterns

1. **Class-Based Views (CBV)**: Use Django's generic views for consistency and code reuse
2. **Template Inheritance**: Extend base.html for consistent layout
3. **Form Processing**: Separate form class for validation logic
4. **Caching**: Read-through cache pattern with TTL
5. **Logging**: Structured logging with context
6. **URL Namespacing**: Prevent naming conflicts
7. **Message Framework**: User feedback for all actions

## Components and Interfaces

### Views (buildorders/views.py)

#### BuildOrderListView
```python
class BuildOrderListView(ListView):
    """
    Display paginated list of build orders with search and sorting.
    
    Query Parameters:
    - q: Search query (searches name)
    - sort: Sort field (name, created_at, updated_at)
    - order: Sort order (asc, desc)
    - page: Page number
    
    Context:
    - buildorder_list: Paginated queryset
    - search_query: Current search term
    - current_sort: Current sort field
    - current_order: Current sort order
    - query_string: URL params for pagination
    """
```

**Responsibilities**:
- Filter build orders by search query (case-insensitive name matching)
- Sort by name, created_at, or updated_at
- Paginate results (25 per page)
- Preserve query parameters in pagination links
- Log query details at debug level

**Key Methods**:
- `get_queryset()`: Apply filters, search, and sorting
- `get_context_data()`: Add search/sort context for template

#### BuildOrderDetailView
```python
class BuildOrderDetailView(DetailView):
    """
    Display detailed build order with calculation summaries.
    
    URL Parameter:
    - pk: BuildOrder UUID
    
    Context:
    - buildorder: BuildOrder instance
    - calculation_summary: Cached calculation results
    - components_with_details: List of component dicts
    - ores_with_details: List of ore dicts
    """
```

**Responsibilities**:
- Retrieve build order by pk (404 if not found)
- Fetch cached calculation summary
- Get component and ore details using helper methods
- Log view access at info level
- Log cache hits/misses at debug level

**Key Methods**:
- `get_object()`: Retrieve BuildOrder by order_id (pk)
- `get_context_data()`: Add calculation data to context

#### BuildOrderCreateView
```python
class BuildOrderCreateView(CreateView):
    """
    Create new build order with form validation.
    
    Form Fields:
    - name: CharField
    - blocks_json: HiddenInput (populated by future JS)
    
    Success:
    - Redirect to detail view
    - Display success message
    - Log creation at info level
    """
```

**Responsibilities**:
- Display empty form
- Validate form submission
- Create BuildOrder instance
- Display success/error messages
- Log creation attempts and validation failures

**Key Methods**:
- `form_valid()`: Handle successful submission
- `form_invalid()`: Handle validation errors
- `get_success_url()`: Redirect to detail view

#### BuildOrderUpdateView
```python
class BuildOrderUpdateView(UpdateView):
    """
    Update existing build order with pre-populated form.
    
    URL Parameter:
    - pk: BuildOrder UUID
    
    Form Fields:
    - name: CharField (pre-populated)
    - blocks_json: HiddenInput (pre-populated)
    
    Success:
    - Redirect to detail view
    - Display success message
    - Log update at info level
    """
```

**Responsibilities**:
- Retrieve build order by pk (404 if not found)
- Pre-populate form with current data
- Validate form submission
- Update BuildOrder instance
- Invalidate cache on save
- Display success/error messages
- Log update attempts and validation failures

**Key Methods**:
- `get_object()`: Retrieve BuildOrder by order_id (pk)
- `form_valid()`: Handle successful update
- `form_invalid()`: Handle validation errors
- `get_success_url()`: Redirect to detail view

#### BuildOrderDeleteView
```python
class BuildOrderDeleteView(DeleteView):
    """
    Delete build order with confirmation.
    
    URL Parameter:
    - pk: BuildOrder UUID
    
    Confirmation:
    - Display build order details
    - Require POST request
    
    Success:
    - Redirect to list view
    - Display success message
    - Log deletion at info level
    """
```

**Responsibilities**:
- Retrieve build order by pk (404 if not found)
- Display confirmation page (GET)
- Delete build order (POST)
- Display success message
- Log deletion attempts

**Key Methods**:
- `get_object()`: Retrieve BuildOrder by order_id (pk)
- `form_valid()`: Handle confirmed deletion
- `get_context_data()`: Add build order details for confirmation

### Forms (buildorders/forms.py)

#### BuildOrderForm
```python
class BuildOrderForm(forms.ModelForm):
    """
    Form for creating/updating BuildOrders.
    
    Fields:
    - name: CharField (required, max 200)
    - blocks_json: CharField (HiddenInput, required)
    
    Validation:
    - Name not empty
    - blocks_json valid JSON structure
    - Block IDs exist in database
    - Quantities are positive integers
    - Calls BuildOrder.validate_blocks()
    """
```

**Responsibilities**:
- Render form fields with Bootstrap 5 styling
- Validate name field (not empty)
- Parse and validate blocks_json
- Convert blocks_json to dict for model
- Call BuildOrder.validate_blocks() for business logic validation
- Display field-specific error messages

**Key Methods**:
- `__init__()`: Pre-populate blocks_json for updates
- `clean_name()`: Validate name field
- `clean()`: Cross-field validation, blocks_json processing
- `save()`: Create/update BuildOrder with validated data

**Validation Flow**:
1. Field-level validation (clean_name)
2. Parse blocks_json from hidden field
3. Validate JSON structure (dict format)
4. Validate each block_id (UUID format, exists in DB)
5. Validate each quantity (positive integer)
6. Call BuildOrder.validate_blocks() for business rules
7. Store validated dict in cleaned_data

### URL Configuration (buildorders/urls.py)

```python
app_name = "buildorders"

urlpatterns = [
    path("", BuildOrderListView.as_view(), name="list"),
    path("<uuid:pk>/", BuildOrderDetailView.as_view(), name="detail"),
    path("create/", BuildOrderCreateView.as_view(), name="create"),
    path("<uuid:pk>/update/", BuildOrderUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete/", BuildOrderDeleteView.as_view(), name="delete"),
]
```

**URL Patterns**:
- `/buildorders/` → List view
- `/buildorders/<uuid>/` → Detail view
- `/buildorders/create/` → Create view
- `/buildorders/<uuid>/update/` → Update view
- `/buildorders/<uuid>/delete/` → Delete view

**URL Naming Convention**:
- Namespace: `buildorders:`
- Names: `list`, `detail`, `create`, `update`, `delete`
- Usage: `{% url 'buildorders:detail' pk=order.order_id %}`

### Templates

#### buildorder_list.html
```
Extends: base.html
Purpose: Display paginated list with search/sort

Layout:
- Header with "Create Build Order" button
- Search/sort form card
  - Search input (name)
  - Sort dropdown (name, created_at, updated_at)
  - Order dropdown (asc, desc)
- Build order cards (responsive grid)
  - Name, created date
  - Total mass (from calculation)
  - Action buttons (View, Edit, Delete)
- Pagination controls
- Empty state message
```

#### buildorder_detail.html
```
Extends: base.html
Purpose: Display build order with calculation summaries

Layout:
- Header with Edit/Delete buttons
- Build order info card
  - Name, created/updated dates
  - Blocks configuration (formatted JSON)
- Calculation summary card
  - Total mass
  - Required components table
    - Component name, quantity, mass
  - Required ores table
    - Ore name, quantity
  - Fabricator times table
    - Fabricator type, time (seconds)
- Back to list button
```

#### buildorder_form.html
```
Extends: base.html
Purpose: Create/update form

Layout:
- Header (Create/Update title)
- Form card
  - Name input (text)
  - blocks_json input (hidden)
  - Note: "Block selector coming in ENH-0000011"
  - Submit button
  - Cancel button
- Validation error display
```

#### buildorder_confirm_delete.html
```
Extends: base.html
Purpose: Deletion confirmation

Layout:
- Warning header
- Build order details card
  - Name
  - Created date
  - Number of blocks
- Confirmation form (POST)
  - "Are you sure?" message
  - Delete button (danger)
  - Cancel button
```

### Template Context

Each view provides specific context data:

**ListView Context**:
- `buildorder_list`: Paginated queryset
- `search_query`: Current search term
- `current_sort`: Current sort field
- `current_order`: Current sort order (asc/desc)
- `query_string`: URL params for pagination links
- `is_paginated`: Boolean
- `page_obj`: Pagination object

**DetailView Context**:
- `buildorder`: BuildOrder instance
- `calculation_summary`: Dict with mass, components, ores, times
- `components_with_details`: List of component dicts
- `ores_with_details`: List of ore dicts

**CreateView/UpdateView Context**:
- `form`: BuildOrderForm instance
- `form_title`: "Create Build Order" or "Update Build Order"
- `button_text`: "Create" or "Update"

**DeleteView Context**:
- `buildorder`: BuildOrder instance (as `delete_buildorder`)
- `blocks_count`: Number of blocks in configuration

## Data Models

### BuildOrder Model (Existing)

The BuildOrder model is already implemented in ENH-0000009. This design leverages its existing structure:

```python
class BuildOrder(models.Model):
    order_id = models.UUIDField(primary_key=True, default=generate_uuid)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    blocks = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Key Methods Used**:
- `validate_blocks()`: Returns list of validation errors
- `calculate_total_mass()`: Returns float (total mass in kg)
- `calculate_required_components()`: Returns dict {component_id: quantity}
- `calculate_required_ores()`: Returns dict {ore_id: quantity}
- `calculate_fabricator_times()`: Returns dict {fabricator_type: seconds}
- `get_calculation_summary()`: Returns dict with all calculations
- `get_cached_calculation_summary(use_cache=True)`: Returns cached or fresh calculations
- `_get_components_with_details()`: Returns list of component detail dicts
- `_get_ores_with_details()`: Returns list of ore detail dicts

**Cache Behavior**:
- Cache key: `buildorder_calc_{order_id}`
- TTL: 300 seconds (5 minutes)
- Invalidation: Automatic on save()
- Optional: `use_cache=False` for testing

### Related Models

The BuildOrder model depends on these existing models:

**Block Model** (from blocks app):
- `block_id`: UUIDField (primary key)
- `name`: CharField
- `mass`: FloatField
- `components`: JSONField (dict mapping component_id to quantity)

**Component Model** (from components app):
- `component_id`: UUIDField (primary key)
- `name`: CharField
- `mass`: FloatField
- `materials`: JSONField (dict mapping ore_id to quantity)
- `fabricator_type`: CharField
- `crafting_time`: FloatField

**Ore Model** (from ores app):
- `ore_id`: CharField (primary key)
- `name`: CharField
- `mass`: FloatField

### Data Flow

#### blocks JSONField Structure
```json
{
  "block-uuid-1": 10,
  "block-uuid-2": 5,
  "block-uuid-3": 20
}
```

#### Calculation Summary Structure
```json
{
  "total_mass": 12500.50,
  "required_components": {
    "component-uuid-1": 150,
    "component-uuid-2": 75
  },
  "required_ores": {
    "Iron": 5000.0,
    "Silicon": 2500.0
  },
  "fabricator_times": {
    "Assembler": 3600.0,
    "Refinery": 1800.0
  }
}
```

#### Component Details Structure
```python
[
  {
    "component": Component instance,
    "quantity": 150,
    "total_mass": 750.0
  },
  ...
]
```

#### Ore Details Structure
```python
[
  {
    "ore": Ore instance,
    "quantity": 5000.0
  },
  ...
]
```

### Form Data Processing

**Form Submission → Model Storage**:

1. User submits form with hidden blocks_json field
2. BuildOrderForm.clean() parses JSON string
3. Validates structure: `{"uuid": int, ...}`
4. Validates each UUID exists in Block table
5. Validates each quantity is positive integer
6. Calls BuildOrder.validate_blocks() for business rules
7. Stores validated dict in cleaned_data["blocks"]
8. BuildOrderForm.save() assigns dict to instance.blocks
9. Model save() triggers cache invalidation

**Model Storage → Form Display**:

1. BuildOrderForm.__init__() receives instance
2. Converts instance.blocks dict to JSON string
3. Sets initial["blocks_json"] for hidden field
4. Template renders hidden input with JSON value
5. Future JavaScript (ENH-0000011) will parse and display


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property Reflection

After analyzing all acceptance criteria, I identified the following redundancies and consolidations:

**Redundancy Analysis**:
1. Properties 5.5, 5.6, 5.7 (create success behavior) can be combined into one comprehensive property
2. Properties 6.7, 6.8, 6.9 (update success behavior) can be combined into one comprehensive property
3. Properties 7.6, 7.7, 7.8 (delete success behavior) can be combined into one comprehensive property
4. Properties 5.10, 6.13, 7.10 (logging creation/update/delete) can be combined into one property about CRUD operation logging
5. Properties 5.11, 6.14 (logging validation failures) are identical and can be combined
6. Properties 11.2, 11.3, 11.4 (logging successful operations) are redundant with the combined CRUD logging property
7. Properties 2.3 and 2.4 (URL parameter preservation and display) can be combined into one property about query parameter round-tripping
8. Properties 3.3 and 3.4 (sort parameter preservation and display) can be combined into one property about sort parameter round-tripping
9. Properties 9.1, 9.2, 9.3 (success messages) can be combined into one property about success message format
10. Properties 4.6 and 4.7 (component and ore details display) can be combined into one property about calculation details display

**Consolidated Properties**:
The following properties represent unique, non-redundant validation requirements that provide comprehensive coverage of the system's correctness.

### Property 1: Pagination Size Consistency

For any dataset of build orders, when the list view is rendered with more than 25 items, the first page should display exactly 25 items.

**Validates: Requirements 1.2**

### Property 2: Build Order Information Display

For any build order in the list view, the rendered HTML should contain the order name, total mass, and creation date.

**Validates: Requirements 1.3**

### Property 3: Pagination Controls Presence

For any dataset with more than 25 build orders, the list view should include pagination controls (next/previous links).

**Validates: Requirements 1.4**

### Property 4: Search Filtering Accuracy

For any search query and any set of build orders, the search results should only include build orders whose names contain the query string (case-insensitive).

**Validates: Requirements 2.2**

### Property 5: Query Parameter Round-Trip

For any search query submitted to the list view, the query should be preserved in the URL as a parameter and displayed in the search input field.

**Validates: Requirements 2.3, 2.4**

### Property 6: Sort Field Correctness

For any sort field (name, created_at, updated_at) and any dataset of build orders, the results should be ordered according to that field.

**Validates: Requirements 3.1**

### Property 7: Sort Direction Correctness

For any sort field and any dataset, sorting in ascending order should produce the opposite order of sorting in descending order.

**Validates: Requirements 3.2**

### Property 8: Sort Parameter Round-Trip

For any sort parameters (field and direction), they should be preserved in the URL and reflected in the UI controls.

**Validates: Requirements 3.3, 3.4**

### Property 9: Detail View Calculation Display

For any build order, the detail view should display all calculation summary fields: total mass, required components, required ores, and fabrication times.

**Validates: Requirements 4.4**

### Property 10: Detail View Resource Details Display

For any build order with components and ores, the detail view should display component details (name, quantity, mass) and ore details (name, quantity) using the model's helper methods.

**Validates: Requirements 4.6, 4.7**

### Property 11: Successful Create Operation

For any valid build order data submitted to the create form, the system should: (1) create a new BuildOrder record in the database, (2) redirect to the detail view of the created order, and (3) display a success message containing the order name.

**Validates: Requirements 5.5, 5.6, 5.7**

### Property 12: Invalid Create Operation

For any invalid build order data submitted to the create form, the system should display validation errors and not create a database record.

**Validates: Requirements 5.8**

### Property 13: Blocks Validation Integration

For any blocks_json input in create or update forms, the BuildOrder.validate_blocks() method should be called, and any validation errors should be displayed to the user.

**Validates: Requirements 5.9, 6.11, 13.3**

### Property 14: Successful Update Operation

For any valid update data submitted for an existing build order, the system should: (1) update the BuildOrder record in the database, (2) redirect to the detail view of the updated order, and (3) display a success message containing the order name.

**Validates: Requirements 6.7, 6.8, 6.9**

### Property 15: Form Pre-Population

For any existing build order, when the update form is loaded, all form fields should be pre-populated with the current build order data.

**Validates: Requirements 6.3**

### Property 16: Invalid Update Operation

For any invalid update data submitted for an existing build order, the system should display validation errors and not modify the database record.

**Validates: Requirements 6.10**

### Property 17: Delete Confirmation Display

For any build order, the delete confirmation page should display the build order name and key details before deletion.

**Validates: Requirements 7.3**

### Property 18: Delete HTTP Method Handling

For any build order, GET requests to the delete URL should display the confirmation page, and POST requests should delete the record.

**Validates: Requirements 7.4**

### Property 19: Successful Delete Operation

For any build order, when deletion is confirmed via POST, the system should: (1) delete the BuildOrder record from the database, (2) redirect to the list view, and (3) display a success message containing the order name.

**Validates: Requirements 7.6, 7.7, 7.8**

### Property 20: Navigation Active State

For any build order page (list, detail, create, update, delete), the "Build Orders" navigation link should have an active CSS class.

**Validates: Requirements 8.4**

### Property 21: Success Message Format

For any successful CRUD operation (create, update, delete), the success message should follow the format: "Build order '[name]' [action] successfully" where [action] is "created", "updated", or "deleted".

**Validates: Requirements 9.1, 9.2, 9.3**

### Property 22: Field-Specific Error Display

For any form validation failure, the system should display error messages specific to the fields that failed validation.

**Validates: Requirements 9.4**

### Property 23: CRUD Operation Logging

For any CRUD operation (create, update, delete), the system should log the operation at info level with relevant context (build order ID, user, action).

**Validates: Requirements 5.10, 6.13, 7.10, 11.2, 11.3, 11.4, 11.7**

### Property 24: Validation Failure Logging

For any form validation failure, the system should log the failure at warning level with relevant context.

**Validates: Requirements 5.11, 6.14, 11.5**

### Property 25: 404 Error Logging

For any request to a non-existent build order (detail, update, delete), the system should return a 404 error and log it at warning level.

**Validates: Requirements 11.6**

### Property 26: View Access Logging

For any view access, the system should log the access at debug level including user and timestamp information.

**Validates: Requirements 11.1**

### Property 27: Name Validation

For any form submission (create or update), if the name field is empty or whitespace-only, the form should fail validation with an appropriate error message.

**Validates: Requirements 13.1**

### Property 28: Block Quantity Validation

For any blocks_json input, if any block quantity is not a positive integer, the form should fail validation with an appropriate error message.

**Validates: Requirements 13.2**

### Property 29: Invalid Block ID Validation

For any blocks_json input containing block IDs that don't exist in the database, the form should fail validation with an error message identifying the invalid IDs.

**Validates: Requirements 13.4**

### Property 30: Invalid Quantity Validation

For any blocks_json input containing non-positive or non-integer quantities, the form should fail validation with an error message identifying the invalid quantities.

**Validates: Requirements 13.5**

### Property 31: Form Submission Prevention

For any form with validation errors, the form should not save to the database until all errors are resolved.

**Validates: Requirements 13.6**

### Property 32: Cache Miss Behavior

For any build order detail view where cached calculations are not available, the system should compute the calculations, cache them with a 5-minute TTL, and display them.

**Validates: Requirements 14.4**

### Property 33: Cache Logging

For any cache access (hit or miss), the system should log the event at debug level.

**Validates: Requirements 14.5**

## Error Handling

### HTTP Error Responses

**404 Not Found**:
- Triggered when: Accessing detail, update, or delete views for non-existent build orders
- Response: Django's 404 page or custom 404 template
- Logging: Warning level with build order ID and user context
- User Experience: Clear message that the build order doesn't exist

**400 Bad Request**:
- Triggered when: Form validation fails
- Response: Re-render form with error messages
- Logging: Warning level with validation errors
- User Experience: Field-specific error messages with Bootstrap danger styling

**500 Internal Server Error**:
- Triggered when: Unexpected exceptions (database errors, cache failures)
- Response: Django's 500 page or custom 500 template
- Logging: Error level with full stack trace
- User Experience: Generic error message with support contact

### Form Validation Errors

**Name Validation**:
- Empty name: "Build order name is required."
- Whitespace-only name: "Build order name cannot be empty."

**Blocks JSON Validation**:
- Invalid JSON format: "Invalid JSON format for blocks."
- Not a dictionary: "Blocks must be a dictionary of {block_id: quantity}."
- Invalid UUID: "Invalid block UUID: {block_id}"
- Block doesn't exist: "Block {block_id} does not exist in database."
- Invalid quantity: "Invalid quantity for block {block_id}: {quantity}. Must be positive integer."
- Empty blocks: "At least one block is required."

**Model Validation Errors**:
- Errors from BuildOrder.validate_blocks() are passed through to the form
- Format: "Block validation errors: {error1}; {error2}; ..."

### Cache Failures

**Cache Unavailable**:
- Fallback: Compute calculations without caching
- Logging: Warning level
- User Experience: No visible impact (slightly slower response)

**Cache Corruption**:
- Fallback: Invalidate cache entry, recompute calculations
- Logging: Warning level with cache key
- User Experience: No visible impact

### Database Errors

**Connection Failures**:
- Response: 500 error page
- Logging: Error level with connection details
- User Experience: "Database temporarily unavailable" message

**Integrity Errors**:
- Response: Form validation error
- Logging: Warning level
- User Experience: "Unable to save build order. Please try again."

### Logging Strategy

**Log Levels**:
- DEBUG: View access, query details, cache hits/misses
- INFO: Successful CRUD operations (create, update, delete)
- WARNING: Validation failures, 404 errors, cache failures
- ERROR: Unexpected exceptions, database errors

**Log Format**:
```
[LEVEL] [TIMESTAMP] [MODULE] [USER] [ACTION] [CONTEXT]
```

**Example Log Messages**:
```
DEBUG BuildOrderListView: user=john, query='armor', sort=name, order=asc, count=15
INFO BuildOrderCreateView: user=john, created build_order=uuid-123, name='Heavy Armor Build'
WARNING BuildOrderUpdateView: user=john, validation_failed build_order=uuid-123, errors=['Invalid block UUID']
WARNING BuildOrderDetailView: user=john, 404 build_order=uuid-999
ERROR BuildOrderDetailView: user=john, exception='Database connection failed'
```

**Log Context**:
- User: Request user (username or 'anonymous')
- Build Order ID: UUID of the build order being accessed/modified
- Action: Operation being performed (create, update, delete, view)
- Query Parameters: Search, sort, pagination parameters
- Validation Errors: Specific validation failures
- Exception Details: Stack trace for errors

## Testing Strategy

### Dual Testing Approach

The testing strategy employs both unit tests and property-based tests for comprehensive coverage:

**Unit Tests**: Verify specific examples, edge cases, and error conditions
- Specific URL routing examples
- Template structure verification
- Bootstrap CSS class presence
- Django messages framework integration
- Empty result set handling
- 404 error responses
- Form widget types (HiddenInput)

**Property-Based Tests**: Verify universal properties across all inputs
- Pagination behavior with varying dataset sizes
- Search filtering with random queries and datasets
- Sorting correctness with random data
- Form validation with generated valid/invalid inputs
- CRUD operation success/failure paths
- Logging behavior across operations
- Cache behavior with hits and misses

Together, these approaches provide comprehensive coverage: unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across the input space.

### Property-Based Testing Configuration

**Library**: Hypothesis (Python property-based testing library)

**Configuration**:
- Minimum 100 iterations per property test
- Each test tagged with comment referencing design property
- Tag format: `# Feature: buildorder-crud-views-templates, Property {number}: {property_text}`

**Example Property Test Structure**:
```python
from hypothesis import given, strategies as st
import hypothesis

@given(
    build_orders=st.lists(
        st.builds(BuildOrder, name=st.text(min_size=1, max_size=200)),
        min_size=0,
        max_size=100
    )
)
@hypothesis.settings(max_examples=100)
def test_pagination_size_consistency(build_orders):
    """
    Feature: buildorder-crud-views-templates, Property 1: 
    For any dataset of build orders, when the list view is rendered 
    with more than 25 items, the first page should display exactly 25 items.
    """
    # Test implementation
```

### Test Categories

**1. URL Routing Tests** (Unit Tests)
- Verify all 5 URL patterns resolve correctly
- Verify URL namespace is 'buildorders:'
- Verify pk parameter name consistency
- Verify URL names (list, detail, create, update, delete)

**2. List View Tests** (Mixed)
- Unit: Basic list rendering, empty state, Bootstrap classes
- Property: Pagination with varying dataset sizes (Property 1, 3)
- Property: Search filtering accuracy (Property 4)
- Property: Query parameter preservation (Property 5)
- Property: Sort field correctness (Property 6, 7)
- Property: Sort parameter preservation (Property 8)

**3. Detail View Tests** (Mixed)
- Unit: 404 for non-existent orders
- Unit: Template structure, Bootstrap classes
- Property: Calculation display completeness (Property 9)
- Property: Resource details display (Property 10)
- Property: Cache behavior (Property 32, 33)

**4. Create View Tests** (Mixed)
- Unit: Form rendering, hidden field widget
- Property: Successful creation workflow (Property 11)
- Property: Invalid data handling (Property 12)
- Property: Blocks validation integration (Property 13)
- Property: Success message format (Property 21)
- Property: Logging behavior (Property 23, 24)

**5. Update View Tests** (Mixed)
- Unit: 404 for non-existent orders
- Unit: Form rendering with pre-populated data
- Property: Form pre-population accuracy (Property 15)
- Property: Successful update workflow (Property 14)
- Property: Invalid data handling (Property 16)
- Property: Blocks validation integration (Property 13)
- Property: Success message format (Property 21)
- Property: Logging behavior (Property 23, 24)

**6. Delete View Tests** (Mixed)
- Unit: 404 for non-existent orders
- Unit: Confirmation page rendering
- Property: Confirmation display (Property 17)
- Property: HTTP method handling (Property 18)
- Property: Successful deletion workflow (Property 19)
- Property: Success message format (Property 21)
- Property: Logging behavior (Property 23)

**7. Form Validation Tests** (Property-Based)
- Property: Name validation (Property 27)
- Property: Block quantity validation (Property 28)
- Property: Invalid block ID handling (Property 29)
- Property: Invalid quantity handling (Property 30)
- Property: Form submission prevention (Property 31)
- Property: Field-specific error display (Property 22)

**8. Navigation Tests** (Mixed)
- Unit: Navigation link presence
- Unit: Link target verification
- Property: Active state indication (Property 20)

**9. Logging Tests** (Property-Based)
- Property: View access logging (Property 26)
- Property: CRUD operation logging (Property 23)
- Property: Validation failure logging (Property 24)
- Property: 404 error logging (Property 25)
- Property: Cache logging (Property 33)

**10. Integration Tests** (Unit Tests)
- Complete CRUD workflow (create → view → update → delete)
- Search → sort → paginate workflow
- Form validation → error display → correction → success
- Cache invalidation on update

### Test Data Generation

**Hypothesis Strategies**:
```python
# Build order names
names = st.text(min_size=1, max_size=200, alphabet=st.characters(blacklist_categories=('Cs',)))

# Block quantities
quantities = st.integers(min_value=1, max_value=1000)

# Block IDs (valid UUIDs)
block_ids = st.uuids().map(str)

# Blocks JSON (valid structure)
blocks_json = st.dictionaries(
    keys=block_ids,
    values=quantities,
    min_size=1,
    max_size=20
)

# Search queries
search_queries = st.text(min_size=0, max_size=100)

# Sort fields
sort_fields = st.sampled_from(['name', 'created_at', 'updated_at'])

# Sort orders
sort_orders = st.sampled_from(['asc', 'desc'])
```

### Coverage Goals

**Overall Coverage**: 90% minimum

**Per-Module Coverage**:
- views.py: 95% (high complexity, critical path)
- forms.py: 95% (validation logic)
- urls.py: 100% (simple configuration)
- templates: 85% (template logic)

**Uncovered Code**:
- Exception handlers for truly exceptional cases
- Defensive code for impossible states
- Logging statements (tested separately)

### Test Execution

**Command**: `pytest app/buildorders/test_*.py --hypothesis-show-statistics`

**CI/CD Integration**:
- Run on every commit
- Fail build if coverage < 90%
- Fail build if any property test fails
- Generate coverage report

**Performance**:
- Target: < 30 seconds for full test suite
- Property tests: 100 iterations each
- Use database transactions for test isolation
- Use Django test client (no browser automation)

