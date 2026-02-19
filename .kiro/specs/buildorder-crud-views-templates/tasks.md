# Implementation Plan: BuildOrder CRUD Views and Templates

## Overview

This implementation plan creates a complete CRUD interface for BuildOrders using Django class-based views, forms, and Bootstrap 5 templates. The implementation follows Phase 2 patterns from blocks/components/ores apps and leverages existing BuildOrder model methods for calculations and validation.

## Tasks

- [ ] 1. Set up URL configuration and project integration
  - Create `app/buildorders/urls.py` with namespace `buildorders:`
  - Define 5 URL patterns: list, detail, create, update, delete (use `pk` parameter)
  - Update `app/se2CalcProject/urls.py` to include buildorders URLs
  - Update `app/templates/base.html` to add "Build Orders" navigation link
  - _Requirements: 8.1, 8.2, 8.3, 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 2. Implement BuildOrderForm with validation
  - [ ] 2.1 Create `app/buildorders/forms.py` with BuildOrderForm class
    - Define form fields: name (CharField), blocks_json (CharField with HiddenInput)
    - Implement `clean_name()` to validate non-empty name
    - Implement `clean()` to parse and validate blocks_json structure
    - Call `BuildOrder.validate_blocks()` for business logic validation
    - Handle validation errors with field-specific messages
    - _Requirements: 5.2, 5.3, 5.9, 6.4, 6.5, 6.11, 13.1, 13.2, 13.3, 13.4, 13.5, 13.6_
  
  - [ ]* 2.2 Write property test for name validation
    - **Property 27: Name Validation**
    - **Validates: Requirements 13.1**
  
  - [ ]* 2.3 Write property test for block quantity validation
    - **Property 28: Block Quantity Validation**
    - **Validates: Requirements 13.2**
  
  - [ ]* 2.4 Write property test for invalid block ID validation
    - **Property 29: Invalid Block ID Validation**
    - **Validates: Requirements 13.4**
  
  - [ ]* 2.5 Write property test for invalid quantity validation
    - **Property 30: Invalid Quantity Validation**
    - **Validates: Requirements 13.5**
  
  - [ ]* 2.6 Write property test for form submission prevention
    - **Property 31: Form Submission Prevention**
    - **Validates: Requirements 13.6**
  
  - [ ]* 2.7 Write unit tests for BuildOrderForm
    - Test form field widgets (HiddenInput for blocks_json)
    - Test empty name validation error messages
    - Test invalid JSON format error messages
    - _Requirements: 5.8, 6.10, 9.4_

- [ ] 3. Implement BuildOrderListView with search and sorting
  - [ ] 3.1 Create `app/buildorders/views.py` with BuildOrderListView class
    - Extend Django ListView with model=BuildOrder
    - Implement `get_queryset()` to apply search filtering (case-insensitive name matching)
    - Implement sorting by name, created_at, updated_at (ascending/descending)
    - Set pagination to 25 items per page
    - Implement `get_context_data()` to add search/sort parameters to context
    - Add comprehensive logging (debug level for queries, info level for access)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 11.1_
  
  - [ ]* 3.2 Write property test for pagination size consistency
    - **Property 1: Pagination Size Consistency**
    - **Validates: Requirements 1.2**
  
  - [ ]* 3.3 Write property test for pagination controls presence
    - **Property 3: Pagination Controls Presence**
    - **Validates: Requirements 1.4**
  
  - [ ]* 3.4 Write property test for search filtering accuracy
    - **Property 4: Search Filtering Accuracy**
    - **Validates: Requirements 2.2**
  
  - [ ]* 3.5 Write property test for query parameter round-trip
    - **Property 5: Query Parameter Round-Trip**
    - **Validates: Requirements 2.3, 2.4**
  
  - [ ]* 3.6 Write property test for sort field correctness
    - **Property 6: Sort Field Correctness**
    - **Validates: Requirements 3.1**
  
  - [ ]* 3.7 Write property test for sort direction correctness
    - **Property 7: Sort Direction Correctness**
    - **Validates: Requirements 3.2**
  
  - [ ]* 3.8 Write property test for sort parameter round-trip
    - **Property 8: Sort Parameter Round-Trip**
    - **Validates: Requirements 3.3, 3.4**
  
  - [ ]* 3.9 Write unit tests for BuildOrderListView
    - Test empty result set display
    - Test Bootstrap CSS classes presence
    - Test "Create Build Order" link presence
    - Test URL routing to buildorders:list
    - _Requirements: 1.6, 1.7, 2.5_

