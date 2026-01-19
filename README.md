# Space Engineers 2 Calculator Project

**Version:** 0.2.0-alpha  
**License:** MIT  
**Framework:** Django 6.0.1  
**Python:** 3.13+

A web-based calculator application built with Django to assist Space Engineers 2 players with in-game calculations and resource management.

## ⚠️ Alpha Release

This is an alpha release (0.2.0-alpha). The project is under active development and features may change.

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
├── scripts/                 # Utility scripts for secret generation
├── docs/                    # Project documentation
├── manage.py               # Django management script
├── pyproject.toml          # Project dependencies
├── docker-compose.yml      # PostgreSQL container setup
└── README.md              # This file
```

## Configuration

The project uses environment variables for configuration. Copy `.env.example` to `.env` and configure as needed:

- `DEBUG` - Debug mode (true/false)
- `SECRET_KEY` - Django secret key (auto-generated)
- `DB_NAME` - PostgreSQL database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password (auto-generated)
- `DB_HOST` - Database host
- `DB_PORT` - Database port

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Changelog

For a detailed list of changes and version history, see [CHANGELOG.md](CHANGELOG.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions, issues, or feature requests, please open an issue on the [GitHub repository](https://github.com/crashtechie/se2-calculator-project/issues).

---

**Copyright © 2026 Dan Smith ([@crashtechie](https://github.com/crashtechie))**