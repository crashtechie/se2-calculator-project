# Enhancement Request: Create Blocks App and Model

**Filename:** `inReview-enh0000003-create-blocks-app-model.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000003  
**Status:** inReview  
**Priority:** High  
**Created Date:** 2026-01-20  
**Updated Date:** 2026-01-20  
**Assigned To:**  
**Estimated Effort:** 8 hours  
**Revision:** 1.2 (Updated with technical specs alignment and consistency improvements)  

---

## Summary

Create the blocks Django app with Block model including complex fields for components, power, and storage.

---

## Description

Implement the blocks app as part of Phase 1 database setup. This app manages block data including component requirements, health, PCU, power consumption/production, and storage capacity. Blocks are the final buildable items in Space Engineers 2.

The Block model is the most complex, requiring validation for consumer/producer logic and JSONField for component recipes. This enhancement completes the three-tier resource calculation system (ores → components → blocks).

---

## Current Behavior

The blocks app does not exist in the project.

---

## Proposed Behavior

- Django app `blocks` created and registered in settings
- Block model with UUIDv7 primary keys and extensive fields
- JSONField for component requirements with validation
- Consumer/producer validation logic
- Admin interface with formatted displays
- Migrations applied successfully

---

## Acceptance Criteria

- [ ] Blocks app created via `python manage.py startapp blocks`
- [ ] App registered in `se2CalcProject/settings.py` INSTALLED_APPS
- [ ] Block model defined with all required fields
- [ ] UUIDv7 primary key using named function (not lambda)
- [ ] Consumer/producer validation implemented (validate_consumer, validate_producer)
- [ ] JSONField validation for components implemented (validate_components)
- [ ] Component relationship helper implemented (get_component_objects)
- [ ] Admin interface displays blocks with formatted JSON (custom display methods)
- [ ] Migrations created and applied
- [ ] Comprehensive test suite created (45+ tests minimum)
- [ ] All tests pass (100% pass rate)
- [ ] Documentation updated

---

## Technical Details

### Dependencies
- uuid-utils library for UUIDv7 support
- Django 6.0.1 (includes JSONField)
- ENH-0000002 (Components app must exist first)

### Affected Components
- blocks app (new)
- se2CalcProject/settings.py

### Files to Modify/Create
- `blocks/__init__.py`
- `blocks/models.py`
- `blocks/admin.py`
- `blocks/apps.py`
- `blocks/migrations/0001_initial.py`
- `se2CalcProject/settings.py`

### Database Changes
- [x] Migrations required
- [x] New models
- [ ] Schema changes

---

## Implementation Plan

### Step 1: Create Django App
Run `uv run python manage.py startapp blocks` and register in INSTALLED_APPS

### Step 2: Define Block Model
Create model with:
- `block_id` UUIDv7 primary key using `generate_uuid()` named function
- Base fields: name, description, mass, health, pcu, snap_size, input_mass, output_mass (all with help_text)
- Components JSONField with `default=list` (array format per technical specs)
- Consumer fields: consumer_type (blank=True), consumer_rate (default=0.0)
- Producer fields: producer_type (blank=True), producer_rate (default=0.0)
- Storage: storage_capacity (default=0.0)
- Timestamps: created_at, updated_at
- Meta: ordering=['name'], verbose_name='Block', verbose_name_plural='Blocks', db_table='blocks_block'

### Step 3: Add Validation Helper Methods
Implement:
- `validate_components()` - validates component_id references and quantities
- `validate_consumer()` - validates consumer_type requires consumer_rate > 0
- `validate_producer()` - validates producer_type requires producer_rate > 0
- `get_component_objects()` - returns Component queryset for this block
- `clean()` - calls all validation methods
- Override `save()` - calls clean() before saving

### Step 4: Configure Admin
Register Block model with:
- list_display: name, health, pcu, mass, components_preview, consumer_info, producer_info, created_at
- search_fields: name, description, consumer_type, producer_type
- list_filter: consumer_type, producer_type, created_at, updated_at
- readonly_fields: block_id, created_at, updated_at, components_formatted, component_objects, validation_status
- Custom display methods: components_preview, components_formatted, component_objects, validation_status, consumer_info, producer_info
- Fieldsets:
  - Basic Information: name, description, mass
  - Block Properties: health, pcu, snap_size, input_mass, output_mass
  - Components & Production: components, components_formatted, component_objects
  - Power & Resources: consumer_type, consumer_rate, producer_type, producer_rate, storage_capacity
  - Validation: validation_status (collapsed)
  - System Information: block_id, created_at, updated_at (collapsed)

### Step 5: Create Comprehensive Test Suite
Create 45+ tests organized into:
- BlockModelCreationTests
- BlockFieldValidationTests
- BlockTimestampTests
- BlockComponentsJSONFieldTests
- BlockConsumerValidationTests
- BlockProducerValidationTests
- BlockComponentRelationshipTests
- BlockMetaTests
- BlockIntegrationTests

### Step 6: Create and Apply Migrations
Generate and apply migrations to database

---

## Testing Requirements

### Automated Test Suite (45+ tests minimum)

**BlockModelCreationTests (7 tests)**
- [ ] Test block creation with all fields
- [ ] Test block creation with minimal fields
- [ ] Test __str__ method
- [ ] Test UUID generation
- [ ] Test UUID uniqueness
- [ ] Test UUID time-ordering
- [ ] Test block with complex field combinations

**BlockFieldValidationTests (8 tests)**
- [ ] Test unique name constraint
- [ ] Test name max_length
- [ ] Test description can be blank
- [ ] Test consumer_type can be blank
- [ ] Test producer_type can be blank
- [ ] Test numeric field values (mass, health, pcu, etc.)
- [ ] Test storage_capacity default
- [ ] Test consumer/producer rate defaults

**BlockTimestampTests (5 tests)**
- [ ] Test created_at auto-populated
- [ ] Test updated_at auto-populated
- [ ] Test timestamps match on creation
- [ ] Test updated_at changes on save
- [ ] Test created_at immutable

**BlockComponentsJSONFieldTests (5 tests)**
- [ ] Test components default empty dict
- [ ] Test components stores single component
- [ ] Test components stores multiple components
- [ ] Test components persist after save
- [ ] Test components can be updated

**BlockConsumerValidationTests (5 tests)**
- [ ] Test consumer_type without rate fails validation
- [ ] Test consumer_type with rate passes validation
- [ ] Test consumer_rate without type is valid
- [ ] Test consumer_rate zero with type fails
- [ ] Test consumer_rate negative fails

**BlockProducerValidationTests (5 tests)**
- [ ] Test producer_type without rate fails validation
- [ ] Test producer_type with rate passes validation
- [ ] Test producer_rate without type is valid
- [ ] Test producer_rate zero with type fails
- [ ] Test producer_rate negative fails

**BlockComponentRelationshipTests (4 tests)**
- [ ] Test get_component_objects single component
- [ ] Test get_component_objects multiple components
- [ ] Test get_component_objects empty components
- [ ] Test get_component_objects preserves quantities

**BlockMetaTests (4 tests)**
- [ ] Test blocks ordered by name
- [ ] Test verbose_name singular
- [ ] Test verbose_name plural
- [ ] Test db_table name

**BlockIntegrationTests (6 tests)**
- [ ] Test complete block creation workflow
- [ ] Test bulk block creation
- [ ] Test block update preserves relationships
- [ ] Test block with consumer and producer
- [ ] Test block with storage capacity
- [ ] Test block deletion does not affect components

**Total: 49 tests minimum**

### Manual Testing
- [ ] Create block via Django shell with all field types
- [ ] Create power consumer block
- [ ] Create power producer block
- [ ] Create storage block
- [ ] Create block with both consumer and producer
- [ ] Verify all fields display correctly in admin
- [ ] Verify validation status shows in admin

---

## Documentation Updates

- [ ] CHANGELOG.md
- [ ] Phase 1 checklist
- [ ] ENH-0000003-deployment-guide.md (following ENH-0000002 template)
- [ ] ENH-0000003-post-deployment-review.md
- [ ] ENH-0000003-test-documentation.md
- [ ] JSONField format documentation for frontend
- [ ] Consumer/producer validation rules documentation

---

## Risks and Considerations

- Risk: Complex validation logic may have edge cases - Mitigation: Comprehensive test coverage
- Risk: Component references in JSON not enforced by database - Mitigation: Application-level validation required
- Risk: Optional field combinations may be confusing - Mitigation: Clear documentation and admin help text

---

## Alternatives Considered

### Alternative 1: Separate BlockComponent model
Not chosen to keep initial implementation simple; can refactor later if needed

### Alternative 2: Separate models for consumer/producer blocks
Not chosen because many blocks have both capabilities

---

## Related Issues/Enhancements

- ENH-0000001: Create Ores App and Model
- ENH-0000002: Create Components App and Model (dependency)

---

## Notes

### Model Fields (Following ENH-0000001/0000002 Patterns)

**Primary Key:**
- block_id: UUIDv7, primary key, default=generate_uuid (named function, not lambda)

**Basic Information:**
- name: CharField(max_length=100), unique=True, required
  - help_text: "Unique name of the block (e.g., 'Large Reactor', 'Small Thruster')"
- description: TextField, blank=True
  - help_text: "Detailed description of the block and its uses"
- mass: FloatField, required
  - help_text: "Total mass of the block in kilograms"

**Components:**
- components: JSONField, default=list, blank=True
  - Format: `[{"component_id": "uuid", "component_name": "name", "quantity": int}, ...]`
  - Note: Using array format per technical specs (includes component names for frontend)
  - help_text: "JSON array of component requirements with IDs, names, and quantities"

**Block Properties:**
- health: FloatField, required
  - help_text: "Block health/integrity points"
- pcu: IntegerField, required
  - help_text: "Performance Cost Units (PCU) for this block"
- snap_size: FloatField, required
  - help_text: "Grid snap size for placement"
- input_mass: IntegerField, required
  - help_text: "Input mass capacity in kg"
- output_mass: IntegerField, required
  - help_text: "Output mass capacity in kg"

**Consumer Fields:**
- consumer_type: CharField(max_length=50), blank=True
  - help_text: "Type of resource consumed (e.g., 'Power', 'Hydrogen', 'Oxygen')"
- consumer_rate: FloatField, default=0.0
  - help_text: "Consumption rate per second"

**Producer Fields:**
- producer_type: CharField(max_length=50), blank=True
  - help_text: "Type of resource produced (e.g., 'Power', 'Hydrogen', 'Oxygen')"
- producer_rate: FloatField, default=0.0
  - help_text: "Production rate per second"

**Storage:**
- storage_capacity: FloatField, default=0.0
  - help_text: "Storage capacity in liters or units"

**Timestamps:**
- created_at: DateTimeField, auto_now_add=True
  - help_text: "Timestamp when the block was created"
- updated_at: DateTimeField, auto_now=True
  - help_text: "Timestamp when the block was last updated"

**Meta Configuration:**
- ordering: ['name']
- verbose_name: 'Block'
- verbose_name_plural: 'Blocks'
- db_table: 'blocks_block'

### Validation Rules
- If consumer_type is set (not empty), consumer_rate must be > 0
- If producer_type is set (not empty), producer_rate must be > 0
- All component_ids in components array must reference valid Component objects
- All quantities in components array must be positive integers
- Each component entry must have: component_id, component_name, quantity keys

### Validation Helper Methods
- `validate_components()` - Returns (is_valid, errors) tuple
- `validate_consumer()` - Returns (is_valid, errors) tuple
- `validate_producer()` - Returns (is_valid, errors) tuple
- `get_component_objects()` - Returns Component queryset
- `clean()` - Calls all validation methods, raises ValidationError if invalid
- `save()` - Overridden to call clean() before saving

### Admin Display Methods
- `components_preview(obj)` - Shows component count in list view
- `components_formatted(obj)` - Shows formatted JSON in detail view
- `component_objects(obj)` - Shows component names with quantities
- `validation_status(obj)` - Shows validation results with errors
- `consumer_info(obj)` - Shows consumer type and rate
- `producer_info(obj)` - Shows producer type and rate

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-20 | inReview | Initial creation |
| 2026-01-20 | inReview | Updated based on ENH-0000001/0000002 lessons learned |
| 2026-01-20 | inReview | Updated with technical specs alignment (array format) and consistency improvements |

---

## Sign-off

**Reviewed By:**  
**Approved By:**  
**Completed By:**  
**Completion Date:**