- [ ] 4. Implement BuildOrderDetailView with calculation summaries
  - [ ] 4.1 Create BuildOrderDetailView class in views.py
    - Extend Django DetailView with model=BuildOrder
    - Use `pk` URL parameter (slug_field='order_id', slug_url_kwarg='pk')
    - Implement `get_context_data()` to add cached calculation summary
    - Call `get_cached_calculation_summary()` for calculations
    - Call `_get_components_with_details()` and `_get_ores_with_details()` for resource details
    - Add comprehensive logging (info level for access, debug level for cache hits/misses, warning level for 404)
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.10, 11.1, 11.6, 14.1, 14.3, 14.4, 14.5_
  
  - [ ]* 4.2 Write property test for calculation display
    - **Property 9: Detail View Calculation Display**
    - **Validates: Requirements 4.4**
  
  - [ ]* 4.3 Write property test for resource details display
    - **Property 10: Detail View Resource Details Display**
    - **Validates: Requirements 4.6, 4.7**
  
  - [ ]* 4.4 Write property test for cache miss behavior
    - **Property 32: Cache Miss Behavior**
    - **Validates: Requirements 14.4**
  
  - [ ]* 4.5 Write property test for cache logging
    - **Property 33: Cache Logging**
    - **Validates: Requirements 14.5**
  
  - [ ]* 4.6 Write unit tests for BuildOrderDetailView
    - Test 404 error for non-existent build orders
    - Test template structure and Bootstrap classes
    - Test edit/delete button links
    - Test URL routing to buildorders:detail
    - _Requirements: 4.9, 4.10_

- [ ] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement BuildOrderCreateView with form handling
  - [ ] 6.1 Create BuildOrderCreateView class in views.py
    - Extend Django CreateView with model=BuildOrder, form_class=BuildOrderForm
    - Implement `form_valid()` to handle successful submission
    - Add success message using Django messages framework
    - Implement `get_success_url()` to redirect to detail view
    - Implement `form_invalid()` to log validation failures
    - Add comprehensive logging (info level for creation, warning level for validation failures)
    - _Requirements: 5.1, 5.4, 5.5, 5.6, 5.7, 5.8, 5.10, 5.11, 9.1, 9.4, 9.5, 9.6, 11.2, 11.5_
  
  - [ ]* 6.2 Write property test for successful create operation
    - **Property 11: Successful Create Operation**
    - **Validates: Requirements 5.5, 5.6, 5.7**
  
  - [ ]* 6.3 Write property test for invalid create operation
    - **Property 12: Invalid Create Operation**
    - **Validates: Requirements 5.8**
  
  - [ ]* 6.4 Write property test for blocks validation integration
    - **Property 13: Blocks Validation Integration**
    - **Validates: Requirements 5.9, 6.11, 13.3**
  
  - [ ]* 6.5 Write property test for CRUD operation logging
    - **Property 23: CRUD Operation Logging**
    - **Validates: Requirements 5.10, 6.13, 7.10, 11.2, 11.3, 11.4, 11.7**
  
  - [ ]* 6.6 Write property test for validation failure logging
    - **Property 24: Validation Failure Logging**
    - **Validates: Requirements 5.11, 6.14, 11.5**
  
  - [ ]* 6.7 Write unit tests for BuildOrderCreateView
    - Test form rendering with hidden blocks_json field
    - Test URL routing to buildorders:create
    - Test success message format
    - _Requirements: 5.1, 5.3, 9.1_

