# ENH-0000016 Quick Start Guide

**Enhancement:** CI/CD Pipeline for Automated Testing  
**Time Required:** 4-6 hours  
**Difficulty:** Medium

---

## What You'll Build

Three GitHub Actions workflows that automatically:
1. Run tests on every push/PR
2. Validate Docker builds
3. Check code quality

---

## Prerequisites

- GitHub repository (already have: se2-calculator-project)
- GitHub account with push access
- Basic understanding of YAML
- Optional: Codecov account (free for open source)

---

## Implementation Steps

### Step 1: Create Workflows Directory (2 minutes)
```bash
mkdir -p .github/workflows
```

### Step 2: Create Test Workflow (30 minutes)
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
```

### Step 3: Create Docker Workflow (45 minutes)
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
          echo "SECRET_KEY=test-secret-key-for-ci" >> .env
          echo "DB_PASSWORD=test-db-password" >> .env
      
      - name: Build Docker images
        run: docker compose build
      
      - name: Start Docker stack
        run: docker compose up -d
      
      - name: Wait for services
        run: sleep 15
      
      - name: Check service health
        run: docker compose ps
      
      - name: Test web service
        run: |
          curl -f http://localhost/ || exit 1
          echo "Web service is responding"
      
      - name: Test static files
        run: |
          curl -f http://localhost/static/css/main.css || exit 1
          echo "Static files are being served"
      
      - name: Check logs for errors
        if: failure()
        run: docker compose logs
      
      - name: Tear down
        if: always()
        run: docker compose down -v
```

### Step 4: Create Lint Workflow (30 minutes)
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
        run: ruff check app/ scripts/
        continue-on-error: true
      
      - name: Run Ruff formatter check
        run: ruff format --check app/ scripts/
        continue-on-error: true
```

### Step 5: Add Status Badges (15 minutes)
Update `README.md` at the top:

```markdown
# Space Engineers 2 Calculator Project

![Tests](https://github.com/crashtechie/se2-calculator-project/workflows/Tests/badge.svg)
![Docker Build](https://github.com/crashtechie/se2-calculator-project/workflows/Docker%20Build/badge.svg)
![Code Quality](https://github.com/crashtechie/se2-calculator-project/workflows/Code%20Quality/badge.svg)

**Version:** 0.6.0-alpha
```

### Step 6: Test Workflows (1 hour)
```bash
# Commit and push workflows
git add .github/workflows/
git commit -m "Add CI/CD workflows for automated testing"
git push

# Check GitHub Actions tab to see workflows run
# Visit: https://github.com/crashtechie/se2-calculator-project/actions
```

### Step 7: Create Documentation (1 hour)
Create `docs/wiki/cicd/cicd-overview.md` with:
- Overview of CI/CD pipeline
- Description of each workflow
- How to interpret results
- Troubleshooting guide

### Step 8: Update CHANGELOG (15 minutes)
Add to `CHANGELOG.md`:

```markdown
## [0.7.0-alpha] - 2026-02-XX

### Added - CI/CD Pipeline
- **ENH-0000016:** CI/CD Pipeline for Automated Testing
  - GitHub Actions workflow for automated testing
  - Docker build validation workflow
  - Code quality and linting workflow
  - Workflow status badges in README
  - CI/CD documentation
```

---

## Testing Your Workflows

### Test 1: Push to Branch
```bash
git checkout -b test/cicd-workflows
git push origin test/cicd-workflows
```
Check GitHub Actions tab - all workflows should run.

### Test 2: Create Pull Request
Create PR from test branch to main.
Check PR page - should show workflow status checks.

### Test 3: Intentional Failure
Break a test, push, verify workflow fails.
Fix test, push, verify workflow passes.

---

## Expected Results

After implementation:
- ✅ Tests run automatically on every push
- ✅ PR checks show test status
- ✅ Coverage reports generated
- ✅ Docker builds validated
- ✅ Code quality checked
- ✅ Status badges show in README

---

## Troubleshooting

### Workflow Not Running
- Check workflow file syntax (YAML is indentation-sensitive)
- Verify branch names match trigger conditions
- Check GitHub Actions tab for errors

### Tests Failing in CI but Pass Locally
- Check Python version (must be 3.13)
- Check environment variables
- Check database setup
- Review workflow logs

### Docker Build Failing
- Verify .env.example exists
- Check Docker file paths in workflow
- Review Docker logs in workflow output

---

## Time Breakdown

| Task | Time |
|------|------|
| Create workflows directory | 2 min |
| Create test workflow | 30 min |
| Create Docker workflow | 45 min |
| Create lint workflow | 30 min |
| Add status badges | 15 min |
| Test workflows | 1 hour |
| Create documentation | 1 hour |
| Update CHANGELOG | 15 min |
| **Total** | **4-6 hours** |

---

## Success Checklist

- [ ] `.github/workflows/test.yml` created
- [ ] `.github/workflows/docker.yml` created
- [ ] `.github/workflows/lint.yml` created
- [ ] Status badges added to README
- [ ] All workflows tested and passing
- [ ] Documentation created
- [ ] CHANGELOG updated
- [ ] Team notified of CI/CD availability

---

## Next Steps After Implementation

1. Monitor workflow performance
2. Optimize slow workflows
3. Add branch protection rules (require checks to pass)
4. Consider adding more checks (security scanning, etc.)
5. Document workflow maintenance procedures

---

## Support

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Workflow Syntax:** https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- **Enhancement Document:** [ENH0000016-cicd-automated-testing-pipeline.md](./ENH0000016-cicd-automated-testing-pipeline.md)

---

**Created:** 2026-02-02  
**Version:** 1.0
