# Kiro Configuration

This directory contains Kiro agent steering files and skills for the Space Engineers 2 Calculator project.

## Directory Structure

```
.kiro/
├── steering/          # Context and guidelines automatically included
│   ├── python-django-best-practices.md
│   ├── code-review-checklist.md
│   ├── testing-strategy.md
│   ├── git-workflow.md
│   ├── performance-optimization.md
│   └── security-best-practices.md
├── skills/            # Specialized knowledge activated on demand
│   ├── test-driven-development.md
│   ├── debugging-techniques.md
│   └── refactoring-patterns.md
└── README.md          # This file
```

## Steering Files

Steering files provide context and guidelines that influence Kiro's behavior. They can be:
- **Always included** (default) - Loaded for every interaction
- **Conditionally included** - Loaded when specific files are accessed
- **Manually included** - Loaded when you reference them with `#`

### Available Steering Files

#### python-django-best-practices.md
- **Inclusion**: Auto (when Python files are accessed)
- **Purpose**: Core Python and Django development standards
- **Topics**: Code quality, testing, security, database, documentation

#### code-review-checklist.md
- **Inclusion**: Manual
- **Purpose**: Comprehensive checklist for code reviews
- **Topics**: Code quality, testing, security, performance, documentation
- **Usage**: Reference with `#code-review-checklist` when reviewing code

#### testing-strategy.md
- **Inclusion**: Auto (when test files are accessed)
- **Purpose**: Testing best practices and strategies
- **Topics**: TDD, test organization, fixtures, mocking, coverage

#### git-workflow.md
- **Inclusion**: Auto
- **Purpose**: Version control best practices
- **Topics**: Branch strategy, commit guidelines, PR process, Git commands

#### performance-optimization.md
- **Inclusion**: Manual
- **Purpose**: Performance tuning and optimization
- **Topics**: Database optimization, caching, profiling, load testing
- **Usage**: Reference with `#performance-optimization` when optimizing

#### security-best-practices.md
- **Inclusion**: Auto
- **Purpose**: Security guidelines and best practices
- **Topics**: Input validation, authentication, CSRF, XSS, secrets management

## Skills

Skills are specialized knowledge modules that can be activated when needed. They provide deep expertise in specific areas.

### Available Skills

#### test-driven-development.md
- **Purpose**: TDD methodology and workflow
- **Topics**: Red-Green-Refactor cycle, TDD for bug fixes, best practices
- **When to use**: Writing new features, fixing bugs, refactoring

#### debugging-techniques.md
- **Purpose**: Systematic debugging approaches
- **Topics**: Django debugging, Python debugger, profiling, troubleshooting
- **When to use**: Investigating bugs, performance issues, test failures

#### refactoring-patterns.md
- **Purpose**: Code refactoring patterns and techniques
- **Topics**: Code smells, refactoring patterns, Django-specific refactoring
- **When to use**: Improving code quality, reducing technical debt

#### database-query-optimization.md
- **Purpose**: Database query optimization and performance tuning
- **Topics**: N+1 queries, select_related, prefetch_related, indexes, bulk operations
- **When to use**: Optimizing slow queries, improving application performance

#### api-design-integration.md
- **Purpose**: RESTful API design and external API integration
- **Topics**: DRF patterns, serializers, viewsets, authentication, versioning
- **When to use**: Building APIs, integrating with external services

#### django-forms-validation.md
- **Purpose**: Django forms and complex validation logic
- **Topics**: ModelForms, formsets, custom validation, dynamic forms, file uploads
- **When to use**: Creating forms, implementing validation, handling file uploads

#### error-handling-logging.md
- **Purpose**: Error handling strategies and application logging
- **Topics**: Exception handling, custom exceptions, logging configuration, monitoring
- **When to use**: Implementing error handling, debugging production issues

#### data-migration-transformation.md
- **Purpose**: Data migrations and bulk data operations
- **Topics**: Django data migrations, bulk operations, import/export, data cleanup
- **When to use**: Migrating data, importing from external sources, data transformations

#### frontend-integration-patterns.md
- **Purpose**: Frontend JavaScript integration with Django
- **Topics**: AJAX, HTMX, Alpine.js, progressive enhancement, real-time updates
- **When to use**: Building interactive UIs, implementing AJAX functionality

## How to Use

### Automatic Inclusion
Most steering files are automatically included based on context:
```python
# When you open a Python file, python-django-best-practices.md is loaded
# When you open a test file, testing-strategy.md is also loaded
```

### Manual Inclusion
Reference steering files or skills explicitly:
```
# In chat
Can you review this code using #code-review-checklist?

# For performance work
Help me optimize this query using #performance-optimization
```

### Activating Skills
Skills can be activated by mentioning them or when Kiro detects relevant work:
```
# Explicit activation
Let's use TDD to implement this feature

# Kiro will automatically suggest skills when appropriate
```

## Customization

### Adding New Steering Files
1. Create a new `.md` file in `.kiro/steering/`
2. Add front-matter to control inclusion:
```markdown
---
inclusion: auto
fileMatchPattern: '**/*.py'
---

# Your Steering Content
```

### Adding New Skills
1. Create a new `.md` file in `.kiro/skills/`
2. Document when to activate and what it covers
3. Provide practical examples and guidelines

### Inclusion Options
- `inclusion: auto` - Always included
- `inclusion: fileMatch` + `fileMatchPattern: '**/*.py'` - Conditional
- `inclusion: manual` - Only when explicitly referenced

## Best Practices

### For Steering Files
- Keep them focused on specific domains
- Use clear, actionable guidelines
- Include examples and code snippets
- Update as project evolves

### For Skills
- Provide step-by-step workflows
- Include practical examples
- Document when to use
- Keep them comprehensive but focused

## Project-Specific Configuration

This configuration is tailored for:
- **Framework**: Django 6.0.1
- **Language**: Python 3.13+
- **Testing**: pytest-django
- **Database**: PostgreSQL (production), SQLite (development)
- **Deployment**: Docker Compose

## Maintenance

### Regular Updates
- Review steering files quarterly
- Update for new Django versions
- Add new patterns as discovered
- Remove outdated practices

### Version Control
- All steering files and skills are version controlled
- Changes should be reviewed like code
- Document significant changes in commit messages

## Resources

### Django Documentation
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)

### Python Resources
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Testing](https://docs.python.org/3/library/unittest.html)
- [Python Debugging](https://docs.python.org/3/library/pdb.html)

### Project Documentation
- [Project README](../README.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Enhancement Requests](../docs/enhancementRequests/)

## Support

For questions or suggestions about Kiro configuration:
1. Review existing steering files and skills
2. Check project documentation
3. Open an issue on GitHub
4. Discuss with the team

---

**Last Updated**: February 2026
**Maintained By**: Project Team