- [ ] 7. Implement BuildOrderUpdateView with form handling
  - [ ] 7.1 Create BuildOrderUpdateView class in views.py
    - Extend Django UpdateView with model=BuildOrder, form_class=BuildOrderForm
    - Use `pk` URL parameter (slug_field='order_id', slug_url_kwarg='pk')
    - Implement `form_valid()` to handle successful update
    - Add success message using Django messages framework
    - Implement `get_success_url()` to redirect to detail view
    - Implement `form_invalid()` to log validation failures
    - Add comprehensive logging (info level for updates, warning level for validation failures and 404)
    - _Requirements: 6.1, 6.2, 6.6, 6.7, 6.8, 6.9, 6.10, 6.12, 6.13, 6.14, 9.2, 9.4, 9.5, 9.7, 11.3, 11.5, 11.6_
  
  - [ ]* 7.2 Write property test for form pre-population
    - **Property 15: Form Pre-Population**
    - **Validates: Requirements 6.3**
  
  - [ ]* 7.3 Write property test for successful update operation
    - **Property 14: Successful Update Operation**
    - **Validates: Requirements 6.7, 6.8, 6.9**
  
  - [ ]* 7.4 Write property test for invalid update operation
    - **Property 16: Invalid Update Operation**
    - **Validates: Requirements 6.10**
  
  - [ ]* 7.5 Write unit tests for BuildOrderUpdateView
    - Test 404 error for non-existent build orders
    - Test form pre-population with current data
    - Test URL routing to buildorders:update
    - Test success message format
    - _Requirements: 6.1, 6.2, 6.3, 6.12, 9.2_

- [ ] 8. Implement BuildOrderDeleteView with confirmation
  - [ ] 8.1 Create BuildOrderDeleteView class in views.py
    - Extend Django DeleteView with model=BuildOrder
    - Use `pk` URL parameter (slug_field='order_id', slug_url_kwarg='pk')
    - Implement `get_success_url()` to redirect to list view
    - Implement `delete()` to add success message
    - Add comprehensive logging (info level for deletion, warning level for 404)
    - _Requirements: 7.1, 7.2, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 9.3, 9.5, 9.7, 11.4, 11.6_
  
  - [ ]* 8.2 Write property test for delete confirmation display
    - **Property 17: Delete Confirmation Display**
    - **Validates: Requirements 7.3**
  
  - [ ]* 8.3 Write property test for delete HTTP method handling
    - **Property 18: Delete HTTP Method Handling**
    - **Validates: Requirements 7.4**
  
  - [ ]* 8.4 Write property test for successful delete operation
    - **Property 19: Successful Delete Operation**
    - **Validates: Requirements 7.6, 7.7, 7.8**
  
  - [ ]* 8.5 Write unit tests for BuildOrderDeleteView
    - Test 404 error for non-existent build orders
    - Test confirmation page rendering
    - Test URL routing to buildorders:delete
    - Test success message format
    - _Requirements: 7.1, 7.2, 7.9, 9.3_

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Create buildorder_list.html template
  - [ ] 10.1 Create `app/buildorders/templates/buildorders/buildorder_list.html`
    - Extend base.html template
    - Add header with "Create Build Order" button linking to buildorders:create
    - Create search/sort form card with Bootstrap 5 styling
    - Add search input field (preserve query parameter)
    - Add sort dropdown (name, created_at, updated_at) with current selection
    - Add order dropdown (asc, desc) with current selection
    - Create responsive grid of build order cards
    - Display name, created date, total mass for each order
    - Add action buttons (View, Edit, Delete) for each order
    - Implement pagination controls with query parameter preservation
    - Add empty state message when no orders exist
    - Use Bootstrap 5 responsive classes
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.6, 1.7, 2.1, 2.3, 2.4, 2.5, 3.3, 3.4, 10.1, 10.2, 10.3_
  
  - [ ]* 10.2 Write property test for build order information display
    - **Property 2: Build Order Information Display**
    - **Validates: Requirements 1.3**
  
  - [ ]* 10.3 Write unit tests for buildorder_list.html
    - Test Bootstrap CSS classes presence
    - Test responsive grid structure
    - Test empty state message display
    - _Requirements: 1.6, 2.5, 10.1, 10.3_

