---
inclusion: manual
description: Comprehensive code review checklist covering quality, testing, security, and best practices
---

# Code Review Checklist

Use this checklist when reviewing code changes or before submitting pull requests.

## General Code Quality

### Readability
- [ ] Code is self-documenting with clear variable/function names
- [ ] Complex logic has explanatory comments
- [ ] No commented-out code (use git history instead)
- [ ] Consistent formatting (Black/Ruff applied)
- [ ] No unnecessary complexity or over-engineering

### Maintainability
- [ ] Functions are small and focused (single responsibility)
- [ ] No code duplication (DRY principle)
- [ ] Magic numbers replaced with named constants
- [ ] Error messages are clear and actionable
- [ ] Code follows project conventions and patterns

## Python & Django Specific

### Type Safety
- [ ] Type hints added for function signatures
- [ ] Type hints added for class attributes
- [ ] Complex types properly annotated (List, Dict, Optional, etc.)
- [ ] mypy passes without errors

### Django Best Practices
- [ ] Models use appropriate field types
- [ ] Model methods contain business logic (not views)
- [ ] Views are thin (delegate to models/services)
- [ ] Forms handle validation properly
- [ ] QuerySets use select_related/prefetch_related where needed
- [ ] No N+1 query problems

### Database
- [ ] Migrations created for model changes
- [ ] Migrations reviewed and tested
- [ ] Database indexes added for frequently queried fields
- [ ] Foreign keys have appropriate on_delete behavior
- [ ] JSONField usage is justified and documented

## Testing

### Test Coverage
- [ ] New code has corresponding tests
- [ ] Tests cover happy path scenarios
- [ ] Tests cover edge cases and error conditions
- [ ] Coverage meets minimum threshold (80%+)
- [ ] All tests pass locally

### Test Quality
- [ ] Tests are independent and can run in any order
- [ ] Test names clearly describe what is being tested
- [ ] Tests use appropriate fixtures
- [ ] Mocks are used for external dependencies
- [ ] Tests are fast (<1s for unit tests)

### Test Organization
- [ ] Tests are in appropriate test files
- [ ] Related tests grouped in test classes
- [ ] Test data setup uses fixtures or factories
- [ ] No test code duplication

## Security

### Input Validation
- [ ] All user inputs are validated
- [ ] Form validation uses Django forms
- [ ] SQL injection prevented (using ORM)
- [ ] XSS prevented (template auto-escaping)
- [ ] CSRF protection enabled for forms

### Authentication & Authorization
- [ ] Views check user permissions
- [ ] Sensitive operations require authentication
- [ ] Authorization logic is tested
- [ ] No hardcoded credentials

### Data Protection
- [ ] Sensitive data not logged
- [ ] No secrets in code or version control
- [ ] Environment variables used for configuration
- [ ] Personal data handling follows privacy requirements

## Performance

### Database Optimization
- [ ] Queries are efficient (no N+1 problems)
- [ ] Appropriate use of select_related/prefetch_related
- [ ] Database indexes added where beneficial
- [ ] Pagination used for large datasets
- [ ] Expensive queries cached when appropriate

### Code Efficiency
- [ ] No unnecessary loops or iterations
- [ ] Appropriate data structures used
- [ ] Caching used for expensive operations
- [ ] No premature optimization (profile first)

## Documentation

### Code Documentation
- [ ] Public functions have docstrings
- [ ] Complex algorithms explained
- [ ] API endpoints documented
- [ ] Model fields have help_text where appropriate

### Project Documentation
- [ ] README updated if needed
- [ ] CHANGELOG updated with changes
- [ ] Migration notes added if required
- [ ] API documentation updated

## Error Handling

### Exception Management
- [ ] Exceptions are caught at appropriate levels
- [ ] Error messages are user-friendly
- [ ] Errors are logged with sufficient context
- [ ] No bare except clauses
- [ ] Custom exceptions used where appropriate

### Logging
- [ ] Appropriate log levels used (DEBUG, INFO, WARNING, ERROR)
- [ ] Sensitive data not logged
- [ ] Logs provide useful debugging information
- [ ] No excessive logging in hot paths

## Git & Version Control

### Commit Quality
- [ ] Commits are atomic and focused
- [ ] Commit messages are clear and descriptive
- [ ] No merge commits in feature branches
- [ ] Branch is up to date with main/develop

### Pull Request
- [ ] PR description explains what and why
- [ ] PR is reasonably sized (not too large)
- [ ] Related issues are linked
- [ ] Breaking changes are documented

## Deployment Considerations

### Configuration
- [ ] Environment-specific settings use environment variables
- [ ] No hardcoded URLs or paths
- [ ] Feature flags used for gradual rollouts
- [ ] Backward compatibility maintained

### Database Migrations
- [ ] Migrations are reversible when possible
- [ ] Data migrations tested with production-like data
- [ ] Migration performance considered for large tables
- [ ] Deployment order documented (migrations before code)

### Monitoring
- [ ] New features have appropriate logging
- [ ] Performance metrics considered
- [ ] Error tracking configured
- [ ] Health check endpoints updated if needed

## Accessibility (if UI changes)

- [ ] Semantic HTML used
- [ ] Forms have proper labels
- [ ] Images have alt text
- [ ] Color contrast meets WCAG standards
- [ ] Keyboard navigation works
- [ ] Screen reader tested (if critical)

## Browser Compatibility (if UI changes)

- [ ] Tested in target browsers
- [ ] Progressive enhancement applied
- [ ] Graceful degradation for older browsers
- [ ] Mobile responsive design

## Final Checks

- [ ] All CI checks pass
- [ ] No linting errors
- [ ] No type checking errors
- [ ] Code reviewed by at least one other developer
- [ ] Reviewer's comments addressed
- [ ] Ready to merge

## Notes for Reviewers

### What to Focus On
1. **Correctness**: Does the code do what it's supposed to do?
2. **Security**: Are there any security vulnerabilities?
3. **Performance**: Will this scale? Any obvious bottlenecks?
4. **Maintainability**: Can others understand and modify this code?
5. **Testing**: Is the code adequately tested?

### Review Etiquette
- Be constructive and specific in feedback
- Explain the "why" behind suggestions
- Distinguish between required changes and suggestions
- Acknowledge good code and improvements
- Ask questions rather than making demands
- Focus on the code, not the person

### When to Approve
- All critical issues resolved
- Tests pass and coverage is adequate
- Code meets project standards
- Documentation is sufficient
- No security concerns
