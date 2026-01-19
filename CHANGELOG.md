# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### In Development
- Components app (planned)
- Blocks app (planned)
- Build Order Calculator feature (planned)

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
  - Implemented lambda wrapper to convert uuid7() output to string format
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

[Unreleased]: https://github.com/crashtechie/se2-calculator-project/compare/v0.2.1-alpha...HEAD
[0.2.1-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.2.0-alpha...v0.2.1-alpha
[0.2.0-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.1.0...v0.2.0-alpha
[0.1.0]: https://github.com/crashtechie/se2-calculator-project/releases/tag/v0.1.0