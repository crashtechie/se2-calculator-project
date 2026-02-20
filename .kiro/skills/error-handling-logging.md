# Error Handling & Logging

## When to Activate This Skill

- Implementing error handling strategies
- Setting up application logging
- Debugging production issues
- Monitoring application health
- Handling exceptions gracefully
- Creating error reporting systems

## Python Exception Handling

### Basic Exception Handling
```python
def calculate_resources(block_id, quantity):
    """Calculate resources with proper error handling"""
    try:
        block = Block.objects.get(id=block_id)
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        return block.calculate_total_resources(quantity)
    except Block.DoesNotExist:
        logger.error(f"Block {block_id} not found")
        raise
    except ValueError as e:
        logger.warning(f"Invalid quantity: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error calculating resources: {e}")
        raise
```

### Custom Exceptions
```python
# exceptions.py
class CalculatorException(Exception):
    """Base exception for calculator app"""
    pass

class InsufficientResourcesError(CalculatorException):
    """Raised when resources are insufficient"""
    def __init__(self, required, available):
        self.required = required
        self.available = available
        super().__init__(f"Required: {required}, Available: {available}")

class InvalidBlockConfigurationError(CalculatorException):
    """Raised when block configuration is invalid"""
    pass

# Usage
def build_order(block, quantity, available_resources):
    required = block.calculate_resources(quantity)
    if required > available_resources:
        raise InsufficientResourcesError(required, available_resources)
```

### Context Managers for Resource Cleanup
```python
from contextlib import contextmanager

@contextmanager
def database_transaction():
    """Context manager for database operations"""
    try:
        yield
        transaction.commit()
    except Exception as e:
        transaction.rollback()
        logger.error(f"Transaction failed: {e}")
        raise
    finally:
        connection.close()

# Usage
with database_transaction():
    Block.objects.create(name="Test")
```

## Django Error Handling

### View Error Handling
```python
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError, PermissionDenied
import logging

logger = logging.getLogger(__name__)

def block_detail(request, pk):
    """View with comprehensive error handling"""
    try:
        block = get_object_or_404(Block, pk=pk)
        
        # Check permissions
        if not block.is_public and block.owner != request.user:
            raise PermissionDenied("You don't have permission to view this block")
        
        return render(request, 'blocks/detail.html', {'block': block})
    
    except PermissionDenied as e:
        logger.warning(f"Permission denied for user {request.user}: {e}")
        return render(request, 'errors/403.html', status=403)
    except Exception as e:
        logger.exception(f"Error displaying block {pk}: {e}")
        return render(request, 'errors/500.html', status=500)
```

### API Error Responses
```python
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """Custom DRF exception handler"""
    response = exception_handler(exc, context)
    
    if response is not None:
        # Standardize error format
        custom_response = {
            'error': {
                'code': response.status_code,
                'message': str(exc),
                'details': response.data
            }
        }
        response.data = custom_response
    else:
        # Handle non-DRF exceptions
        logger.exception(f"Unhandled exception: {exc}")
        custom_response = {
            'error': {
                'code': 500,
                'message': 'Internal server error',
                'details': str(exc) if settings.DEBUG else 'An error occurred'
            }
        }
        response = Response(custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response

# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.utils.custom_exception_handler'
}
```

### Custom Error Pages
```python
# views.py
def handler404(request, exception):
    """Custom 404 error handler"""
    logger.warning(f"404 error: {request.path}")
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """Custom 500 error handler"""
    logger.error(f"500 error on {request.path}")
    return render(request, 'errors/500.html', status=500)

# urls.py
handler404 = 'myapp.views.handler404'
handler500 = 'myapp.views.handler500'
```

## Logging Configuration

### Basic Logging Setup
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/errors.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myapp': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

### Structured Logging
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Format logs as JSON for easier parsing"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        return json.dumps(log_data)

