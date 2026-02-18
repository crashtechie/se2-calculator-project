# Write Tests

Use this prompt to generate comprehensive tests following project standards.

## Test Coverage Requirements

- **Overall**: >80% code coverage
- **Critical Paths**: 100% coverage (calculations, validation)
- **Models**: All methods, properties, validation
- **Views**: All CRUD operations, edge cases
- **Forms**: Validation and error handling

## Test Structure

### File Organization
```
app/{app_name}/tests/
├── __init__.py
├── test_models.py
├── test_views.py
├── test_forms.py
└── test_utils.py
```

### Naming Conventions
- Test files: `test_*.py`
- Test classes: `Test{FeatureName}`
- Test methods: `test_{what_is_being_tested}`

## Test Types to Include

### 1. Model Tests
- [ ] Object creation with valid data
- [ ] String representation (`__str__`)
- [ ] Field validation (required, max_length, choices)
- [ ] Custom methods and properties
- [ ] JSONField data integrity
- [ ] Constraint validation
- [ ] Edge cases (empty, null, invalid)

### 2. View Tests
- [ ] GET requests return correct templates
- [ ] GET requests return correct context data
- [ ] POST requests create/update objects
- [ ] POST requests with invalid data show errors
- [ ] Redirects after successful POST
- [ ] Pagination works correctly
- [ ] Search/filtering functionality
- [ ] 404 for non-existent objects
- [ ] Permission checks (if applicable)

### 3. Integration Tests
- [ ] Full workflows (create → read → update → delete)
- [ ] Resource chain calculations
- [ ] Cache behavior
- [ ] Database transactions

## Test Template

```python
import pytest
from django.urls import reverse
from {app}.models import {Model}

@pytest.mark.django_db
class Test{Model}Model:
    def test_creation(self):
        """Test {model} can be created with valid data."""
        obj = {Model}.objects.create(
            name="Test Name",
            # ... other fields
        )
        assert obj.id is not None
        assert obj.name == "Test Name"
    
    def test_str_representation(self):
        """Test string representation."""
        obj = {Model}.objects.create(name="Test")
        assert str(obj) == "Test"
    
    def test_validation_error(self):
        """Test validation raises error for invalid data."""
        with pytest.raises(ValidationError):
            obj = {Model}(name="")
            obj.full_clean()

@pytest.mark.django_db
class Test{Model}Views:
    def test_list_view(self, client):
        """Test list view returns correct template."""
        response = client.get(reverse('{app}:{model}_list'))
        assert response.status_code == 200
        assert '{app}/{model}_list.html' in [t.name for t in response.templates]
    
    def test_create_view_post(self, client):
        """Test create view with valid POST data."""
        data = {'name': 'Test', 'description': 'Test desc'}
        response = client.post(reverse('{app}:{model}_create'), data)
        assert response.status_code == 302  # Redirect
        assert {Model}.objects.filter(name='Test').exists()
```

## Fixtures

Use pytest fixtures for reusable test data:

```python
@pytest.fixture
def sample_{model}():
    return {Model}.objects.create(
        name="Sample",
        # ... fields
    )

@pytest.fixture
def sample_{model}_list():
    return [
        {Model}.objects.create(name=f"Item {i}")
        for i in range(5)
    ]
```

## Running Tests

```bash
# All tests
uv run pytest --cov

# Specific file
uv run pytest app/{app}/tests/test_models.py

# Specific test
uv run pytest app/{app}/tests/test_models.py::Test{Model}::test_creation

# With verbose output
uv run pytest -v

# Generate HTML coverage report
uv run pytest --cov --cov-report=html
```

## Checklist

- [ ] All CRUD operations tested
- [ ] Validation logic tested
- [ ] Edge cases covered
- [ ] Fixtures used for test data
- [ ] Tests are independent
- [ ] Coverage >80%
- [ ] All tests pass
- [ ] No warnings or deprecations
