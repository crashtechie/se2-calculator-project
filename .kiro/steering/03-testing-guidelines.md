# Testing Guidelines

## Test Coverage Requirements

### Minimum Standards
- **Overall Coverage**: >80% across all apps
- **Critical Paths**: 100% coverage for resource calculations, data validation
- **Models**: Test all methods, properties, and validation logic
- **Views**: Test all CRUD operations and edge cases
- **Forms**: Test validation and error handling

## Test Organization

### File Structure
```
app_name/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_forms.py
│   └── test_utils.py
```

### Naming Conventions
- Test files: `test_*.py`
- Test classes: `Test{FeatureName}`
- Test methods: `test_{what_is_being_tested}`

## Fixtures

### Location
Store fixtures in `app_name/fixtures/`:
- `sample_ores.json`
- `sample_components.json`
- `sample_blocks.json`

### Usage
```python
@pytest.fixture
def sample_ore():
    return Ore.objects.create(
        name="Iron Ore",
        mass=1.0,
        description="Basic iron ore"
    )
```

### Loading Order
When loading fixtures, respect dependencies:
1. Ores (no dependencies)
2. Components (depends on Ores)
3. Blocks (depends on Components)
4. BuildOrders (depends on Blocks)

## Test Types

### Model Tests
- Creation and validation
- String representations
- Custom methods and properties
- JSONField data integrity
- Constraint validation

### View Tests
- GET requests return correct templates
- POST requests create/update objects
- Form validation errors display correctly
- Pagination works as expected
- Search and filtering functionality
- Permission checks (if applicable)

### Integration Tests
- Full resource chain calculations
- Cache invalidation on updates
- Multi-block build order totals
- Complex filtering scenarios

## Running Tests

### Basic Commands
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific app
uv run pytest ores/tests/

# Run specific test file
uv run pytest ores/tests/test_models.py

# Run specific test
uv run pytest ores/tests/test_models.py::TestOreModel::test_creation

# Run with verbose output
uv run pytest -v

# Run with print statements visible
uv run pytest -s
```

### Coverage Reports
```bash
# Generate HTML coverage report
uv run pytest --cov --cov-report=html

# View report
open htmlcov/index.html
```

## Best Practices

### Test Independence
- Each test should be independent
- Use fixtures or setUp/tearDown for test data
- Don't rely on test execution order
- Clean up after tests (pytest-django handles this automatically)

### Assertions
- Use descriptive assertion messages
- Test one concept per test method
- Use appropriate assertion methods:
  - `assert obj.field == expected`
  - `assert obj in queryset`
  - `assert response.status_code == 200`

### Mocking
- Mock external services and APIs
- Mock time-dependent operations
- Use `unittest.mock` or `pytest-mock`

### Test Data
- Use realistic but minimal test data
- Avoid hardcoding UUIDs (generate dynamically)
- Use factories for complex object creation (if needed)

## Continuous Integration

### GitHub Actions
Tests run automatically on:
- Push to main branch
- Pull request creation
- Pull request updates

### Pre-commit Checks
Consider running tests before committing:
```bash
# Add to .git/hooks/pre-commit
#!/bin/bash
uv run pytest --cov --cov-fail-under=80
```

## Debugging Failed Tests

### Common Issues
1. **Database state**: Ensure migrations are applied
2. **Fixture loading**: Check dependency order
3. **Cache pollution**: Clear cache between tests
4. **Time-dependent tests**: Mock datetime operations

### Debug Commands
```bash
# Run with pdb on failure
uv run pytest --pdb

# Show local variables on failure
uv run pytest -l

# Stop on first failure
uv run pytest -x
```