- [ ] 11. Create buildorder_detail.html template
  - [ ] 11.1 Create `app/buildorders/templates/buildorders/buildorder_detail.html`
    - Extend base.html template
    - Add header with Edit and Delete buttons
    - Create build order info card with name, created/updated dates, blocks configuration
    - Format blocks JSON for display
    - Create calculation summary card with total mass
    - Create required components table (component name, quantity, mass)
    - Create required ores table (ore name, quantity)
    - Create fabricator times table (fabricator type, time in seconds)
    - Add "Back to List" button
    - Use Bootstrap 5 responsive classes
    - Stack cards vertically on small screens
    - _Requirements: 4.1, 4.3, 4.4, 4.6, 4.7, 4.9, 10.1, 10.2, 10.4_
  
  - [ ]* 11.2 Write unit tests for buildorder_detail.html
    - Test Bootstrap CSS classes presence
    - Test calculation summary display structure
    - Test component and ore table structure
    - Test responsive stacking on small screens
    - _Requirements: 10.1, 10.2, 10.4_

- [ ] 12. Create buildorder_form.html template
  - [ ] 12.1 Create `app/buildorders/templates/buildorders/buildorder_form.html`
    - Extend base.html template
    - Add dynamic header (Create/Update based on context)
    - Create form card with Bootstrap 5 styling
    - Render name input field with validation error display
    - Render blocks_json hidden input field
    - Add note: "Block selector coming in ENH-0000011"
    - Add Submit button (dynamic text: Create/Update)
    - Add Cancel button linking back to list or detail view
    - Display field-specific validation errors with Bootstrap danger styling
    - Use Bootstrap 5 responsive form layout
    - _Requirements: 5.1, 5.2, 5.3, 5.8, 6.1, 6.4, 6.5, 6.10, 9.4, 9.7, 10.1, 10.2, 10.5_
  
  - [ ]* 12.2 Write property test for field-specific error display
    - **Property 22: Field-Specific Error Display**
    - **Validates: Requirements 9.4**
  
  - [ ]* 12.3 Write unit tests for buildorder_form.html
    - Test form field rendering
    - Test hidden blocks_json field widget
    - Test validation error display styling
    - Test responsive form layout
    - _Requirements: 5.3, 6.5, 9.7, 10.1, 10.2, 10.5_

- [ ] 13. Create buildorder_confirm_delete.html template
  - [ ] 13.1 Create `app/buildorders/templates/buildorders/buildorder_confirm_delete.html`
    - Extend base.html template
    - Add warning header
    - Create build order details card (name, created date, number of blocks)
    - Create confirmation form (POST method)
    - Add "Are you sure?" message
    - Add Delete button with Bootstrap danger styling
    - Add Cancel button linking back to detail view
    - Use Bootstrap 5 responsive classes
    - _Requirements: 7.1, 7.3, 7.4, 10.1, 10.2_
  
  - [ ]* 13.2 Write unit tests for buildorder_confirm_delete.html
    - Test confirmation message display
    - Test build order details display
    - Test POST form structure
    - Test Bootstrap danger styling on delete button
    - _Requirements: 7.3, 7.4, 10.1_

