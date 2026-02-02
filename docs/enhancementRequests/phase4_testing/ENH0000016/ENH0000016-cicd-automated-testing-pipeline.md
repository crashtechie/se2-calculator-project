# ENH-0000016: CI/CD Pipeline for Automated Testing

**Enhancement ID:** ENH-0000016  
**Status:** Planned  
**Priority:** High  
**Created Date:** 2026-02-02  
**Updated Date:** 2026-02-02  
**Completion Date:** (pending)  
**Assigned To:** (pending)  
**Estimated Effort:** 4-6 hours

---

## Summary

Implement GitHub Actions CI/CD pipeline with automated testing, Docker build validation, and code quality checks to ensure code quality and prevent regressions on every push and pull request.

---

## Description

This enhancement adds continuous integration and continuous deployment (CI/CD) capabilities to the project using GitHub Actions. The pipeline will automatically run tests, validate Docker builds, and perform code quality checks whenever code is pushed to the repository or a pull request is created.

**Current Gap:** All testing and validation is currently manual, requiring developers to remember to run `uv run pytest` before pushing code. There are no automated quality gates to prevent broken code from being merged.

**Solution:** Implement three GitHub Actions workflows that automatically validate code quality, run the full test suite, and verify Docker builds on every push and pull request.

**Benefits:**
- Catch breaking changes before they reach main branch
- Enforce 87% test coverage standard automatically
- Validate Docker configuration changes immediately
- Reduce manual testing overhead for developers
- Provide immediate feedback on PRs with test results and coverage reports
- Prevent regressions during Phase 3 and Phase 4 development
- Establish quality gates for production readiness

---

## Current Behavior

- Developers manually run `uv run pytest` to execute tests
- Docker builds are manually validated with `docker compose build`
- No automated checks on push or pull request
- Code quality and style consistency relies on manual review
- Test coverage is manually checked with `pytest --cov`
- No automated feedback on PRs

---

## Proposed Behavior

After implementation:
- Every push to any branch triggers automated test suite
- Every pull request shows test results and coverage in PR checks
- Docker builds are automatically validated on infrastructure changes
- Code quality checks run automatically with clear pass/fail status
- Failed checks block PR merges (configurable)
- Coverage reports are automatically generated and tracked
- Developers receive immediate feedback on code quality issues

---

## Acceptance Criteria

- [ ] GitHub Actions workflow for automated testing created and functional
- [ ] Tests run automatically on every push to any branch
- [ ] Tests run automatically on every pull request
- [ ] Test results visible in GitHub PR checks
- [ ] Coverage reports generated and uploaded to Codecov (or similar)
- [ ] Docker build validation workflow created and functional
- [ ] Docker workflow validates full stack (web + nginx + database)
- [ ] Code quality/linting workflow created and functional
- [ ] All workflows use Python 3.13
- [ ] All workflows use UV package manager
- [ ] Workflow status badges added to README.md
- [ ] Documentation created for CI/CD pipeline
- [ ] All three workflows tested and passing

---

## Technical Details

### Dependencies
- GitHub Actions (no cost for public repositories)
- Python 3.13
- UV package manager
- Docker and Docker Compose
- Optional: Codecov account for coverage tracking (free for open source)
- Optional: Ruff for linting (already compatible with project)

### Affected Components
- `.github/workflows/` directory (new)
- `README.md` (add status badges)
- Documentation (new CI/CD guide)

### Files to Modify/Create

**New Files:**
- `.github/workflows/test.yml` - Automated testing workflow
- `.github/workflows/docker.yml` - Docker build validation workflow
- `.github/workflows/lint.yml` - Code quality and linting workflow
- `docs/wiki/cicd/cicd-overview.md` - CI/CD documentation
- `docs/wiki/cicd/github-actions-workflows.md` - Workflow documentation

**Modified Files:**
- `README.md` - Add workflow status badges
- `.gitignore` - Ensure workflow artifacts are ignored if needed

### Database Changes
- [ ] No migrations required
- [ ] No new models
- [ ] No schema changes

---

## Implementation Plan

### Step 1: Create Automated Testing Workflow
**Priority: Critical - Implement First**

Create `.github/workflows/test.yml` with:
- Trigger on push and pull_request events
- Use Ubuntu latest runner
- Checkout code
- Setup Python 3.13
- Install UV package manager
- Install project dependencies with UV
- Run pytest with coverage
- Upload coverage report to Codecov (optional)
- Generate coverage badge

