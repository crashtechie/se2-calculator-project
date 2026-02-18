# Requirements Document: Build Order Calculator

## Introduction

The Build Order Calculator is a comprehensive web interface for managing and calculating resource requirements for Space Engineers 2 build projects. This feature completes Phase 3 of the SE2 Calculator project by providing CRUD operations for BuildOrder objects and an interactive interface for selecting blocks and viewing real-time resource calculations.

The system builds upon the existing resource chain (Ores → Components → Blocks → BuildOrders) and leverages the calculation methods already implemented in the BuildOrder model. Users can create, view, update, and delete build orders while seeing detailed breakdowns of required components, ores, total mass, and fabrication times.

## Glossary

- **BuildOrder**: A collection of blocks with quantities representing a construction project
- **Block**: A game object that can be placed in Space Engineers 2, composed of components
- **Component**: A crafted item made from ores, used to construct blocks
- **Ore**: Raw material extracted from asteroids or planets
- **Resource_Chain**: The hierarchical calculation from blocks to components to ores
- **Fabricator**: A game machine that crafts components from ores
- **Web_Interface**: The Django-based web application providing the user interface
- **CRUD**: Create, Read, Update, Delete operations
- **Dynamic_Selector**: JavaScript-based interface for adding/removing blocks with quantities
- **Live_Preview**: Real-time calculation display updated via AJAX
- **Calculation_Summary**: Aggregated data showing total mass, components, ores, and fabrication times

## Requirements

### Requirement 1: Build Order List View

**User Story:** As a player, I want to view all my build orders in a paginated list, so that I can browse and manage my construction projects.

#### Acceptance Criteria

1. THE Web_Interface SHALL display all BuildOrders in a paginated list with 10 items per page
2. WHEN a user searches by name or description, THE Web_Interface SHALL filter the BuildOrder list to show only matching results
3. WHEN a user sorts by name, created date, or updated date, THE Web_Interface SHALL reorder the list accordingly
4. WHEN a user clicks on a BuildOrder, THE Web_Interface SHALL navigate to the detail view
5. THE Web_Interface SHALL display each BuildOrder's name, description, block count, and creation date in the list
6. WHEN the list is empty, THE Web_Interface SHALL display a message prompting the user to create their first build order

### Requirement 2: Build Order Detail View

**User Story:** As a player, I want to view detailed information about a build order, so that I can see the complete resource breakdown and plan my construction.

#### Acceptance Criteria

1. THE Web_Interface SHALL display the BuildOrder name, description, and timestamps
2. THE Web_Interface SHALL display all blocks in the BuildOrder with their quantities
3. THE Web_Interface SHALL display the total mass calculation for the entire build order
4. THE Web_Interface SHALL display the complete list of required components with quantities
5. THE Web_Interface SHALL display the complete list of required ores with quantities
6. THE Web_Interface SHALL display fabrication times grouped by fabricator type
7. WHEN calculation data is cached, THE Web_Interface SHALL retrieve results from cache within 5 minutes TTL
8. THE Web_Interface SHALL provide navigation links to edit or delete the BuildOrder

### Requirement 3: Build Order Creation

**User Story:** As a player, I want to create a new build order by selecting blocks and quantities, so that I can plan my construction projects.

#### Acceptance Criteria

1. THE Web_Interface SHALL provide a form with fields for name and description
2. THE Web_Interface SHALL provide a Dynamic_Selector for adding blocks with quantities
3. WHEN a user searches for a block, THE Web_Interface SHALL filter available blocks by name
4. WHEN a user adds a block, THE Web_Interface SHALL display it in the selected blocks list with a quantity input
5. WHEN a user removes a block, THE Web_Interface SHALL remove it from the selected blocks list
6. WHEN a user submits the form with valid data, THE Web_Interface SHALL create a new BuildOrder
7. WHEN a user submits the form with invalid data, THE Web_Interface SHALL display validation errors
8. WHEN a BuildOrder is created, THE Web_Interface SHALL redirect to the detail view
9. THE Web_Interface SHALL require at least one block with a positive quantity

### Requirement 4: Build Order Updates

**User Story:** As a player, I want to update an existing build order, so that I can modify my construction plans as needs change.

#### Acceptance Criteria

1. THE Web_Interface SHALL pre-populate the form with existing BuildOrder data
2. THE Web_Interface SHALL pre-populate the Dynamic_Selector with existing blocks and quantities
3. WHEN a user modifies the name or description, THE Web_Interface SHALL update those fields
4. WHEN a user adds, removes, or changes block quantities, THE Web_Interface SHALL update the blocks JSONField
5. WHEN a user submits valid changes, THE Web_Interface SHALL save the updated BuildOrder
6. WHEN a BuildOrder is updated, THE Web_Interface SHALL invalidate the calculation cache
7. WHEN a user submits invalid changes, THE Web_Interface SHALL display validation errors
8. WHEN a BuildOrder is updated, THE Web_Interface SHALL redirect to the detail view

