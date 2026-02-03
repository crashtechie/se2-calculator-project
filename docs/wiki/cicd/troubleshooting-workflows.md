# CI/CD Workflows - Troubleshooting Guide

**Last Updated:** 2026-02-02  
**Enhancement:** ENH-0000016  
**Status:** Active

---

## Table of Contents

1. [Quick Diagnosis](#quick-diagnosis)
2. [Test Workflow Issues](#test-workflow-issues)
3. [Docker Workflow Issues](#docker-workflow-issues)
4. [Code Quality Workflow Issues](#code-quality-workflow-issues)
5. [General Workflow Issues](#general-workflow-issues)
6. [How to Read Workflow Logs](#how-to-read-workflow-logs)
7. [How to Debug Locally](#how-to-debug-locally)
8. [How to Re-run Workflows](#how-to-re-run-workflows)
9. [Getting Help](#getting-help)

---

## Quick Diagnosis

### Workflow Status Quick Reference

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ Green | All checks passed | Ready to merge |
| ❌ Red | One or more checks failed | Review logs, fix issues |
| 🟡 Yellow | Workflow running | Wait for completion |
| ⚪ Gray | Workflow skipped | Normal if conditions not met |
| ⏸️ Canceled | Manually stopped | Re-run if needed |

### Common Error Patterns

| Error Message | Likely Cause | Quick Fix |
|---------------|--------------|-----------|
| `ModuleNotFoundError` | Missing dependency | Add to `pyproject.toml` |
| `AssertionError` | Test failure | Fix test or code |
| `SyntaxError` | Python syntax error | Fix syntax |
| `Connection refused` | Service not ready | Increase wait time |
| `Permission denied` | File permissions | Check file permissions |
| `No space left` | Disk full | Clean up or optimize |

---

## Test Workflow Issues

### Issue: Tests Pass Locally But Fail in CI

**Symptoms:**
- `uv run pytest` succeeds on your machine
- GitHub Actions test workflow fails
- Same tests, different results

**Common Causes:**

#### 1. Database Differences

**Problem:** Local uses PostgreSQL, CI uses SQLite

**Solution:**
```yaml
# In .github/workflows/test.yml
env:
  DB_NAME: ""  # Force SQLite
```

**Verify locally:**
```bash
cd app
DB_NAME="" uv run pytest
```

#### 2. Timezone Issues

**Problem:** Tests depend on specific timezone

**Solution:**
```python
# In test file
import os
os.environ['TZ'] = 'UTC'
```

Or in workflow:
```yaml
env:
  TZ: UTC
```

#### 3. Missing Environment Variables

**Problem:** Tests expect environment variables

**Solution:**
```yaml
# In workflow
env:
  SECRET_KEY: test-key
  DEBUG: true
```

#### 4. File Path Issues

**Problem:** Tests use absolute paths

**Solution:**
```python
# Use relative paths or Path
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
```

### Issue: Coverage Below Threshold

**Symptoms:**
- Tests pass but coverage check fails
- Message: "Coverage: 85% (target: 87%)"

**Diagnosis:**
```bash
cd app
uv run pytest --cov --cov-report=term-missing
# Shows which lines are not covered
```

**Solutions:**

1. **Add tests for new code:**
```bash
# Find uncovered files
uv run pytest --cov --cov-report=html
# Open htmlcov/index.html in browser
```

2. **Exclude non-critical files:**
```toml
# In pyproject.toml
[tool.coverage.run]
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/admin.py",
]
```

3. **Lower threshold temporarily:**
```yaml
# In workflow (not recommended)
- run: pytest --cov --cov-fail-under=85
```

### Issue: Dependency Installation Fails

**Symptoms:**
- Error during "Install dependencies" step
- Message: "Could not find a version that satisfies..."

**Diagnosis:**
```bash
# Test locally
uv pip install --dry-run -e .
```

**Solutions:**

1. **Update pyproject.toml:**
```toml
[project]
dependencies = [
    "django>=6.0.1",  # Add missing package
]
```

2. **Check for conflicts:**
```bash
uv pip install -e .
# UV will show conflict details
```

3. **Lock dependencies:**
```bash
uv lock
git add uv.lock
git commit -m "Update dependency lock"
```

### Issue: Tests Timeout

**Symptoms:**
- Workflow runs for >10 minutes
- Eventually times out

**Diagnosis:**
```bash
# Run tests with timing
cd app
uv run pytest --durations=10
# Shows slowest 10 tests
```

**Solutions:**

1. **Optimize slow tests:**
```python
# Use fixtures instead of creating data in each test
@pytest.fixture
def sample_data():
    return create_test_data()
```

2. **Increase timeout:**
```yaml
# In workflow
- name: Run tests
  run: pytest
  timeout-minutes: 15  # Default is 360
```

3. **Parallelize tests:**
```bash
# Install pytest-xdist
uv pip install pytest-xdist

# Run in parallel
uv run pytest -n auto
```

---

## Docker Workflow Issues

### Issue: Docker Build Fails

**Symptoms:**
- Error during "Build Docker images" step
- Message: "ERROR [stage-X Y/Z] RUN ..."

**Diagnosis:**
```bash
# Build locally
docker compose build --no-cache
```

**Solutions:**

1. **Missing system dependencies:**
```dockerfile
# In Dockerfile
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \  # Add missing packages
    && rm -rf /var/lib/apt/lists/*
```

2. **Python dependency issues:**
```dockerfile
# Use specific versions
RUN uv pip install --system django==6.0.1
```

3. **Build context too large:**
```
# In .dockerignore
.git
.venv
__pycache__
*.pyc
node_modules
```

### Issue: Services Fail Health Check

**Symptoms:**
- Error during "Check service health" step
- Services show as "unhealthy" or "exited"

**Diagnosis:**
```bash
# Check locally
docker compose up -d
docker compose ps
docker compose logs web
```

**Solutions:**

1. **Increase wait time:**
```yaml
# In workflow
- name: Wait for services
  run: sleep 30  # Increase from 20
```

2. **Fix health check:**
```dockerfile
# In Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')"
```

3. **Check service logs:**
```yaml
# In workflow (add before health check)
- name: Show logs
  run: docker compose logs
```

### Issue: Web Service Unreachable

**Symptoms:**
- Error during "Test web service endpoint" step
- Message: "curl: (7) Failed to connect"

**Diagnosis:**
```bash
# Test locally
docker compose up -d
sleep 20
curl -v http://localhost/
docker compose logs nginx
docker compose logs web
```

**Solutions:**

1. **Check nginx configuration:**
```nginx
# In nginx.conf
upstream web {
    server web:8000;  # Ensure correct service name and port
}
```

2. **Check Django ALLOWED_HOSTS:**
```python
# In settings.py
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
```

3. **Check port mapping:**
```yaml
# In docker-compose.yml
services:
  nginx:
    ports:
      - "80:80"  # Ensure correct mapping
```

### Issue: Static Files Not Served

**Symptoms:**
- Error during "Test static files serving" step
- Message: "curl: (22) The requested URL returned error: 404"

**Diagnosis:**
```bash
# Check locally
docker compose up -d
curl -I http://localhost/static/css/main.css
docker compose logs nginx
```

**Solutions:**

1. **Collect static files:**
```dockerfile
# In Dockerfile
RUN python app/manage.py collectstatic --noinput --clear
```

2. **Check nginx static configuration:**
```nginx
# In nginx.conf
location /static/ {
    alias /app/staticfiles/;
}
```

3. **Check volume mounting:**
```yaml
# In docker-compose.yml
services:
  nginx:
    volumes:
      - static_files:/app/staticfiles
```

---

## Code Quality Workflow Issues

### Issue: Many Linting Errors

**Symptoms:**
- Ruff reports many style violations
- Workflow shows warnings (but passes)

**Diagnosis:**
```bash
# Check locally
uv run ruff check app/ scripts/
```

**Solutions:**

1. **Auto-fix issues:**
```bash
uv run ruff check --fix app/ scripts/
git add -A
git commit -m "Fix linting issues"
```

2. **Format code:**
```bash
uv run ruff format app/ scripts/
git add -A
git commit -m "Format code"
```

3. **Configure rules:**
```toml
# In pyproject.toml
[tool.ruff]
line-length = 100
ignore = ["E501"]  # Ignore specific rules
```

### Issue: False Positive Warnings

**Symptoms:**
- Ruff flags valid code as problematic
- Warnings don't make sense for your use case

**Solutions:**

1. **Ignore specific line:**
```python
# Add comment to ignore
result = some_function()  # noqa: F841
```

2. **Ignore specific file:**
```toml
# In pyproject.toml
[tool.ruff]
exclude = ["migrations/", "tests/"]
```

3. **Disable specific rule:**
```toml
# In pyproject.toml
[tool.ruff]
ignore = ["F841"]  # Unused variable
```

---

## General Workflow Issues

### Issue: Workflow Not Triggering

**Symptoms:**
- Push code but no workflow runs
- PR created but no checks appear

**Diagnosis:**
```bash
# Check workflow syntax
uv run yamllint .github/workflows/*.yml

# Check branch name
git branch --show-current
```

**Solutions:**

1. **Fix YAML syntax:**
```bash
# Install yamllint
uv pip install yamllint

# Check files
uv run yamllint .github/workflows/
```

2. **Check branch pattern:**
```yaml
# In workflow
on:
  push:
    branches: [main, development, 'enhancement/**']
    # Ensure your branch matches
```

3. **Enable GitHub Actions:**
- Go to Settings → Actions → General
- Ensure "Allow all actions" is selected

### Issue: Workflow Stuck/Hanging

**Symptoms:**
- Workflow runs for very long time
- No progress in logs

**Solutions:**

1. **Cancel and re-run:**
- Click workflow run
- Click "Cancel workflow"
- Click "Re-run all jobs"

2. **Check GitHub status:**
- Visit https://www.githubstatus.com/
- Check for GitHub Actions incidents

3. **Add timeout:**
```yaml
# In workflow
jobs:
  test:
    timeout-minutes: 10
```

### Issue: Secrets Not Working

**Symptoms:**
- Error: "secret not found"
- Codecov upload fails

**Solutions:**

1. **Add secret:**
- Go to Settings → Secrets and variables → Actions
- Click "New repository secret"
- Add name and value

2. **Check secret name:**
```yaml
# In workflow - must match exactly
env:
  CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

3. **Verify secret scope:**
- Secrets are repository-specific
- Check you're in the correct repository

---

## How to Read Workflow Logs

### Accessing Logs

1. **From PR:**
   - Scroll to bottom of PR
   - Click "Details" next to failed check

2. **From Actions tab:**
   - Click "Actions" tab
   - Click workflow run
   - Click failed job

### Understanding Log Structure

```
▼ Job: test
  ▼ Step: Checkout code
    ✓ Completed in 5s
  ▼ Step: Setup Python
    ✓ Completed in 10s
  ▼ Step: Run tests
    ✗ Failed in 45s
    [Error details here]
```

### Finding Errors

1. **Look for red text** - Indicates errors
2. **Check exit codes** - Non-zero means failure
3. **Read last 20 lines** - Usually contains error
4. **Search for "Error"** - Use browser search (Ctrl+F)

### Example Error Analysis

```
Error: AssertionError: 200 != 404
  File "tests/test_views.py", line 42, in test_home_page
    self.assertEqual(response.status_code, 200)
```

**Analysis:**
- **Error type:** AssertionError
- **Location:** tests/test_views.py, line 42
- **Problem:** Expected 200, got 404
- **Fix:** Check view returns correct status code

---

## How to Debug Locally

### Reproduce CI Environment

```bash
# Use same Python version
uv python install 3.13
uv python pin 3.13

# Use same database
export DB_NAME=""  # Force SQLite

# Run same commands
cd app
uv run pytest --cov --cov-report=term
```

### Test Docker Locally

```bash
# Build and test
docker compose build
docker compose up -d
sleep 20

# Check services
docker compose ps
docker compose logs web

# Test endpoints
curl -f http://localhost/
curl -f http://localhost/static/css/main.css

# Cleanup
docker compose down -v
```

### Test Linting Locally

```bash
# Run same checks as CI
uv run ruff check app/ scripts/
uv run ruff format --check app/ scripts/

# Auto-fix issues
uv run ruff check --fix app/ scripts/
uv run ruff format app/ scripts/
```

### Debug Specific Test

```bash
# Run single test with verbose output
cd app
uv run pytest tests/test_views.py::TestClass::test_method -vv

# Run with debugger
uv run pytest --pdb tests/test_views.py::TestClass::test_method
```

---

## How to Re-run Workflows

### Re-run All Jobs

1. Go to "Actions" tab
2. Click the workflow run
3. Click "Re-run jobs" dropdown (top right)
4. Select "Re-run all jobs"

### Re-run Failed Jobs Only

1. Go to "Actions" tab
2. Click the workflow run
3. Click "Re-run jobs" dropdown
4. Select "Re-run failed jobs"

### Re-run from PR

1. Go to your pull request
2. Scroll to checks section
3. Click "Re-run" next to failed check

### Force New Run

```bash
# Make trivial change
echo "" >> README.md
git add README.md
git commit -m "Trigger workflow"
git push
```

---

## Getting Help

### Self-Help Resources

1. **Check this guide** - Most common issues covered
2. **Read workflow logs** - Error messages are usually clear
3. **Test locally** - Reproduce the issue on your machine
4. **Search GitHub Issues** - Someone may have had same problem

### When to Ask for Help

- Issue persists after trying solutions
- Error message is unclear
- Problem seems like a bug
- Need clarification on workflow behavior

### How to Ask for Help

**Good issue report:**

```markdown
## Problem
Test workflow fails with "ModuleNotFoundError: No module named 'xyz'"

## What I tried
1. Added xyz to pyproject.toml
2. Ran `uv lock`
3. Pushed changes
4. Still fails

## Workflow run
https://github.com/user/repo/actions/runs/12345

## Local test
Works fine locally with `uv run pytest`

## Environment
- Branch: enhancement/feature-x
- Python: 3.13
- UV: 0.x.x
```

### Contact Options

- **GitHub Issues:** For bugs and feature requests
- **GitHub Discussions:** For questions and help
- **Team Chat:** For urgent issues (if applicable)

---

## Prevention Tips

### Before Pushing

```bash
# Run all checks locally
cd app
uv run pytest --cov
cd ..
uv run ruff check app/ scripts/
uv run ruff format --check app/ scripts/

# Test Docker if changed
docker compose build
docker compose up -d
# ... test endpoints ...
docker compose down -v
```

### Use Pre-commit Hooks

```bash
# Install pre-commit
uv pip install pre-commit

# Setup hooks
pre-commit install

# Now checks run automatically on commit
```

### Keep Dependencies Updated

```bash
# Update dependencies
uv pip install --upgrade -e .

# Update lock file
uv lock

# Test everything still works
uv run pytest
```

---

## Related Documentation

- **[CI/CD Overview](./cicd-overview.md)** - High-level pipeline overview
- **[GitHub Actions Workflows](./github-actions-workflows.md)** - Detailed workflow documentation
- **[GitHub Actions Docs](https://docs.github.com/en/actions)** - Official documentation

---

**Last Updated:** 2026-02-02  
**Maintained By:** Dan Smith (@crashtechie)  
**Questions?** Open an issue on GitHub
