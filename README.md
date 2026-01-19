# Space Engineers 2 Calculator Project

**Version:** 0.2.0-alpha  
**License:** MIT  
**Framework:** Django 6.0.1  
**Python:** 3.13+  
**Status:** 🚧 In Active Development

A comprehensive web-based calculator and resource management tool built with Django to assist Space Engineers 2 players with crafting calculations, build order planning, and resource optimization.

## ⚠️ Alpha Release Notice

This is an early alpha release (0.2.0-alpha). The project is under active development with core features being implemented. The foundation is in place, but functional features are still being developed.

### Current Development Status

- ✅ **Phase 0**: Django project foundation and infrastructure
- 🔄 **Phase 1**: Models & Database (In Progress)
  - Ores app created (models pending implementation)
  - Components app (not yet created)
  - Blocks app (not yet created)
- 📋 **Phase 2**: Views & Templates (Planned)
- 📋 **Phase 3**: Build Order Calculator (Planned)
- 📋 **Phase 4**: Testing & Documentation (Planned)

### Planned Features

- 📊 **Ore Management**: Track and manage raw material data
- 🔧 **Component Tracking**: Database of craftable components with material requirements
- 🏗️ **Block Catalog**: Complete database of Space Engineers 2 blocks
- 🧮 **Build Order Calculator**: Multi-block resource calculation and optimization
- 📈 **Resource Chain Visualization**: See the full crafting chain from ore to final block
- 💾 **Data Export/Import**: Save and share build orders

## Features

- 🚀 Built on Django 6.0.1 framework
- 🐘 PostgreSQL database support with SQLite fallback
- 🔒 Secure environment-based configuration
- 🐳 Docker Compose setup for easy database deployment
- 🧪 Testing infrastructure with pytest-django
- 📝 Comprehensive development documentation

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

5. **Start PostgreSQL (optional):**
   ```bash
   docker compose up -d
   ```

6. **Run the development server:**
   ```bash
   uv run python manage.py runserver
   ```

7. **Open your browser:**
   Navigate to http://localhost:8000

## Development Setup

For detailed development environment setup instructions, see [docs/devEnvSetup/uv_installation.md](docs/devEnvSetup/uv_installation.md).

## Project Structure

```
se2-calculator-project/
├── se2CalcProject/          # Main Django project configuration
├── ores/                    # Ores app (in development)
├── scripts/                 # Utility scripts for secret generation
├── docs/                    # Project documentation
│   ├── projectPlan/        # Development phases and timeline
│   ├── design/             # Application design documents
│   ├── devEnvSetup/        # Development environment guides
│   └── enhancementRequests/ # Feature requests and enhancements
├── logs/                    # Application logs directory
├── manage.py               # Django management script
├── pyproject.toml          # Project dependencies
├── docker-compose.yml      # PostgreSQL container setup
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

**Estimated Total Timeline:** 9-13 days

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
# Start PostgreSQL container
docker compose up -d

# Stop PostgreSQL container
docker compose down

# View logs
docker compose logs -f
```

## Testing

The project uses pytest-django for testing. Test files follow the `test_*.py` naming convention. The goal is to maintain >80% code coverage across all modules.

Run tests with:
```bash
uv run pytest
```

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