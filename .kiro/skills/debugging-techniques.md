# Debugging Techniques Skill

## When to Activate
Use this skill when:
- Investigating bugs or unexpected behavior
- Tests are failing
- Application crashes or errors occur
- Performance issues need diagnosis
- User reports issues that can't be reproduced

## Systematic Debugging Approach

### 1. Reproduce the Issue
- Create minimal test case that triggers the bug
- Document exact steps to reproduce
- Note environment details (OS, Python version, dependencies)
- Verify issue exists in clean environment

### 2. Isolate the Problem
- Binary search: Comment out half the code
- Narrow down to specific function/module
- Identify last working version (git bisect)
- Remove unrelated code

### 3. Understand the Root Cause
- Read error messages carefully
- Check stack traces
- Review recent changes
- Verify assumptions

### 4. Fix and Verify
- Write test that reproduces bug
- Implement fix
- Verify test passes
- Check for regressions

## Django-Specific Debugging

### Django Debug Toolbar
```python
# settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# Shows:
# - SQL queries and execution time
# - Template rendering time
# - Cache hits/misses
# - Signal calls
# - Request/response headers
```

### Django Shell for Investigation
```bash
# Start Django shell
python manage.py shell

# Import models and test
from app.blocks.models import Block
block = Block.objects.first()
print(block.calculate_total_mass())

# Test queries
from django.db import connection
Block.objects.filter(mass__gt=10)
print(connection.queries[-1])  # See last query
```

### Django Logging
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'app': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}

# In code
import logging
logger = logging.getLogger(__name__)

def my_view(request):
    logger.debug(f"Request data: {request.POST}")
    logger.info("Processing request")
    logger.warning("Potential issue detected")
    logger.error("Error occurred", exc_info=True)
```

## Python Debugging Tools

### PDB (Python Debugger)
```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint() (Python 3.7+)
breakpoint()

# PDB Commands:
# n (next) - Execute next line
# s (step) - Step into function
# c (continue) - Continue execution
# l (list) - Show code context
# p variable - Print variable value
# pp variable - Pretty print variable
# w (where) - Show stack trace
# u (up) - Move up stack frame
# d (down) - Move down stack frame
# q (quit) - Exit debugger
```

### IPython Debugger (ipdb)
```python
# More user-friendly than pdb
import ipdb; ipdb.set_trace()

# Features:
# - Tab completion
# - Syntax highlighting
# - Better history
```

### Post-Mortem Debugging
```python
import pdb
import traceback

try:
    # Code that might fail
    risky_operation()
except Exception:
    traceback.print_exc()
    pdb.post_mortem()  # Debug at point of exception
```

## Debugging Techniques

### Print Debugging (Strategic Logging)
```python
# BAD: Random prints
print("here")
print("here2")
print(x)

# GOOD: Structured logging
logger.debug(f"Entering function with args: {args}")
logger.debug(f"Intermediate result: {result}")
logger.debug(f"Exiting function with return: {return_value}")
```

### Assertion Debugging
```python
def calculate_mass(components):
    assert isinstance(components, dict), "Components must be dict"
    assert all(q > 0 for q in components.values()), "Quantities must be positive"
    
    total = sum(get_component_mass(c) * q for c, q in components.items())
    
    assert total >= 0, f"Total mass cannot be negative: {total}"
    return total
```

### Binary Search Debugging
```python
# When bug is in large function, comment out half
def large_function():
    step1()
    step2()
    step3()
    # step4()  # Comment out second half
    # step5()
    # step6()
    
    # If bug still occurs, it's in first half
    # If bug disappears, it's in second half
    # Repeat until isolated
```

### Rubber Duck Debugging
1. Explain code line-by-line to rubber duck (or colleague)
2. Often reveals the issue during explanation
3. Forces you to question assumptions
4. Clarifies mental model

## Common Django Issues

### Database Query Issues
```python
# Issue: N+1 queries
# Debug: Use Django Debug Toolbar or log queries
from django.db import connection
from django.db import reset_queries

reset_queries()
# Your code here
print(f"Number of queries: {len(connection.queries)}")
for query in connection.queries:
    print(query['sql'])
```

### Migration Issues
```bash
# Check migration status
python manage.py showmigrations

# Check for conflicts
python manage.py makemigrations --check

# Fake migration if needed
python manage.py migrate --fake app_name migration_name

