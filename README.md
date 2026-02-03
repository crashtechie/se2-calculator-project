# Space Engineers 2 Calculator Project

[![Tests](https://github.com/crashtechie/se2-calculator-project/actions/workflows/test.yml/badge.svg)](https://github.com/crashtechie/se2-calculator-project/actions/workflows/test.yml)  
[![Docker Build](https://github.com/crashtechie/se2-calculator-project/actions/workflows/docker.yml/badge.svg)](https://github.com/crashtechie/se2-calculator-project/actions/workflows/docker.yml)  
[![Code Quality](https://github.com/crashtechie/se2-calculator-project/actions/workflows/lint.yml/badge.svg)](https://github.com/crashtechie/se2-calculator-project/actions/workflows/lint.yml)  
[![codecov](https://codecov.io/github/crashtechie/se2-calculator-project/graph/badge.svg?token=TohStlR1r2)](https://codecov.io/github/crashtechie/se2-calculator-project)  

**Version:** 0.6.1-alpha  
**License:** MIT  
**Framework:** Django 6.0.1  
**Python:** 3.13+  
**Status:** 🚧 In Active Development

A comprehensive web-based calculator and resource management tool built with Django to assist Space Engineers 2 players with crafting calculations, build order planning, and resource optimization.

## ⚠️ Alpha Release Notice

This is an early alpha release (0.6.1-alpha). Phase 2 (Views & Templates) is complete with full CRUD functionality. Phase 3 (Build Order Calculator) is in progress with the core BuildOrder model implemented. Docker infrastructure has been stabilized with all known issues resolved.

### Current Development Status

- ✅ **Phase 1: Models** (Completed)
  - Ores, Components, Blocks models implemented
  - Fixtures created and validated
  
- ✅ **Phase 2: Views & Templates** (Complete)
  - ✅ ENH-0000005: Ores views and templates (Complete)
  - ✅ ENH-0000006: Components views and templates (Complete)
  - ✅ ENH-0000007: Blocks views and templates (Complete)
  - ✅ ENH-0000008: Core Infrastructure - Docker stack (Complete)
  
- 🚧 **Phase 3: Build Order Calculator** (In Progress)
  - ✅ ENH-0000009: BuildOrder Model & Core Logic (Complete)
    - BuildOrder model with UUIDv7 primary keys
    - Calculation methods for resource aggregation
    - Caching system with 5-minute TTL
    - Admin interface with custom displays
    - 52 comprehensive tests (90% coverage)
    - Complete documentation (algorithms, deployment, post-deployment)
  - ⏳ ENH-0000010: Build Order Views & Templates (Planned)
  - ⏳ ENH-0000011: Dynamic Block Selector (Planned)
  
- ⏳ **Phase 4: Testing, Documentation & Core Infrastructure** (Planned)
  - Core app with validation mixins and utilities (deferred from ENH-0000008)
  - API endpoints for AJAX functionality
  - Structured logging configuration
  - Custom error pages (404/500)
  - Additional security settings
  - Comprehensive test suite (>80% coverage)
  - OpenAPI/Swagger specifications
  - Architecture diagrams and data flow documentation
  - Advanced performance tuning guides

### Planned Features

- 📊 **Ore Management**: Track and manage raw material data
- 🔧 **Component Tracking**: Database of craftable components with material requirements
- 🏗️ **Block Catalog**: Complete database of Space Engineers 2 blocks with CRUD interface
  - Full resource chain visualization (Blocks → Components → Ores)
  - Component quantity management with validation
  - Dynamic component selector interface
- 🧮 **Build Order Calculator**: Multi-block resource calculation and optimization (Phase 3 - planned)
- 📈 **Resource Chain Visualization**: See the full crafting chain from ore to final block (implemented)
- 💾 **Data Export/Import**: Save and share build orders

## Features

- 🚀 Built on Django 6.0.1 framework
- 🐘 PostgreSQL database support with SQLite fallback
- 🔒 Secure environment-based configuration
- 🐳 Docker Compose stack for web + nginx + PostgreSQL (fully operational)
- 🛡️ Security headers via nginx reverse proxy
- 📦 Static files served by nginx with caching
- ❤️ Health check endpoints for container monitoring
- 🧪 Testing infrastructure with pytest-django (107 tests, 87% coverage)
- 📝 Comprehensive development documentation
- 💾 JSONField-based component/material management
- ⚡ Performance optimization with caching
- 🔗 Full resource chain tracking and calculations
- 📋 Advanced search, filtering, and pagination

## Quick Start

### Prerequisites

- Python 3.13+
- UV package manager
- Docker & Docker Compose (for PostgreSQL)

### Installation

1. **Install UV package manager:**
   ```bash
   # See: https://docs.astral.sh/uv/getting-started/installation/
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/crashtechie/se2-calculator-project.git
   cd se2-calculator-project
   ```

3. **Install Python 3.13 using UV:**
   ```bash
   uv python install 3.13
   ```

4. **Setup environment variables:**
   ```bash
   cp .env.example .env
   uv run python scripts/secrets_gen.py
   ```

5. **Start Docker stack (web + nginx + database):**
   ```bash
   docker compose build
   docker compose up -d
   docker compose exec web python manage.py migrate
   ```

6. **Run the development server:**
   ```bash
   uv run python manage.py runserver
   ```

7. **Open your browser:**
   Navigate to http://localhost:8000

## Docker Quick Start

Run the production-like stack locally (nginx reverse proxy + Django + PostgreSQL):

```bash
# Build images
docker compose build

# Start services
docker compose up -d

# Apply migrations
docker compose exec web python app/manage.py migrate

# Create superuser (optional)
docker compose exec web python app/manage.py createsuperuser

# Load sample data (optional)
docker compose exec web python app/manage.py loaddata sample_ores sample_components sample_blocks

# Verify health
curl http://localhost/health/

# Access application
open http://localhost/
```

**Important Notes:**
- Set `DB_HOST=database` in your `.env` when using Docker
- nginx listens on port 80; Django runs internally on port 8000
- Logs and static files persist via named volumes (`logs`, `static_files`)
- Health check endpoint available at `/health/`
- All containers include health checks and will show as "healthy" when ready

**Troubleshooting:**
- If containers fail to start, check logs: `docker compose logs web`
- If database connection fails, recreate volumes: `docker compose down -v && docker compose up -d`
- If health checks fail, verify nginx configuration and Django ALLOWED_HOSTS setting

## Development Setup

For detailed development environment setup instructions, see [docs/devEnvSetup/uv_installation.md](docs/devEnvSetup/uv_installation.md).

## Project Structure

```
se2-calculator-project/
├── se2CalcProject/          # Main Django project configuration
├── ores/                    # Ores app (completed)
├── components/              # Components app (completed)
├── blocks/                  # Blocks app (completed)
├── scripts/                 # Utility scripts for secret generation
├── docs/                    # Project documentation
│   ├── projectPlan/        # Development phases and timeline
│   ├── design/             # Application design documents
│   ├── devEnvSetup/        # Development environment guides
│   └── enhancementRequests/ # Feature requests and enhancements
├── logs/                    # Application logs directory
├── manage.py               # Django management script
├── pyproject.toml          # Project dependencies
├── docker-compose.yml      # Full stack: web + nginx + PostgreSQL
├── Dockerfile              # Python 3.13 image with health checks
├── nginx.conf              # Reverse proxy and static file serving
├── CHANGELOG.md            # Version history and changes
├── CONTRIBUTING.md         # Contribution guidelines
└── README.md              # This file
```

## Development Roadmap

### Phase 1: Models & Database (2-3 days)
- Create three Django apps: ores, components, blocks
- Implement models with UUIDv7 primary keys
- Set up Django admin interface
- Create initial data fixtures

### Phase 2: Views & Templates (3-4 days)
- Implement CRUD operations for all models
- Create responsive templates
- Add search and filtering capabilities

### Phase 3: Build Order Calculator (2-3 days)
- Multi-block selection interface
- Recursive resource calculation
- Material breakdown and totaling

### Phase 4: Testing & Polish (2-3 days)
- Comprehensive test suite (>80% coverage)
- Performance optimization
- Documentation completion

**Estimated Total Timeline:** 10-14 days

## Configuration

The project uses environment variables for configuration. Copy `.env.example` to `.env` and configure as needed:

- `DEBUG` - Debug mode (true/false)
- `SECRET_KEY` - Django secret key (auto-generated)
- `DB_NAME` - PostgreSQL database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password (auto-generated)
- `DB_HOST` - Database host
- `DB_PORT` - Database port

## Common Commands

### Development Server
```bash
uv run python manage.py runserver
```

### Database Management
```bash
# Create migrations
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate

# Create superuser for admin access
uv run python manage.py createsuperuser
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest path/to/test_file.py
```

### Database Container Management
```bash
# Start full stack (web + nginx + database)
docker compose up -d

# Stop all services
docker compose down

# Stop and remove volumes (WARNING: destroys data)
docker compose down -v

# View logs for specific service
docker compose logs -f web
docker compose logs -f database
docker compose logs -f nginx

# Check container health status
docker compose ps

# Restart a specific service
docker compose restart web
docker compose restart nginx

# Execute commands in web container
docker compose exec web python app/manage.py migrate
docker compose exec web python app/manage.py createsuperuser
```

## Testing

The project uses pytest-django for testing. Test files follow the `test_*.py` naming convention. The goal is to maintain >80% code coverage across all modules.

Run tests with:
```bash
uv run pytest
```

## Loading Sample Data

Sample fixtures are provided for quick setup.

```bash
# Load all fixtures (order matters)
uv run python manage.py loaddata sample_ores sample_components sample_blocks

# Reset and reload (destroys existing data)
uv run python manage.py flush --no-input
uv run python manage.py loaddata sample_ores sample_components sample_blocks
```

Fixture contents: 15 ores, 15 components, 15 blocks with validated UUIDv7 relationships.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Links

- **Repository**: [crashtechie/se2-calculator-project](https://github.com/crashtechie/se2-calculator-project)
- **Issues**: [GitHub Issues](https://github.com/crashtechie/se2-calculator-project/issues)
- **Wiki**: [Project Wiki](https://github.com/crashtechie/se2-calculator-project/wiki) (Coming Soon)

## Acknowledgments

Built for the Space Engineers 2 community. Special thanks to all contributors and the Keen Software House development team for creating an amazing game.

## Technical Architecture

### Database Models

The application uses three core models:

1. **Ores** - Base resources with mass and description
2. **Components** - Craftable items made from ores (with JSONField for material requirements)
3. **Blocks** - Buildable structures made from components (with JSONField for component requirements)

All models use UUIDv7 as primary keys for better performance and distributed system compatibility.

### Key Technologies

- **Django 6.0.1** - Modern Python web framework
- **PostgreSQL** - Production database with JSONField support
- **SQLite** - Development fallback database
- **Docker Compose** - Container orchestration for database
- **UV** - Fast Python package manager
- **pytest-django** - Testing framework
- **python-dotenv** - Environment configuration management

### Data Flow

```
Ores \u2192 Components \u2192 Blocks \u2192 Build Orders
```

Each level tracks its dependencies via JSON structures, enabling efficient recursive calculations.

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Project Plan](docs/projectPlan/overview.md)** - Overall project roadmap and phases
- **[Technical Specs](docs/projectPlan/technical_specs.md)** - Data structures and database schema
- **[Design Documents](docs/design/)** - Application architecture and design decisions
- **[Enhancement Requests](docs/enhancementRequests/)** - Feature requests and development workflow
- **[Development Setup](docs/devEnvSetup/uv_installation.md)** - Detailed environment setup guide

### ENH-0000008 (Core Infrastructure) Documentation

- **Core Spec:** [docs/enhancementRequests/Phase2_views/ENH0000008/ENH0000008-core-infrastructure.md](docs/enhancementRequests/Phase2_views/ENH0000008/ENH0000008-core-infrastructure.md)
- **Deployment Guide:** [docs/enhancementRequests/Phase2_views/ENH0000008/ENH0000008_DEPLOYMENT_GUIDE.md](docs/enhancementRequests/Phase2_views/ENH0000008/ENH0000008_DEPLOYMENT_GUIDE.md)
- **Docker Setup:** [docs/enhancementRequests/Phase2_views/ENH0000008/DOCKER_SETUP_GUIDE.md](docs/enhancementRequests/Phase2_views/ENH0000008/DOCKER_SETUP_GUIDE.md)
- **Docker Summary:** [docs/enhancementRequests/Phase2_views/ENH0000008/DOCKER_CONFIGURATION_SUMMARY.md](docs/enhancementRequests/Phase2_views/ENH0000008/DOCKER_CONFIGURATION_SUMMARY.md)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

### Enhancement Request Process

1. Review existing enhancement requests in `docs/enhancementRequests/`
2. Use the enhancement request template for new features
3. Follow the project plan phases for coordinated development
4. Submit pull requests with clear descriptions and test coverage

## Changelog

For a detailed list of changes and version history, see [CHANGELOG.md](CHANGELOG.md).

## Support

For questions, issues, or feature requests, please open an issue on the [GitHub repository](https://github.com/crashtechie/se2-calculator-project/issues).

---

**Copyright © 2026 Dan Smith ([@crashtechie](https://github.com/crashtechie))**