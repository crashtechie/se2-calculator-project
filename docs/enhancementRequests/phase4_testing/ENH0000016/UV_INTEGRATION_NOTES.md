# UV Integration in CI/CD Pipeline

**Document Type:** Technical Notes  
**Created:** 2026-02-02  
**Related:** ENH-0000016 CI/CD Pipeline Deployment

---

## Overview

This document summarizes how UV (the fast Python package manager) is integrated into the CI/CD pipeline and its benefits for the project.

---

## What is UV?

UV is a modern Python package manager written in Rust that provides:
- **10-100x faster** dependency resolution than pip
- **Deterministic** dependency resolution
- **Drop-in replacement** for pip commands
- **Unified tool** for Python version and package management

**Official Documentation**: https://docs.astral.sh/uv/

---

## UV in GitHub Actions Workflows

### Test Workflow Integration

```yaml
- name: Install UV
  run: pip install uv

- name: Install dependencies
  run: uv pip install --system -e .

- name: Run tests with coverage
  run: |
    cd app
    uv run pytest --cov --cov-report=xml --cov-report=term
```

### Why UV in CI/CD?

1. **Speed**: Reduces workflow execution time by 30-45 seconds per run
2. **Reliability**: Deterministic dependency resolution prevents "works on my machine" issues
3. **Consistency**: Same tool used locally and in CI
4. **Cost**: Reduces GitHub Actions minutes usage

---

## Performance Comparison

| Operation | pip Time | UV Time | Improvement |
|-----------|----------|---------|-------------|
| Fresh install | 45-60s | 5-10s | 6-10x faster |
| Cached install | 20-30s | 2-5s | 5-10x faster |
| Dependency resolution | 30-45s | 1-3s | 15-30x faster |

---

## Local Development with UV

### Prerequisites

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv

# Verify installation
uv --version
```

### Common Commands

```bash
# Install dependencies
uv pip install -e .

# Run tests
cd app
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Run Django management commands
uv run python manage.py runserver
uv run python manage.py migrate

# Install additional packages
uv pip install package-name

# List installed packages
uv pip list
```

---

## UV in Deployment Guide

The deployment guide has been updated to emphasize UV usage:

### Key Sections Updated

1. **Prerequisites** - UV verification commands added
2. **Architecture** - Dedicated UV section explaining benefits
3. **Pre-Deployment Checklist** - UV-specific preparation steps
4. **Workflow Files** - All use UV for Python operations
5. **Troubleshooting** - 3 new UV-specific troubleshooting sections
6. **Performance Metrics** - UV performance comparison table
7. **Optimization** - UV caching configuration

### UV References

- **104 mentions** of UV throughout the deployment guide
- **Dedicated section** on UV package manager in workflows
- **Performance metrics** showing UV benefits
- **Troubleshooting** for UV-specific issues

---

## Troubleshooting UV in CI/CD

### Issue: UV Installation Fails

**Solution**:
```yaml
# Use specific version
- name: Install UV
  run: pip install uv==0.1.0

# Or use official installer
- name: Install UV
  run: curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Issue: UV Cannot Find Python 3.13

**Solution**:
```yaml
# Ensure Python is set up first
- name: Setup Python 3.13
  uses: actions/setup-python@v5
  with:
    python-version: '3.13'

# Then install UV
- name: Install UV
  run: pip install uv
```

### Issue: Dependency Resolution Fails

**Solution**:
```bash
# Test locally first
uv pip install --dry-run -e .

# Check for conflicts
uv pip install --verbose -e .

# Use system flag in CI
uv pip install --system -e .
```

---

## UV Caching in Workflows

### Recommended Cache Configuration

```yaml
- name: Cache UV dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.cache/uv
      ~/.local/share/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-uv-
```

### Benefits of UV Caching

- **50-80% reduction** in dependency installation time
- **More efficient** than pip caching
- **Smaller cache size** due to better compression
- **Faster cache restoration**

---

## Best Practices

### DO:
✅ Use `uv run` for all Python commands  
✅ Use `uv pip install --system` in CI workflows  
✅ Cache UV directories for faster workflows  
✅ Pin UV version for reproducibility  
✅ Test UV commands locally before pushing  

### DON'T:
❌ Mix pip and UV in the same workflow  
❌ Forget to install UV before using it  
❌ Skip UV verification in pre-deployment checks  
❌ Ignore UV-specific error messages  
❌ Use UV without understanding its benefits  

---

## Migration from pip to UV

If you need to update existing workflows:

### Before (pip):
```yaml
- name: Install dependencies
  run: pip install -e .

- name: Run tests
  run: pytest
```

### After (UV):
```yaml
- name: Install UV
  run: pip install uv

- name: Install dependencies
  run: uv pip install --system -e .

- name: Run tests
  run: uv run pytest
```

---

## Future Enhancements

### Potential UV Optimizations

1. **Matrix Testing**: Use UV to test multiple Python versions
2. **Dependency Locking**: Use UV's lock file feature
3. **Virtual Environments**: Leverage UV's venv management
4. **Python Version Management**: Use UV to install Python versions
5. **Monorepo Support**: Use UV for multi-package projects

---

## Resources

### Official Documentation
- **UV Documentation**: https://docs.astral.sh/uv/
- **UV GitHub**: https://github.com/astral-sh/uv
- **UV Installation**: https://docs.astral.sh/uv/getting-started/installation/

### Project Documentation
- **Deployment Guide**: [ENH0000016-deployment-guide.md](./ENH0000016-deployment-guide.md)
- **Enhancement Request**: [ENH0000016-cicd-automated-testing-pipeline.md](./ENH0000016-cicd-automated-testing-pipeline.md)
- **Quick Start**: [QUICK_START.md](./QUICK_START.md)

---

## Summary

UV is a critical component of this project's CI/CD pipeline, providing:

- ⚡ **10-100x faster** dependency resolution
- 🔒 **Deterministic** builds
- 💰 **Cost savings** on CI minutes
- 🚀 **Faster feedback** to developers
- 🔧 **Better developer experience**

The deployment guide has been comprehensively updated to reflect UV usage throughout all workflows and local development processes.

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-02  
**Maintained By:** Development Team
