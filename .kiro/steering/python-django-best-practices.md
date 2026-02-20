---
inclusion: auto
fileMatchPattern: '**/*.py'
description: Core Python and Django development standards covering code quality, testing requirements, security practices, and documentation
---

# Python & Django Development Best Practices

## Code Quality Standards

### Python Style
- Follow PEP 8 style guidelines
- Use type hints for function signatures and class attributes
- Maximum line length: 88 characters (Black formatter standard)
- Use meaningful variable and function names
- Prefer explicit over implicit code

### Django Conventions
- Follow Django's naming conventions for models, views, and templates
- Use Django's built-in features before custom solutions
- Keep views thin, models fat (business logic in models)
- Use Django ORM efficiently (select_related, prefetch_related)
- Always use Django's form validation

## Testing Requirements

### Test Coverage
- Maintain minimum 80% code coverage
- Write tests before fixing bugs (TDD for bug fixes)
- Test both happy paths and edge cases
- Use pytest fixtures for test data setup

### Test Organization
- Place tests in `test_*.py` files within each app
- Use descriptive test names: `test_<what>_<condition>_<expected>`
- Group related tests in test classes
- Use `conftest.py` for shared fixtures

### Django Testing Best Practices
- Use Django's TestCase for database tests
- Use pytest-django for modern test features
- Mock external services and APIs
- Test model methods, form validation, and view logic separately
- Use factory_boy or model_bakery for test data generation

## Security Practices

- Never commit secrets or credentials
- Use environment variables for configuration
- Validate and sanitize all user inputs
- Use Django's CSRF protection
- Keep dependencies updated (check for security vulnerabilities)
- Use Django's built-in authentication and authorization

## Database Best Practices

- Always create migrations for model changes
- Review migrations before applying
- Use database indexes for frequently queried fields
- Avoid N+1 queries (use select_related/prefetch_related)
- Use database transactions for related operations

## Code Review Checklist

Before submitting code:
- [ ] All tests pass
- [ ] Code follows style guidelines (ruff/black formatted)
- [ ] Type hints added for new functions
- [ ] Documentation updated if needed
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] Migrations created and tested
- [ ] Security considerations addressed

## Performance Considerations

- Profile before optimizing
- Use database indexes appropriately
- Cache expensive operations
- Optimize database queries
- Use pagination for large datasets
- Consider async views for I/O-bound operations

## Documentation Standards

- Add docstrings to all public functions and classes
- Use Google or NumPy docstring format
- Document complex business logic
- Keep README.md updated
- Document API endpoints and data models
