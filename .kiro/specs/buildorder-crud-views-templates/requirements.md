# Requirements Document

## Introduction

This document specifies the requirements for implementing complete CRUD (Create, Read, Update, Delete) views and templates for Build Orders in the EVE Online manufacturing calculator. The feature builds upon the existing BuildOrder model (ENH-0000009) to provide a user-facing web interface for managing build orders with calculation summary displays.

The system will provide a responsive Bootstrap 5 interface at `/buildorders/` URLs, allowing users to list, view, create, update, and delete build orders. The interface will display calculation summaries including total mass, required components, required ores, and fabrication times using cached calculations from the BuildOrder model.

## Glossary

- **BuildOrder**: A Django model representing a manufacturing order with blocks, quantity, and calculation methods
- **CRUD_Interface**: The web interface providing Create, Read, Update, Delete operations
- **List_View**: A paginated view displaying all build orders with search and sorting capabilities
- **Detail_View**: A view displaying a single build order with full calculation summaries
- **Create_Form**: A web form for creating new build orders
- **Update_Form**: A web form for editing existing build orders
- **Delete_Confirmation**: A page confirming deletion of a build order
- **Calculation_Summary**: Aggregated data including total mass, required components, required ores, and fabrication times
- **Blocks_JSONField**: A JSON field storing block configuration data (dict mapping block IDs to quantities)
- **Cached_Calculation**: Calculation results stored in cache with 5-minute TTL
- **URL_Namespace**: The Django URL namespace for build order routes (buildorders:)
- **Phase_2_Pattern**: Established patterns from blocks, components, and ores apps

## Requirements

### Requirement 1: List View Display

**User Story:** As a user, I want to view a list of all build orders, so that I can see my manufacturing orders at a glance.

#### Acceptance Criteria

1. THE List_View SHALL display build orders at the URL path `/buildorders/`
2. THE List_View SHALL display 25 build orders per page
3. THE List_View SHALL show order name, quantity, total mass, and creation date for each build order
4. WHEN the number of build orders exceeds 25, THE List_View SHALL provide pagination controls
5. THE List_View SHALL use the URL_Namespace `buildorders:list` for routing
6. THE List_View SHALL render using a Bootstrap 5 responsive template
7. THE List_View SHALL include a link to create new build orders

### Requirement 2: Search Functionality

**User Story:** As a user, I want to search build orders by name, so that I can quickly find specific orders.

#### Acceptance Criteria

1. THE List_View SHALL provide a search input field
2. WHEN a search query is submitted, THE List_View SHALL filter build orders by name using case-insensitive matching
3. THE List_View SHALL preserve the search query in the URL as a query parameter
4. THE List_View SHALL display the current search query in the search input field
5. THE List_View SHALL show a message when no build orders match the search query

### Requirement 3: Sorting Functionality

**User Story:** As a user, I want to sort build orders by different fields, so that I can organize my view of the data.

#### Acceptance Criteria

1. THE List_View SHALL support sorting by name, quantity, total mass, and creation date
2. THE List_View SHALL support both ascending and descending sort order
3. WHEN a sort option is selected, THE List_View SHALL preserve the sort parameters in the URL
4. THE List_View SHALL indicate the current sort field and direction in the interface
5. THE List_View SHALL default to sorting by creation date in descending order

### Requirement 4: Detail View Display

**User Story:** As a user, I want to view detailed information about a build order, so that I can see all calculation summaries.

#### Acceptance Criteria

1. THE Detail_View SHALL display build order details at the URL path `/buildorders/<pk>/`
2. THE Detail_View SHALL use `pk` as the URL parameter name for consistency with Phase_2_Pattern
3. THE Detail_View SHALL display order name, quantity, blocks configuration, and timestamps
4. THE Detail_View SHALL display the Calculation_Summary including total mass, required components, required ores, and fabrication times
5. THE Detail_View SHALL use Cached_Calculation from the BuildOrder model method `get_cached_calculation_summary()`
6. THE Detail_View SHALL display component details with names, quantities, and mass using BuildOrder helper method `_get_components_with_details()`
7. THE Detail_View SHALL display ore details with names, quantities, and mass using BuildOrder helper method `_get_ores_with_details()`
8. THE Detail_View SHALL use the URL_Namespace `buildorders:detail` for routing
9. THE Detail_View SHALL provide links to update and delete the build order
10. IF the build order does not exist, THEN THE Detail_View SHALL return a 404 error

### Requirement 5: Create Form

**User Story:** As a user, I want to create new build orders, so that I can plan manufacturing operations.

