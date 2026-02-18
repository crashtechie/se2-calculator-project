# ENH-0000019: Core App - Validation Mixins & Utilities

**Status:** Planned  
**Phase:** 4 - Testing, Documentation & Core Infrastructure  
**Priority:** High  
**Dependencies:** None

## Overview

Create a `core` Django app containing reusable validation mixins, utility functions, and base classes used across the project. This reduces code duplication and provides a consistent foundation.

## Related Files

- Steering: `#[[file:.kiro/steering/01-django-standards.md]]`
- Code Style: `#[[file:.kiro/steering/05-code-style.md]]`
- Resource Chain: `#[[file:.kiro/steering/06-resource-chain.md]]`

## Requirements

### Functional Requirements
1. JSONField validation mixin
2. UUID validation utilities
3. Quantity validation mixin
4. Base model with common fields
5. Custom exceptions
6. Utility functions for calculations

### Non-Functional Requirements
1. Well-documented with docstrings
2. Comprehensive unit tests (>90% coverage)
3. Type hints throughout
4. No external dependencies beyond Django
5. Performance optimized

## Implementation Tasks

### 1. App Setup
- [ ] Create `app/core/` directory
- [ ] Initialize Django app: `python manage.py startapp core`
- [ ] Add to `INSTALLED_APPS`
- [ ] Create directory structure

### 2. Validation Mixins
- [ ] `JSONFieldValidationMixin` - Validate JSON structure
- [ ] `UUIDValidationMixin` - Validate UUID references
- [ ] `QuantityValidationMixin` - Validate positive integers
- [ ] `ResourceChainMixin` - Common resource calculation methods

### 3. Base Models
- [ ] `TimeStampedModel` - created_at, updated_at fields
- [ ] `UUIDModel` - UUIDv7 primary key
- [ ] `NamedModel` - name, description fields

### 4. Utility Functions
- [ ] `validate_uuid_exists(model, uuid)` - Check UUID exists
- [ ] `validate_positive_quantity(value)` - Validate quantity
- [ ] `aggregate_resources(resources_list)` - Sum resources
- [ ] `format_resource_display(resources)` - Format for display

### 5. Custom Exceptions
- [ ] `ValidationError` extensions
- [ ] `ResourceNotFoundError`
- [ ] `InvalidQuantityError`
- [ ] `CircularDependencyError`

### 6. Testing
- [ ] Unit tests for each mixin
- [ ] Unit tests for utilities
- [ ] Integration tests with existing models
- [ ] Edge case testing
- [ ] Achieve >90% coverage

## Acceptance Criteria

- [ ] Core app created and configured
- [ ] All mixins implemented and tested
- [ ] Utilities function correctly
- [ ] Existing apps refactored to use core
- [ ] Tests pass with >90% coverage
- [ ] Documentation complete

## Code Examples

### JSONFieldValidationMixin

```python
class JSONFieldValidationMixin:
    """Mixin for validating JSONField data."""
    
    def validate_json_structure(self, field_name, required_keys=None):
        """Validate JSON field has required structure."""
        data = getattr(self, field_name)
        if not isinstance(data, dict):
            raise ValidationError(f"{field_name} must be a dictionary")
        
        if required_keys:
            missing = set(required_keys) - set(data.keys())
            if missing:
                raise ValidationError(f"Missing keys: {missing}")
        
        return data
```

### UUIDValidationMixin

```python
class UUIDValidationMixin:
    """Mixin for validating UUID references."""
    
    def validate_uuid_references(self, field_name, model_class):
        """Validate all UUIDs in field reference existing objects."""
        data = getattr(self, field_name)
        uuids = data.keys() if isinstance(data, dict) else data
        
        existing = model_class.objects.filter(
            id__in=uuids
        ).values_list('id', flat=True)
        
        missing = set(uuids) - set(existing)
        if missing:
            raise ValidationError(
                f"Invalid {model_class.__name__} UUIDs: {missing}"
            )
```

### Base Models

```python
class TimeStampedModel(models.Model):
    """Abstract model with timestamp fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class UUIDModel(models.Model):
    """Abstract model with UUIDv7 primary key."""
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid7,
        editable=False
    )
    
    class Meta:
        abstract = True
```

## Directory Structure

```
app/core/
├── __init__.py
├── apps.py
├── mixins/
│   ├── __init__.py
│   ├── validation.py
│   └── resource_chain.py
├── models/
│   ├── __init__.py
│   └── base.py
├── utils/
│   ├── __init__.py
│   ├── validation.py
│   └── calculations.py
├── exceptions.py
└── tests/
    ├── __init__.py
    ├── test_mixins.py
    ├── test_models.py
    └── test_utils.py
```

## Refactoring Existing Code

After implementing core app, refactor existing models:

```python
# Before
class Block(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

# After
from core.models import UUIDModel, TimeStampedModel, NamedModel

class Block(UUIDModel, TimeStampedModel, NamedModel):
    # Only block-specific fields
    components = models.JSONField(default=dict)
```

## Implementation Notes

- Use abstract base classes for models
- Provide clear docstrings with examples
- Include type hints for all functions
- Keep utilities pure functions where possible
- Avoid circular imports
- Follow Django best practices

## Testing Strategy

```python
# Test mixin functionality
class TestJSONFieldValidationMixin(TestCase):
    def test_validate_json_structure_valid(self):
        # Test valid JSON structure
        pass
    
    def test_validate_json_structure_invalid(self):
        # Test invalid JSON structure
        pass

# Test utilities
class TestValidationUtils(TestCase):
    def test_validate_uuid_exists(self):
        # Test UUID validation
        pass
```

## References

- Django Model Mixins: https://docs.djangoproject.com/en/6.0/topics/db/models/#abstract-base-classes
- Type Hints: https://docs.python.org/3/library/typing.html
- Testing: `#[[file:.kiro/steering/03-testing-guidelines.md]]`
