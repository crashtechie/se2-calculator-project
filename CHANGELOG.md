# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### In Development
- Phase 3: Build Order Calculator (in progress)

## [0.7.0-alpha] - 2026-02-02

### Added - CI/CD Pipeline (ENH-0000016)
- **GitHub Actions workflow for automated testing**
  - Runs pytest suite on every push and PR
  - Executes 107+ tests with 87%+ coverage
  - Generates coverage reports in XML and terminal formats
  - Uploads coverage to Codecov (optional)
  - Uses UV package manager for fast dependency installation
  - Forces SQLite in CI for consistent test environment
  - Completes in ~2-3 minutes
- **Docker build validation workflow**
  - Validates Docker stack builds correctly
  - Tests service health and endpoints
  - Runs database migrations in containerized environment
  - Validates static file serving through nginx
  - Only runs on infrastructure file changes (Dockerfile, docker-compose.yml, nginx.conf, .dockerignore)
  - Includes comprehensive logging on failure
  - Automatic cleanup with volume removal
  - Completes in ~5-7 minutes
- **Code quality workflow**
  - Runs Ruff linter on Python code (app/ and scripts/)
  - Checks code formatting standards
  - Provides non-blocking quality feedback
  - Continues workflow even with linting issues
  - Completes in ~1 minute
- **Workflow status badges in README**
  - Tests badge with link to workflow runs
  - Docker Build badge with link to workflow runs
  - Code Quality badge with link to workflow runs
  - Codecov coverage badge (optional)
  - Real-time status visibility
- **Comprehensive CI/CD documentation**
  - Pipeline overview (docs/wiki/cicd/cicd-overview.md)
  - Detailed workflow documentation (docs/wiki/cicd/github-actions-workflows.md)
  - Troubleshooting guide (docs/wiki/cicd/troubleshooting-workflows.md)
  - Step-by-step deployment guide
  - Common issues and solutions
  - Local debugging instructions

### Changed
- **README.md:** Added workflow status badges at top of document
- **Development workflow:** Tests now run automatically on push
- **pyproject.toml:** Added pytest-cov>=6.0.0 dependency for coverage reporting
- **Code formatting:** Applied Ruff formatting to 54 Python files across codebase
- **Code quality:** Removed unused imports and fixed linting issues

