---
inclusion: auto
description: Security best practices for Django applications including input validation, authentication, CSRF protection, and secrets management
---

# Security Best Practices

## Security Mindset

### Defense in Depth
- Multiple layers of security
- Assume each layer can be breached
- Validate at every boundary
- Never trust user input

### Principle of Least Privilege
- Grant minimum necessary permissions
- Restrict access by default
- Require explicit authorization
- Regularly audit permissions

## Django Security Settings

### Essential Settings
```python
# settings.py

# CRITICAL: Never use DEBUG=True in production
DEBUG = False

# Set allowed hosts explicitly
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Use strong secret key (never commit to git)
SECRET_KEY = os.environ.get('SECRET_KEY')

# HTTPS/SSL settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

## Input Validation

### Always Validate User Input
```python
# BAD: No validation
def create_block(request):
    name = request.POST.get('name')
    mass = request.POST.get('mass')
    Block.objects.create(name=name, mass=mass)

# GOOD: Use Django forms
from django import forms

class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ['name', 'mass', 'description']
    
    def clean_mass(self):
        mass = self.cleaned_data['mass']
        if mass <= 0:
            raise forms.ValidationError("Mass must be positive")
        if mass > 1000000:
            raise forms.ValidationError("Mass too large")
        return mass

def create_block(request):
    form = BlockForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        # Handle errors
        pass
