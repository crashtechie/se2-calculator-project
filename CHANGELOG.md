# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0-alpha] - 2026-01-18

### Added
- Initial Django 6.0.1 project setup with `se2CalcProject` configuration
- PostgreSQL database support with SQLite fallback for development
- Environment-based configuration using python-dotenv
- Docker Compose setup for PostgreSQL database
- Automated secret generation scripts (`secrets_gen.py`, `generate_django_secret.py`, `generate_postgres_password.py`)
- Development environment setup documentation with UV package manager guide
- Project documentation structure in `docs/` directory
- Testing support with pytest-django
- MIT License
- Contributing guidelines (CONTRIBUTING.md)
- Comprehensive .gitignore for Python/Django projects
- Project dependencies management via pyproject.toml

### Infrastructure
- Django admin interface at `/admin/` endpoint
- WSGI and ASGI application configurations
- Environment variable validation for production deployments
- Security settings including SECRET_KEY management and ALLOWED_HOSTS configuration

## [0.1.0] - 2026-01-18

### Added
- Initial project structure and repository setup

[Unreleased]: https://github.com/crashtechie/se2-calculator-project/compare/v0.2.0-alpha...HEAD
[0.2.0-alpha]: https://github.com/crashtechie/se2-calculator-project/compare/v0.1.0...v0.2.0-alpha
[0.1.0]: https://github.com/crashtechie/se2-calculator-project/releases/tag/v0.1.0