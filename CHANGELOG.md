# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### In Development
- Phase 3: Build Order Calculator (planned)
- REST API for Blocks module (ENH-0000008 - planned)

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

[Unreleased]: https://github.com/crashtechie/se2-calculator-project/compare/v0.4.2-alpha...HEAD
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