### Requirement 5: Build Order Deletion

**User Story:** As a player, I want to delete a build order I no longer need, so that I can keep my project list organized.

#### Acceptance Criteria

1. THE Web_Interface SHALL display a confirmation page before deletion
2. THE Web_Interface SHALL show the BuildOrder name and block count on the confirmation page
3. WHEN a user confirms deletion, THE Web_Interface SHALL remove the BuildOrder from the database
4. WHEN a BuildOrder is deleted, THE Web_Interface SHALL redirect to the list view
5. WHEN a user cancels deletion, THE Web_Interface SHALL return to the detail view without deleting

### Requirement 6: Dynamic Block Selector Interface

**User Story:** As a player, I want an intuitive interface for selecting blocks, so that I can quickly build my construction plan without confusion.

#### Acceptance Criteria

1. THE Dynamic_Selector SHALL provide a searchable dropdown or autocomplete for block selection
2. WHEN a user types in the search field, THE Dynamic_Selector SHALL filter blocks by name in real-time
3. WHEN a user selects a block, THE Dynamic_Selector SHALL add it to the selected blocks list
4. THE Dynamic_Selector SHALL prevent adding the same block multiple times
5. WHEN a block is added, THE Dynamic_Selector SHALL provide a quantity input field with default value of 1
6. WHEN a user clicks remove, THE Dynamic_Selector SHALL remove the block from the selected list
7. THE Dynamic_Selector SHALL validate that quantities are positive integers
8. THE Dynamic_Selector SHALL display block names clearly in the selected list

### Requirement 7: Live Calculation Preview

**User Story:** As a player, I want to see resource calculations update in real-time as I add blocks, so that I can make informed decisions about my build order.

#### Acceptance Criteria

1. WHEN a user adds or removes a block, THE Live_Preview SHALL update the total mass display
2. WHEN a user changes a block quantity, THE Live_Preview SHALL recalculate and display updated totals
3. THE Live_Preview SHALL display the total number of blocks in the build order
4. THE Live_Preview SHALL display the total number of unique components required
5. THE Live_Preview SHALL display the total number of unique ores required
6. THE Live_Preview SHALL update calculations via AJAX without page reload
7. WHEN calculations are in progress, THE Live_Preview SHALL display a loading indicator
8. WHEN calculation errors occur, THE Live_Preview SHALL display an error message

### Requirement 8: Form Validation

**User Story:** As a player, I want clear validation feedback, so that I can correct errors and successfully create or update build orders.

#### Acceptance Criteria

1. WHEN a user submits a form without a name, THE Web_Interface SHALL display an error message
2. WHEN a user submits a form without any blocks, THE Web_Interface SHALL display an error message
3. WHEN a user enters a quantity less than 1, THE Web_Interface SHALL display an error message
4. WHEN a user enters a non-integer quantity, THE Web_Interface SHALL display an error message
5. WHEN a user references a non-existent block UUID, THE Web_Interface SHALL display an error message
6. THE Web_Interface SHALL display validation errors next to the relevant form fields
7. THE Web_Interface SHALL preserve user input when displaying validation errors
8. WHEN all validation passes, THE Web_Interface SHALL save the BuildOrder successfully

### Requirement 9: Responsive Design

**User Story:** As a player, I want the interface to work on different screen sizes, so that I can manage build orders on desktop, tablet, or mobile devices.

#### Acceptance Criteria

1. THE Web_Interface SHALL use Bootstrap 5 responsive grid system
2. WHEN viewed on mobile devices, THE Web_Interface SHALL stack form elements vertically
3. WHEN viewed on tablets, THE Web_Interface SHALL optimize layout for medium screens
4. WHEN viewed on desktop, THE Web_Interface SHALL utilize full screen width efficiently
5. THE Web_Interface SHALL ensure buttons and interactive elements are touch-friendly on mobile
6. THE Web_Interface SHALL maintain readability of tables and lists on all screen sizes

### Requirement 10: Navigation and User Experience

**User Story:** As a player, I want intuitive navigation between views, so that I can efficiently manage my build orders.

#### Acceptance Criteria

1. THE Web_Interface SHALL provide a "Create Build Order" button on the list view
2. THE Web_Interface SHALL provide "Edit" and "Delete" buttons on the detail view
3. THE Web_Interface SHALL provide a "Back to List" link on all views
4. THE Web_Interface SHALL display success messages after create, update, or delete operations
5. THE Web_Interface SHALL display error messages when operations fail
6. THE Web_Interface SHALL use consistent styling with existing ores, components, and blocks apps
7. THE Web_Interface SHALL include breadcrumb navigation showing current location

