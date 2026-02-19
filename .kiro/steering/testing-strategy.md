---
inclusion: auto
fileMatchPattern: '**/test_*.py'
description: Testing strategy and best practices including TDD, test organization, fixtures, and coverage goals
---

# Testing Strategy & Best Practices

## Test-Driven Development (TDD)

### TDD Workflow
1. Write a failing test that defines desired behavior
2. Write minimal code to make the test pass
3. Refactor while keeping tests green
4. Repeat

### When to Use TDD
- Bug fixes: Always write a test that reproduces the bug first
- New features: Write tests for critical business logic
- Refactoring: Ensure existing tests pass before and after

## Test Organization

### Test File Structure
```python
# test_models.py
class TestModelName:
    """Group related model tests"""
    
    def test_model_creation_with_valid_data(self):
        """Test happy path"""
        pass
    
    def test_model_validation_with_invalid_data(self):
        """Test edge cases"""
        pass
```

### Test Naming Convention
- Format: `test_<what>_<condition>_<expected_result>`
- Examples:
  - `test_create_block_with_valid_components_succeeds`
  - `test_calculate_resources_with_zero_quantity_raises_error`
  - `test_delete_ore_with_dependencies_prevents_deletion`

## Test Categories

### Unit Tests
- Test individual functions/methods in isolation
- Mock external dependencies
- Fast execution (<1ms per test)
- Focus on business logic

### Integration Tests
- Test interactions between components
- Use real database (Django TestCase)
- Test model relationships and queries
- Verify form validation with database constraints

### Functional Tests
- Test complete user workflows
- Use Django test client
- Verify view logic and template rendering
- Test authentication and permissions

## Fixtures and Test Data

### Use pytest Fixtures
```python
@pytest.fixture
def sample_ore():
    """Reusable test data"""
    return Ore.objects.create(
        name="Iron Ore",
        mass=1.0,
        description="Basic ore"
    )

@pytest.fixture
def component_with_materials(sample_ore):
    """Fixture that depends on another"""
    return Component.objects.create(
        name="Steel Plate",
        materials={str(sample_ore.id): 3}
    )
```

### Factory Pattern
- Use factory_boy or model_bakery for complex objects
- Create factories for each model
- Use traits for variations

## Mocking Best Practices

### When to Mock
- External API calls
- File system operations
- Time-dependent code
- Expensive computations
- Third-party services

### Mock Examples
```python
from unittest.mock import patch, Mock

def test_api_call_with_mocked_response():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': 'test'}
        result = fetch_data()
        assert result == {'data': 'test'}
```

## Coverage Goals

### Minimum Coverage Targets
- Overall project: 80%
- Critical business logic: 95%
- Models: 90%
- Views: 85%
- Forms: 90%
- Utilities: 95%

### Coverage Exclusions
- Migration files
- Settings files
- `__init__.py` files
- Third-party code

## Django-Specific Testing

### Database Tests
```python
from django.test import TestCase

class ModelTestCase(TestCase):
    """Use TestCase for database tests"""
    
    def setUp(self):
        """Runs before each test"""
        self.ore = Ore.objects.create(name="Test Ore")
    
    def test_model_str_representation(self):
        assert str(self.ore) == "Test Ore"
```

### View Tests
```python
def test_list_view_returns_all_ores(client):
    """Use pytest-django client fixture"""
    Ore.objects.create(name="Ore 1")
    Ore.objects.create(name="Ore 2")
    
    response = client.get('/ores/')
    
    assert response.status_code == 200
    assert len(response.context['object_list']) == 2
```

### Form Tests
```python
def test_form_validation_with_invalid_data():
    form = OreForm(data={'name': '', 'mass': -1})
    
    assert not form.is_valid()
    assert 'name' in form.errors
    assert 'mass' in form.errors
```

## Performance Testing

### Query Optimization Tests
```python
from django.test.utils import override_settings
from django.db import connection
from django.test import TestCase

class QueryOptimizationTest(TestCase):
    def test_list_view_uses_select_related(self):
        """Verify N+1 queries are avoided"""
        with self.assertNumQueries(1):
            list(Block.objects.select_related('component').all())
```

### Load Testing Considerations
- Use locust or pytest-benchmark for load tests
- Test with realistic data volumes
- Measure response times under load
- Identify bottlenecks early

## Test Maintenance

### Keep Tests Fast
- Use pytest-xdist for parallel execution
- Mock slow operations
- Use in-memory SQLite for unit tests
- Minimize database operations

### Avoid Test Interdependence
- Each test should be independent
- Use fixtures for setup, not other tests
- Clean up after tests (Django does this automatically)

### Regular Test Review
- Remove obsolete tests
- Update tests when requirements change
- Refactor duplicated test code
- Keep test code as clean as production code

## Continuous Integration

### Pre-commit Checks
- Run tests locally before pushing
- Use pre-commit hooks for linting
- Verify coverage thresholds

### CI Pipeline
- Run full test suite on every push
- Generate coverage reports
- Fail builds on coverage drops
- Run linting and type checking

## Debugging Failed Tests

### Useful pytest Options
```bash
# Run specific test
pytest path/to/test_file.py::test_function_name

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run last failed tests
pytest --lf

# Verbose output
pytest -vv
```

### Django Test Debugging
```python
# Use Django's test client for debugging
response = client.get('/url/')
print(response.content.decode())  # See rendered HTML
print(response.context)  # See template context
```

## Property-Based Testing

### Use Hypothesis for Complex Logic
```python
from hypothesis import given
from hypothesis import strategies as st

@given(st.integers(min_value=1, max_value=1000))
def test_resource_calculation_with_any_quantity(quantity):
    """Test with generated inputs"""
    result = calculate_resources(quantity)
    assert result >= 0
    assert isinstance(result, int)
```

### When to Use Property-Based Testing
- Mathematical calculations
- Data transformations
- Parsing and serialization
- Edge case discovery

## Test Documentation

### Document Test Intent
```python
def test_build_order_calculates_total_mass():
    """
    Verify that BuildOrder.calculate_total_mass() correctly sums
    the mass of all components multiplied by their quantities.
    
    Given: A build order with 2 blocks, each requiring components
    When: calculate_total_mass() is called
    Then: The total mass equals sum of (component.mass * quantity)
    """
    pass
```

### Maintain Test README
- Document test setup requirements
- Explain complex test scenarios
- List known test limitations
- Provide troubleshooting guide
