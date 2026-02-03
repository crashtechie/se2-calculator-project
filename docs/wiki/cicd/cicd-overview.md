# CI/CD Pipeline Overview

**Last Updated:** 2026-02-02  
**Enhancement:** ENH-0000016  
**Status:** Active

---

## Table of Contents

1. [Introduction](#introduction)
2. [Pipeline Purpose](#pipeline-purpose)
3. [Benefits](#benefits)
4. [Workflow Overview](#workflow-overview)
5. [How to Interpret Results](#how-to-interpret-results)
6. [Quick Reference](#quick-reference)
7. [Related Documentation](#related-documentation)

---

## Introduction

The SE2 Calculator Project uses GitHub Actions to provide automated continuous integration and continuous deployment (CI/CD) capabilities. This pipeline automatically tests, validates, and checks code quality for every change pushed to the repository.

### What is CI/CD?

**Continuous Integration (CI)** is the practice of automatically building and testing code changes as they are committed. This helps catch bugs early and ensures that new code integrates well with existing code.

**Continuous Deployment (CD)** is the practice of automatically deploying code changes to production environments after they pass all tests and checks.

Our current implementation focuses on CI, with CD capabilities planned for future phases.

---

## Pipeline Purpose

The CI/CD pipeline serves several critical purposes:

### 1. Automated Quality Assurance
- Runs comprehensive test suite on every code change
- Validates Docker infrastructure builds correctly
- Checks code quality and formatting standards
- Prevents broken code from being merged

### 2. Early Bug Detection
- Catches issues before they reach production
- Identifies integration problems immediately
- Validates changes across different environments
- Reduces debugging time and effort

### 3. Development Velocity
- Provides immediate feedback on code changes
- Reduces manual testing burden
- Enables confident refactoring
- Supports rapid iteration

### 4. Team Collaboration
- Ensures consistent code quality across contributors
- Provides visibility into build status
- Facilitates code review process
- Documents test results for each change

---

## Benefits

### For Developers

- **Immediate Feedback**: Know within minutes if your changes break anything
- **Confidence**: Refactor and improve code without fear
- **Time Savings**: Automated testing replaces manual verification
- **Learning**: See how your changes affect the entire system

### For the Project

- **Quality Assurance**: Maintain high code quality standards
- **Stability**: Prevent regressions and breaking changes
- **Documentation**: Test results serve as living documentation
- **Professionalism**: Demonstrates mature development practices

### For Users

- **Reliability**: Fewer bugs reach production
- **Faster Features**: Developers can move faster with confidence
- **Transparency**: Build status visible via badges
- **Trust**: Professional development practices inspire confidence

---

## Workflow Overview

Our CI/CD pipeline consists of three main workflows:

### 1. Tests Workflow

**Purpose**: Run the complete pytest test suite with coverage reporting

**Triggers**:
- Push to `main`, `development`, or `enhancement/**` branches
- Pull requests to `main` or `development`

**What it does**:
- Sets up Python 3.13 environment
- Installs dependencies using UV package manager
- Runs all 107+ tests
- Generates coverage report (target: 87%+)
- Uploads coverage to Codecov (optional)

**Duration**: ~2-3 minutes

**Status Badge**: ![Tests](https://github.com/crashtechie/se2-calculator-project/actions/workflows/test.yml/badge.svg)

### 2. Docker Build Workflow

**Purpose**: Validate Docker infrastructure builds and runs correctly

**Triggers**:
- Push to `main` or `development` (only when Docker files change)
- Pull requests to `main` or `development` (only when Docker files change)

**Monitored Files**:
- `Dockerfile`
- `docker-compose.yml`
- `nginx.conf`
- `.dockerignore`

**What it does**:
- Builds Docker images for web, nginx, and database services
- Starts the complete Docker Compose stack
- Runs database migrations
- Tests web service endpoints
- Validates static file serving
- Tears down stack cleanly

**Duration**: ~5-7 minutes

**Status Badge**: ![Docker Build](https://github.com/crashtechie/se2-calculator-project/actions/workflows/docker.yml/badge.svg)

### 3. Code Quality Workflow

**Purpose**: Check code quality and formatting standards

**Triggers**:
- Push to `main`, `development`, or `enhancement/**` branches
- Pull requests to `main` or `development`

**What it does**:
- Runs Ruff linter on Python code
- Checks code formatting standards
- Reports issues (non-blocking)
- Provides quality feedback

**Duration**: ~1 minute

**Status Badge**: ![Code Quality](https://github.com/crashtechie/se2-calculator-project/actions/workflows/lint.yml/badge.svg)

---

## How to Interpret Results

### Workflow Status Indicators

#### ✅ Green Checkmark (Success)
- All tests passed
- All checks completed successfully
- Code is ready to merge

#### ❌ Red X (Failure)
- One or more tests failed
- Build or validation errors occurred
- Code needs fixes before merging

#### 🟡 Yellow Dot (In Progress)
- Workflow is currently running
- Wait for completion before merging

#### ⚪ Gray Circle (Skipped)
- Workflow did not run (e.g., Docker workflow when no Docker files changed)
- This is normal and expected

#### ⏸️ Gray Dash (Cancelled)
- Workflow was manually cancelled
- May need to re-run

### Reading Workflow Logs

1. **Click on the workflow status** in your PR or commit
2. **Select the failed job** to see detailed logs
3. **Expand failed steps** to see error messages
4. **Look for red text** indicating failures
5. **Check the summary** at the bottom for quick overview

### Common Status Messages

**"All checks have passed"**
- ✅ Your code is good to merge
- All tests passed, quality checks passed

**"Some checks were not successful"**
- ❌ Review the failed checks
- Click details to see what failed
- Fix issues and push again

**"Waiting for status to be reported"**
- 🟡 Workflow is queued or running
- Be patient, usually completes in <10 minutes

---

## Quick Reference

### Workflow Execution Times

| Workflow | Average Duration | Max Duration |
|----------|-----------------|--------------|
| Tests | 2-3 minutes | 5 minutes |
| Docker Build | 5-7 minutes | 10 minutes |
| Code Quality | 1 minute | 2 minutes |
| **Total** | **3-8 minutes** | **15 minutes** |

### When Workflows Run

| Event | Tests | Docker | Lint |
|-------|-------|--------|------|
| Push to `main` | ✅ | ✅* | ✅ |
| Push to `development` | ✅ | ✅* | ✅ |
| Push to `enhancement/**` | ✅ | ❌ | ✅ |
| PR to `main` | ✅ | ✅* | ✅ |
| PR to `development` | ✅ | ✅* | ✅ |

*Only runs if Docker-related files changed

### Key Technologies

- **Python**: 3.13
- **Package Manager**: UV (fast, modern Python package manager)
- **Test Framework**: pytest with pytest-django
- **Coverage Tool**: pytest-cov + Codecov
- **Linter**: Ruff (fast Python linter and formatter)
- **Container Platform**: Docker + Docker Compose
- **CI Platform**: GitHub Actions

---

## Related Documentation

### Detailed Documentation

- **[GitHub Actions Workflows](./github-actions-workflows.md)** - Detailed workflow documentation
- **[Troubleshooting Guide](./troubleshooting-workflows.md)** - Common issues and solutions
- **[Deployment Guide](../../enhancementRequests/phase4_testing/ENH0000016/ENH0000016-deployment-guide.md)** - Complete deployment instructions

### External Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [Docker Documentation](https://docs.docker.com/)

### Project Documentation

- [README.md](../../../README.md) - Project overview with status badges
- [CONTRIBUTING.md](../../../CONTRIBUTING.md) - Contribution guidelines
- [CHANGELOG.md](../../../CHANGELOG.md) - Version history

---

## Getting Help

### If Workflows Fail

1. **Check the logs** - Click on the failed workflow to see details
2. **Review the error message** - Look for specific failure reasons
3. **Test locally** - Run the same commands on your machine
4. **Consult troubleshooting guide** - See [troubleshooting-workflows.md](./troubleshooting-workflows.md)
5. **Ask for help** - Open an issue or ask in team chat

### If You Need to Re-run a Workflow

1. Go to the "Actions" tab in GitHub
2. Find the workflow run
3. Click "Re-run jobs" button
4. Select "Re-run all jobs" or specific failed jobs

### If Workflows Are Slow

- Check GitHub Actions status: https://www.githubstatus.com/
- Review workflow logs for bottlenecks
- Consider optimizing test suite or enabling caching
- Most workflows complete in <10 minutes

---

**Last Updated:** 2026-02-02  
**Maintained By:** Dan Smith (@crashtechie)  
**Questions?** Open an issue on GitHub
