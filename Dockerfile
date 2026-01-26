# Multi-stage Dockerfile for SE2 Calculator
# Optimized for development and production use
# Supports Django with PostgreSQL, nginx reverse proxy

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
RUN pip install uv && \
    uv pip install --system --no-cache-dir -e .

# Copy project code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs && \
    chmod 755 /app/logs

# Collect static files for production
# Use || true to continue even if no static files exist
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose port for Django application
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/', timeout=5)" || exit 1

# Default command - for development
# Production should use gunicorn or similar
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
