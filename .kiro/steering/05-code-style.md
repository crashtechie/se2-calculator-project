# Code Style & Formatting

## Python Style

### PEP 8 Compliance
- Follow PEP 8 guidelines for Python code
- Line length: 88 characters (Black default)
- Use 4 spaces for indentation
- Two blank lines between top-level definitions
- One blank line between method definitions

### Naming Conventions
- **Classes**: PascalCase (e.g., `BuildOrder`, `OreModel`)
- **Functions/Methods**: snake_case (e.g., `calculate_total_ores`, `get_context_data`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `CACHE_TTL`, `MAX_ITEMS_PER_PAGE`)
- **Private methods**: Prefix with underscore (e.g., `_calculate_internal`)

### Import Organization
```python
# Standard library imports
import json
from datetime import datetime

# Third-party imports
from django.db import models
from django.urls import reverse

# Local application imports
from ores.models import Ore
from .utils import calculate_resources
```

## Django-Specific Conventions

### Model Field Order
1. Database fields
2. Custom manager attributes
3. Meta class
4. `__str__()` method
5. `save()` method
6. `get_absolute_url()` method
7. Custom methods

### View Method Order
1. Class attributes
2. `dispatch()` method
3. `get_queryset()` method
4. `get_context_data()` method
5. `form_valid()` method
6. `get_success_url()` method
7. Custom methods

## Template Conventions

### Indentation
- Use 2 spaces for template indentation
- Indent template tags and HTML consistently

### Template Tag Spacing
```django
{# Good #}
{% if condition %}
  <div>Content</div>
{% endif %}

{# Bad #}
{%if condition%}
<div>Content</div>
{%endif%}
```

### Variable Naming
- Use descriptive names: `{{ block_list }}` not `{{ bl }}`
- Follow Python naming conventions in context variables

## Comments & Documentation

### Docstrings
```python
def calculate_total_ores(blocks):
    """
    Calculate total ore requirements for a list of blocks.
    
    Args:
        blocks (list): List of Block instances with quantities
        
    Returns:
        dict: Mapping of ore IDs to required quantities
        
    Raises:
        ValueError: If blocks list is empty or invalid
    """
    pass
```

### Inline Comments
- Use sparingly for complex logic
- Explain "why" not "what"
- Keep comments up-to-date with code changes

### TODO Comments
```python
# TODO(username): Brief description of what needs to be done
# FIXME(username): Description of bug that needs fixing
# NOTE: Important information about this code
```

## File Organization

### App Structure
```
app_name/
├── __init__.py
├── admin.py           # Admin configuration
├── apps.py            # App configuration
├── models.py          # Database models
├── views.py           # View classes/functions
├── urls.py            # URL patterns
├── forms.py           # Form classes (if needed)
├── utils.py           # Helper functions
├── fixtures/          # Sample data
├── templates/         # App templates
│   └── app_name/
├── static/            # App static files
│   └── app_name/
└── tests/             # Test files
    ├── __init__.py
    ├── test_models.py
    ├── test_views.py
    └── test_utils.py
```

## Git Commit Messages

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples
```
feat(buildorder): Add multi-block resource calculation

Implement recursive calculation method that aggregates
component and ore requirements across multiple blocks.

Closes ENH-0000009
```

```
fix(blocks): Correct component quantity validation

Component quantities must be positive integers.
Added validation in clean() method.

Fixes #42
```

## Code Review Checklist

- [ ] Follows PEP 8 and project style guidelines
- [ ] Includes appropriate docstrings and comments
- [ ] Has corresponding tests with >80% coverage
- [ ] Updates relevant documentation
- [ ] No hardcoded secrets or credentials
- [ ] Proper error handling and validation
- [ ] Efficient database queries (no N+1 problems)
- [ ] Security best practices followed