#### Acceptance Criteria

1. THE Create_Form SHALL be accessible at the URL path `/buildorders/create/`
2. THE Create_Form SHALL provide input fields for name, quantity, and blocks_json
3. THE Create_Form SHALL hide the blocks_json field from direct user input
4. THE Create_Form SHALL use the URL_Namespace `buildorders:create` for routing
5. WHEN the form is submitted with valid data, THE Create_Form SHALL create a new BuildOrder record
6. WHEN the form is submitted with valid data, THE Create_Form SHALL redirect to the Detail_View of the created build order
7. WHEN the form is submitted with valid data, THE Create_Form SHALL display a success message
8. WHEN the form is submitted with invalid data, THE Create_Form SHALL display validation errors
9. THE Create_Form SHALL validate blocks_json using the BuildOrder model method `validate_blocks()`
10. THE Create_Form SHALL log creation attempts at info level
11. THE Create_Form SHALL log validation failures at warning level

### Requirement 6: Update Form

**User Story:** As a user, I want to update existing build orders, so that I can modify manufacturing plans.

#### Acceptance Criteria

1. THE Update_Form SHALL be accessible at the URL path `/buildorders/<pk>/update/`
2. THE Update_Form SHALL use `pk` as the URL parameter name for consistency with Phase_2_Pattern
3. THE Update_Form SHALL pre-populate form fields with current build order data
4. THE Update_Form SHALL provide input fields for name, quantity, and blocks_json
5. THE Update_Form SHALL hide the blocks_json field from direct user input
6. THE Update_Form SHALL use the URL_Namespace `buildorders:update` for routing
7. WHEN the form is submitted with valid data, THE Update_Form SHALL update the BuildOrder record
8. WHEN the form is submitted with valid data, THE Update_Form SHALL redirect to the Detail_View of the updated build order
9. WHEN the form is submitted with valid data, THE Update_Form SHALL display a success message
10. WHEN the form is submitted with invalid data, THE Update_Form SHALL display validation errors
11. THE Update_Form SHALL validate blocks_json using the BuildOrder model method `validate_blocks()`
12. IF the build order does not exist, THEN THE Update_Form SHALL return a 404 error
13. THE Update_Form SHALL log update attempts at info level
14. THE Update_Form SHALL log validation failures at warning level

### Requirement 7: Delete Confirmation

**User Story:** As a user, I want to confirm deletion of build orders, so that I can avoid accidental data loss.

#### Acceptance Criteria

1. THE Delete_Confirmation SHALL be accessible at the URL path `/buildorders/<pk>/delete/`
2. THE Delete_Confirmation SHALL use `pk` as the URL parameter name for consistency with Phase_2_Pattern
3. THE Delete_Confirmation SHALL display the build order name and key details
4. THE Delete_Confirmation SHALL require POST request confirmation to delete
5. THE Delete_Confirmation SHALL use the URL_Namespace `buildorders:delete` for routing
6. WHEN deletion is confirmed, THE Delete_Confirmation SHALL delete the BuildOrder record
7. WHEN deletion is confirmed, THE Delete_Confirmation SHALL redirect to the List_View
8. WHEN deletion is confirmed, THE Delete_Confirmation SHALL display a success message
9. IF the build order does not exist, THEN THE Delete_Confirmation SHALL return a 404 error
10. THE Delete_Confirmation SHALL log deletion attempts at info level

### Requirement 8: Navigation Integration

**User Story:** As a user, I want to access build order views from the main navigation, so that I can easily navigate the application.

#### Acceptance Criteria

1. THE CRUD_Interface SHALL add a "Build Orders" link to the main navigation menu
2. THE navigation link SHALL direct users to the List_View
3. THE navigation link SHALL be visually consistent with other navigation items
4. THE navigation link SHALL indicate the active state when on build order pages

### Requirement 9: Success and Error Messages

**User Story:** As a user, I want to see feedback messages after actions, so that I know whether operations succeeded or failed.

#### Acceptance Criteria

1. WHEN a build order is created, THE CRUD_Interface SHALL display the message "Build order '[name]' created successfully"
2. WHEN a build order is updated, THE CRUD_Interface SHALL display the message "Build order '[name]' updated successfully"
3. WHEN a build order is deleted, THE CRUD_Interface SHALL display the message "Build order '[name]' deleted successfully"
4. WHEN a form validation fails, THE CRUD_Interface SHALL display field-specific error messages
5. THE CRUD_Interface SHALL use Django messages framework for displaying feedback
6. THE CRUD_Interface SHALL style success messages with Bootstrap success styling
7. THE CRUD_Interface SHALL style error messages with Bootstrap danger styling

