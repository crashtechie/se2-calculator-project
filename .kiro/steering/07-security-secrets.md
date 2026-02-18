# Security & Secrets Management

## Environment Variables

### Required Secrets
- `SECRET_KEY` - Django secret key (50+ characters)
- `DB_PASSWORD` - PostgreSQL password
- Never commit these to version control

### Secret Generation
```bash
# Use the provided script
uv run python scripts/secrets_gen.py

# Manually generate if needed
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Environment Files
- `.env` - Local development (gitignored)
- `.env.example` - Template with placeholder values (committed)
- Production: Use environment variables directly, not .env files

## Database Credentials

### Development
- Use generated credentials from `secrets_gen.py`
- Store in `.env` file
- Never share credentials in chat, issues, or documentation

### Docker
- Set `DB_HOST=database` for Docker stack
- Set `DB_HOST=localhost` for local development
- Credentials must match between `.env` and `docker-compose.yml`

### Production
- Use managed database services (AWS RDS, etc.)
- Rotate credentials regularly (quarterly minimum)
- Use IAM authentication where possible
- Enable SSL/TLS for database connections

## Django Security Settings

### Required Settings
```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### CSRF Protection
- Always include `{% csrf_token %}` in forms
- Use `@csrf_protect` decorator for function views
- Never disable CSRF protection

### XSS Protection
- Use Django's template auto-escaping (enabled by default)
- Use `|safe` filter only for trusted content
- Sanitize user input before storage
- Use `mark_safe()` only when necessary

## API Keys & Third-Party Services

### Storage
- Store in environment variables
- Never hardcode in source code
- Use Django's `settings.py` to access: `settings.API_KEY`

### Rotation
- Rotate API keys when team members leave
- Rotate after any suspected compromise
- Document rotation procedures

## User Authentication

### Password Requirements
- Minimum 8 characters (Django default)
- Use Django's built-in password validators
- Enable password reset functionality
- Never store plaintext passwords

### Session Management
- Use Django's session framework
- Set appropriate `SESSION_COOKIE_AGE`
- Enable `SESSION_EXPIRE_AT_BROWSER_CLOSE` for sensitive apps

## File Upload Security

### Validation
- Validate file types and extensions
- Limit file sizes
- Scan for malware (production)
- Store uploads outside web root

### Storage
```python
# Use Django's FileField/ImageField
# Configure MEDIA_ROOT and MEDIA_URL
# Serve via nginx in production, not Django
```

## Dependency Security

### Regular Updates
```bash
# Check for vulnerabilities
uv pip list --outdated

# Update dependencies
uv pip install --upgrade package-name

# Update all (carefully)
uv sync --upgrade
```

### Monitoring
- Enable GitHub Dependabot alerts
- Review security advisories regularly
- Test updates in development first

## Logging & Monitoring

### Sensitive Data
- Never log passwords or tokens
- Redact sensitive data in logs
- Use structured logging for security events

### Security Events to Log
- Failed login attempts
- Permission denied errors
- Suspicious activity patterns
- Database connection failures

## Docker Security

### Image Security
- Use official base images
- Keep base images updated
- Scan images for vulnerabilities
- Use specific version tags, not `latest`

### Container Security
- Run as non-root user (already configured)
- Limit container resources
- Use read-only filesystems where possible
- Enable Docker security scanning

## Incident Response

### If Credentials Compromised
1. Immediately rotate all affected credentials
2. Review access logs for unauthorized activity
3. Update `.env` and redeploy
4. Notify team members
5. Document incident

### If Database Compromised
1. Take database offline if actively attacked
2. Restore from clean backup
3. Rotate all credentials
4. Review and patch vulnerabilities
5. Enable additional monitoring

## Security Checklist

### Before Deployment
- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] Database credentials rotated
- [ ] `ALLOWED_HOSTS` configured
- [ ] HTTPS enabled
- [ ] Security headers configured (via nginx)
- [ ] Dependencies updated
- [ ] No secrets in version control
- [ ] Backup procedures tested

### Regular Maintenance
- [ ] Rotate credentials quarterly
- [ ] Update dependencies monthly
- [ ] Review access logs weekly
- [ ] Test backup restoration quarterly
- [ ] Security audit annually
