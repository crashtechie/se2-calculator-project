# Code Review Checklist

Use this prompt to perform thorough code reviews following project standards.

## Code Quality

### Style & Formatting
- [ ] Follows PEP 8 guidelines
- [ ] Line length ≤88 characters
- [ ] Proper import organization (stdlib → third-party → local)
- [ ] Consistent naming conventions (PascalCase, snake_case, UPPER_SNAKE_CASE)
- [ ] No unused imports or variables
- [ ] Passes `ruff check` and `ruff format --check`

### Documentation
- [ ] Docstrings for all public methods/classes
- [ ] Complex logic has explanatory comments
- [ ] Comments explain "why" not "what"
- [ ] TODO/FIXME comments include username
- [ ] README/docs updated if needed

## Django-Specific

### Models
- [ ] Uses UUIDv7 for primary keys
- [ ] Includes `created_at`/`updated_at` timestamps
- [ ] Has meaningful `__str__()` method
- [ ] Validation in `clean()` method
- [ ] JSONField data properly structured
- [ ] Appropriate indexes defined
- [ ] Meta class properly configured

### Views
- [ ] Uses class-based views appropriately
- [ ] Implements `get_context_data()` for extra context
- [ ] Pagination configured (10 items default)
- [ ] Search/filtering implemented
- [ ] Proper use of `reverse_lazy()` for URLs
- [ ] No N+1 query problems

### Templates
- [ ] Extends `base.html`
- [ ] Includes `{% csrf_token %}` in forms
- [ ] Proper template tag spacing
- [ ] Responsive design (Bootstrap 5)
- [ ] Confirmation for delete operations
- [ ] Accessible (WCAG compliant)

### URLs
- [ ] Uses `app_name` for namespacing
- [ ] All patterns have descriptive names
- [ ] Follows RESTful conventions
- [ ] Logical grouping

## Testing

- [ ] Tests written for new functionality
- [ ] Coverage >80% for modified code
- [ ] All tests pass locally
- [ ] Edge cases covered
- [ ] Fixtures used appropriately
- [ ] No test warnings or deprecations

## Security

- [ ] No hardcoded secrets or credentials
- [ ] User input validated and sanitized
- [ ] CSRF protection enabled
- [ ] No SQL injection vulnerabilities
- [ ] Proper authentication/authorization
- [ ] Sensitive data not logged
- [ ] Dependencies up to date

## Performance

- [ ] No N+1 queries (use `select_related`/`prefetch_related`)
- [ ] Appropriate database indexes
- [ ] Caching used for expensive operations
- [ ] Efficient algorithms (no unnecessary loops)
- [ ] Bulk operations used where appropriate

## Database

- [ ] Migrations generated and tested
- [ ] Migration dependencies correct
- [ ] Reversible migrations
- [ ] No direct SQL unless necessary
- [ ] Fixtures updated if needed

## Documentation Updates

- [ ] CHANGELOG.md updated
- [ ] README.md updated (if needed)
- [ ] ENH document updated (if applicable)
- [ ] API documentation updated (if applicable)
- [ ] Inline code documentation adequate

## Git & Version Control

- [ ] Commit messages follow convention (`type(scope): subject`)
- [ ] Commits are logical and atomic
- [ ] No merge conflicts
- [ ] Branch name follows convention
- [ ] No sensitive files committed

## CI/CD

- [ ] All GitHub Actions workflows pass
- [ ] Test workflow succeeds
- [ ] Docker build workflow succeeds
- [ ] Lint workflow succeeds
- [ ] Coverage meets threshold
- [ ] No new security alerts

## Deployment Readiness

- [ ] Works in Docker environment
- [ ] Environment variables documented
- [ ] Static files collected properly
- [ ] Database migrations applied
- [ ] Health checks pass
- [ ] No breaking changes (or documented)

## Review Comments Template

### Blocking Issues (Must Fix)
- Issue description
- Why it's blocking
- Suggested fix

### Suggestions (Nice to Have)
- Improvement suggestion
- Rationale
- Example (if applicable)

### Questions
- Clarification needed
- Alternative approach consideration

### Praise
- What was done well
- Good patterns to highlight

## Final Checklist

- [ ] All blocking issues resolved
- [ ] Tests pass
- [ ] Documentation complete
- [ ] Ready to merge