### Technical Details
- All workflows use Python 3.13
- All workflows use UV package manager for fast dependency management
- Test workflow runs in ~2-3 minutes
- Docker workflow runs in ~5-7 minutes (conditional)
- Lint workflow runs in ~1 minute
- Total CI time: ~3-8 minutes depending on triggers
- Workflows trigger on push to main, development, and enhancement/** branches
- Pull requests to main and development trigger all applicable workflows
- Docker workflow uses path filters for efficiency
- Test workflow uses SQLite to avoid PostgreSQL dependency in CI
- All workflows include proper error handling and logging

### Benefits
- **Automated quality assurance:** Every code change is tested automatically
- **Early bug detection:** Issues caught before merge
- **Faster development:** Immediate feedback on changes
- **Team collaboration:** Consistent quality standards across contributors
- **Professional practices:** Industry-standard CI/CD implementation
- **Visibility:** Build status visible via badges and PR checks

### Fixed - Docker Infrastructure
- **ISSUE-013:** Nginx static files path mismatch in Docker environment
  - Fixed nginx.conf to serve static files from `/app/app/staticfiles/` instead of `/app/staticfiles/`
  - Removed conflicting `static_files` named volume mount that was creating empty directory
  - Updated nginx service to use project mount (`.:/app:ro`) for static file access
  - Removed unused `static_files` volume definition from docker-compose.yml
  - Fixed Dockerfile permissions: create appuser before staticfiles directory, set proper ownership
  - Run collectstatic as appuser instead of root to prevent PermissionError
  - Added explicit `collectstatic` step to CI/CD workflow for verification
  - Updated `.gitignore` to exclude generated `staticfiles/` directory
  - Root cause: Volume mount path mismatch with nested Django project structure + permission issues
  - Static files now serve correctly through nginx with 200 OK response
  - CI/CD Docker build workflow now passes static file serving test



## [0.6.1-alpha] - 2026-02-02

### Fixed - Docker Infrastructure
- **ISSUE-009:** Dockerfile manage.py path incorrect
  - Updated Dockerfile to reference `app/manage.py` instead of `manage.py`
  - Fixed collectstatic command path
  - Fixed CMD startup command path
  - Container now starts successfully with correct file paths
- **ISSUE-010:** Database credentials mismatch in Docker volume
  - Resolved PostgreSQL authentication failures
  - Documented volume recreation procedure for credential changes
  - Added prevention guidelines for future credential updates
- **ISSUE-011:** Health check Host header missing in nginx configuration
  - Added `proxy_set_header Host $host;` to nginx health check location
  - Health endpoint now returns correct JSON response
  - Docker health checks pass successfully
  - All containers marked as healthy
- **ISSUE-007:** Missing health endpoint (resolved)
  - Discovered health endpoint already existed in Django
  - Issue was nginx configuration, not missing endpoint
  - Cross-referenced with ISSUE-011 resolution
- **ISSUE-005:** Docker Compose warning "r" variable not set (resolved)
  - Spurious variable reference removed during password generation script cleanup
  - No more variable warnings during Docker operations
  - Clean startup output

### Changed
- Updated `.env` to include `django_app` in ALLOWED_HOSTS (for nginx upstream)
- Improved nginx.conf health check configuration
- Enhanced Docker documentation with troubleshooting guides

### Documentation
- Created comprehensive issue reports for all Docker-related problems:
  - ISSUE-005: Docker Compose warning resolved
  - ISSUE-007: Health endpoint issue resolved
  - ISSUE-009: Dockerfile path issue with full technical details
  - ISSUE-010: Database credentials with prevention guidelines
  - ISSUE-011: Nginx configuration with best practices
- All issue reports include root cause analysis, solutions, and verification steps
- Moved 5 issues from open to resolved status

## [0.6.0-alpha] - 2026-02-02

### Added - Phase 3 Start: Build Order Model
- **ENH-0000009:** Build Order Model & Core Logic
  - BuildOrder model with UUIDv7 primary key following Phase 1 patterns
  - JSONField for blocks storage using dict format {block_id: quantity}
  - Comprehensive validation methods (validate_blocks, get_block_objects, clean, save)
  - Calculation methods for resource aggregation:
    - `calculate_total_mass()` - sum block masses × quantities
    - `calculate_required_components()` - aggregate components across blocks
    - `calculate_required_ores()` - traverse components to ores
    - `calculate_fabricator_times()` - group by fabricator type
    - `get_calculation_summary()` - complete summary with all calculations
  - Helper methods for detailed data (_get_components_with_details, _get_ores_with_details)
  - Caching implementation with 5-minute TTL and automatic invalidation on save
  - Cache key format: `buildorder_calc_{order_id}`
  - Admin interface with custom display methods:
    - List display: name, blocks_count, total_mass, created_at, updated_at
    - Formatted JSON display for blocks
    - Complete calculation summary with tables
    - Validation status with visual indicators
  - Database migrations created and applied (0001_initial.py)
  - Registered in INSTALLED_APPS

### Testing
- Comprehensive test suite: **52 tests** (exceeds minimum of 50)
  - 5 Model Creation Tests (100% coverage)
  - 10 Validation Tests (100% coverage)
  - 17 Calculation Tests (100% coverage)
  - 10 Property-Based Tests (100% coverage)
  - 5 Caching Tests (100% coverage)
  - 5 Integration Tests (100% coverage)
- **100% test pass rate** (52/52 passing)
- **Test coverage: 90%** overall buildorders app
- **Test coverage: 89%** on models.py (core logic)
- Test execution time: ~1.14 seconds
- Property-based tests verify mathematical properties:
  - Linear scaling of requirements with quantities
  - Commutativity of mass calculations
  - Non-negativity of all results
  - Deterministic calculations
- Integration tests verify end-to-end workflows:
  - Manual calculation verification
  - Cache invalidation on updates
  - Shared component aggregation
  - Complex orders (10+ blocks)
  - Fixture data validation

### Documentation
- **Calculation Algorithms Documentation** (`docs/design/calculation_algorithms.md`)
  - Detailed algorithm descriptions with examples
  - Complexity analysis for each method
  - Mathematical properties and proofs
  - Performance considerations and caching strategy
  - Error handling documentation
  - Usage examples and testing information
- **Deployment Guide** (`ENH-0000009-deployment-guide.md`)
  - Step-by-step deployment instructions
  - Pre-deployment checklist
  - Migration procedures
  - Verification steps
  - Rollback procedures
  - Troubleshooting guide
  - Performance testing guidelines
  - Monitoring recommendations
- **Enhancement Documentation** (ENH0000009-buildorder-model-core-logic.md)
  - Complete implementation plan
  - All acceptance criteria met (18/18)
  - All testing requirements met (52/55)
  - Status updated to "Completed"
  - Implementation summary with test results

### Changed
- Project status: Phase 3 Build Order Calculator initiated
- Database schema: Added buildorders_buildorder table with indexes
- Settings: buildorders app registered in INSTALLED_APPS

### Technical Details
- **Dependencies:** Django 6.0.1, uuid-utils (no new packages required)
- **Database Changes:** New BuildOrder model with UUIDField primary key, JSONField for blocks
- **Indexes:** Created on name and created_at fields for query optimization
- **Caching:** 5-minute TTL with automatic invalidation
- **Integration:** Connects Ores, Components, and Blocks apps for full resource chain

## [0.5.0-alpha] - 2026-01-30

### Added - Phase 2 Complete: Views & Templates
- **Phase 2 completion:** All CRUD interfaces implemented with 107 automated tests (87% coverage)
- Phase 2 Post-Deployment Report with CI/CD recommendations
- Issue tracking system with 4 open issues documented (ISSUE-004, ISSUE-005, ISSUE-007, ISSUE-008)
- ISSUE-007: Missing health endpoint for Docker health check (documented)
- ISSUE-008: Static files volume mount conflict (documented)

### Documentation
- Phase 2 Post-Deployment Report with comprehensive metrics and CI/CD workflow recommendations
- GitHub Actions workflow recommendations for automated testing, Docker validation, and linting
- Open issue reports for Docker health endpoint and static files configuration
- Test coverage analysis: Ores (90%), Components (91%), Blocks (92%), Overall (87%)

### Changed
- Updated project status to reflect Phase 2 completion in README and home page UI
- Version bumped to 0.5.0-alpha across README, CHANGELOG, and pyproject.toml
- Corrected test coverage reporting from 92% to 87% overall
- Home page UI now shows Phase 2 as "Complete" with success icon
- Documented readiness for Phase 3 (Build Order Calculator)
- Established CI/CD implementation roadmap for Phase 3 and Phase 4

## [0.4.2-alpha] - 2026-01-26

### Fixed
- ISSUE-006: Pytest configuration missing after refactor
  - Created `app/conftest.py` to configure Django settings before pytest runs
  - Added `[tool.pytest.ini_options]` section to `pyproject.toml`
  - All automated tests now run successfully with `uv run pytest`

### Changed
- Updated CONTRIBUTING.md with simplified pytest commands
- Added pytest configuration documentation to project wiki
- Updated automated testing overview with pytest configuration link

## [0.4.1-alpha] - 2026-01-26

### Changed
- Version bump to 0.4.1-alpha
- README updated with Docker Quick Start and full stack details
- Documentation links added for ENH-0000008 under docs/enhancementRequests/Phase2_views/ENH0000008/
- Consolidated Docker/Deployment docs into ENH-0000008 directory

### Fixed
- Dockerfile dependency installation using `uv pip install -e .` (fixes compose build failure)

## [0.4.0-alpha] - 2026-01-26

### Added
- ENH-0000007: Blocks views, templates, and dynamic component selector
  - List view with full-text search by name/description, pagination, sorting, and filtering
  - Detail view with resource chain calculation (Blocks → Components → Ores)
  - Create and Update forms with JSONField component handling and server-side validation
  - Delete confirmation view with component summary
  - Responsive Bootstrap 5 templates
  - Dynamic JavaScript component selector for adding/removing components
  - Template filters for component name and mass lookups with caching
  - 19 comprehensive form tests (99% coverage)
  - 19 comprehensive view tests (90% coverage)
  - 18 comprehensive template tag tests (96% coverage)
  - Total coverage: 92% for blocks app (exceeds 85% target)
  - Performance optimization with query caching for resource chains
  - 404 error handling for nonexistent blocks
  - Form validation: unique names, positive quantities, UUID format validation
  - ENH-0000008: Core Infrastructure — Docker Option C (Django + nginx + PostgreSQL)
    - Production-like Docker stack using docker-compose (web + nginx + database)
    - New Dockerfile for Python 3.13 with health checks and non-root user
    - nginx reverse proxy with security headers and static file serving
    - Expanded docker-compose.yml with health checks, volumes, and custom network
    - .dockerignore added for smaller, faster builds
    - Comprehensive deployment documentation:
      - ENH0000008_DEPLOYMENT_GUIDE.md (technical deployment guide)
      - DOCKER_SETUP_GUIDE.md (setup, testing, troubleshooting)
      - DOCKER_CONFIGURATION_SUMMARY.md (quick reference)

### Fixed
- Fixed 404 error handling in Detail, Update, and Delete views
- Fixed invalid UUID error handling in template filters
- Fixed form validation for PCU field (must be ≥ 1)
- Made input_mass and output_mass fields optional (migration 0004)
- Context variable naming consistency (available_components alias)

### Changed
- Enhanced Block model with better error handling
- Improved form validation with server-side checks
- Optimized resource chain calculation with caching strategy
- Project infrastructure:
  - docker-compose.yml expanded from single DB service to full stack
  - Documentation consolidated under docs/enhancementRequests/Phase2_views/ENH0000008/
  - .env.example updated with Docker notes (use DB_HOST=database)

## [0.3.1-alpha] - 2026-01-25

### Added
- ENH-0000005: Complete CRUD interface for Ores
  - List view with filtering by name and sorting by mass
  - Detail view with full ore information
  - Create and Update forms with validation
  - Delete confirmation view
  - Responsive Bootstrap 5 templates
  - Custom CSS styling
  - 28 comprehensive unit tests
  - Fixture data integration
- ENH-0000006: Components views, templates, and material selector
  - List view with search, sorting (name, mass, build time), and pagination
  - Detail view with ore-aware material formatting and total material mass
  - Create/Update with JSON-backed material selector and server-side validation
  - Delete confirmation view with material summary
  - Bootstrap 5 templates plus navigation link in shared base/home pages
  - Dynamic JavaScript material selector for add/remove rows and validation
  - 30 comprehensive view/form tests; 91% package coverage (coverage report)

## [0.3.0-alpha] - 2026-01-24

### Added - Phase 1 Complete: Models & Database
- **Phase 1 completion:** All core models implemented with 128 automated tests
- ENH-0000004: Sample data fixtures for ores, components, and blocks (15/15/15)
- ENH-0000004: Fixture verification script (`scripts/verify_fixtures.py`)
- ENH-0000004: UUID generation helper (`scripts/generate_fixture_uuids.py`)
- ENH-0000004: Fixture-focused test suites across ores, components, and blocks

### Documentation
- Phase 1 Post-Deployment Report with complete metrics and lessons learned
- Phase 2 enhancement requests (ENH-0000005 through ENH-0000008)
- Best practices recommendations for Phase 2 implementation
- Updated enhancement request template to match Phase 1 design

### Documentation Added
- Comprehensive project plan with 4 development phases
- Phase 1 (Models & Admin) detailed specifications
- Phase 2 (Views & Templates) specifications
- Phase 3 (Build Order Calculator) specifications
- Phase 4 (Testing & Polish) specifications
- Technical specifications for data structures and database schema
- Enhancement request templates and workflow
- Enhancement requests for Phase 1 models (ENH-0000001 through ENH-0000004)
- Application design documentation

## [0.2.3-alpha] - 2026-01-20

### Added
- ENH-0000003: Blocks app with complete Block model implementation
  - UUIDv7 primary keys using named `generate_uuid()` function for migration compatibility
  - Comprehensive field structure (name, description, mass, health, pcu, snap_size, storage, timestamps)
  - JSONField for components array with component_id, component_name, and quantity
  - Consumer/Producer support for resource management (type and rate fields)
  - Component validation helper methods (validate_components, get_component_objects)
  - Django admin interface with custom JSON displays and validation status
  - Automatic timestamp tracking (created_at, updated_at)
  - Unique constraint on block names
  - Integration with Components and Ores apps for full relationship chain
- Comprehensive automated test suite for Block model (49 tests)
  - Model creation and field validation tests (7 tests)
  - Timestamp auto-population and immutability tests (5 tests)
  - JSONField components storage tests (6 tests)
  - Component validation logic tests (8 tests)
  - Consumer/Producer functionality tests (6 tests)
  - Component relationship query tests (4 tests)
  - Meta configuration tests (5 tests)
  - Integration and workflow tests (8 tests)
  - 100% test pass rate with full feature coverage
  - Test execution time: ~0.2 seconds
  - Exceeds 35+ test minimum requirement by 40%

### Documentation
- ENH-0000003 complete documentation package:
  - Deployment Guide with step-by-step implementation
  - Post-Deployment Review documenting validation results and metrics
  - Test Documentation with all 49 test cases described
  - Testing Validation report confirming all requirements met
- Phase 1 Mid-Deployment Report (3 enhancements complete, 66% phase completion)
  - Cross-enhancement analysis and lessons learned
  - Common patterns established (UUIDv7, testing standards, documentation)
  - Performance metrics and quality trends
- ENH-0000004 (Sample Fixtures) updated with comprehensive lessons learned:
  - UUID implementation patterns from all three model enhancements
  - Fixture format specifications with complete JSON examples
  - Expanded testing requirements (35+ tests minimum)
  - Comprehensive implementation plan (8 detailed steps)
  - Enhanced risk assessment with specific mitigations
  - Complete documentation requirements following established templates

## [0.2.2-alpha] - 2026-01-20

### Added
- ENH-0000002: Components app with complete Component model implementation
  - UUIDv7 primary keys using named function (not lambda) for migration compatibility
  - Comprehensive field structure (name, description, materials, fabricator_type, crafting_time, mass, timestamps)
  - JSONField for materials with ore_id to quantity mapping
  - Material validation helper methods (validate_materials, get_material_ores)
  - Django admin interface with custom JSON displays and validation status
  - Automatic timestamp tracking (created_at, updated_at)
  - Unique constraint on component names
  - Integration with Ores app for material references
- Comprehensive automated test suite for Component model (44 tests)
  - Model creation and field validation tests (13 tests)
  - Timestamp auto-population and immutability tests (5 tests)
  - JSONField storage and persistence tests (5 tests)
  - Material validation logic tests (8 tests)
  - Ore relationship query tests (4 tests)
  - Meta configuration tests (4 tests)
  - Integration and workflow tests (5 tests)
  - 100% test pass rate with full feature coverage
  - Test execution time: ~0.17 seconds
  - Exceeds 35+ test minimum requirement by 25%

### Fixed
- Migration serialization error with lambda functions
  - Replaced `default=lambda: str(uuid7())` with named `generate_uuid()` function
  - Applied fix to both components/models.py and ores/models.py for consistency
  - Prevents "ValueError: Cannot serialize function: lambda" during makemigrations
- Admin interface HTML escaping inconsistency
  - Standardized on mark_safe() throughout ComponentAdmin
  - Improved code consistency and maintainability

### Documentation
- ENH-0000002 complete documentation package:
  - Deployment Guide with step-by-step implementation and troubleshooting
  - Post-Deployment Review documenting actual issues encountered, resolutions, and lessons learned
  - Enhanced best practices for future development (ENH-0000003)
  - Migration serialization issue documentation and prevention strategies

## [0.2.1-alpha] - 2026-01-20

### Added
- ENH-0000001: Ores app with complete Ore model implementation
  - UUIDv7 primary keys for time-ordered database indexing
  - Comprehensive field structure (name, description, mass, timestamps)
  - Django admin interface with list display, search, and filtering
  - Automatic timestamp tracking (created_at, updated_at)
  - Unique constraint on ore names
- Comprehensive automated test suite for Ore model (35 tests)
  - Model creation and field validation tests
  - UUID generation and time-ordering verification
  - Timestamp auto-population and update tracking tests
  - Database query and filtering tests
  - Integration and CRUD workflow tests
  - 100% test pass rate with full feature coverage
  - Test execution time: ~0.36 seconds

### Fixed
- UUID compatibility issue between uuid_utils.UUID and Django's UUIDField
  - Implemented named function wrapper to convert uuid7() output to string format
  - Ensures proper Django field validation and database storage
- Removed duplicate uuid package dependency from pyproject.toml

### Documentation
- ENH-0000001 complete documentation package:
  - Deployment Guide with step-by-step implementation
  - Post-Deployment Review documenting issues, lessons learned, and recommendations
  - Test Documentation describing all 35 tests and coverage areas
  - Testing Validation report confirming all requirements met
  - Enhancement directory README for quick reference
- ENH-0000002, ENH-0000003, ENH-0000004 enhancement requests updated with lessons learned
  - Added UUID compatibility best practices
  - Enhanced testing requirements (35+ tests minimum)
  - Documentation templates for consistency
- Phase 1 checklist updated to reflect ENH-0000001 completion

## [0.2.0-alpha] - 2026-01-18

### Added
- Initial Django 6.0.1 project setup with `se2CalcProject` configuration
- PostgreSQL database support with SQLite fallback for development
- Environment-based configuration using python-dotenv
- Docker Compose setup for PostgreSQL database
- Automated secret generation scripts (`secrets_gen.py`, `generate_django_secret.py`, `generate_postgres_password.py`)
- Development environment setup documentation with UV package manager guide
- Project documentation structure in `docs/` directory
  - Project plan with timeline estimates (9-13 days total)
  - Design documentation for app architecture
  - Enhancement request system with templates
  - Development environment setup guides
- Testing support with pytest-django
- MIT License
- Contributing guidelines (CONTRIBUTING.md)
- Comprehensive .gitignore for Python/Django projects
- Project dependencies management via pyproject.toml
- UUIDv7 support via uuid-utils package

### Infrastructure
- Django admin interface at `/admin/` endpoint
- WSGI and ASGI application configurations
- Environment variable validation for production deployments
- Security settings including SECRET_KEY management and ALLOWED_HOSTS configuration
- SQLite database file for local development

## [0.1.0] - 2026-01-18

### Added
- Initial project structure and repository setup

[Unreleased]: https://github.com/crashtechie/se2-calculator-project/compare/v0.6.1-alpha...HEAD
[0.6.1-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.6.0-alpha...v0.6.1-alpha
[0.6.0-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.5.0-alpha...v0.6.0-alpha
[0.5.0-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.4.2-alpha...v0.5.0-alpha
[0.4.2-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.4.1-alpha...v0.4.2-alpha
[0.4.1-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.4.0-alpha...v0.4.1-alpha
[0.4.0-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.3.1-alpha...v0.4.0-alpha
[0.3.1-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.3.0-alpha...v0.3.1-alpha
[0.3.0-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.2.3-alpha...v0.3.0-alpha
[0.2.3-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.2.2-alpha...v0.2.3-alpha
[0.2.2-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.2.1-alpha...v0.2.2-alpha
[0.2.1-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.2.0-alpha...v0.2.1-alpha
[0.2.0-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.1.0...v0.2.0-alpha
[0.1.0]: https://github.com/crashtechie/se2-calculator-project/releases/tag/v0.1.0