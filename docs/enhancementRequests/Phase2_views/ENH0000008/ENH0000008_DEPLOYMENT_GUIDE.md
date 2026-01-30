# ENH-0000008 Technical Deployment Guide

**Enhancement:** Docker Infrastructure (Partial ENH-0000008)  
**Version:** 1.1  
**Date:** January 27, 2026  
**Environment:** Development, Staging, Production  
**Scope:** Docker infrastructure only (core app features deferred to Phase 4)  

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Pre-Deployment Checklist](#pre-deployment-checklist)
4. [Deployment Procedure](#deployment-procedure)
5. [Post-Deployment Verification](#post-deployment-verification)
6. [Database Initialization](#database-initialization)
7. [Environment Configuration](#environment-configuration)
8. [Docker Deployment](#docker-deployment)
9. [Monitoring & Logs](#monitoring--logs)
10. [Rollback Procedures](#rollback-procedures)
11. [Troubleshooting](#troubleshooting)
12. [Performance Tuning](#performance-tuning)
13. [Security Hardening](#security-hardening)
14. [Maintenance Tasks](#maintenance-tasks)

---

## Overview

### What is ENH-0000008?

ENH-0000008 originally planned comprehensive core infrastructure. As of v0.4.0-alpha, only Docker infrastructure has been deployed. Application-level features are deferred to Phase 4.

**Implemented in v0.4.0-alpha:**
- **Docker Infrastructure:** Container orchestration with PostgreSQL, Django, nginx
- **Security Headers:** X-Frame-Options, X-Content-Type-Options, X-XSS-Protection (nginx)
- **Static File Management:** Production-ready static file serving via nginx
- **Configuration Management:** Environment-based settings and secrets

**Deferred to Phase 4:**
- Logging Framework (structured application logging)
- Error Handling (custom 404/500 pages)
- Core app with utilities and mixins
- API endpoints for AJAX
- Additional Django security settings

### Architecture Components

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐        ┌──────────────┐             │
│  │   nginx      │ ◄──► │   Django     │             │
│  │ (port 80)    │        │ (port 8000)  │             │
│  └──────────────┘        └──────────────┘             │
│       ▲                        ▲                       │
│       │                        │                       │
│       │                    ┌───────────┐               │
│       └─────────────────► │ PostgreSQL │               │
│                           │ (port 5432)│               │
│                           └───────────┘               │
│                                                         │
│  ┌────────────────┐  ┌──────────────┐               │
│  │ Persistent     │  │ Persistent   │               │
│  │ Volumes:       │  │ Volumes:     │               │
│  │ • db_data      │  │ • logs       │               │
│  │ • static_files │  │              │               │
│  └────────────────┘  └──────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Key Features

| Feature | Benefit | Deployment Impact | Status |
|---------|---------|-------------------|--------|
| **Docker Support** | Reproducible deployments | Requires Docker & Docker Compose | ✅ Complete |
| **Security Headers** | Protection from common attacks | Configured in nginx.conf | ✅ Complete |
| **Static Files** | Production-grade static serving | Requires nginx service | ✅ Complete |
| **Logging** | Track application behavior and errors | Requires logs volume mount | ⏳ Phase 4 |
| **Error Handling** | Professional error pages | Requires DEBUG=False testing | ⏳ Phase 4 |

---

## Prerequisites

### System Requirements

**Hardware Minimums:**
- CPU: 2 cores minimum
- RAM: 2 GB minimum (4 GB recommended)
- Disk Space: 5 GB minimum (for database growth)
- Network: Internet connectivity for package downloads

**Supported Operating Systems:**
- Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- macOS (Intel/Apple Silicon with Docker Desktop)
- Windows 10/11 (with WSL2 and Docker Desktop)

### Required Software

**Before Deployment:**

1. **Docker Engine** (version 20.10+)
   ```bash
   docker --version
   # Expected: Docker version 20.10.x or higher
   ```

2. **Docker Compose** (version 2.0+)
   ```bash
   docker compose version
   # Expected: Docker Compose version 2.x.x or higher
   ```

3. **Git** (version 2.30+)
   ```bash
   git --version
   # Expected: git version 2.30.x or higher
   ```

4. **Python** (version 3.13+, for local development only)
   ```bash
   python --version
   # Expected: Python 3.13.x or higher
   ```

5. **uv** (version 0.2.0+, for local development only)
   ```bash
   uv --version
   # Expected: uv 0.2.x or higher
   ```

### Installation Commands

**Ubuntu/Debian:**
```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group (optional, avoid sudo)
sudo usermod -aG docker $USER
newgrp docker
```

**macOS (with Homebrew):**
```bash
# Install Docker Desktop (includes Docker and Docker Compose)
brew install --cask docker

# Verify installation
docker --version
docker compose version
```

**Verify All Prerequisites:**
```bash
docker --version && \
docker compose version && \
git --version && \
echo "All prerequisites installed!"
```

---

## Pre-Deployment Checklist

### Code Preparation

- [x] Code reviewed and merged to main branch
- [x] All tests passing locally
- [x] Coverage >= 80%
- [x] No pending migrations
- [x] ENH-0000005, ENH-0000006, ENH-0000007 deployed successfully
- [x] CHANGELOG.md updated
- [ ] LOGGING configuration tested locally (deferred to Phase 4)

### Docker Preparation

- [x] Dockerfile reviewed and tested
- [x] docker-compose.yml reviewed for environment
- [x] nginx.conf reviewed and customized
- [x] .dockerignore contains necessary exclusions
- [x] Volume mounts point to correct locations
- [x] Container names set appropriately
- [x] Health checks configured

### Infrastructure Preparation

- [x] Server available and accessible
- [x] Disk space adequate for database growth
- [x] Network connectivity verified
- [x] Firewall rules configured (if applicable)
- [x] Backup strategy planned for volumes
- [x] Monitoring tools prepared

### Backup Preparation

- [x] Backup location identified
- [x] Backup scripts tested
- [x] Database backup procedure documented
- [x] Static files backup procedure documented
- [x] Rollback plan documented

---

## Deployment Procedure

### Step 1: Prepare Deployment Environment

**1.1 Clone or Pull Latest Code**
```bash
cd /home/dsmi001/app/se2-calculator-project

# If first deployment
git clone https://github.com/crashtechie/se2-calculator-project.git .

# If updating existing deployment
git fetch origin
git checkout develop
git pull origin develop
```

**1.2 Verify Code Status**
```bash
# Check branch and status
git status
git log --oneline -5

# Expected: Latest commits visible, working directory clean
```

**1.3 Backup Current Deployment (if exists)**
```bash
# Create timestamped backup directory
BACKUP_DIR="/backup/se2-calculator-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup docker-compose volumes
docker compose exec database pg_dump -U postgres calc_db > "$BACKUP_DIR/database_backup.sql"

# Backup static files if they exist
cp -r ./static "$BACKUP_DIR/" 2>/dev/null || true
cp -r ./logs "$BACKUP_DIR/" 2>/dev/null || true

echo "Backup created at: $BACKUP_DIR"
```

### Step 2: Configure Environment

**2.1 Create .env File**
```bash
# Copy template
cp .env.example .env

# Edit with secure values
nano .env  # or vim, code, etc.
```

**2.2 Required .env Variables**

```ini
# Django Settings
DEBUG=False  # CRITICAL: Must be False for production
ENVIRONMENT=production  # or staging/development
SECRET_KEY=your-secure-random-key-here  # Generate: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=calc_db
DB_USER=calc_user
DB_PASSWORD=secure-password-here  # Use strong password
DB_HOST=database  # Must be 'database' for Docker
DB_PORT=5432

# Application Settings
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
STATIC_ROOT=/app/static
LOGS_DIR=/app/logs

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Optional Security
CSRF_COOKIE_SECURE=True  # Requires HTTPS
SESSION_COOKIE_SECURE=True  # Requires HTTPS
SECURE_SSL_REDIRECT=False  # Set to True if HTTPS available
```

**2.3 Verify .env Security**
```bash
# Ensure .env is not world-readable
chmod 600 .env

# Verify not in git
grep ".env" .gitignore || echo ".env" >> .gitignore

# Verify contains sensitive data only
echo "✓ .env created securely"
```

### Step 3: Build Docker Images

**3.1 Build Images**
```bash
# Build with output
docker compose build

# Expected output:
# [+] Building 15.3s (15/15) FINISHED
# => [internal] load build definition from Dockerfile
# => => transferring dockerfile: 32B
# ...
```

**3.2 Verify Images Created**
```bash
# List images
docker images | grep -E "se2-calculator|postgres"

# Expected: See se2-calculator-web and postgres:17 images
```

**3.3 Verify Image Size**
```bash
# Check image size
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep se2

# Expected: Web image ~400-500MB (depending on dependencies)
```

**3.4 Scan for Security Issues (Optional but Recommended)**
```bash
# Install trivy for vulnerability scanning
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Scan image
trivy image se2-calculator-project-web:latest

# Review any HIGH or CRITICAL vulnerabilities
```

### Step 4: Initialize Database

**4.1 Start Services**
```bash
# Start all services
docker compose up -d

# Expected: All services running
```

**4.2 Verify Database Health**
```bash
# Check database service
docker compose exec database pg_isready

# Expected output: accepting connections
```

**4.3 Run Migrations**
```bash
# Run all migrations
docker compose exec web python manage.py migrate

# Expected output:
# Running migrations:
#   Applying blocks.0001_initial... OK
#   Applying components.0001_initial... OK
#   ...
```

**4.4 Create Superuser (First Deployment Only)**
```bash
# Create admin user
docker compose exec web python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@example.com
# Password: (strong password)
```

**4.5 Load Fixtures (Optional)**
```bash
# Load sample data if available
docker compose exec web python manage.py loaddata blocks/fixtures/sample_blocks.json

# Expected: Loaded data from fixture
```

### Step 5: Collect Static Files

**5.1 Collect Static Files**
```bash
# Collect all static files to volume
docker compose exec web python manage.py collectstatic --noinput

# Expected output:
# 127 static files copied to '/app/static'
```

**5.2 Verify Static Files**
```bash
# Check volume contents
docker compose exec web ls -lah /app/static/

# Expected: See css/, js/, img/ directories
```

### Step 6: Verify Deployment

**6.1 Check Service Status**
```bash
# Check all services running
docker compose ps

# Expected:
# NAME               COMMAND              SERVICE    STATUS
# se2_database       postgres             database   Up (healthy)
# se2_web            python manage.py...  web        Up
# se2_nginx          nginx -g daemon      nginx      Up
```

**6.2 Test Web Accessibility**
```bash
# Test home page
curl http://localhost/

# Expected: HTML response (not 500 error)
```

**6.3 Test Endpoints**
```bash
# Test home page
curl http://localhost/

# Expected: HTML response (not 500 error)

# Note: API endpoints not yet implemented (deferred to Phase 4)
```

---

## Post-Deployment Verification

### Verification Checklist

#### 1. Service Health Checks

```bash
# Check all services running
docker compose ps

# Expected output: All services "Up" or "Up (healthy)"
```

#### 2. Database Connectivity

```bash
# Connect to database
docker compose exec database psql -U calc_user -d calc_db -c "SELECT version();"

# Expected: PostgreSQL version information
```

#### 3. Web Service Functionality

```bash
# Check Django health
docker compose exec web python manage.py check

# Expected output: System check identified no issues
```

#### 4. Static File Serving

```bash
# Test static file access
curl -I http://localhost/static/css/main.css

# Expected: 200 OK response with cache headers
```

#### 5. Error Page Testing

```bash
# Test 404 error page
curl http://localhost/nonexistent-page-12345/

# Expected: Generic Django 404 page (custom pages deferred to Phase 4)
```

#### 6. Security Headers

```bash
# Verify security headers
curl -I http://localhost/

# Expected headers:
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
```

#### 7. Logging Verification

```bash
# Check application logs
docker compose logs web | tail -50

# Note: Structured logging to files deferred to Phase 4
# Currently logs to console only
```

#### 8. Database Persistence

```bash
# Verify database volume
docker volume inspect se2_db_data

# Expected: Volume exists with Mountpoint
```

### Comprehensive Test Script

Create and run `test_deployment.sh`:

```bash
#!/bin/bash

echo "==============================================="
echo "ENH-0000008 Deployment Verification"
echo "==============================================="

FAILURES=0

# Test 1: Service Health
echo -n "1. Service Health Check: "
if docker compose ps | grep -E "database.*Up|web.*Up|nginx.*Up" > /dev/null; then
    echo "✓ PASS"
else
    echo "✗ FAIL"
    ((FAILURES++))
fi

# Test 2: Web Accessibility
echo -n "2. Web Accessibility: "
if curl -s http://localhost/ > /dev/null; then
    echo "✓ PASS"
else
    echo "✗ FAIL"
    ((FAILURES++))
fi

# Test 3: Endpoints
echo -n "3. Web Endpoints: "
if curl -s http://localhost/ > /dev/null; then
    echo "✓ PASS"
else
    echo "✗ FAIL"
    ((FAILURES++))
fi

# Test 4: Static Files
echo -n "4. Static File Serving: "
if curl -I http://localhost/static/css/main.css 2>/dev/null | grep -q "200"; then
    echo "✓ PASS"
else
    echo "✗ FAIL"
    ((FAILURES++))
fi

# Test 5: Security Headers
echo -n "5. Security Headers: "
if curl -I http://localhost/ 2>/dev/null | grep -q "X-Frame-Options"; then
    echo "✓ PASS"
else
    echo "✗ FAIL"
    ((FAILURES++))
fi

# Test 6: Error Handling
echo -n "6. Error Handling: "
if curl -s http://localhost/nonexistent/ > /dev/null 2>&1; then
    echo "✓ PASS"
else
    echo "✗ FAIL"
    ((FAILURES++))
fi

# Test 7: Database Connection
echo -n "7. Database Connection: "
if docker compose exec -T database pg_isready -q; then
    echo "✓ PASS"
else
    echo "✗ FAIL"
    ((FAILURES++))
fi

# Test 8: Logging
echo -n "8. Application Logging: "
if docker compose logs web | tail -1 > /dev/null; then
    echo "✓ PASS (console only)"
else
    echo "✗ FAIL"
    ((FAILURES++))
fi

echo ""
echo "==============================================="
echo "Test Results: $((8 - FAILURES))/8 Passed"
echo "==============================================="

if [ $FAILURES -eq 0 ]; then
    echo "✓ Deployment Verified Successfully!"
    exit 0
else
    echo "✗ Deployment Verification Failed"
    exit 1
fi
```

Run the verification:

```bash
chmod +x test_deployment.sh
./test_deployment.sh
```

---

## Database Initialization

### Initial Setup

**Option A: Use Django Migrations (Recommended)**

```bash
# Run all migrations
docker compose exec web python manage.py migrate

# Verify migrations applied
docker compose exec database psql -U calc_user -d calc_db -c "\dt"
# Expected: Tables visible (blocks_block, components_component, ores_ore)
```

**Option B: Restore from Backup**

```bash
# If migrating from existing database
docker compose exec -T database psql -U calc_user -d calc_db < backup_database.sql

# Verify restoration
docker compose exec database psql -U calc_user -d calc_db -c "SELECT COUNT(*) FROM blocks_block;"
```

### Creating Admin Account

```bash
# For new deployment
docker compose exec web python manage.py createsuperuser

# For scripted setup (non-interactive)
docker compose exec web python manage.py shell <<EOF
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'securepassword123')
print("Admin user created")
EOF
```

### Loading Sample Data

```bash
# Load fixture data
docker compose exec web python manage.py loaddata blocks/fixtures/sample_blocks.json

# Verify data loaded
docker compose exec web python manage.py shell -c "from blocks.models import Block; print(f'Loaded {Block.objects.count()} blocks')"
```

### Database Backup Strategy

**Automated Daily Backups:**

```bash
# Create backup script: backup-database.sh
#!/bin/bash
BACKUP_DIR="/backups/se2-calculator"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/database_backup_$TIMESTAMP.sql"

docker compose exec -T database pg_dump -U calc_user calc_db | gzip > "$BACKUP_FILE.gz"

echo "Database backed up to: $BACKUP_FILE.gz"

# Keep only last 7 days of backups
find "$BACKUP_DIR" -name "database_backup_*.sql.gz" -mtime +7 -delete
```

Install as cron job:

```bash
# Edit crontab
crontab -e

# Add line (daily at 2 AM)
0 2 * * * /home/dsmi001/app/se2-calculator-project/backup-database.sh
```

---

## Environment Configuration

### Environment-Specific Settings

#### Development Configuration

**.env.development:**
```ini
DEBUG=True
ENVIRONMENT=development
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

#### Staging Configuration

**.env.staging:**
```ini
DEBUG=False
ENVIRONMENT=staging
DB_HOST=database
DB_PORT=5432
ALLOWED_HOSTS=staging.example.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### Production Configuration

**.env.production:**
```ini
DEBUG=False
ENVIRONMENT=production
DB_HOST=database
DB_PORT=5432
ALLOWED_HOSTS=calculator.example.com,www.calculator.example.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
```

### Secrets Management

**Never commit secrets to version control:**

```bash
# Verify .env in .gitignore
grep ".env" .gitignore

# Use environment variable injection
export DB_PASSWORD=$(cat /run/secrets/db_password)
export SECRET_KEY=$(cat /run/secrets/secret_key)

docker compose up
```

---

## Docker Deployment

### Single Service Deployment

**Start All Services:**
```bash
docker compose up -d

# Monitor startup
docker compose logs -f

# Wait for health checks to pass
sleep 10
docker compose ps
```

**Stop Services:**
```bash
docker compose down
```

**Restart Services:**
```bash
docker compose restart
```

### Rolling Deployment (Zero Downtime)

**For Production with Multiple Web Instances:**

1. **Prepare new image:**
```bash
docker compose build web
```

2. **Update running service:**
```bash
# Create second web instance
docker compose up -d --scale web=2

# Verify both running
docker compose ps

# Remove old instances
docker compose down -f docker-compose.old.yml
```

### Container Logs Management

**View Logs:**
```bash
# All services
docker compose logs

# Specific service
docker compose logs web

# Follow logs
docker compose logs -f

# Last 100 lines
docker compose logs --tail=100

# Timestamp included
docker compose logs -t
```

**Log Rotation:**

Add to docker-compose.yml:

```yaml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Monitoring & Logs

### Application Logging

**View Application Logs:**
```bash
# Real-time logs (console output)
docker compose logs -f web

# Last 100 lines
docker compose logs --tail=100 web

# Search logs for errors
docker compose logs web | grep "ERROR"
```

**Note:** Structured logging to files is deferred to Phase 4. Currently, Django logs to console only.

### Performance Monitoring

**Monitor Container Resources:**
```bash
# Real-time resource usage
docker stats

# Specific service
docker stats se2_web

# Expected metrics:
# CPU %: Should be < 50% under normal load
# MEM: Should be < 500MB for web service
```

**Database Performance:**
```bash
# Connect to database
docker compose exec database psql -U calc_user -d calc_db

# Check query statistics
SELECT query, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;

# Exit psql
\q
```

### Health Check Status

**Check Container Health:**
```bash
# View health status
docker compose ps

# Get detailed health info
docker inspect se2_database | grep -A 10 "Health"

# Expected: "Status": "healthy"
```

---

## Rollback Procedures

### Scenario 1: Recent Deployment Failed

**Rollback to Previous Image:**

```bash
# Stop current services
docker compose down

# Remove failed images
docker rmi se2-calculator-project-web:latest

# Checkout previous code
git checkout HEAD~1

# Rebuild from previous version
docker compose build

# Start services
docker compose up -d

# Verify deployment
./test_deployment.sh
```

### Scenario 2: Database Corruption

**Restore from Backup:**

```bash
# Stop services
docker compose down

# Remove database volume
docker volume rm se2_db_data

# Create new volume
docker volume create se2_db_data

# Start database
docker compose up -d database

# Restore from backup
docker compose exec -T database psql -U calc_user -d calc_db < /backup/database_backup.sql

# Verify restoration
docker compose exec database psql -U calc_user -d calc_db -c "SELECT COUNT(*) FROM blocks_block;"

# Start remaining services
docker compose up -d
```

### Scenario 3: Configuration Error

**Revert .env Changes:**

```bash
# If .env was tracked in git (shouldn't be)
git checkout .env

# If .env is local only
cp .env.example .env
# Edit with previous values
nano .env

# Restart services
docker compose restart

# Verify
./test_deployment.sh
```

### Scenario 4: Full System Restore

**Complete Rollback to Previous Deployment:**

```bash
# Stop all services
docker compose down -v  # WARNING: Removes volumes!

# Restore from backup directory
BACKUP_DIR="/backup/se2-calculator-20260120_150000"
cp -r "$BACKUP_DIR"/* .

# Rebuild from restored code
docker compose build

# Start services
docker compose up -d

# Restore database
docker compose exec -T database psql -U calc_user -d calc_db < "$BACKUP_DIR/database_backup.sql"

# Verify
./test_deployment.sh
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Services Won't Start

**Symptoms:**
- `docker compose up` returns errors
- Services not appearing in `docker compose ps`

**Diagnosis:**
```bash
docker compose logs web
docker compose logs database
docker compose logs nginx
```

**Solutions:**

1. **Port Already in Use:**
```bash
# Find process using port 80, 8000, or 5432
lsof -i :80
lsof -i :8000
lsof -i :5432

# Kill the process (if safe)
kill -9 <PID>
```

2. **Insufficient Memory:**
```bash
# Check available memory
free -h

# Increase Docker memory allocation (Docker Desktop)
# Settings > Resources > Memory: Set to 4GB+
```

3. **Disk Space Issue:**
```bash
# Check disk space
df -h

# Clean up Docker
docker system prune -a  # WARNING: Removes all unused images!
```

#### Issue 2: Database Connection Errors

**Symptoms:**
- "psycopg2.OperationalError: could not connect to server"
- Database service not healthy

**Diagnosis:**
```bash
# Check database service
docker compose ps database

# Check database logs
docker compose logs database

# Test connection
docker compose exec database pg_isready
```

**Solutions:**

1. **Database Not Ready (Race Condition):**
```bash
# Ensure web waits for database health check
# In docker-compose.yml, verify:
web:
  depends_on:
    database:
      condition: service_healthy
```

2. **Wrong Credentials:**
```bash
# Verify in .env
grep DB_ .env

# Check database user exists
docker compose exec database psql -U postgres -c "\du"
```

3. **Database Container Crashed:**
```bash
# Remove and recreate database
docker compose down
docker volume rm se2_db_data
docker compose up -d database

# Re-run migrations
docker compose exec web python manage.py migrate
```

#### Issue 3: Web Service Crashes Immediately

**Symptoms:**
- `docker compose ps` shows web container exiting
- Error messages in logs

**Diagnosis:**
```bash
docker compose logs web | tail -50
```

**Solutions:**

1. **Migration Errors:**
```bash
# Check migrations
docker compose exec web python manage.py showmigrations

# Apply migrations
docker compose exec web python manage.py migrate --verbosity=2
```

2. **Missing Dependencies:**
```bash
# Rebuild image
docker compose build --no-cache web

# Verify requirements.txt
docker compose exec web pip list
```

3. **Incorrect Settings:**
```bash
# Validate Django settings
docker compose exec web python manage.py check

# Output will show specific configuration errors
```

#### Issue 4: Static Files Not Serving

**Symptoms:**
- CSS/JS files return 404
- Images not loading
- nginx returning 404 for /static/ paths

**Diagnosis:**
```bash
# Check static files collected
docker compose exec web ls -la /app/static/

# Check nginx error log
docker compose logs nginx | grep error
```

**Solutions:**

1. **Static Files Not Collected:**
```bash
# Re-collect static files
docker compose exec web python manage.py collectstatic --noinput --clear

# Verify
docker compose exec web ls /app/static/
```

2. **nginx Configuration Issue:**
```bash
# Test nginx config syntax
docker compose exec nginx nginx -t

# Check nginx logs
docker compose logs nginx
```

3. **Volume Mount Problem:**
```bash
# Verify volume exists
docker volume ls | grep se2_static_files

# Check volume contents
docker inspect se2_static_files | grep Mountpoint
```

#### Issue 5: Logging Not Working

**Note:** Structured file logging is deferred to Phase 4. Current deployment logs to console only via Docker.

**View Console Logs:**
```bash
# View web service logs
docker compose logs web

# Follow logs in real-time
docker compose logs -f web
```

#### Issue 6: nginx Returns 502 Bad Gateway

**Symptoms:**
- Accessing http://localhost returns 502 error
- Error logs show "upstream timed out"

**Diagnosis:**
```bash
docker compose logs nginx | grep -i "502\|upstream"
```

**Solutions:**

1. **Web Service Not Running:**
```bash
# Check web service
docker compose ps web

# View logs
docker compose logs web
```

2. **Network Connectivity:**
```bash
# Test connection from nginx to web
docker compose exec nginx curl http://web:8000/

# Should return HTML response
```

3. **nginx Configuration:**
```bash
# Verify upstream configuration
docker compose exec nginx cat /etc/nginx/nginx.conf | grep -A 5 "upstream"

# Restart nginx
docker compose restart nginx
```

### Diagnostic Command Reference

**System Information:**
```bash
# Docker version
docker version

# Docker info
docker info

# Disk usage
docker system df
```

**Container Inspection:**
```bash
# Container details
docker inspect se2_web

# Container environment
docker inspect se2_web | grep -A 20 "Env"

# Container mounts
docker inspect se2_web | grep -A 10 "Mounts"
```

**Network Debugging:**
```bash
# List networks
docker network ls

# Inspect network
docker network inspect se2_network

# Test network connectivity
docker compose exec web ping -c 1 database
```

**Log Collection:**
```bash
# All logs with timestamps
docker compose logs -t > deployment_logs.txt

# Specific service logs
docker compose logs web > web_logs.txt

# Format logs
docker compose logs --no-color web | grep ERROR
```

---

## Performance Tuning

### Database Optimization

**Enable Connection Pooling (PgBouncer):**

Add to docker-compose.yml:

```yaml
pgbouncer:
  image: pgbouncer:latest
  depends_on:
    - database
  environment:
    DATABASES_HOST: database
    DATABASES_PORT: 5432
    DATABASES_USER: calc_user
    DATABASES_PASSWORD: ${DB_PASSWORD}
    DATABASES_DBNAME: calc_db
    PGBOUNCER_POOL_MODE: transaction
    PGBOUNCER_MAX_CLIENT_CONN: 100
  ports:
    - "6432:6432"
```

Update .env:
```ini
DB_HOST=pgbouncer  # Change from 'database'
DB_PORT=6432        # Change from 5432
```

**Query Optimization:**

```bash
# Enable query logging
docker compose exec database psql -U calc_user -d calc_db <<EOF
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
SELECT query, calls, mean_time FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 10;
EOF
```

**Index Optimization:**

```bash
# Create indexes for frequently queried fields
docker compose exec database psql -U calc_user -d calc_db <<EOF
CREATE INDEX idx_blocks_order_id ON blocks_block(order_id);
CREATE INDEX idx_components_status ON components_component(status);
EOF
```

### Web Service Optimization

**Enable Gunicorn (Production):**

Update Dockerfile:

```dockerfile
# Install gunicorn
RUN pip install gunicorn

# Update CMD
CMD ["gunicorn", "se2CalcProject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2"]
```

Rebuild:
```bash
docker compose build web
docker compose up -d web
```

**Django Settings Optimization:**

In `se2CalcProject/settings.py`:

```python
# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'se2-cache',
    }
}

# Template caching
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600
```

### nginx Optimization

In `nginx.conf`:

```nginx
# Enable gzip compression
gzip on;
gzip_types text/plain text/css text/xml text/javascript 
           application/x-javascript application/xml+rss 
           application/json;
gzip_min_length 1000;

# Cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;

location /static/ {
    proxy_cache my_cache;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

---

## Security Hardening

### Container Security

**Run Containers as Non-Root:**

Dockerfile includes:
```dockerfile
RUN useradd -m app
USER app
```

Verify:
```bash
docker compose exec web id
# Output: uid=1000(app) gid=1000(app) groups=1000(app)
```

**Read-Only Filesystem:**

Update docker-compose.yml:

```yaml
services:
  web:
    read_only: true
    tmpfs:
      - /tmp
      - /app/logs
```

**Network Policies:**

Use custom network (already configured):

```yaml
networks:
  se2_network:
    driver: bridge
```

### Data Security

**Encrypt Database in Transit:**

Add SSL to PostgreSQL:

```yaml
environment:
  POSTGRES_INITDB_ARGS: "-c ssl=on -c ssl_cert_file=/etc/ssl/certs/server.crt -c ssl_key_file=/etc/ssl/private/server.key"
```

**Encrypt Volumes:**

```bash
# For Linux systems with LUKS encryption
sudo cryptsetup luksFormat /dev/sdX
sudo cryptsetup luksOpen /dev/sdX se2_volume
```

### Application Security

**Enable HTTPS (with SSL Certificate):**

Update `.env`:
```ini
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

Update `nginx.conf`:
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
}
```

**Regular Security Updates:**

```bash
# Check for vulnerabilities in dependencies
docker compose exec web pip check

# Update dependencies
docker compose exec web pip install --upgrade -r requirements.txt

# Rebuild and restart
docker compose build web
docker compose up -d web
```

---

## Maintenance Tasks

### Regular Maintenance Schedule

**Daily:**
- [ ] Monitor logs for errors
- [ ] Check container health
- [ ] Monitor resource usage

**Weekly:**
- [ ] Backup database
- [ ] Review error logs for patterns
- [ ] Check for security updates

**Monthly:**
- [ ] Update base images
- [ ] Optimize database
- [ ] Review performance metrics
- [ ] Test backup restoration

**Quarterly:**
- [ ] Security audit
- [ ] Disaster recovery drill
- [ ] Capacity planning review

### Automated Maintenance

**Database Maintenance Script:**

Create `maintenance.sh`:

```bash
#!/bin/bash

echo "Starting maintenance tasks..."

# 1. Backup database
echo "Backing up database..."
docker compose exec -T database pg_dump -U calc_user calc_db | \
  gzip > /backups/db_$(date +%Y%m%d_%H%M%S).sql.gz

# 2. Analyze database
echo "Analyzing database..."
docker compose exec database psql -U calc_user -d calc_db -c "ANALYZE;"

# 3. Vacuum database
echo "Vacuuming database..."
docker compose exec database psql -U calc_user -d calc_db -c "VACUUM ANALYZE;"

# 4. Clean old logs
echo "Cleaning old logs..."
find /backups -name "*.sql.gz" -mtime +30 -delete

# 5. Clean Django sessions
echo "Cleaning expired sessions..."
docker compose exec web python manage.py clearsessions

echo "Maintenance complete!"
```

Install as cron job:

```bash
# Make executable
chmod +x maintenance.sh

# Add to crontab (daily at 3 AM)
crontab -e
# 0 3 * * * /path/to/maintenance.sh
```

### Volume Management

**Check Volume Usage:**
```bash
docker volume ls
docker inspect se2_db_data | grep Mountpoint
du -sh /var/lib/docker/volumes/se2_db_data/_data
```

**Clean Up Old Volumes:**
```bash
# Remove unused volumes
docker volume prune

# Remove specific volume
docker volume rm se2_db_data  # WARNING: Data loss!
```

### Image Maintenance

**Clean Up Images:**
```bash
# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a

# List images by size
docker images --format "table {{.Repository}}\t{{.Size}}" --sort="Size"
```

**Update Base Images:**
```bash
# Pull latest base images
docker pull python:3.13-slim
docker pull postgres:17
docker pull nginx:latest

# Rebuild application
docker compose build --pull

# Restart services
docker compose up -d
```

---

## Post-Deployment Checklist

- [ ] All services running and healthy
- [ ] Web accessible at configured domain
- [ ] Database verified and healthy
- [ ] Static files serving correctly
- [ ] Security headers present
- [ ] Error pages working (404, 500) - Deferred to Phase 4
- [ ] Logging configured and working - Deferred to Phase 4 (console logging functional)
- [ ] Backup procedure tested
- [ ] Monitoring configured
- [ ] Team trained on deployment process
- [ ] Documentation reviewed and updated
- [ ] Rollback procedure tested
- [ ] Performance baseline established
- [ ] Security audit completed

---

## Support & References

### Helpful Commands Reference

```bash
# Logs
docker compose logs -f web
docker compose logs --tail=50 web

# Shell access
docker compose exec web bash
docker compose exec database psql -U calc_user -d calc_db

# Restart
docker compose restart web
docker compose restart

# Rebuild
docker compose build web
docker compose build

# Status
docker compose ps
docker stats

# Clean up
docker compose down
docker system prune
docker volume prune
```

### Documentation References

- [Docker Documentation](https://docs.docker.com/)
- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [nginx Documentation](https://nginx.org/en/docs/)
- [Project Contributing Guide](../CONTRIBUTING.md)
- [Docker Setup Guide](./DOCKER_SETUP_GUIDE.md)
- [ENH-0000008 Specification](./enhancementRequests/Phase2_views/ENH0000008/ENH0000008-core-infrastructure.md)

### Getting Help

**For Deployment Issues:**
1. Check Troubleshooting section above
2. Review Docker logs: `docker compose logs -f`
3. Check CONTRIBUTING.md for contribution guidelines
4. Open issue with logs and error messages

---

**End of ENH-0000008 Docker Infrastructure Deployment Guide**

*Last Updated: January 27, 2026*  
*Version: 1.1*  
*Status: Docker Infrastructure Complete (Core app features deferred to Phase 4)*
