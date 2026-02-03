#!/bin/sh
# Docker entrypoint script for SE2 Calculator web service
# Handles static file copying and Django startup

set -e

echo "Starting SE2 Calculator web service..."

# Copy static files from build to volume if volume is empty or in CI/CD mode
if [ ! -f "/app/app/staticfiles/css/main.css" ]; then
    echo "Copying static files to volume..."
    # Static files were collected during build to a temp location
    # We need to ensure they're in the right place
    python app/manage.py collectstatic --noinput --clear || echo "Warning: collectstatic failed"
fi

# Run database migrations
echo "Running database migrations..."
python app/manage.py migrate --noinput

# Start Django development server
echo "Starting Django server..."
exec python app/manage.py runserver 0.0.0.0:8000