### Requirement 11: Performance and Caching

**User Story:** As a player, I want fast page loads and calculations, so that I can work efficiently without waiting.

#### Acceptance Criteria

1. THE Web_Interface SHALL cache calculation results for 5 minutes
2. WHEN a BuildOrder is updated, THE Web_Interface SHALL invalidate the cache for that BuildOrder
3. THE Web_Interface SHALL use database query optimization to avoid N+1 queries
4. WHEN loading the detail view, THE Web_Interface SHALL prefetch related blocks, components, and ores
5. THE Web_Interface SHALL load the list view in under 2 seconds for up to 100 BuildOrders
6. THE Web_Interface SHALL load the detail view in under 3 seconds for BuildOrders with up to 50 blocks

### Requirement 12: Data Integrity

**User Story:** As a system administrator, I want data validation at all levels, so that the database maintains referential integrity.

#### Acceptance Criteria

1. THE Web_Interface SHALL validate that all block UUIDs exist in the database before saving
2. THE Web_Interface SHALL validate that all quantities are positive integers before saving
3. THE Web_Interface SHALL call the BuildOrder model's clean() method before saving
4. WHEN validation fails, THE Web_Interface SHALL prevent saving and display errors
5. THE Web_Interface SHALL use Django's transaction management to ensure atomic saves
6. THE Web_Interface SHALL handle database errors gracefully and display user-friendly messages

### Requirement 13: URL Routing and RESTful Design

**User Story:** As a developer, I want clean, RESTful URLs, so that the application is maintainable and follows Django best practices.

#### Acceptance Criteria

1. THE Web_Interface SHALL use the URL pattern `/buildorders/` for the list view
2. THE Web_Interface SHALL use the URL pattern `/buildorders/<uuid>/` for the detail view
3. THE Web_Interface SHALL use the URL pattern `/buildorders/create/` for the create view
4. THE Web_Interface SHALL use the URL pattern `/buildorders/<uuid>/update/` for the update view
5. THE Web_Interface SHALL use the URL pattern `/buildorders/<uuid>/delete/` for the delete view
6. THE Web_Interface SHALL use the app namespace `buildorders` for all URL names
7. THE Web_Interface SHALL use UUIDv7 format for all BuildOrder identifiers in URLs

### Requirement 14: Template Consistency

**User Story:** As a player, I want a consistent look and feel across all pages, so that the application is easy to learn and use.

#### Acceptance Criteria

1. THE Web_Interface SHALL extend the base.html template for all BuildOrder views
2. THE Web_Interface SHALL use Bootstrap 5 classes for styling
3. THE Web_Interface SHALL follow the same layout patterns as ores, components, and blocks apps
4. THE Web_Interface SHALL use consistent button styles (primary, secondary, danger)
5. THE Web_Interface SHALL use consistent table formatting for lists
6. THE Web_Interface SHALL use consistent card layouts for detail views
7. THE Web_Interface SHALL include consistent page titles and headings

### Requirement 15: JavaScript Functionality

**User Story:** As a player, I want smooth, interactive features, so that managing blocks feels responsive and modern.

#### Acceptance Criteria

1. THE Dynamic_Selector SHALL use vanilla JavaScript or minimal jQuery
2. THE Dynamic_Selector SHALL handle block addition without page reload
3. THE Dynamic_Selector SHALL handle block removal without page reload
4. THE Dynamic_Selector SHALL handle quantity changes without page reload
5. THE Live_Preview SHALL make AJAX requests to calculate totals
6. THE Live_Preview SHALL debounce calculation requests to avoid excessive server calls
7. THE Web_Interface SHALL degrade gracefully when JavaScript is disabled
8. THE Web_Interface SHALL provide clear feedback for all JavaScript interactions

### Requirement 16: Testing Coverage

**User Story:** As a developer, I want comprehensive test coverage, so that the feature is reliable and maintainable.

#### Acceptance Criteria

1. THE test suite SHALL achieve at least 85% code coverage for the buildorders app
2. THE test suite SHALL include unit tests for all view classes
3. THE test suite SHALL include integration tests for the complete CRUD workflow
4. THE test suite SHALL test form validation for all error conditions
5. THE test suite SHALL test the Dynamic_Selector JavaScript functionality
6. THE test suite SHALL test cache invalidation on BuildOrder updates
7. THE test suite SHALL test pagination, search, and sorting functionality
8. THE test suite SHALL use pytest-django framework and follow project conventions