# settings.py
LOGGING = {
    'formatters': {
        'json': {
            '()': 'myapp.logging.JSONFormatter',
        },
    },
    'handlers': {
        'json_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.json',
            'formatter': 'json',
        },
    },
}
```

### Logger Usage
```python
import logging

logger = logging.getLogger(__name__)

def process_build_order(order_id):
    """Example of proper logging"""
    logger.info(f"Processing build order {order_id}")
    
    try:
        order = BuildOrder.objects.get(id=order_id)
        logger.debug(f"Order details: {order}")
        
        # Process order
        result = order.calculate_resources()
        logger.info(f"Order {order_id} processed successfully", extra={
            'order_id': order_id,
            'resource_count': len(result)
        })
        
        return result
    
    except BuildOrder.DoesNotExist:
        logger.error(f"Build order {order_id} not found")
        raise
    except Exception as e:
        logger.exception(f"Failed to process order {order_id}: {e}", extra={
            'order_id': order_id,
            'error_type': type(e).__name__
        })
        raise
```

## Monitoring and Alerting

### Health Check Endpoint
```python
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Health check endpoint for monitoring"""
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'checks': {}
    }
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['checks']['database'] = 'ok'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = f'error: {str(e)}'
        logger.error(f"Database health check failed: {e}")
    
    # Cache check
    try:
        from django.core.cache import cache
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            health_status['checks']['cache'] = 'ok'
        else:
            raise Exception("Cache read/write failed")
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['cache'] = f'error: {str(e)}'
        logger.error(f"Cache health check failed: {e}")
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)
```

### Performance Monitoring
```python
import time
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"{func.__name__} completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{func.__name__} failed after {duration:.3f}s: {e}")
            raise
    return wrapper

@monitor_performance
def expensive_calculation(block_id):
    """Function with performance monitoring"""
    return Block.objects.get(id=block_id).calculate_all_resources()
```


### Request ID Tracking
```python
import uuid
from django.utils.deprecation import MiddlewareMixin

class RequestIDMiddleware(MiddlewareMixin):
    """Add unique request ID for tracking"""
    
    def process_request(self, request):
        request.id = str(uuid.uuid4())
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'id'):
            response['X-Request-ID'] = request.id
        return response

# Use in logging
logger.info("Processing request", extra={'request_id': request.id})
```

## Error Reporting

### Sentry Integration
```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False,
    environment=os.environ.get('ENVIRONMENT', 'development'),
)

# Custom error context
from sentry_sdk import capture_exception, set_context

def process_order(order_id):
    try:
        order = BuildOrder.objects.get(id=order_id)
        set_context("order", {
            "id": order.id,
            "status": order.status,
            "user": order.user.username
        })
        # Process order
    except Exception as e:
        capture_exception(e)
        raise
```

### Email Error Notifications
```python
# settings.py
ADMINS = [('Admin Name', 'admin@example.com')]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Custom email handler
from django.core.mail import mail_admins

def notify_admins_on_error(error_message, details):
    """Send email notification for critical errors"""
    subject = f"Critical Error: {error_message}"
    message = f"""
    Error: {error_message}
    
    Details:
    {details}
    
    Time: {timezone.now()}
    """
    mail_admins(subject, message, fail_silently=True)
```

## Debugging Techniques

### Django Debug Toolbar
```python
# settings.py (development only)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
    
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    }
```

### Print Debugging (Development)
```python
import pprint

def debug_view(request):
    """Debugging helper"""
    print("=" * 50)
    print("REQUEST DEBUG INFO")
    print("=" * 50)
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print(f"User: {request.user}")
    print("\nGET params:")
    pprint.pprint(dict(request.GET))
    print("\nPOST params:")
    pprint.pprint(dict(request.POST))
    print("=" * 50)
```

### Python Debugger (pdb)
```python
def complex_calculation(data):
    """Use pdb for interactive debugging"""
    result = process_step_1(data)
    
    # Set breakpoint
    import pdb; pdb.set_trace()
    
    result = process_step_2(result)
    return result

# Or use breakpoint() in Python 3.7+
def another_function():
    breakpoint()  # Cleaner syntax
```

## Best Practices

### Logging Levels
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages for potentially harmful situations
- ERROR: Error messages for serious problems
- CRITICAL: Critical messages for very serious errors

### What to Log
```python
# Good logging practices
logger.info("User login", extra={'user_id': user.id, 'ip': request.META['REMOTE_ADDR']})
logger.warning("Rate limit exceeded", extra={'user_id': user.id, 'endpoint': request.path})
logger.error("Payment processing failed", extra={'order_id': order.id, 'amount': order.total})
logger.exception("Unexpected error in calculation")  # Includes traceback
```

### What NOT to Log
```python
# Bad: Don't log sensitive data
logger.info(f"User password: {password}")  # Never!
logger.info(f"Credit card: {card_number}")  # Never!
logger.info(f"API key: {api_key}")  # Never!

# Good: Log safely
logger.info(f"User authenticated", extra={'user_id': user.id})
logger.info(f"Payment processed", extra={'last_4_digits': card_number[-4:]})
```

### Exception Handling Strategy
- Catch specific exceptions, not generic Exception
- Log before re-raising
- Provide context in error messages
- Clean up resources in finally blocks
- Don't silence exceptions without logging

### Production Considerations
- Use log rotation to prevent disk space issues
- Send critical errors to monitoring services
- Set appropriate log levels (INFO or WARNING in production)
- Don't log sensitive information
- Monitor log volume and performance impact

## Testing Error Handling

### Testing Exceptions
```python
import pytest
from django.test import TestCase

class ErrorHandlingTest(TestCase):
    def test_invalid_quantity_raises_error(self):
        """Test that invalid quantity raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_resources(block_id=1, quantity=-1)
    
    def test_missing_block_raises_not_found(self):
        """Test that missing block raises DoesNotExist"""
        with self.assertRaises(Block.DoesNotExist):
            Block.objects.get(id=99999)
    
    def test_custom_exception_message(self):
        """Test custom exception message"""
        with self.assertRaisesMessage(
            InsufficientResourcesError,
            "Required: 100, Available: 50"
        ):
            raise InsufficientResourcesError(100, 50)
