# Contributing to SE2 Calculator Project

## Getting Started

- Fork the repository
- Clone your fork locally
- Create a new branch for your changes
- Set up your development environment (see [Development Setup](#development-setup) below)

## Development Setup

### Prerequisites

- **Python**: 3.13+
- **uv**: 0.2.0+ (package manager)
- **PostgreSQL**: 13+ (for local database)
- **Docker & Docker Compose**: 20.10+ and 2.0+ (for local testing with containers)

### Local Development Environment

1. **Configure Python environment:**
   ```bash
   # Python venv is automatically created by uv
   uv sync
   ```

2. **Set up PostgreSQL locally or use Docker:**
   ```bash
   # Option A: Docker (recommended)
   docker run -d \
     --name se2_postgres \
     -e POSTGRES_USER=se2_user \
     -e POSTGRES_PASSWORD=password \
     -e POSTGRES_DB=se2_calculator_db \
     -p 5432:5432 \
     postgres:17
   
   # Option B: Use system PostgreSQL
   createdb -U postgres se2_calculator_db
   ```

3. **Create .env file:**
   ```bash
   cp .env.example .env
   # Update DB credentials to match your setup
   ```

4. **Run migrations:**
   ```bash
   uv run --env-file .env python manage.py migrate
   ```

5. **Run tests:**
   ```bash
   DJANGO_SETTINGS_MODULE=se2CalcProject.settings uv run --env-file .env python -m pytest
   ```

## Making Changes

### Code Style & Standards

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **Django**: Follow [Django coding style](https://docs.djangoproject.com/en/stable/internals/contributing/coding-style/)
- **Imports**: Use absolute imports; organize as `django` → third-party → local
- **Comments**: Use clear, concise docstrings (Google style)

### Testing Requirements

**All code changes MUST include tests and pass the full suite:**

1. **Unit Tests**
   - Create tests in `<app>/test_*.py` files
   - Test models, forms, views, and utilities
   - Aim for high branch coverage

2. **Test Execution** (using pytest + Django)
   ```bash
   # Run all tests with PostgreSQL
   DJANGO_SETTINGS_MODULE=se2CalcProject.settings uv run --env-file .env python -m pytest
   
   # Run specific app tests
   DJANGO_SETTINGS_MODULE=se2CalcProject.settings uv run --env-file .env python -m pytest blocks/
   
   # Run with coverage
   DJANGO_SETTINGS_MODULE=se2CalcProject.settings uv run --env-file .env coverage run -m pytest
   DJANGO_SETTINGS_MODULE=se2CalcProject.settings uv run --env-file .env coverage report
   ```

3. **Coverage Requirements**
   - **Minimum**: 80% total coverage
   - **Target**: >90% for views/forms, >85% for models
   - **Views/Forms**: Aim for 100% coverage
   - **Admin**: Optional (lower priority)
   - **Migrations**: Tested by `manage.py migrate`

4. **Database Setup for Tests**
   - Tests use PostgreSQL (from .env) via pytest-django
   - Transactions are rolled back after each test
   - Use `@pytest.mark.django_db` for tests accessing DB
   - Use `@pytest.mark.django_db(transaction=True)` for tests needing transaction context

5. **Performance Test Patterns**
   ```python
   import pytest
   
   @pytest.fixture
   def sample_data(db):
       """Create minimal test data using self-contained fixtures."""
       # Create only what this test needs
       return {"object": SomeModel.objects.create(...)}
   
   @pytest.mark.django_db(transaction=True)
   def test_something(sample_data):
       """Test with data fixture."""
       # Test code here
   ```

### Database Changes

**All database schema changes MUST use migrations:**

1. **Create migrations:**
   ```bash
   uv run --env-file .env python manage.py makemigrations --name <descriptive_name>
   ```

2. **PostgreSQL Compatibility** (ENH-0000008 requirement)
   - Use `RemoveField`, `AddField`, `AlterField` operations (not raw SQL when possible)
   - If raw SQL needed, ensure PostgreSQL 13+ compatibility
   - Avoid SQLite-specific syntax
   - Test migrations on PostgreSQL: `uv run --env-file .env python manage.py migrate`

3. **Migration Best Practices**
   - One logical change per migration
   - Write descriptive migration names
   - Avoid data migrations unless necessary
   - Always test on fresh database

### Logging (ENH-0000008)

When adding new logging:

1. **Use structured logging:**
   ```python
   import logging
   logger = logging.getLogger(__name__)
   
   logger.debug(f"BlockListView query: search='{search_query}', sort={sort_by}")
   logger.error(f"Failed to process block: {error}")
   ```

2. **Log levels:**
   - `DEBUG`: Development/diagnostic info (query counts, state changes)
   - `INFO`: Important application events
   - `WARNING`: Recoverable issues
   - `ERROR`: Errors that need attention (logged to persistent volume in production)

3. **Avoid logging sensitive data** (passwords, tokens, user PII)

### Security Headers (ENH-0000008)

When adding new views or modifying responses:

1. **Security headers are configured in nginx.conf** (production)
2. **For development/testing, verify:**
   - `X-Frame-Options: DENY`
   - `X-Content-Type-Options: nosniff`
   - `X-XSS-Protection: 1; mode=block`
   - `Content-Security-Policy` (if adding new external resources)

3. **CSRF Protection:**
   - All POST/PUT/DELETE views require `@csrf_protect` or use forms with `{% csrf_token %}`
   - Set `CSRF_COOKIE_SECURE=True` in production .env

### Docker Configuration (ENH-0000008)

If modifying Dockerfile, docker-compose.yml, or nginx.conf:

1. **Test locally:**
   ```bash
   docker compose build
   docker compose up
   # Verify services and test endpoints
   ```

2. **Best practices:**
   - Keep Dockerfile lean; use multi-stage builds if needed
   - Document any new environment variables in `.env.example`
   - Ensure all services have health checks
   - Volume mounts should persist logs, database, and static files

## Submitting Changes

1. **Before creating a PR:**
   - Run full test suite: `DJANGO_SETTINGS_MODULE=se2CalcProject.settings uv run --env-file .env python -m pytest`
   - Check coverage: `DJANGO_SETTINGS_MODULE=se2CalcProject.settings uv run --env-file .env coverage report` (≥80%)
   - Run migrations on clean database: `uv run --env-file .env python manage.py migrate`
   - Format code (follow PEP 8)

2. **Create a Pull Request:**
   - Push your changes to your fork
   - Title: `<scope>: <description>` (e.g., `blocks: add bulk import functionality`)
   - Description: Explain what changed and why
   - Link related issues: `Closes #123`

3. **PR Checklist:**
   - [ ] Tests written and passing (108 tests pass with 0 failures)
   - [ ] Coverage ≥80% for all new code
   - [ ] No pending migrations (or migrations included)
   - [ ] Documentation updated if needed
   - [ ] Code follows style guidelines
   - [ ] No hardcoded secrets or sensitive data
   - [ ] CONTRIBUTING.md updated if patterns change

## Code Review

- **Reviews are required before merging**
- Be open to feedback and constructive criticism
- Respond to review comments promptly
- Make requested changes in new commits (don't amend old ones)
- Resolve conversations once issues are addressed
- Request re-review after updates

## Reporting Issues

- **Search existing issues first** (use GitHub search)
- **For bugs:** Provide:
  - Clear reproduction steps
  - Expected vs. actual behavior
  - Error messages and stack traces
  - Your environment (OS, Python version, uv version, PostgreSQL version)
  - Test data (if applicable)

- **For feature requests:** Describe:
  - Use case and motivation
  - Proposed solution (if any)
  - Alternative approaches considered

## Documentation

- Update [README.md](README.md) for user-facing changes
- Update [CONTRIBUTING.md](CONTRIBUTING.md) (this file) for new development patterns
- Add docstrings to new functions/classes (Google style)
- Update deployment guide ([docs/enhancementRequests/Phase2_views/ENH0000008/ENH0000008_DEPLOYMENT_GUIDE.md](docs/enhancementRequests/Phase2_views/ENH0000008/ENH0000008_DEPLOYMENT_GUIDE.md)) if infrastructure changes

## Questions?

- Check existing [GitHub Issues](https://github.com/crashtechie/se2-calculator-project/issues)
- Start a [GitHub Discussion](https://github.com/crashtechie/se2-calculator-project/discussions)
- See [ENH-0000008 Deployment Guide](docs/enhancementRequests/Phase2_views/ENH0000008/ENH0000008_DEPLOYMENT_GUIDE.md) for infrastructure questions

Thank you for contributing to SE2 Calculator Project!