- [ ] 14. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 15. Implement navigation integration and active state
  - [ ] 15.1 Update base.html navigation
    - Add "Build Orders" link to main navigation menu
    - Link to buildorders:list URL
    - Implement active state indication for build order pages
    - Ensure visual consistency with other navigation items
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  
  - [ ]* 15.2 Write property test for navigation active state
    - **Property 20: Navigation Active State**
    - **Validates: Requirements 8.4**
  
  - [ ]* 15.3 Write unit tests for navigation integration
    - Test navigation link presence
    - Test link target verification
    - Test visual consistency
    - _Requirements: 8.1, 8.2, 8.3_

- [ ] 16. Implement success message formatting
  - [ ] 16.1 Add success message logic to views
    - Ensure create view uses format: "Build order '[name]' created successfully"
    - Ensure update view uses format: "Build order '[name]' updated successfully"
    - Ensure delete view uses format: "Build order '[name]' deleted successfully"
    - Use Django messages framework with success level
    - _Requirements: 9.1, 9.2, 9.3, 9.5, 9.6_
  
  - [ ]* 16.2 Write property test for success message format
    - **Property 21: Success Message Format**
    - **Validates: Requirements 9.1, 9.2, 9.3**
  
  - [ ]* 16.3 Write unit tests for success messages
    - Test message display in templates
    - Test Bootstrap success styling
    - _Requirements: 9.5, 9.6_

- [ ] 17. Implement comprehensive logging
  - [ ] 17.1 Add logging to all views
    - Add debug level logging for view access (user, timestamp)
    - Add info level logging for successful CRUD operations
    - Add warning level logging for validation failures
    - Add warning level logging for 404 errors
    - Add debug level logging for cache hits/misses
    - Include relevant context in all log messages (build order ID, user, action)
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 14.5_
  
  - [ ]* 17.2 Write property test for view access logging
    - **Property 26: View Access Logging**
    - **Validates: Requirements 11.1**
  
  - [ ]* 17.3 Write property test for 404 error logging
    - **Property 25: 404 Error Logging**
    - **Validates: Requirements 11.6**
  
  - [ ]* 17.4 Write unit tests for logging
    - Test log message format
    - Test log context inclusion
    - Test log level correctness
    - _Requirements: 11.7_

- [ ] 18. Write integration tests for complete CRUD workflows
  - [ ]* 18.1 Write integration test for complete CRUD workflow
    - Test create → view → update → delete sequence
    - Verify database state at each step
    - Verify success messages at each step
    - Verify redirects at each step
    - _Requirements: 15.7_
  
  - [ ]* 18.2 Write integration test for search → sort → paginate workflow
    - Test query parameter preservation across operations
    - Verify result accuracy at each step
    - _Requirements: 15.7_
  
  - [ ]* 18.3 Write integration test for form validation → error → correction → success
    - Test validation error display
    - Test form re-submission with corrected data
    - Verify database state after correction
    - _Requirements: 15.7, 15.8_
  
  - [ ]* 18.4 Write integration test for cache invalidation on update
    - Create build order and view detail (cache calculation)
    - Update build order
    - View detail again and verify cache was invalidated
    - _Requirements: 14.3, 14.4_

- [ ] 19. Final checkpoint - Ensure all tests pass and coverage meets target
  - Run full test suite with coverage report
  - Verify at least 35 automated tests exist
  - Verify at least 90% test coverage achieved
  - Ensure all tests pass, ask the user if questions arise.
  - _Requirements: 15.1, 15.2_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties (33 properties from design)
- Unit tests validate specific examples and edge cases
- Integration tests validate complete workflows
- The implementation leverages existing BuildOrder model methods (validate_blocks, get_cached_calculation_summary, _get_components_with_details, _get_ores_with_details)
- URL parameter naming uses `pk` for consistency with Phase 2 patterns
- All views use comprehensive logging at appropriate levels (debug, info, warning)
- Templates use Bootstrap 5 responsive design
- Forms use Django messages framework for user feedback
- The blocks_json field is hidden because the JavaScript selector comes in ENH-0000011