```

### Testing Logging
```python
from unittest.mock import patch
import logging

class LoggingTest(TestCase):
    @patch('myapp.views.logger')
    def test_error_is_logged(self, mock_logger):
        """Test that errors are logged"""
        response = self.client.get('/invalid-url/')
        mock_logger.error.assert_called_once()
    
    def test_log_output(self):
        """Test log output with caplog"""
        with self.assertLogs('myapp', level='INFO') as cm:
            logger = logging.getLogger('myapp')
            logger.info('Test message')
            self.assertIn('Test message', cm.output[0])
```

## Common Pitfalls

### Swallowing Exceptions
```python
# Bad: Silent failure
try:
    risky_operation()
except Exception:
    pass  # Error is lost!

# Good: Log and handle
try:
    risky_operation()
except Exception as e:
    logger.exception(f"Operation failed: {e}")
    # Handle or re-raise
```

### Logging in Loops
```python
# Bad: Too much logging
for item in large_list:
    logger.info(f"Processing {item}")  # Floods logs

# Good: Log summary
logger.info(f"Processing {len(large_list)} items")
for item in large_list:
    process(item)
logger.info("Processing complete")
```

### Not Using Log Levels
```python
# Bad: Everything is INFO
logger.info("Starting process")
logger.info("Error occurred!")  # Should be ERROR

# Good: Appropriate levels
logger.info("Starting process")
logger.error("Error occurred!")
```

## Resources

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Django Logging](https://docs.djangoproject.com/en/stable/topics/logging/)
- [Sentry Documentation](https://docs.sentry.io/)
- [12 Factor App Logs](https://12factor.net/logs)
