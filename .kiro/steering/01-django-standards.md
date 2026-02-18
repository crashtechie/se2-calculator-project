# Django Development Standards

## Code Organization

### Models
- Use UUIDv7 for all primary keys via `uuid_utils.uuid7()`
- Include `created_at` and `updated_at` timestamps
- Add `__str__()` method returning meaningful representation
- Use JSONField for flexible nested data (components, materials)
- Add validation in `clean()` method
- Document complex fields with comments

### Views
- Use class-based views (ListView, DetailView, CreateView, UpdateView, DeleteView)
- Implement `get_context_data()` for additional template context
- Add pagination (default: 10 items per page)
- Include search and filtering capabilities
- Use `get_success_url()` with `reverse_lazy()`

### Templates
- Extend `base.html` for consistent layout
- Use template inheritance and includes
- Follow Bootstrap 5 conventions for styling
- Include CSRF tokens in all forms
- Add confirmation for delete operations
- Implement responsive design

### URLs
- Use `app_name` for namespacing
- Name all URL patterns descriptively
- Follow RESTful conventions where applicable
- Group related URLs logically

## Testing Requirements

### Coverage
- Maintain >80% code coverage across all apps
- Test all CRUD operations
- Test validation logic
- Test edge cases and error conditions

### Test Structure
- Use pytest-django framework
- Follow `test_*.py` naming convention
- Group tests by functionality
- Use fixtures for test data
- Mock external dependencies

### Test Types
- **Unit tests**: Individual functions/methods
- **Integration tests**: Multiple components working together
- **View tests**: HTTP requests and responses
- **Model tests**: Database operations and validation

## Documentation

### Code Comments
- Document complex algorithms
- Explain non-obvious business logic
- Add docstrings to all public methods
- Use type hints where beneficial

### Enhancement Requests
- Create ENH document in `docs/enhancementRequests/`
- Follow template structure
- Include acceptance criteria
- Document implementation details
- Update CHANGELOG.md upon completion

## Performance

### Database
- Use `select_related()` and `prefetch_related()` to avoid N+1 queries
- Add database indexes for frequently queried fields
- Use `only()` and `defer()` for large querysets

### Caching
- Cache expensive calculations (5-minute TTL default)
- Use Django's cache framework
- Invalidate cache on data updates
- Document cache keys and TTL values

## Security

### Best Practices
- Never commit secrets or API keys
- Use environment variables for configuration
- Validate all user input
- Sanitize data before display
- Use Django's built-in CSRF protection
- Keep dependencies updated
