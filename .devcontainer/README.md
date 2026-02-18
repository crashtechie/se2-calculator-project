# Development Container Setup

This directory contains the configuration for a VS Code development container that provides a consistent development environment for the SE2 Calculator project.

> **Note:** Dev containers are a VS Code-specific feature and are not supported in Kiro IDE. If you're using Kiro IDE, use the standard Docker Compose setup in the project root (`docker-compose.yml`) to run PostgreSQL, and work directly with your local Python environment using UV.

## What's Included

- Python 3.13
- UV package manager
- PostgreSQL 17 database
- All project dependencies pre-installed
- VS Code extensions for Python, Django, and Docker
- Configured linting and formatting (Ruff)

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [VS Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Opening the Project

1. Open VS Code
2. Open the project folder
3. When prompted, click "Reopen in Container"
4. Wait for the container to build and start (first time takes a few minutes)

**If you're not prompted automatically:**

1. Open the Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Type and select: "Dev Containers: Reopen in Container"
3. Alternatively, click the green button in the bottom-left corner of VS Code
4. Select "Reopen in Container" from the menu

The container will automatically:
- Install all Python dependencies using UV
- Run database migrations
- Forward ports 8000 (Django) and 5432 (PostgreSQL)

### Running the Development Server

Once inside the container, open a terminal and run:

```bash
cd app
python manage.py runserver
```

Access the application at http://localhost:8000

### Common Commands

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov

# Create migrations
python app/manage.py makemigrations

# Apply migrations
python app/manage.py migrate

# Create superuser
python app/manage.py createsuperuser

# Load sample data
python app/manage.py loaddata sample_ores sample_components sample_blocks

# Run linting
ruff check .

# Format code
ruff format .
```

### Database Access

The PostgreSQL database is accessible at:
- Host: `db` (from within container) or `localhost` (from host machine)
- Port: `5432`
- Database: `se2_calculator_dev`
- User: `postgres`
- Password: `postgres`

### Rebuilding the Container

If you need to rebuild the container (e.g., after changing dependencies):

1. Command Palette → "Dev Containers: Rebuild Container"
2. Or manually: `docker compose -f .devcontainer/docker-compose.yml build --no-cache`

### Troubleshooting

**Container won't start:**
- Check Docker Desktop is running
- Try rebuilding: "Dev Containers: Rebuild Container"

**Database connection errors:**
- Ensure the `db` service is healthy: `docker compose -f .devcontainer/docker-compose.yml ps`
- Check environment variables in `docker-compose.yml`

**Port already in use:**
- Stop any local PostgreSQL or Django servers
- Change port mappings in `devcontainer.json` if needed
