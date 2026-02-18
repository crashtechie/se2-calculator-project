# CI/CD & GitHub Actions

## Workflow Overview

The project uses three main GitHub Actions workflows:

### 1. Test Workflow (`.github/workflows/test.yml`)
- Runs on: Push to main, pull requests
- Python versions: 3.13
- Database: PostgreSQL 17
- Coverage: Uploads to Codecov
- Badge: [![Tests](badge-url)](workflow-url)

### 2. Docker Build Workflow (`.github/workflows/docker.yml`)
- Runs on: Push to main, pull requests
- Builds: web, nginx, database containers
- Tests: Health checks for all services
- Validates: Docker Compose configuration

### 3. Lint Workflow (`.github/workflows/lint.yml`)
- Runs on: Push to main, pull requests
- Tools: Ruff (linting and formatting)
- Checks: Code quality, style compliance

## Workflow Best Practices

### Test Workflow
```yaml
# Key requirements:
- Use PostgreSQL service container
- Set DATABASE_URL environment variable
- Run migrations before tests
- Generate coverage reports
- Upload to Codecov with token
```

### Docker Workflow
```yaml
# Key requirements:
- Build all services (web, nginx, database)
- Wait for health checks to pass
- Test health endpoints
- Verify static file serving
- Check database connectivity
```

### Lint Workflow
```yaml
# Key requirements:
- Install Ruff via UV
- Run: uv run ruff check .
- Run: uv run ruff format --check .
- Fail on any violations
```

## Environment Variables for CI

### Required Secrets
- `CODECOV_TOKEN` - For coverage uploads
- `GITHUB_TOKEN` - Automatically provided

### Workflow Environment Variables
```yaml
env:
  DEBUG: false
  SECRET_KEY: test-secret-key-for-ci
  DB_NAME: test_se2_calculator
  DB_USER: postgres
  DB_PASSWORD: postgres
  DB_HOST: localhost
  DB_PORT: 5432
```

## Troubleshooting Common Issues

### Test Failures

**Database Connection Issues**
```bash
# Check PostgreSQL service is running
# Verify DATABASE_URL format
# Ensure migrations run before tests
```

**Import Errors**
```bash
# Verify PYTHONPATH includes app directory
# Check all dependencies in pyproject.toml
# Ensure UV sync runs before tests
```

**Coverage Upload Failures**
```bash
# Verify CODECOV_TOKEN is set
# Check coverage.xml is generated
# Ensure codecov action version is current
```

### Docker Build Failures

**Health Check Timeouts**
```bash
# Increase timeout values
# Check container logs for errors
# Verify health endpoints are accessible
# Ensure database is ready before web starts
```

**Static Files Not Found**
```bash
# Run collectstatic in Dockerfile
# Verify volume mounts in docker-compose.yml
# Check nginx configuration paths
# Ensure STATIC_ROOT is correct
```

**Database Connection Refused**
```bash
# Wait for database health check
# Verify DB_HOST=database in .env
# Check database service is defined
# Ensure network connectivity between containers
```

### Lint Failures

**Ruff Check Failures**
```bash
# Run locally: uv run ruff check .
# Auto-fix: uv run ruff check --fix .
# Review specific violations
```

**Format Check Failures**
```bash
# Run locally: uv run ruff format .
# Check: uv run ruff format --check .
# Commit formatted files
```

## Badge Maintenance

### Updating Badge URLs
```markdown
[![Tests](https://github.com/USER/REPO/actions/workflows/test.yml/badge.svg)](https://github.com/USER/REPO/actions/workflows/test.yml)
[![Docker Build](https://github.com/USER/REPO/actions/workflows/docker.yml/badge.svg)](https://github.com/USER/REPO/actions/workflows/docker.yml)
[![Code Quality](https://github.com/USER/REPO/actions/workflows/lint.yml/badge.svg)](https://github.com/USER/REPO/actions/workflows/lint.yml)
[![codecov](https://codecov.io/github/USER/REPO/graph/badge.svg?token=TOKEN)](https://codecov.io/github/USER/REPO)
```

### Badge Status Meanings
- **Passing (Green)**: All checks successful
- **Failing (Red)**: One or more checks failed
- **No Status**: Workflow hasn't run yet

## Local Testing Before Push

### Run Tests Locally
```bash
# Full test suite
uv run pytest --cov

# Specific app
uv run pytest app/buildorders/tests/

# With coverage report
uv run pytest --cov --cov-report=html
```

### Lint Locally
```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Docker Build Locally
```bash
# Build and start
docker compose up -d --build

# Check health
docker compose ps
curl http://localhost/health/

# View logs
docker compose logs web
```

## Workflow Optimization

### Caching Dependencies
```yaml
- name: Cache UV dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}
```

### Parallel Jobs
```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.13']
        # Add more versions if needed
```

### Conditional Execution
```yaml
# Only run on specific paths
on:
  push:
    paths:
      - 'app/**'
      - 'tests/**'
      - 'pyproject.toml'
```

## Deployment Checklist

### Before Merging PR
- [ ] All workflow checks pass
- [ ] Coverage meets >80% threshold
- [ ] No lint violations
- [ ] Docker build succeeds
- [ ] Health checks pass
- [ ] Manual testing completed

### After Merge to Main
- [ ] Workflows run successfully
- [ ] Badges update to passing
- [ ] Codecov report generated
- [ ] No new security alerts
- [ ] CHANGELOG.md updated

## Monitoring & Alerts

### GitHub Actions
- Enable email notifications for failures
- Review workflow run history regularly
- Monitor workflow execution times
- Check for deprecated actions

### Codecov
- Set coverage thresholds
- Enable PR comments
- Monitor coverage trends
- Review uncovered lines

## Documentation References

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Codecov Documentation](https://docs.codecov.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Docker Compose CI](https://docs.docker.com/compose/ci/)
