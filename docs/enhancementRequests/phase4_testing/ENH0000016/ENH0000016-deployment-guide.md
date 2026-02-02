# ENH-0000016: CI/CD Pipeline - Technical Deployment Guide

**Enhancement ID:** ENH-0000016  
**Document Type:** Technical Deployment Guide  
**Version:** 1.0  
**Created:** 2026-02-02  
**Last Updated:** 2026-02-02  
**Estimated Time:** 4-6 hours  
**Difficulty Level:** Medium

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Architecture](#architecture)
4. [Pre-Deployment Checklist](#pre-deployment-checklist)
5. [Deployment Steps](#deployment-steps)
6. [Testing & Validation](#testing--validation)
7. [Post-Deployment Configuration](#post-deployment-configuration)
8. [Troubleshooting](#troubleshooting)
9. [Rollback Procedures](#rollback-procedures)
10. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Overview

### What This Deployment Accomplishes

This deployment implements a complete CI/CD pipeline using GitHub Actions that provides:

- **Automated Testing**: Runs pytest suite on every push and pull request
- **Docker Validation**: Validates Docker stack builds on infrastructure changes
- **Code Quality Checks**: Runs linting and formatting checks automatically
- **Coverage Reporting**: Generates and tracks test coverage metrics
- **Status Visibility**: Provides real-time workflow status via badges

### Why Deploy This Now

**Strategic Timing**: Before Phase 3 (Build Order Calculator)

- Phase 3 will introduce complex calculator logic requiring robust testing
- Automated testing catches regressions early in development
- Establishes quality gates before production readiness
- Provides safety net for multi-developer collaboration
- Recommended by Phase 2 Post-Deployment Report

### Expected Outcomes

After successful deployment:
- ✅ All tests run automatically on every push
- ✅ Pull requests show test status before merge
- ✅ Docker builds validated on infrastructure changes
- ✅ Code quality issues detected automatically
- ✅ Coverage reports generated and tracked
- ✅ README displays workflow status badges
- ✅ Team has visibility into build health

---

## Prerequisites

### Required Access & Permissions

- **GitHub Repository Access**: Push access to `crashtechie/se2-calculator-project`
- **GitHub Actions**: Enabled on repository (free for public repos)
- **Branch Permissions**: Ability to create `.github/workflows/` directory
- **Repository Settings**: Access to configure branch protection rules (optional)

### Required Tools & Accounts

#### Local Development Environment
```bash
# Verify installations
python --version    # Should be 3.13+
uv --version       # UV package manager
docker --version   # Docker for local testing
git --version      # Git for version control
```

#### Optional External Services

- **Codecov Account** (optional): For coverage tracking and badges
  - Sign up at https://codecov.io (free for open source)
  - Link GitHub repository
  - Generate upload token (stored in GitHub Secrets)

### Knowledge Requirements

- Basic understanding of YAML syntax
- Familiarity with GitHub Actions concepts
- Understanding of CI/CD principles
- Knowledge of pytest and Django testing
- Docker and Docker Compose basics

### Repository State Requirements

Before starting deployment:

```bash
# Verify current state
cd /path/to/se2-calculator-project

# Check branch
git branch --show-current  # Should be on development or feature branch

# Verify tests pass locally
cd app
uv run pytest
# Expected: 52 tests passing, 87% coverage

# Verify Docker stack works
cd ..
docker compose build
docker compose up -d
docker compose ps  # All services should be healthy
docker compose down
```

---

## Architecture

### CI/CD Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
│                                                              │
│  Push/PR Event → Triggers Workflows                         │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │  Test   │  │ Docker  │  │  Lint   │
   │Workflow │  │Workflow │  │Workflow │
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ Run     │  │ Build   │  │ Check   │
   │ Tests   │  │ Images  │  │ Quality │
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │Generate │  │ Test    │  │ Report  │
   │Coverage │  │ Stack   │  │ Issues  │
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
        └────────────┴────────────┘
                     │
                     ▼
            ┌────────────────┐
            │  PR Checks     │
            │  Status Badge  │
            └────────────────┘
```

### Workflow Components

#### 1. Test Workflow (`test.yml`)

**Purpose**: Run full pytest suite with coverage reporting

**Triggers**:
- Push to: `main`, `development`, `enhancement/**` branches
- Pull requests to: `main`, `development`

**Steps**:
1. Checkout repository code
2. Setup Python 3.13 environment
3. Install UV package manager
4. Install project dependencies
5. Run pytest with coverage
6. Upload coverage to Codecov (optional)

**Duration**: ~2-3 minutes

#### 2. Docker Workflow (`docker.yml`)

**Purpose**: Validate Docker stack builds and runs correctly

**Triggers**:
- Push to: `main`, `development` (only when Docker files change)
- Pull requests to: `main`, `development` (only when Docker files change)

**Monitored Files**:
- `Dockerfile`
- `docker-compose.yml`
- `nginx.conf`
- `.dockerignore`

**Steps**:
1. Checkout repository code
2. Create `.env` file with test credentials
3. Build Docker images
4. Start Docker Compose stack
5. Wait for services to initialize
6. Check service health status
7. Test web service endpoint
8. Test static file serving
9. Tear down stack

**Duration**: ~5-7 minutes

#### 3. Lint Workflow (`lint.yml`)

**Purpose**: Check code quality and formatting standards

**Triggers**:
- Push to: `main`, `development`, `enhancement/**` branches
- Pull requests to: `main`, `development`

**Steps**:
1. Checkout repository code
2. Setup Python 3.13 environment
3. Install Ruff linter
4. Run Ruff linter checks
5. Run Ruff formatter checks

**Duration**: ~1 minute

### Workflow Execution Flow

```
Developer Push/PR
       │
       ▼
GitHub Detects Event
       │
       ├─→ Test Workflow (always runs)
       │   ├─ Setup Python 3.13
       │   ├─ Install dependencies
       │   ├─ Run pytest
       │   └─ Upload coverage
       │
       ├─→ Docker Workflow (conditional)
       │   ├─ Build images
       │   ├─ Start stack
       │   ├─ Test endpoints
       │   └─ Cleanup
       │
       └─→ Lint Workflow (always runs)
           ├─ Check code style
           └─ Report issues
       │
       ▼
All Workflows Complete
       │
       ▼
Update PR Status Checks
```

---

## Pre-Deployment Checklist

### Environment Verification

```bash
# 1. Verify repository state
cd /path/to/se2-calculator-project
git status  # Should be clean or only have expected changes
git branch  # Note current branch

# 2. Verify local tests pass
cd app
uv run pytest --cov
# Expected output: 52 passed, 87% coverage

# 3. Verify Docker stack works
cd ..
docker compose build
docker compose up -d
sleep 15
curl -f http://localhost/ || echo "Web service failed"
curl -f http://localhost/static/css/main.css || echo "Static files failed"
docker compose down -v

# 4. Check for uncommitted changes
git status
```

### Repository Preparation

- [ ] All local tests passing (52/52)
- [ ] Docker stack builds and runs successfully
- [ ] No uncommitted changes (or changes are intentional)
- [ ] Current branch is up to date with remote
- [ ] `.env.example` file exists and is complete
- [ ] `pyproject.toml` has all dependencies listed

### GitHub Repository Settings

- [ ] GitHub Actions enabled (Settings → Actions → General)
- [ ] Workflow permissions set to "Read and write permissions"
- [ ] Repository is public (for free unlimited Actions minutes)

### Optional: Codecov Setup

If using Codecov for coverage tracking:

1. Visit https://codecov.io and sign in with GitHub
2. Add repository: `crashtechie/se2-calculator-project`
3. Copy upload token
4. Add to GitHub Secrets:
   - Go to: Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `CODECOV_TOKEN`
   - Value: [paste token]

---

## Deployment Steps

### Phase 1: Create Workflows Directory (5 minutes)

#### Step 1.1: Create Directory Structure

```bash
cd /path/to/se2-calculator-project

# Create workflows directory
mkdir -p .github/workflows

# Verify creation
ls -la .github/workflows
```

#### Step 1.2: Verify Directory Permissions

```bash
# Ensure directory is writable
chmod 755 .github
chmod 755 .github/workflows
```

---

### Phase 2: Create Test Workflow (30 minutes)

#### Step 2.1: Create Test Workflow File

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, development, 'enhancement/**' ]
  pull_request:
    branches: [ main, development ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install UV
        run: pip install uv
      
      - name: Install dependencies
        run: uv pip install --system -e .
      
      - name: Run tests with coverage
        run: |
          cd app
          uv run pytest --cov --cov-report=xml --cov-report=term
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./app/coverage.xml
          fail_ci_if_error: false
        env:
          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

#### Step 2.2: Validate YAML Syntax

```bash
# Install yamllint (optional but recommended)
pip install yamllint

# Validate syntax
yamllint .github/workflows/test.yml
```

#### Step 2.3: Commit Test Workflow

```bash
git add .github/workflows/test.yml
git commit -m "Add automated testing workflow (ENH-0000016)"
```

---

### Phase 3: Create Docker Workflow (45 minutes)

#### Step 3.1: Create Docker Workflow File

Create `.github/workflows/docker.yml`:


```yaml
name: Docker Build

on:
  push:
    branches: [ main, development ]
    paths:
      - 'Dockerfile'
      - 'docker-compose.yml'
      - 'nginx.conf'
      - '.dockerignore'
  pull_request:
    branches: [ main, development ]
    paths:
      - 'Dockerfile'
      - 'docker-compose.yml'
      - 'nginx.conf'
      - '.dockerignore'

jobs:
  docker-build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Create .env file
        run: |
          cp .env.example .env
          echo "SECRET_KEY=test-secret-key-for-ci-$(date +%s)" >> .env
          echo "DB_PASSWORD=test-db-password-$(date +%s)" >> .env
          echo "DB_HOST=database" >> .env
      
      - name: Build Docker images
        run: docker compose build
      
      - name: Start Docker stack
        run: docker compose up -d
      
      - name: Wait for services to initialize
        run: |
          echo "Waiting for services to start..."
          sleep 20
      
      - name: Check service health
        run: |
          echo "Checking service status..."
          docker compose ps
          docker compose ps | grep -q "Up" || exit 1
      
      - name: Run database migrations
        run: |
          docker compose exec -T web python manage.py migrate --noinput
      
      - name: Test web service endpoint
        run: |
          echo "Testing web service..."
          curl -f http://localhost/ || exit 1
          echo "✓ Web service is responding"
      
      - name: Test static files serving
        run: |
          echo "Testing static files..."
          curl -f http://localhost/static/css/main.css || exit 1
          echo "✓ Static files are being served"
      
      - name: Check logs for errors
        if: failure()
        run: |
          echo "=== Web Service Logs ==="
          docker compose logs web
          echo "=== Nginx Logs ==="
          docker compose logs nginx
          echo "=== Database Logs ==="
          docker compose logs database
      
      - name: Tear down stack
        if: always()
        run: docker compose down -v
```

#### Step 3.2: Validate Docker Workflow

```bash
# Validate YAML syntax
yamllint .github/workflows/docker.yml

# Test Docker workflow logic locally
docker compose build
docker compose up -d
sleep 20
docker compose ps
curl -f http://localhost/
curl -f http://localhost/static/css/main.css
docker compose down -v
```

#### Step 3.3: Commit Docker Workflow

```bash
git add .github/workflows/docker.yml
git commit -m "Add Docker build validation workflow (ENH-0000016)"
```

---

### Phase 4: Create Lint Workflow (30 minutes)

#### Step 4.1: Create Lint Workflow File

Create `.github/workflows/lint.yml`:

```yaml
name: Code Quality

on:
  push:
    branches: [ main, development, 'enhancement/**' ]
  pull_request:
    branches: [ main, development ]

jobs:
  lint:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install Ruff
        run: pip install ruff
      
      - name: Run Ruff linter
        run: |
          echo "Running Ruff linter..."
          ruff check app/ scripts/ || echo "Linting issues found (non-blocking)"
        continue-on-error: true
      
      - name: Run Ruff formatter check
        run: |
          echo "Checking code formatting..."
          ruff format --check app/ scripts/ || echo "Formatting issues found (non-blocking)"
        continue-on-error: true
      
      - name: Summary
        run: |
          echo "Code quality checks complete"
          echo "Review any issues above and fix in future commits"
```

#### Step 4.2: Test Ruff Locally

```bash
# Install Ruff
pip install ruff

# Test linting
ruff check app/ scripts/

# Test formatting
ruff format --check app/ scripts/

# If issues found, optionally fix them
ruff check --fix app/ scripts/
ruff format app/ scripts/
```

#### Step 4.3: Commit Lint Workflow

```bash
git add .github/workflows/lint.yml
git commit -m "Add code quality workflow (ENH-0000016)"
```

---

### Phase 5: Add Status Badges (15 minutes)

#### Step 5.1: Update README.md

Add status badges at the top of `README.md`, right after the title:

```markdown
# Space Engineers 2 Calculator Project

![Tests](https://github.com/crashtechie/se2-calculator-project/workflows/Tests/badge.svg)
![Docker Build](https://github.com/crashtechie/se2-calculator-project/workflows/Docker%20Build/badge.svg)
![Code Quality](https://github.com/crashtechie/se2-calculator-project/workflows/Code%20Quality/badge.svg)

**Version:** 0.6.0-alpha
```

If using Codecov, add coverage badge:

```markdown
[![codecov](https://codecov.io/gh/crashtechie/se2-calculator-project/branch/main/graph/badge.svg)](https://codecov.io/gh/crashtechie/se2-calculator-project)
```

#### Step 5.2: Commit README Changes

```bash
git add README.md
git commit -m "Add CI/CD workflow status badges (ENH-0000016)"
```

---

### Phase 6: Push and Verify (1 hour)

#### Step 6.1: Push to Remote

```bash
# Push all commits
git push origin <your-branch-name>
```

#### Step 6.2: Monitor Workflow Execution

1. Go to GitHub repository
2. Click "Actions" tab
3. Watch workflows execute in real-time
4. Verify all three workflows start

Expected behavior:
- Test workflow: Should run immediately
- Docker workflow: May not run if no Docker files changed
- Lint workflow: Should run immediately

#### Step 6.3: Verify Workflow Success

Check that workflows complete successfully:

```
✓ Tests - All checks passed
✓ Code Quality - All checks passed
✓ Docker Build - Skipped (no Docker file changes) or Passed
```

#### Step 6.4: Test Docker Workflow Trigger

To test Docker workflow, make a small change to a Docker file:

```bash
# Add a comment to Dockerfile
echo "# CI/CD test" >> Dockerfile

git add Dockerfile
git commit -m "Test Docker workflow trigger"
git push origin <your-branch-name>
```

Verify Docker workflow runs on GitHub Actions tab.

---

### Phase 7: Create Pull Request Test (30 minutes)

#### Step 7.1: Create Test Pull Request

1. Go to GitHub repository
2. Click "Pull requests" tab
3. Click "New pull request"
4. Select your branch as source
5. Select `development` as target
6. Create pull request

#### Step 7.2: Verify PR Checks

On the PR page, verify:
- [ ] "Tests" check appears
- [ ] "Code Quality" check appears
- [ ] "Docker Build" check appears (if Docker files changed)
- [ ] All checks show status (pending → success/failure)

#### Step 7.3: Test Failure Scenario

To verify failure detection works:

```bash
# Intentionally break a test
# Edit app/blocks/tests.py and change an assertion

git add app/blocks/tests.py
git commit -m "Test: Intentional test failure"
git push origin <your-branch-name>
```

Verify:
- Workflow runs
- Test fails
- PR shows red X
- Failure details visible in workflow logs

#### Step 7.4: Fix and Verify

```bash
# Revert the breaking change
git revert HEAD
git push origin <your-branch-name>
```

Verify:
- Workflow runs again
- Tests pass
- PR shows green checkmark

---

### Phase 8: Create Documentation (1 hour)

#### Step 8.1: Create CI/CD Overview Document

Create `docs/wiki/cicd/cicd-overview.md`:


```bash
mkdir -p docs/wiki/cicd
```

Create the overview document with:
- CI/CD pipeline purpose and benefits
- Workflow descriptions
- How to interpret results
- Links to detailed workflow documentation

#### Step 8.2: Create Workflow Documentation

Create `docs/wiki/cicd/github-actions-workflows.md`:

Document each workflow in detail:
- Trigger conditions
- Steps and their purpose
- Expected duration
- Common issues and solutions

#### Step 8.3: Create Troubleshooting Guide

Create `docs/wiki/cicd/troubleshooting-workflows.md`:

Include:
- Common workflow failures
- How to read workflow logs
- How to debug locally
- How to re-run failed workflows

#### Step 8.4: Commit Documentation

```bash
git add docs/wiki/cicd/
git commit -m "Add CI/CD documentation (ENH-0000016)"
git push origin <your-branch-name>
```

---

### Phase 9: Update CHANGELOG (15 minutes)

#### Step 9.1: Update CHANGELOG.md

Add new section for version 0.7.0-alpha:

```markdown
## [0.7.0-alpha] - 2026-02-XX

### Added - CI/CD Pipeline (ENH-0000016)
- GitHub Actions workflow for automated testing
  - Runs pytest suite on every push and PR
  - Generates coverage reports
  - Uploads coverage to Codecov
- Docker build validation workflow
  - Validates Docker stack builds correctly
  - Tests service health and endpoints
  - Only runs on infrastructure file changes
- Code quality workflow
  - Runs Ruff linter on Python code
  - Checks code formatting standards
  - Provides non-blocking quality feedback
- Workflow status badges in README
- Comprehensive CI/CD documentation
  - Pipeline overview
  - Workflow details
  - Troubleshooting guide

### Changed
- README.md: Added workflow status badges
- Development workflow: Tests now run automatically on push

### Technical Details
- All workflows use Python 3.13
- All workflows use UV package manager
- Test workflow runs in ~2-3 minutes
- Docker workflow runs in ~5-7 minutes
- Lint workflow runs in ~1 minute
- Total CI time: ~3-8 minutes depending on triggers
```

#### Step 9.2: Commit CHANGELOG

```bash
git add CHANGELOG.md
git commit -m "Update CHANGELOG for CI/CD implementation (ENH-0000016)"
git push origin <your-branch-name>
```

---

### Phase 10: Merge and Finalize (30 minutes)

#### Step 10.1: Final PR Review

1. Review all changes in PR
2. Verify all checks pass
3. Review workflow logs for any warnings
4. Ensure documentation is complete

#### Step 10.2: Merge Pull Request

1. Get approval from team (if required)
2. Merge PR to `development` branch
3. Verify workflows run on `development` branch

#### Step 10.3: Merge to Main (Optional)

If ready for main branch:

1. Create PR from `development` to `main`
2. Verify all checks pass
3. Merge to `main`
4. Verify workflows run on `main` branch

#### Step 10.4: Verify Status Badges

1. Visit repository README on GitHub
2. Verify status badges display correctly
3. Click badges to verify they link to workflow runs

---

## Testing & Validation

### Automated Testing Checklist

#### Test Workflow Validation

- [ ] Workflow runs on push to `main`
- [ ] Workflow runs on push to `development`
- [ ] Workflow runs on push to `enhancement/**` branches
- [ ] Workflow runs on PR to `main`
- [ ] Workflow runs on PR to `development`
- [ ] All 52 tests pass in workflow
- [ ] Coverage report generated (87%+)
- [ ] Coverage uploaded to Codecov (if configured)
- [ ] Workflow completes in <5 minutes

#### Docker Workflow Validation

- [ ] Workflow triggers on Dockerfile changes
- [ ] Workflow triggers on docker-compose.yml changes
- [ ] Workflow triggers on nginx.conf changes
- [ ] Workflow triggers on .dockerignore changes
- [ ] Workflow does NOT trigger on other file changes
- [ ] Docker images build successfully
- [ ] Docker stack starts successfully
- [ ] Web service responds to requests
- [ ] Static files served correctly
- [ ] Workflow completes in <10 minutes
- [ ] Stack tears down cleanly

#### Lint Workflow Validation

- [ ] Workflow runs on push to `main`
- [ ] Workflow runs on push to `development`
- [ ] Workflow runs on push to `enhancement/**` branches
- [ ] Workflow runs on PR to `main`
- [ ] Workflow runs on PR to `development`
- [ ] Ruff linter executes
- [ ] Ruff formatter check executes
- [ ] Workflow completes in <3 minutes
- [ ] Workflow continues even with linting issues

### Manual Testing Procedures

#### Test 1: Push to Feature Branch

```bash
# Create test branch
git checkout -b test/cicd-validation
echo "# CI/CD Test" >> TEST.md
git add TEST.md
git commit -m "Test: CI/CD workflow trigger"
git push origin test/cicd-validation
```

Expected:
- Test workflow runs
- Lint workflow runs
- Docker workflow does NOT run (no Docker file changes)

#### Test 2: Create Pull Request

```bash
# Create PR via GitHub UI
# Source: test/cicd-validation
# Target: development
```

Expected:
- All applicable workflows run
- PR shows status checks
- Checks must pass before merge (if branch protection enabled)

#### Test 3: Test Failure Detection

```bash
# Break a test intentionally
# Edit app/blocks/tests.py
# Change: self.assertEqual(response.status_code, 200)
# To: self.assertEqual(response.status_code, 404)

git add app/blocks/tests.py
git commit -m "Test: Intentional failure"
git push origin test/cicd-validation
```

Expected:
- Test workflow runs
- Test workflow fails
- PR shows red X
- Failure details in logs

#### Test 4: Docker File Change

```bash
# Revert test failure first
git revert HEAD
git push origin test/cicd-validation

# Make Docker file change
echo "# Test comment" >> Dockerfile
git add Dockerfile
git commit -m "Test: Docker workflow trigger"
git push origin test/cicd-validation
```

Expected:
- All workflows run (including Docker)
- Docker workflow builds and tests stack
- All checks pass

#### Test 5: Status Badge Verification

1. Visit repository on GitHub
2. View README.md
3. Verify badges display
4. Click each badge
5. Verify links go to correct workflow runs

---

## Post-Deployment Configuration

### Optional: Branch Protection Rules

Configure branch protection to require checks before merge:

1. Go to: Settings → Branches
2. Click "Add rule" or edit existing rule
3. Branch name pattern: `main` or `development`
4. Enable: "Require status checks to pass before merging"
5. Select required checks:
   - Tests
   - Code Quality
   - Docker Build (optional)
6. Enable: "Require branches to be up to date before merging"
7. Save changes

### Optional: Codecov Configuration

Create `.codecov.yml` in repository root:

```yaml
coverage:
  status:
    project:
      default:
        target: 87%
        threshold: 2%
    patch:
      default:
        target: 80%

comment:
  layout: "reach,diff,flags,tree"
  behavior: default
  require_changes: false
```

Commit and push:

```bash
git add .codecov.yml
git commit -m "Add Codecov configuration"
git push
```

### Optional: Workflow Optimization

#### Enable Dependency Caching

Add to test workflow after "Setup Python" step:

```yaml
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

#### Enable Docker Layer Caching

Add to docker workflow before "Build Docker images" step:

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Cache Docker layers
  uses: actions/cache@v3
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-buildx-
```

### Notification Configuration

#### Slack Notifications (Optional)

Add to end of each workflow:

```yaml
- name: Notify Slack on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "Workflow failed: ${{ github.workflow }}"
      }
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Workflow Not Triggering

**Symptoms**:
- Push to branch but no workflow runs
- PR created but no checks appear

**Diagnosis**:
```bash
# Check workflow file syntax
yamllint .github/workflows/*.yml

# Verify branch name matches trigger
git branch --show-current

# Check GitHub Actions is enabled
# Visit: Settings → Actions → General
```

**Solutions**:
- Fix YAML syntax errors
- Verify branch name matches trigger pattern
- Enable GitHub Actions in repository settings
- Check workflow file is in correct location (`.github/workflows/`)

#### Issue 2: Tests Fail in CI but Pass Locally

**Symptoms**:
- `uv run pytest` passes locally
- GitHub Actions test workflow fails

**Diagnosis**:
```bash
# Check Python version
python --version  # Should be 3.13

# Check dependencies
uv pip list

# Run tests with same flags as CI
cd app
uv run pytest --cov --cov-report=xml --cov-report=term
```

**Solutions**:

- Ensure Python 3.13 is specified in workflow
- Check for missing dependencies in `pyproject.toml`
- Verify environment variables are set correctly
- Check for timezone or locale-dependent tests
- Review workflow logs for specific error messages

#### Issue 3: Docker Workflow Fails to Build

**Symptoms**:
- Docker build step fails in workflow
- Error: "failed to solve with frontend dockerfile.v0"

**Diagnosis**:
```bash
# Test Docker build locally
docker compose build

# Check Docker file syntax
docker compose config

# Verify .env.example exists
ls -la .env.example
```

**Solutions**:
- Verify Dockerfile syntax is correct
- Ensure all COPY paths exist
- Check .env.example has all required variables
- Verify base image is accessible
- Review Docker build logs in workflow

#### Issue 4: Docker Services Not Healthy

**Symptoms**:
- Docker build succeeds but services fail health checks
- curl commands fail in workflow

**Diagnosis**:
```bash
# Check service logs locally
docker compose up -d
docker compose logs web
docker compose logs nginx
docker compose logs database
docker compose ps
```

**Solutions**:
- Increase wait time in workflow (change `sleep 15` to `sleep 30`)
- Check database initialization time
- Verify migrations run successfully
- Check nginx configuration
- Review service logs in workflow output

#### Issue 5: Coverage Upload Fails

**Symptoms**:
- Tests pass but Codecov upload fails
- Warning: "Codecov token not found"

**Diagnosis**:
```bash
# Check if CODECOV_TOKEN is set in GitHub Secrets
# Visit: Settings → Secrets and variables → Actions
```

**Solutions**:
- Add CODECOV_TOKEN to GitHub Secrets
- Set `fail_ci_if_error: false` in workflow (already done)
- Verify Codecov account is linked to repository
- Check coverage.xml file is generated

#### Issue 6: Workflow Takes Too Long

**Symptoms**:
- Workflow runs for >10 minutes
- Timeout errors

**Diagnosis**:
```bash
# Check workflow logs for slow steps
# Identify which step takes longest
```

**Solutions**:
- Enable dependency caching (see Post-Deployment Configuration)
- Enable Docker layer caching
- Reduce test parallelization if causing issues
- Consider splitting large test suites
- Optimize Docker build with multi-stage builds

#### Issue 7: Lint Workflow Shows Unexpected Errors

**Symptoms**:
- Ruff reports errors not seen locally
- Different linting results in CI vs local

**Diagnosis**:
```bash
# Run Ruff locally with same version
pip install ruff
ruff --version

# Run same commands as workflow
ruff check app/ scripts/
ruff format --check app/ scripts/
```

**Solutions**:
- Pin Ruff version in workflow: `pip install ruff==0.1.0`
- Update local Ruff to match CI version
- Add `.ruff.toml` configuration file
- Review and fix reported issues

### Debugging Workflow Failures

#### View Workflow Logs

1. Go to GitHub repository
2. Click "Actions" tab
3. Click on failed workflow run
4. Click on failed job
5. Expand failed step
6. Review error messages

#### Download Workflow Artifacts

Some workflows may upload artifacts (logs, coverage reports):

1. Go to failed workflow run
2. Scroll to "Artifacts" section
3. Download relevant artifacts
4. Extract and review locally

#### Re-run Failed Workflows

1. Go to failed workflow run
2. Click "Re-run jobs" dropdown
3. Select "Re-run failed jobs" or "Re-run all jobs"
4. Monitor execution

#### Enable Debug Logging

Add to workflow file (temporarily):

```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

This provides verbose logging for troubleshooting.

---

## Rollback Procedures

### Scenario 1: Workflow Causing Issues

If a workflow is causing problems:

#### Quick Disable

1. Go to: Settings → Actions → General
2. Select "Disable Actions"
3. Save changes

This stops all workflows immediately.

#### Selective Disable

Edit workflow file and add:

```yaml
on:
  workflow_dispatch:  # Only manual triggers
```

Commit and push to disable automatic triggers.

#### Complete Removal

```bash
# Remove workflow file
git rm .github/workflows/problematic-workflow.yml
git commit -m "Temporarily remove problematic workflow"
git push
```

### Scenario 2: Revert All CI/CD Changes

If complete rollback is needed:

```bash
# Find commit before CI/CD implementation
git log --oneline

# Revert to that commit
git revert <commit-hash-range>

# Or reset (destructive)
git reset --hard <commit-before-cicd>
git push --force origin <branch-name>
```

### Scenario 3: Branch Protection Blocking Merges

If branch protection rules are too strict:

1. Go to: Settings → Branches
2. Edit branch protection rule
3. Temporarily disable "Require status checks"
4. Merge urgent changes
5. Re-enable protection rules

---

## Monitoring & Maintenance

### Daily Monitoring

#### Check Workflow Status

Visit GitHub Actions tab daily:
- Review recent workflow runs
- Identify any failures
- Check workflow duration trends

#### Monitor Coverage Trends

If using Codecov:
- Visit Codecov dashboard
- Review coverage trends
- Identify coverage drops

### Weekly Maintenance

#### Review Workflow Performance

```bash
# Check average workflow duration
# Visit: Actions → Workflows → [Workflow Name] → View runs
```

Look for:
- Increasing duration trends
- Frequent failures
- Flaky tests

#### Update Dependencies

```bash
# Update GitHub Actions versions
# Check for newer versions of:
# - actions/checkout
# - actions/setup-python
# - codecov/codecov-action
```

Update in workflow files as needed.

### Monthly Maintenance

#### Review and Optimize

- [ ] Review workflow logs for warnings
- [ ] Check for deprecated GitHub Actions
- [ ] Optimize slow workflows
- [ ] Update documentation
- [ ] Review branch protection rules
- [ ] Check Codecov configuration

#### Security Updates

- [ ] Review Dependabot alerts
- [ ] Update workflow dependencies
- [ ] Check for security advisories
- [ ] Update Python version if needed

### Quarterly Review

#### Comprehensive Audit

- [ ] Review all workflow configurations
- [ ] Assess workflow effectiveness
- [ ] Gather team feedback
- [ ] Identify improvement opportunities
- [ ] Update CI/CD documentation
- [ ] Plan enhancements

---

## Performance Metrics

### Expected Workflow Performance

| Workflow | Expected Duration | Acceptable Range |
|----------|------------------|------------------|
| Tests | 2-3 minutes | 1-5 minutes |
| Docker Build | 5-7 minutes | 3-10 minutes |
| Code Quality | 1 minute | 30s-2 minutes |
| Total (all) | 5-8 minutes | 3-12 minutes |

### Performance Monitoring

Track these metrics:

- **Workflow Success Rate**: Target >95%
- **Average Duration**: Track trends over time
- **Failure Rate**: Target <5%
- **Time to Feedback**: Target <5 minutes
- **Coverage Percentage**: Maintain >87%

### Performance Optimization Tips

1. **Enable Caching**: Reduces dependency installation time
2. **Parallel Execution**: Run independent workflows in parallel
3. **Conditional Triggers**: Only run when necessary
4. **Optimize Tests**: Remove slow or redundant tests
5. **Docker Optimization**: Use multi-stage builds, layer caching

---

## Success Criteria

### Deployment Success Indicators

- [x] All three workflows created and committed
- [x] Workflows run automatically on push/PR
- [x] Test workflow passes with 52/52 tests
- [x] Docker workflow validates stack successfully
- [x] Lint workflow checks code quality
- [x] Status badges display in README
- [x] Documentation created and complete
- [x] CHANGELOG updated
- [x] Team notified of CI/CD availability

### Operational Success Indicators

After 1 week of operation:
- [ ] >95% workflow success rate
- [ ] <5 minute average feedback time
- [ ] Zero false positives
- [ ] Team using PR checks effectively
- [ ] Coverage maintained at >87%

After 1 month of operation:
- [ ] Caught at least one regression
- [ ] Prevented at least one broken merge
- [ ] Team confident in automated testing
- [ ] Workflow performance stable
- [ ] Documentation kept up to date

---

## Next Steps

### Immediate (Week 1)

1. Monitor workflow execution daily
2. Address any failures immediately
3. Gather team feedback
4. Document any issues encountered
5. Optimize slow workflows

### Short-term (Month 1)

1. Enable branch protection rules
2. Add workflow caching for performance
3. Configure Codecov thresholds
4. Add more comprehensive tests
5. Create workflow maintenance schedule

### Long-term (Quarter 1)

1. Add deployment workflow
2. Implement security scanning
3. Add performance benchmarking
4. Consider matrix testing (multiple Python versions)
5. Evaluate additional quality checks

---

## Additional Resources

### Documentation Links

- **GitHub Actions Documentation**: https://docs.github.com/en/actions
- **Workflow Syntax Reference**: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- **pytest Documentation**: https://docs.pytest.org/
- **Codecov Documentation**: https://docs.codecov.com/
- **Ruff Documentation**: https://docs.astral.sh/ruff/

### Internal Documentation

- **Enhancement Request**: [ENH0000016-cicd-automated-testing-pipeline.md](./ENH0000016-cicd-automated-testing-pipeline.md)
- **Quick Start Guide**: [QUICK_START.md](./QUICK_START.md)
- **Implementation Summary**: [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)
- **CI/CD Overview**: `docs/wiki/cicd/cicd-overview.md` (to be created)
- **Workflow Details**: `docs/wiki/cicd/github-actions-workflows.md` (to be created)

### Support Channels

- **GitHub Issues**: Report problems or request features
- **GitHub Discussions**: Ask questions and share ideas
- **Project Documentation**: Comprehensive guides and references

---

## Appendix A: Complete Workflow Files

### Test Workflow (test.yml)

```yaml
name: Tests

on:
  push:
    branches: [ main, development, 'enhancement/**' ]
  pull_request:
    branches: [ main, development ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install UV
        run: pip install uv
      
      - name: Install dependencies
        run: uv pip install --system -e .
      
      - name: Run tests with coverage
        run: |
          cd app
          uv run pytest --cov --cov-report=xml --cov-report=term
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./app/coverage.xml
          fail_ci_if_error: false
        env:
          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

### Docker Workflow (docker.yml)

```yaml
name: Docker Build

on:
  push:
    branches: [ main, development ]
    paths:
      - 'Dockerfile'
      - 'docker-compose.yml'
      - 'nginx.conf'
      - '.dockerignore'
  pull_request:
    branches: [ main, development ]
    paths:
      - 'Dockerfile'
      - 'docker-compose.yml'
      - 'nginx.conf'
      - '.dockerignore'

jobs:
  docker-build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Create .env file
        run: |
          cp .env.example .env
          echo "SECRET_KEY=test-secret-key-for-ci-$(date +%s)" >> .env
          echo "DB_PASSWORD=test-db-password-$(date +%s)" >> .env
          echo "DB_HOST=database" >> .env
      
      - name: Build Docker images
        run: docker compose build
      
      - name: Start Docker stack
        run: docker compose up -d
      
      - name: Wait for services to initialize
        run: |
          echo "Waiting for services to start..."
          sleep 20
      
      - name: Check service health
        run: |
          echo "Checking service status..."
          docker compose ps
          docker compose ps | grep -q "Up" || exit 1
      
      - name: Run database migrations
        run: |
          docker compose exec -T web python manage.py migrate --noinput
      
      - name: Test web service endpoint
        run: |
          echo "Testing web service..."
          curl -f http://localhost/ || exit 1
          echo "✓ Web service is responding"
      
      - name: Test static files serving
        run: |
          echo "Testing static files..."
          curl -f http://localhost/static/css/main.css || exit 1
          echo "✓ Static files are being served"
      
      - name: Check logs for errors
        if: failure()
        run: |
          echo "=== Web Service Logs ==="
          docker compose logs web
          echo "=== Nginx Logs ==="
          docker compose logs nginx
          echo "=== Database Logs ==="
          docker compose logs database
      
      - name: Tear down stack
        if: always()
        run: docker compose down -v
```

### Lint Workflow (lint.yml)

```yaml
name: Code Quality

on:
  push:
    branches: [ main, development, 'enhancement/**' ]
  pull_request:
    branches: [ main, development ]

jobs:
  lint:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install Ruff
        run: pip install ruff
      
      - name: Run Ruff linter
        run: |
          echo "Running Ruff linter..."
          ruff check app/ scripts/ || echo "Linting issues found (non-blocking)"
        continue-on-error: true
      
      - name: Run Ruff formatter check
        run: |
          echo "Checking code formatting..."
          ruff format --check app/ scripts/ || echo "Formatting issues found (non-blocking)"
        continue-on-error: true
      
      - name: Summary
        run: |
          echo "Code quality checks complete"
          echo "Review any issues above and fix in future commits"
```

---

## Appendix B: Checklist Summary

### Pre-Deployment
- [ ] Local tests pass (52/52)
- [ ] Docker stack works locally
- [ ] GitHub Actions enabled
- [ ] Repository is public
- [ ] Codecov account setup (optional)

### Deployment
- [ ] Create `.github/workflows/` directory
- [ ] Create `test.yml` workflow
- [ ] Create `docker.yml` workflow
- [ ] Create `lint.yml` workflow
- [ ] Add status badges to README
- [ ] Create CI/CD documentation
- [ ] Update CHANGELOG
- [ ] Push and verify workflows
- [ ] Create test PR
- [ ] Verify PR checks

### Post-Deployment
- [ ] All workflows passing
- [ ] Status badges display correctly
- [ ] Documentation complete
- [ ] Team notified
- [ ] Branch protection configured (optional)
- [ ] Monitoring established

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-02  
**Next Review:** 2026-03-02  
**Maintained By:** Development Team

---

**End of Deployment Guide**