**Configuration:**
```yaml
name: Tests
on:
  push:
    branches: [main, development, 'enhancement/**']
  pull_request:
    branches: [main, development]

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

### Step 2: Create Docker Build Validation Workflow
**Priority: High - Implement Second**

Create `.github/workflows/docker.yml` with:
- Trigger on push to main/development and PRs that modify Docker files
- Build Docker images
- Start Docker Compose stack
- Wait for services to be healthy
- Run basic health checks (curl endpoints)
- Verify database connectivity
- Verify static files are served
- Tear down stack

**Configuration:**
```yaml
name: Docker Build
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

### Step 3: Create Code Quality Workflow
**Priority: Medium - Implement Third**

Create `.github/workflows/lint.yml` with:
- Trigger on push and pull_request
- Run Ruff linter for Python code quality
- Check for common issues (unused imports, undefined names, etc.)
- Optional: Add Black for code formatting checks
- Optional: Add mypy for type checking

**Configuration:**
```yaml
name: Code Quality
on:
  push:
    branches: [main, development, 'enhancement/**']
  pull_request:
    branches: [main, development]

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

### Step 4: Add Workflow Status Badges to README
Update `README.md` to include status badges at the top:

```markdown
# Space Engineers 2 Calculator Project

![Tests](https://github.com/crashtechie/se2-calculator-project/workflows/Tests/badge.svg)
![Docker Build](https://github.com/crashtechie/se2-calculator-project/workflows/Docker%20Build/badge.svg)
![Code Quality](https://github.com/crashtechie/se2-calculator-project/workflows/Code%20Quality/badge.svg)
[![codecov](https://codecov.io/gh/crashtechie/se2-calculator-project/branch/main/graph/badge.svg)](https://codecov.io/gh/crashtechie/se2-calculator-project)
```

### Step 5: Create CI/CD Documentation
Create comprehensive documentation:
- Overview of CI/CD pipeline
- Description of each workflow
- How to interpret workflow results
- How to debug failed workflows
- How to add new workflows
- Best practices for CI/CD

### Step 6: Test Workflows
- Create test branch
- Push code to trigger workflows
- Verify all workflows run successfully
- Create test PR to verify PR checks
- Intentionally break a test to verify failure detection
- Fix and verify workflow passes

### Step 7: Configure Branch Protection (Optional)
Configure GitHub repository settings:
- Require status checks to pass before merging
- Require test workflow to pass
- Require Docker workflow to pass (for infrastructure changes)
- Require code quality checks to pass

---

## Testing Requirements

### Workflow Testing (Manual)
- [ ] Test workflow runs on push to main branch
- [ ] Test workflow runs on push to development branch
- [ ] Test workflow runs on push to enhancement branches
- [ ] Test workflow runs on pull request creation
- [ ] Test workflow runs on pull request update
- [ ] Verify test results appear in PR checks
- [ ] Verify coverage report is generated
- [ ] Verify Docker build workflow triggers on Dockerfile changes
- [ ] Verify Docker build workflow triggers on docker-compose.yml changes
- [ ] Verify lint workflow detects code quality issues
- [ ] Test workflow failure scenarios (intentionally break a test)
- [ ] Verify workflow status badges display correctly in README

### Integration Testing
- [ ] All three workflows run in parallel without conflicts
- [ ] Workflows complete in reasonable time (<5 minutes for tests)
- [ ] Workflows use appropriate caching to speed up runs
- [ ] Workflow artifacts are properly stored (coverage reports)

### Documentation Testing
- [ ] CI/CD documentation is clear and complete
- [ ] Workflow documentation includes troubleshooting steps
- [ ] README badges link to correct workflow runs

---

## Deliverables

- [ ] `.github/workflows/test.yml` - Automated testing workflow
- [ ] `.github/workflows/docker.yml` - Docker build validation workflow
- [ ] `.github/workflows/lint.yml` - Code quality workflow
- [ ] Updated README.md with workflow status badges
- [ ] CI/CD documentation (`docs/wiki/cicd/`)
- [ ] All workflows tested and passing
- [ ] Deployment guide for CI/CD setup
- [ ] CHANGELOG.md updated

---

## Documentation Updates

- [ ] README.md - Add workflow status badges and CI/CD section
- [ ] CHANGELOG.md - Document CI/CD implementation
- [ ] Create `docs/wiki/cicd/cicd-overview.md`
- [ ] Create `docs/wiki/cicd/github-actions-workflows.md`
- [ ] Create `docs/wiki/cicd/troubleshooting-workflows.md`
- [ ] Update CONTRIBUTING.md with CI/CD workflow information

---

## Risks and Considerations

### Risk 1: GitHub Actions Minutes Limit
**Description:** Free GitHub accounts have limited Actions minutes per month  
**Mitigation:** 
- Project is open source (unlimited minutes for public repos)
- Optimize workflows to run quickly (<5 minutes)
- Use caching to reduce build times
- Only run Docker workflow on infrastructure changes

### Risk 2: Test Flakiness
**Description:** Flaky tests could cause false failures in CI  
**Mitigation:**
- Current test suite is stable (52/52 passing consistently)
- Use `--reuse-db` flag to speed up tests
- Add retry logic for network-dependent tests if needed
- Monitor workflow failures and fix flaky tests immediately

### Risk 3: Docker Build Time
**Description:** Docker builds can be slow, increasing workflow time  
**Mitigation:**
- Only run Docker workflow on infrastructure file changes
- Use Docker layer caching in GitHub Actions
- Consider using pre-built base images
- Run Docker workflow less frequently than test workflow

### Risk 4: Coverage Report Integration
**Description:** Codecov integration requires account setup  
**Mitigation:**
- Make Codecov optional (workflow continues if upload fails)
- Can use GitHub Actions artifacts for coverage reports
- Alternative: Use Coveralls or similar service
- Can generate coverage reports locally without external service

### Risk 5: Workflow Maintenance
**Description:** Workflows need updates as project evolves  
**Mitigation:**
- Document workflow structure clearly
- Use workflow templates for consistency
- Review workflows during each phase
- Keep workflows simple and focused

---

## Alternatives Considered

### Alternative 1: GitLab CI/CD
**Rejected:** Project is hosted on GitHub; GitHub Actions is native and well-integrated

### Alternative 2: Jenkins
**Rejected:** Requires self-hosted infrastructure; GitHub Actions is simpler and free for open source

### Alternative 3: Travis CI
**Rejected:** GitHub Actions has better integration and is more actively maintained

### Alternative 4: CircleCI
**Rejected:** GitHub Actions is sufficient for project needs and has no additional cost

### Alternative 5: Manual Testing Only
**Rejected:** Manual testing is error-prone and doesn't scale; automated testing is industry standard

---

## Related Issues/Enhancements

- **Enables:** All future enhancements (provides quality gates)
- **Recommended By:** Phase 2 Post-Deployment Report (PHASE2-POST-DEPLOYMENT-REPORT.md)
- **Supports:** ENH-0000010 (Build Order Views) - Will catch regressions
- **Supports:** ENH-0000011 (Dynamic Block Selector) - Will validate UI changes
- **Prepares For:** Phase 4 (Testing & Polish) - Establishes CI/CD foundation

---

## Notes

### Implementation Timing
**Recommendation:** Implement before starting ENH-0000010 (Build Order Views)
- Phase 3 will involve significant new code
- Automated testing will catch regressions early
- Provides safety net for complex calculator logic
- Establishes quality gates before production readiness

### Workflow Optimization
- Use caching for Python dependencies to speed up workflows
- Consider matrix testing for multiple Python versions (future)
- Add workflow dispatch triggers for manual runs
- Use concurrency groups to cancel outdated workflow runs

### Future Enhancements
- Add deployment workflow for production releases
- Add automated version bumping and changelog generation
- Add security scanning (Dependabot, CodeQL)
- Add performance benchmarking in CI
- Add visual regression testing for UI changes

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-02 | Planned | Initial creation based on Phase 2 recommendations |

---

## Sign-off

**Reviewed By:** (pending)  
**Approved By:** (pending)  
**Completed By:** (pending)  
**Completion Date:** (pending)

---

## Completion Notes

(To be filled in when enhancement is completed)

### Achievements
- List key accomplishments
- Highlight workflow performance metrics
- Note any unexpected benefits

### Deliverables
1. Three GitHub Actions workflows (test, docker, lint)
2. Workflow status badges in README
3. Complete CI/CD documentation
4. All workflows tested and passing

### Workflow Performance
- ✅ Test workflow: X minutes average
- ✅ Docker workflow: X minutes average
- ✅ Lint workflow: X minutes average
- ✅ Total CI time: X minutes per push

### Documentation
- ENH-0000016-deployment-guide.md
- docs/wiki/cicd/cicd-overview.md
- docs/wiki/cicd/github-actions-workflows.md
- docs/wiki/cicd/troubleshooting-workflows.md

### Next Steps
- Monitor workflow performance and optimize as needed
- Add additional quality checks as project matures
- Consider deployment automation for production releases
