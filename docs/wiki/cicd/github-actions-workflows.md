# GitHub Actions Workflows - Detailed Documentation

**Last Updated:** 2026-02-02  
**Enhancement:** ENH-0000016  
**Status:** Active

---

## Table of Contents

1. [Overview](#overview)
2. [Test Workflow](#test-workflow)
3. [Docker Build Workflow](#docker-build-workflow)
4. [Code Quality Workflow](#code-quality-workflow)
5. [Workflow Configuration](#workflow-configuration)
6. [Common Patterns](#common-patterns)
7. [Optimization Tips](#optimization-tips)

---

## Overview

This document provides detailed technical documentation for each GitHub Actions workflow in the SE2 Calculator Project. Each workflow is designed to validate different aspects of the codebase automatically.

### Workflow Files Location

All workflow files are located in `.github/workflows/`:

```
.github/
└── workflows/
    ├── test.yml          # Test workflow
    ├── docker.yml        # Docker build workflow
    └── lint.yml          # Code quality workflow
```

### Common Workflow Structure

All workflows follow this general structure:

```yaml
name: Workflow Name
on: [trigger events]
jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - name: Step description
        uses: action@version  # or run: command
```

---

## Test Workflow

**File:** `.github/workflows/test.yml`  
**Purpose:** Run complete pytest test suite with coverage reporting  
**Status Badge:** ![Tests](https://github.com/crashtechie/se2-calculator-project/actions/workflows/test.yml/badge.svg)

### Trigger Conditions

```yaml
on:
  push:
    branches: [main, development, 'enhancement/**']
  pull_request:
    branches: [main, development]
```

**When it runs:**
- Every push to `main` branch
- Every push to `development` branch
- Every push to branches matching `enhancement/**` pattern
- Every pull request targeting `main` or `development`

### Workflow Steps

#### 1. Checkout Code

```yaml
- name: Checkout code
  uses: actions/checkout@v4
```

**Purpose:** Downloads repository code to the runner  
**Duration:** ~5 seconds  
**Why:** Workflows need access to code to test it

#### 2. Setup Python 3.13

```yaml
- name: Setup Python 3.13
  uses: actions/setup-python@v5
  with:
    python-version: '3.13'
```

**Purpose:** Installs Python 3.13 on the runner  
**Duration:** ~10 seconds (cached after first run)  
**Why:** Project requires Python 3.13 for compatibility

#### 3. Install UV Package Manager

```yaml
- name: Install UV
  run: pip install uv
```

**Purpose:** Installs UV, a fast Python package manager  
**Duration:** ~5 seconds  
**Why:** UV is faster than pip and provides better dependency resolution  
**Note:** UV is the primary package manager for this project

#### 4. Install Dependencies

```yaml
- name: Install dependencies
  run: uv pip install --system -e .
```

**Purpose:** Installs all project dependencies from `pyproject.toml`  
**Duration:** ~30-60 seconds  
**Why:** Tests need all dependencies to run  
**Flags:**
- `--system`: Install to system Python (not a venv)
- `-e .`: Install project in editable mode

#### 5. Run Tests with Coverage

```yaml
- name: Run tests with coverage
  run: |
    cd app
    uv run pytest --cov --cov-report=xml --cov-report=term
  env:
    DB_NAME: ""  # Force SQLite for CI tests
```

**Purpose:** Execute pytest test suite and generate coverage reports  
**Duration:** ~60-90 seconds  
**Why:** Validates code correctness and tracks test coverage  
**Flags:**
- `--cov`: Enable coverage measurement
- `--cov-report=xml`: Generate XML report for Codecov
- `--cov-report=term`: Display coverage in terminal
**Environment:**
- `DB_NAME=""`: Forces Django to use SQLite instead of PostgreSQL

#### 6. Upload Coverage to Codecov (Optional)

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./app/coverage.xml
    fail_ci_if_error: false
  env:
    CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

**Purpose:** Upload coverage data to Codecov for tracking  
**Duration:** ~10 seconds  
**Why:** Provides coverage trends and PR coverage diffs  
**Note:** Requires `CODECOV_TOKEN` secret to be configured

### Expected Output

**Success:**
```
✓ 107 tests passed
✓ Coverage: 87%
✓ All checks passed
```

**Failure:**
```
✗ 1 test failed
✗ Coverage: 85% (below threshold)
✗ Some checks failed
```

### Common Issues

**Issue:** Tests pass locally but fail in CI
- **Cause:** Environment differences (database, timezone, etc.)
- **Solution:** Check environment variables, use SQLite in CI

**Issue:** Coverage below threshold
- **Cause:** New code added without tests
- **Solution:** Add tests for new functionality

**Issue:** Dependency installation fails
- **Cause:** Missing or incompatible dependencies
- **Solution:** Update `pyproject.toml` with correct versions

---

## Docker Build Workflow

**File:** `.github/workflows/docker.yml`  
**Purpose:** Validate Docker infrastructure builds and runs correctly  
**Status Badge:** ![Docker Build](https://github.com/crashtechie/se2-calculator-project/actions/workflows/docker.yml/badge.svg)

### Trigger Conditions

```yaml
on:
  push:
    branches: [main, development]
    paths:
      - 'Dockerfile'
      - 'docker-compose.yml'
      - 'nginx.conf'
      - '.dockerignore'
  pull_request:
    branches: [main, development]
    paths:
      - 'Dockerfile'
      - 'docker-compose.yml'
      - 'nginx.conf'
      - '.dockerignore'
```

**When it runs:**
- Push to `main` or `development` **AND** Docker files changed
- Pull request to `main` or `development` **AND** Docker files changed

**Monitored files:**
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Multi-container orchestration
- `nginx.conf` - Reverse proxy configuration
- `.dockerignore` - Build context exclusions

### Workflow Steps

#### 1. Checkout Code

```yaml
- name: Checkout code
  uses: actions/checkout@v4
```

**Purpose:** Downloads repository code  
**Duration:** ~5 seconds

#### 2. Create .env File

```yaml
- name: Create .env file
  run: |
    cp .env.example .env
    echo "SECRET_KEY=test-secret-key-for-ci-$(date +%s)" >> .env
    echo "DB_PASSWORD=test-db-password-$(date +%s)" >> .env
    echo "DB_HOST=database" >> .env
```

**Purpose:** Generate test environment configuration  
**Duration:** ~1 second  
**Why:** Docker stack requires environment variables  
**Note:** Uses timestamp to ensure unique secrets per run

#### 3. Build Docker Images

```yaml
- name: Build Docker images
  run: docker compose build
```

**Purpose:** Build all Docker images (web, nginx, database)  
**Duration:** ~2-3 minutes  
**Why:** Validates Dockerfile syntax and build process  
**Images built:**
- `se2-calculator-web` - Django application
- `nginx` - Reverse proxy
- `postgres` - Database (pulled, not built)

#### 4. Start Docker Stack

```yaml
- name: Start Docker stack
  run: docker compose up -d
```

**Purpose:** Start all services in detached mode  
**Duration:** ~10 seconds  
**Why:** Validates services can start successfully  
**Services started:**
- `web` - Django on port 8000
- `nginx` - Reverse proxy on port 80
- `database` - PostgreSQL on port 5432

#### 5. Wait for Services

```yaml
- name: Wait for services to initialize
  run: |
    echo "Waiting for services to start..."
    sleep 20
```

**Purpose:** Allow services time to fully initialize  
**Duration:** 20 seconds  
**Why:** Services need time to start and become healthy

#### 6. Check Service Health

```yaml
- name: Check service health
  run: |
    echo "Checking service status..."
    docker compose ps
    docker compose ps | grep -q "Up" || exit 1
```

**Purpose:** Verify all services are running  
**Duration:** ~2 seconds  
**Why:** Ensures containers didn't crash on startup

#### 7. Run Database Migrations

```yaml
- name: Run database migrations
  run: |
    docker compose exec -T web python app/manage.py migrate --noinput
```

**Purpose:** Apply Django database migrations  
**Duration:** ~5 seconds  
**Why:** Validates migrations work in containerized environment  
**Flag:** `-T` disables TTY allocation (required for CI)

#### 8. Test Web Service Endpoint

```yaml
- name: Test web service endpoint
  run: |
    echo "Testing web service..."
    curl -f http://localhost/ || exit 1
    echo "✓ Web service is responding"
```

**Purpose:** Verify web service responds to HTTP requests  
**Duration:** ~1 second  
**Why:** Validates nginx → Django routing works  
**Flag:** `-f` makes curl fail on HTTP errors

#### 9. Test Static Files Serving

```yaml
- name: Test static files serving
  run: |
    echo "Testing static files..."
    curl -f http://localhost/static/css/main.css || exit 1
    echo "✓ Static files are being served"
```

**Purpose:** Verify static files are served correctly  
**Duration:** ~1 second  
**Why:** Validates nginx static file configuration

#### 10. Check Logs on Failure

```yaml
- name: Check logs for errors
  if: failure()
  run: |
    echo "=== Web Service Logs ==="
    docker compose logs web
    echo "=== Nginx Logs ==="
    docker compose logs nginx
    echo "=== Database Logs ==="
    docker compose logs database
```

**Purpose:** Display logs when workflow fails  
**Duration:** ~5 seconds  
**Why:** Helps diagnose failures  
**Condition:** Only runs if previous steps failed

#### 11. Tear Down Stack

```yaml
- name: Tear down stack
  if: always()
  run: docker compose down -v
```

**Purpose:** Stop and remove all containers and volumes  
**Duration:** ~5 seconds  
**Why:** Clean up resources  
**Condition:** Always runs, even if workflow failed  
**Flag:** `-v` removes volumes to ensure clean state

### Expected Output

**Success:**
```
✓ Images built successfully
✓ Services started
✓ All services healthy
✓ Migrations applied
✓ Web service responding
✓ Static files served
✓ Stack torn down
```

**Failure:**
```
✗ Build failed / Service crashed / Endpoint unreachable
✗ Logs displayed for debugging
✗ Stack torn down
```

### Common Issues

**Issue:** Build fails with dependency errors
- **Cause:** Missing system dependencies in Dockerfile
- **Solution:** Add required packages to `apt-get install` step

**Issue:** Services fail health check
- **Cause:** Services taking too long to start
- **Solution:** Increase wait time or add proper health checks

**Issue:** Web service unreachable
- **Cause:** nginx misconfiguration or Django not binding correctly
- **Solution:** Check nginx.conf and Django ALLOWED_HOSTS

---

## Code Quality Workflow

**File:** `.github/workflows/lint.yml`  
**Purpose:** Check code quality and formatting standards  
**Status Badge:** ![Code Quality](https://github.com/crashtechie/se2-calculator-project/actions/workflows/lint.yml/badge.svg)

### Trigger Conditions

```yaml
on:
  push:
    branches: [main, development, 'enhancement/**']
  pull_request:
    branches: [main, development]
```

**When it runs:**
- Every push to `main`, `development`, or `enhancement/**` branches
- Every pull request to `main` or `development`

### Workflow Steps

#### 1. Checkout Code

```yaml
- name: Checkout code
  uses: actions/checkout@v4
```

**Purpose:** Downloads repository code  
**Duration:** ~5 seconds

#### 2. Setup Python 3.13

```yaml
- name: Setup Python 3.13
  uses: actions/setup-python@v5
  with:
    python-version: '3.13'
```

**Purpose:** Installs Python 3.13  
**Duration:** ~10 seconds (cached)

#### 3. Install Ruff

```yaml
- name: Install Ruff
  run: pip install ruff
```

**Purpose:** Install Ruff linter and formatter  
**Duration:** ~5 seconds  
**Why:** Ruff is a fast Python linter (10-100x faster than flake8)

#### 4. Run Ruff Linter

```yaml
- name: Run Ruff linter
  run: |
    echo "Running Ruff linter..."
    ruff check app/ scripts/ || echo "Linting issues found (non-blocking)"
  continue-on-error: true
```

**Purpose:** Check code for style and quality issues  
**Duration:** ~5 seconds  
**Why:** Maintains consistent code quality  
**Targets:** `app/` and `scripts/` directories  
**Note:** Non-blocking (workflow continues even if issues found)

#### 5. Run Ruff Formatter Check

```yaml
- name: Run Ruff formatter check
  run: |
    echo "Checking code formatting..."
    ruff format --check app/ scripts/ || echo "Formatting issues found (non-blocking)"
  continue-on-error: true
```

**Purpose:** Check code formatting consistency  
**Duration:** ~5 seconds  
**Why:** Ensures consistent code style  
**Flag:** `--check` only checks, doesn't modify files  
**Note:** Non-blocking (workflow continues even if issues found)

#### 6. Summary

```yaml
- name: Summary
  run: |
    echo "Code quality checks complete"
    echo "Review any issues above and fix in future commits"
```

**Purpose:** Display completion message  
**Duration:** ~1 second  
**Why:** Provides clear workflow completion status

### Expected Output

**Success (no issues):**
```
✓ Ruff linter: No issues found
✓ Ruff formatter: Code is properly formatted
✓ Code quality checks complete
```

**Success (with issues):**
```
⚠ Ruff linter: 5 issues found (non-blocking)
⚠ Ruff formatter: 2 files need formatting (non-blocking)
✓ Code quality checks complete
```

### Common Issues

**Issue:** Many linting errors reported
- **Cause:** Code doesn't follow style guidelines
- **Solution:** Run `ruff check --fix app/ scripts/` locally

**Issue:** Formatting issues reported
- **Cause:** Code not formatted consistently
- **Solution:** Run `ruff format app/ scripts/` locally

**Issue:** False positives
- **Cause:** Ruff rules too strict for specific cases
- **Solution:** Add `# noqa` comments or configure `pyproject.toml`

---

## Workflow Configuration

### Environment Variables

Workflows can use environment variables for configuration:

```yaml
env:
  PYTHON_VERSION: '3.13'
  DB_NAME: ''  # Empty for SQLite in CI
```

### Secrets

Sensitive data stored in GitHub Secrets:

- `CODECOV_TOKEN` - Codecov upload token (optional)

**To add secrets:**
1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value

### Caching

Workflows can cache dependencies for faster runs:

```yaml
- name: Cache Python packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
```

**Benefits:**
- Faster dependency installation
- Reduced workflow duration
- Lower bandwidth usage

---

## Common Patterns

### Conditional Steps

Run steps only under certain conditions:

```yaml
- name: Upload coverage
  if: success()  # Only if previous steps succeeded
  
- name: Show logs
  if: failure()  # Only if previous steps failed
  
- name: Cleanup
  if: always()  # Always run, regardless of status
```

### Matrix Builds

Test across multiple versions:

```yaml
strategy:
  matrix:
    python-version: ['3.12', '3.13']
steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

### Reusable Workflows

Share workflow logic across files:

```yaml
jobs:
  call-workflow:
    uses: ./.github/workflows/reusable.yml
    with:
      parameter: value
```

---

## Optimization Tips

### 1. Use Caching

Cache dependencies to speed up workflows:

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('pyproject.toml') }}
```

### 2. Parallelize Jobs

Run independent jobs in parallel:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
  lint:
    runs-on: ubuntu-latest  # Runs in parallel with test
```

### 3. Use Path Filters

Only run workflows when relevant files change:

```yaml
on:
  push:
    paths:
      - 'app/**'
      - 'tests/**'
```

### 4. Optimize Docker Builds

Use BuildKit and layer caching:

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
```

### 5. Use UV Package Manager

UV is 10-100x faster than pip:

```yaml
- run: pip install uv
- run: uv pip install --system -e .
```

---

## Related Documentation

- **[CI/CD Overview](./cicd-overview.md)** - High-level pipeline overview
- **[Troubleshooting Guide](./troubleshooting-workflows.md)** - Common issues and solutions
- **[GitHub Actions Docs](https://docs.github.com/en/actions)** - Official documentation

---

**Last Updated:** 2026-02-02  
**Maintained By:** Dan Smith (@crashtechie)  
**Questions?** Open an issue on GitHub