### Requirement 10: Responsive Template Design

**User Story:** As a user, I want the interface to work on different screen sizes, so that I can access it from various devices.

#### Acceptance Criteria

1. THE CRUD_Interface SHALL use Bootstrap 5 responsive grid system
2. THE CRUD_Interface SHALL adapt layout for mobile, tablet, and desktop screen sizes
3. THE List_View SHALL display data in a responsive table or card layout
4. THE Detail_View SHALL stack calculation summaries vertically on small screens
5. THE Create_Form and Update_Form SHALL use responsive form layouts

### Requirement 11: Logging

**User Story:** As a developer, I want comprehensive logging of view operations, so that I can debug issues and monitor usage.

#### Acceptance Criteria

1. THE CRUD_Interface SHALL log view access at debug level including user and timestamp
2. THE CRUD_Interface SHALL log successful create operations at info level
3. THE CRUD_Interface SHALL log successful update operations at info level
4. THE CRUD_Interface SHALL log successful delete operations at info level
5. THE CRUD_Interface SHALL log validation failures at warning level
6. THE CRUD_Interface SHALL log 404 errors at warning level
7. THE CRUD_Interface SHALL include relevant context in log messages (build order ID, user, action)

### Requirement 12: URL Configuration

**User Story:** As a developer, I want consistent URL patterns, so that the application follows Django best practices.

#### Acceptance Criteria

1. THE CRUD_Interface SHALL use the URL_Namespace `buildorders:` for all routes
2. THE CRUD_Interface SHALL use `pk` as the URL parameter name in all detail, update, and delete URLs
3. THE CRUD_Interface SHALL follow RESTful URL conventions
4. THE CRUD_Interface SHALL register URLs in the buildorders app urls.py
5. THE CRUD_Interface SHALL include URLs in the project's main urls.py with the namespace

### Requirement 13: Form Validation

**User Story:** As a user, I want forms to validate my input, so that I cannot create invalid build orders.

#### Acceptance Criteria

1. THE Create_Form and Update_Form SHALL validate that name is not empty
2. THE Create_Form and Update_Form SHALL validate that quantity is a positive integer
3. THE Create_Form and Update_Form SHALL validate blocks_json structure using BuildOrder.validate_blocks()
4. WHEN blocks_json contains invalid block IDs, THE forms SHALL display an error message
5. WHEN blocks_json contains invalid quantity values, THE forms SHALL display an error message
6. THE forms SHALL prevent submission until all validation errors are resolved

### Requirement 14: Calculation Display Performance

**User Story:** As a user, I want calculation summaries to load quickly, so that I have a responsive experience.

#### Acceptance Criteria

1. THE Detail_View SHALL use Cached_Calculation to avoid redundant computation
2. THE List_View SHALL use database-level aggregation for total mass display
3. THE Detail_View SHALL retrieve cached calculations with 5-minute TTL
4. WHEN cached calculations are not available, THE Detail_View SHALL compute and cache them
5. THE CRUD_Interface SHALL log cache hits and misses at debug level

### Requirement 15: Testing Coverage

**User Story:** As a developer, I want comprehensive automated tests, so that I can ensure the feature works correctly.

#### Acceptance Criteria

1. THE CRUD_Interface SHALL have at least 35 automated tests
2. THE CRUD_Interface SHALL achieve at least 90% test coverage
3. THE test suite SHALL include property-based tests for view calculations
4. THE test suite SHALL include property-based tests for pagination behavior
5. THE test suite SHALL include property-based tests for search functionality
6. THE test suite SHALL include property-based tests for sorting functionality
7. THE test suite SHALL include integration tests for complete CRUD workflows
8. THE test suite SHALL test form validation with valid and invalid inputs
9. THE test suite SHALL test 404 error handling
10. THE test suite SHALL test success and error message display

## Notes

This feature builds directly on ENH-0000009 (BuildOrder Model) and follows established Phase 2 patterns from the blocks, components, and ores apps. The implementation should leverage existing BuildOrder model methods for calculations and validation rather than duplicating logic in views.

The blocks_json field is intentionally hidden in forms because the JavaScript block selector interface will be implemented in ENH-0000011. For now, the field can be populated programmatically in tests or through the Django admin interface.

The recommended updates document (ENH0000010-RECOMMENDED-UPDATES.md) provides additional guidance on implementation patterns, caching strategies, and testing approaches that align with Phase 2 standards.