```

### Sanitize Output
```django
{# Django templates auto-escape by default #}
{{ user_input }}  {# Safe - auto-escaped #}

{# Only use |safe when you control the content #}
{{ trusted_html|safe }}  {# Use sparingly #}

{# For JSON in templates #}
{{ data|json_script:"data-id" }}
```

## SQL Injection Prevention

### Use Django ORM
```python
# GOOD: Django ORM (parameterized)
Block.objects.filter(name=user_input)

# GOOD: Parameterized raw SQL
Block.objects.raw(
    "SELECT * FROM blocks WHERE name = %s",
    [user_input]
)

# BAD: String formatting (SQL injection risk)
Block.objects.raw(f"SELECT * FROM blocks WHERE name = '{user_input}'")

# BAD: String concatenation
query = "SELECT * FROM blocks WHERE name = '" + user_input + "'"
```

### Validate Query Parameters
```python
def search_blocks(request):
    # Validate search term
    search = request.GET.get('q', '')
    if len(search) > 100:
        return HttpResponseBadRequest("Search term too long")
    
    # Use ORM safely
    blocks = Block.objects.filter(name__icontains=search)
    return render(request, 'search.html', {'blocks': blocks})
```

## Cross-Site Scripting (XSS) Prevention

### Template Auto-Escaping
```django
{# Django auto-escapes by default #}
<p>{{ user_comment }}</p>  {# Safe #}

{# Disable only when necessary #}
{% autoescape off %}
    {{ trusted_content }}
{% endautoescape %}
```

### JavaScript Context
```django
{# BAD: XSS vulnerability #}
<script>
    var name = "{{ user_name }}";  {# Dangerous #}
</script>

{# GOOD: Use json_script #}
{{ user_data|json_script:"user-data" }}
<script>
    const userData = JSON.parse(
        document.getElementById('user-data').textContent
    );
</script>
```

## Cross-Site Request Forgery (CSRF) Prevention

### Use CSRF Protection
```python
# Django enables CSRF by default
# Always include {% csrf_token %} in forms

# In templates
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>

# For AJAX requests
// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Include in AJAX headers
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
});
```

## Authentication & Authorization

### Require Authentication
```python
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Function-based view
@login_required
def my_view(request):
    pass

# Class-based view
class MyView(LoginRequiredMixin, View):
    pass
```

### Check Permissions
```python
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

# Decorator
@permission_required('blocks.add_block')
def create_block(request):
    pass

# Manual check
def edit_block(request, pk):
    block = Block.objects.get(pk=pk)
    if block.owner != request.user:
        raise PermissionDenied
    # Edit logic
```

### Object-Level Permissions
```python
def delete_block(request, pk):
    block = get_object_or_404(Block, pk=pk)
    
    # Check ownership
    if block.owner != request.user and not request.user.is_staff:
        raise PermissionDenied("You don't own this block")
    
    block.delete()
    return redirect('block_list')
```

## Password Security

### Strong Password Requirements
```python
# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### Never Store Plain Passwords
```python
# GOOD: Django handles hashing automatically
user = User.objects.create_user(
    username='john',
    password='secure_password'  # Automatically hashed
)

# Check password
user.check_password('secure_password')  # Returns True/False

# BAD: Never do this
user.password = 'plain_password'  # Don't store plain text
```

## Secrets Management

### Environment Variables
```python
# settings.py
import os
from pathlib import Path

# Load from environment
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
API_KEY = os.environ.get('API_KEY')

# Fail if critical secrets missing
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")
```

### .env Files (Development Only)
```bash
# .env (never commit this file)
SECRET_KEY=your-secret-key-here
DB_PASSWORD=your-db-password
API_KEY=your-api-key

# .env.example (commit this)
SECRET_KEY=
DB_PASSWORD=
API_KEY=
```

### .gitignore
```
# .gitignore
.env
*.key
*.pem
secrets.json
```

## File Upload Security

### Validate File Types
```python
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.jpg', '.png']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class Document(models.Model):
    file = models.FileField(
        upload_to='documents/',
        validators=[validate_file_extension]
    )
```

### Limit File Size
```python
# settings.py
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# In form
class UploadForm(forms.Form):
    file = forms.FileField()
    
    def clean_file(self):
        file = self.cleaned_data['file']
        if file.size > 5242880:  # 5MB
            raise forms.ValidationError("File too large (max 5MB)")
        return file
```

### Store Files Securely
```python
# settings.py
# Don't serve uploaded files from STATIC_ROOT
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# In production, serve media files through web server
# with proper access controls
```

## API Security

### Rate Limiting
```python
from django.core.cache import cache
from django.http import HttpResponseForbidden

def rate_limit(max_requests=100, window=3600):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Get client IP
            ip = request.META.get('REMOTE_ADDR')
            cache_key = f'rate_limit_{ip}'
            
            # Check rate limit
            requests = cache.get(cache_key, 0)
            if requests >= max_requests:
                return HttpResponseForbidden("Rate limit exceeded")
            
            # Increment counter
            cache.set(cache_key, requests + 1, window)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_requests=100, window=3600)
def api_endpoint(request):
    pass
```

### API Authentication
```python
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_view(request):
    # Only authenticated users can access
    pass
```

## Logging and Monitoring

### Security Logging
```python
import logging

security_logger = logging.getLogger('security')

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        security_logger.info(f"Successful login: {username}")
    else:
        security_logger.warning(f"Failed login attempt: {username}")
```

### Monitor for Attacks
```python
# Log suspicious activity
def suspicious_activity(request, reason):
    logger = logging.getLogger('security')
    logger.warning(
        f"Suspicious activity detected: {reason}",
        extra={
            'ip': request.META.get('REMOTE_ADDR'),
            'user': request.user.username if request.user.is_authenticated else 'anonymous',
            'path': request.path,
            'user_agent': request.META.get('HTTP_USER_AGENT'),
        }
    )
```

## Dependency Security

### Keep Dependencies Updated
```bash
# Check for security vulnerabilities
pip install safety
safety check

# Update dependencies
pip list --outdated
pip install --upgrade package-name
```

### Pin Dependencies
```
# requirements.txt
Django==6.0.1  # Pin exact versions
psycopg2-binary==2.9.9
pytest-django==4.8.0
```

## Security Checklist

### Development
- [ ] Never commit secrets to git
- [ ] Use environment variables for configuration
- [ ] Enable DEBUG=False in production
- [ ] Use HTTPS in production
- [ ] Validate all user input
- [ ] Use Django forms for validation
- [ ] Enable CSRF protection
- [ ] Use Django ORM (avoid raw SQL)

### Authentication
- [ ] Require strong passwords
- [ ] Use Django's authentication system
- [ ] Implement proper authorization checks
- [ ] Use HTTPS for login pages
- [ ] Implement rate limiting for login
- [ ] Log authentication events

### Data Protection
- [ ] Encrypt sensitive data at rest
- [ ] Use HTTPS for data in transit
- [ ] Sanitize output to prevent XSS
- [ ] Validate file uploads
- [ ] Implement proper access controls
- [ ] Regular security audits

### Monitoring
- [ ] Log security events
- [ ] Monitor for suspicious activity
- [ ] Set up alerts for security issues
- [ ] Regular security reviews
- [ ] Keep dependencies updated
- [ ] Scan for vulnerabilities

## Security Resources

### Django Security
- Django Security Documentation
- OWASP Top 10
- Django Security Releases

### Tools
- Safety (dependency scanning)
- Bandit (Python security linter)
- Django Security Middleware
- django-axes (brute force protection)

### Best Practices
- Regular security audits
- Penetration testing
- Security training for developers
- Incident response plan