# Reset migrations (development only)
python manage.py migrate app_name zero
rm app_name/migrations/000*.py
python manage.py makemigrations
python manage.py migrate
```

### Template Issues
```python
# Debug template context
def my_view(request):
    context = {'blocks': Block.objects.all()}
    print(f"Template context: {context}")  # Debug
    return render(request, 'template.html', context)

# Debug template rendering
from django.template import Template, Context
template = Template("{{ blocks }}")
context = Context({'blocks': Block.objects.all()})
print(template.render(context))
```

### Form Validation Issues
```python
# Debug form errors
form = BlockForm(data=request.POST)
if not form.is_valid():
    print(f"Form errors: {form.errors}")
    print(f"Form data: {form.data}")
    print(f"Cleaned data: {form.cleaned_data}")
```

## Testing and Debugging

### Debugging Failing Tests
```bash
# Run specific test with verbose output
pytest path/to/test.py::test_function_name -vv

# Show print statements
pytest -s

# Drop into debugger on failure
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb

# Show local variables on failure
pytest -l
```

### Test Isolation Issues
```python
# Issue: Tests pass individually but fail together
# Cause: Shared state or database pollution

# Solution 1: Use pytest fixtures with proper scope
@pytest.fixture(scope="function")  # New instance per test
def sample_data():
    return create_test_data()

# Solution 2: Use Django TestCase (automatic rollback)
from django.test import TestCase

class MyTest(TestCase):
    def test_something(self):
        # Database changes rolled back after test
        pass

# Solution 3: Explicit cleanup
def test_something():
    # Test code
    pass
    # Cleanup
    Model.objects.all().delete()
```

## Performance Debugging

### Profiling Slow Code
```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Code to profile
    slow_function()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 slowest functions
```

### Memory Debugging
```python
import tracemalloc

# Start tracing
tracemalloc.start()

# Code to debug
large_operation()

# Get memory usage
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 10**6:.2f} MB")
print(f"Peak memory: {peak / 10**6:.2f} MB")

# Get top memory allocations
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)

tracemalloc.stop()
```

### Query Performance
```python
# Use Django's explain()
queryset = Block.objects.filter(mass__gt=100)
print(queryset.explain())

# Analyze with timing
import time
start = time.time()
result = list(queryset)
print(f"Query took: {time.time() - start:.2f}s")
```

## Git Bisect for Bug Hunting

```bash
# Find commit that introduced bug
git bisect start
git bisect bad  # Current commit is bad
git bisect good v0.6.0  # Known good commit

# Git will checkout middle commit
# Test if bug exists
python manage.py test

# Mark as good or bad
git bisect good  # or git bisect bad

# Repeat until bug commit found
# Reset when done
git bisect reset
```

## Debugging Checklist

### Initial Investigation
- [ ] Read error message completely
- [ ] Check stack trace
- [ ] Reproduce issue consistently
- [ ] Check recent changes (git log)
- [ ] Verify environment (dependencies, settings)

### Isolation
- [ ] Create minimal test case
- [ ] Remove unrelated code
- [ ] Test in clean environment
- [ ] Verify assumptions with assertions

### Root Cause Analysis
- [ ] Use debugger to step through code
- [ ] Log intermediate values
- [ ] Check database state
- [ ] Review related code
- [ ] Search for similar issues

### Fix and Verify
- [ ] Write test that reproduces bug
- [ ] Implement fix
- [ ] Verify test passes
- [ ] Run full test suite
- [ ] Check for regressions
- [ ] Document fix in commit message

## Common Debugging Mistakes

### Don't Make Random Changes
- Understand the problem first
- Make targeted changes
- Test each change

### Don't Skip Error Messages
- Read the full error message
- Check the stack trace
- Look for root cause, not symptoms

### Don't Debug in Production
- Reproduce in development
- Use logging, not print statements
- Never leave debug code in production

### Don't Assume
- Verify assumptions with tests
- Check actual values, not expected
- Question everything

## Debugging Resources

### Django Documentation
- Django Debug Toolbar docs
- Django logging documentation
- Database query optimization guide

### Python Documentation
- pdb documentation
- logging module documentation
- traceback module documentation

### Tools
- Django Debug Toolbar
- Sentry (error tracking)
- New Relic (APM)
- PyCharm debugger
- VS Code debugger
