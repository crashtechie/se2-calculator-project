# Automated Testing: Unit Tests

**Project:** SE2 Calculator Project  
**Document Type:** Quality Assurance - Unit Testing Guide  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document provides comprehensive guidance for writing, organizing, and maintaining unit tests in the SE2 Calculator Project. Unit tests verify that individual components function correctly in isolation.

---

## Unit Testing Fundamentals

### What is a Unit Test?

A unit test verifies a single "unit" of functionality:
- A model method
- A view function
- A form validation rule
- A utility function
- A template tag

### Characteristics of Good Unit Tests

✅ **Fast** - Executes in milliseconds  
✅ **Isolated** - Tests one thing at a time  
✅ **Repeatable** - Same result every time  
✅ **Self-validating** - Pass or fail, no manual checking  
✅ **Timely** - Written at or before implementation  

---

## Test Organization by App

### Ores App Unit Tests

**Location:** `app/ores/tests/`

**Files:**
```
ores/tests/
├── __init__.py
├── test_models.py          # 35+ model tests
├── test_views.py           # 25+ view tests
└── test_fixtures.py        # 10+ fixture tests
```

**Test Classes in test_models.py:**
```python
class OreModelCreationTests(TestCase)           # 4 tests
class OreFieldValidationTests(TestCase)         # 6 tests
class OreUUIDTests(TestCase)                    # 5 tests
class OreTimestampTests(TestCase)               # 5 tests
class OreQueryTests(TestCase)                   # 6 tests
class OreMetaConfigTests(TestCase)              # 4 tests
class OrePrimaryKeyTests(TestCase)              # 2 tests
class OreIntegrationTests(TestCase)             # 3 tests
```

**Running Ores Unit Tests:**
```bash
cd app

# All ores tests
uv run python manage.py test ores -v 2

# Model tests only
uv run python manage.py test ores.tests.test_models -v 2

# Specific test class
uv run python manage.py test ores.tests.test_models.OreFieldValidationTests -v 2

# Single test
uv run python manage.py test ores.tests.test_models.OreFieldValidationTests.test_name_max_length -v 2
```

---

### Components App Unit Tests

**Location:** `app/components/tests/`

**Files:**
```
components/tests/
├── __init__.py
├── test_models.py          # 44+ model tests
├── test_views.py           # 25+ view tests
└── test_fixtures.py        # 10+ fixture tests
```

**Test Classes in test_models.py:**
```python
class ComponentModelCreationTests(TestCase)         # 6 tests
class ComponentFieldValidationTests(TestCase)       # 8 tests
class ComponentMaterialsJSONTests(TestCase)         # 12 tests
class ComponentMaterialValidationTests(TestCase)    # 8 tests
class ComponentOreRelationshipTests(TestCase)       # 4 tests
class ComponentMetaTests(TestCase)                  # 4 tests
class ComponentIntegrationTests(TestCase)           # 5 tests
```

**Running Components Unit Tests:**
```bash
cd app

# All components tests
uv run python manage.py test components -v 2

# Model tests
uv run python manage.py test components.tests.test_models -v 2

# View tests
uv run python manage.py test components.tests.test_views -v 2
```

---

### Blocks App Unit Tests

**Location:** `app/blocks/tests/`

**Files:**
```
blocks/tests/
├── __init__.py
├── test_models.py          # 49+ model tests
├── test_views.py           # 25+ view tests
├── test_forms.py           # 10+ form tests
├── test_templatetags.py    # 5+ template tag tests
└── test_fixtures.py        # 10+ fixture tests
```

**Test Classes in test_models.py:**
```python
class BlockModelCreationTests(TestCase)             # 6 tests
class BlockFieldValidationTests(TestCase)           # 8 tests
class BlockComponentValidationTests(TestCase)       # 10 tests
class BlockConsumerProducerTests(TestCase)          # 8 tests
class BlockComponentRelationshipTests(TestCase)     # 6 tests
class BlockMetaConfigTests(TestCase)                # 4 tests
class BlockQueryTests(TestCase)                     # 4 tests
class BlockIntegrationTests(TestCase)               # 5 tests
```

**Running Blocks Unit Tests:**
```bash
cd app

# All blocks tests
uv run python manage.py test blocks -v 2

# Model tests
uv run python manage.py test blocks.tests.test_models -v 2

# Form tests
uv run python manage.py test blocks.tests.test_forms -v 2

# Template tag tests
uv run python manage.py test blocks.tests.test_templatetags -v 2
```

---

## Writing Unit Tests

### Basic Test Template

```python
"""
Unit tests for [Feature/Component].

Tests verify [what is being tested].
"""
from django.test import TestCase
from myapp.models import MyModel


class MyFeatureTests(TestCase):
    """Test suite for [specific feature]."""
    
    def setUp(self):
        """Set up test data for each test method.
        
        This runs before EACH test method.
        """
        # Create test objects
        self.test_obj = MyModel.objects.create(
            name="Test Object",
            value=100
        )
    
    def test_feature_with_valid_data(self):
        """Test [feature] works with valid data."""
        # Arrange - prepare test data
        expected = "expected_value"
        
        # Act - execute the functionality
        result = self.test_obj.some_method()
        
        # Assert - verify the result
        self.assertEqual(result, expected)
    
    def test_feature_with_invalid_data(self):
        """Test [feature] handles invalid data correctly."""
        # Test that appropriate exception is raised
        with self.assertRaises(ValueError):
            self.test_obj.invalid_operation()
```

---

## Model Testing

### Testing Model Creation

```python
from django.test import TestCase
from ores.models import Ore


class OreModelCreationTests(TestCase):
    """Test ore model creation."""
    
    def test_create_ore_with_all_fields(self):
        """Test creating an ore with all fields."""
        ore = Ore.objects.create(
            name="Iron Ore",
            mass=50.0,
            description="Basic iron ore"
        )
        
        self.assertEqual(ore.name, "Iron Ore")
        self.assertEqual(ore.mass, 50.0)
        self.assertEqual(ore.description, "Basic iron ore")
        self.assertIsNotNone(ore.ore_id)
        self.assertIsNotNone(ore.created_at)
        self.assertIsNotNone(ore.updated_at)
    
    def test_create_ore_minimal_fields(self):
        """Test creating ore with only required fields."""
        ore = Ore.objects.create(
            name="Minimal Ore",
            mass=10.0
        )
        
        self.assertEqual(ore.name, "Minimal Ore")
        self.assertEqual(ore.mass, 10.0)
        self.assertEqual(ore.description, "")  # Default value
```

### Testing Field Validation

```python
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class OreFieldValidationTests(TestCase):
    """Test ore field validation."""
    
    def test_name_is_required(self):
        """Test that name field is required."""
        with self.assertRaises(IntegrityError):
            Ore.objects.create(mass=50.0)  # Missing name
    
    def test_name_max_length(self):
        """Test that name respects max_length."""
        long_name = "A" * 101  # Assuming max_length=100
        ore = Ore(name=long_name, mass=50.0)
        
        with self.assertRaises(ValidationError):
            ore.full_clean()  # Triggers validation
    
    def test_name_must_be_unique(self):
        """Test that ore names must be unique."""
        Ore.objects.create(name="Duplicate", mass=50.0)
        
        with self.assertRaises(IntegrityError):
            Ore.objects.create(name="Duplicate", mass=60.0)
    
    def test_mass_must_be_positive(self):
        """Test that mass cannot be negative."""
        ore = Ore(name="Test", mass=-10.0)
        
        with self.assertRaises(ValidationError):
            ore.full_clean()
```

### Testing Model Methods

```python
class ComponentMethodTests(TestCase):
    """Test component model methods."""
    
    def setUp(self):
        """Create test component."""
        self.ore1 = Ore.objects.create(name="Iron", mass=50.0)
        self.ore2 = Ore.objects.create(name="Coal", mass=25.0)
        
        self.component = Component.objects.create(
            name="Steel",
            materials={
                str(self.ore1.ore_id): 10,
                str(self.ore2.ore_id): 5
            }
        )
    
    def test_get_material_list(self):
        """Test getting formatted material list."""
        materials = self.component.get_materials()
        
        self.assertEqual(len(materials), 2)
        self.assertIn(str(self.ore1.ore_id), materials)
        self.assertEqual(materials[str(self.ore1.ore_id)], 10)
    
    def test_total_mass_calculation(self):
        """Test total mass calculation from materials."""
        total = self.component.calculate_total_mass()
        
        expected = (50.0 * 10) + (25.0 * 5)  # 500 + 125 = 625
        self.assertEqual(total, expected)
```

### Testing Relationships

```python
class BlockRelationshipTests(TestCase):
    """Test block relationships with components."""
    
    def setUp(self):
        """Create test data."""
        self.comp1 = Component.objects.create(name="Comp1")
        self.comp2 = Component.objects.create(name="Comp2")
        self.comp3 = Component.objects.create(name="Comp3")
        
        self.block = Block.objects.create(name="Test Block")
        self.block.consumer_components.add(self.comp1, self.comp2)
        self.block.producer_components.add(self.comp3)
    
    def test_consumer_components_relationship(self):
        """Test consumer components are correctly linked."""
        consumers = self.block.consumer_components.all()
        
        self.assertEqual(consumers.count(), 2)
        self.assertIn(self.comp1, consumers)
        self.assertIn(self.comp2, consumers)
    
    def test_producer_components_relationship(self):
        """Test producer components are correctly linked."""
        producers = self.block.producer_components.all()
        
        self.assertEqual(producers.count(), 1)
        self.assertIn(self.comp3, producers)
    
    def test_deleting_component_affects_block(self):
        """Test cascade behavior when component is deleted."""
        self.comp1.delete()
        
        # Refresh block from database
        self.block.refresh_from_db()
        consumers = self.block.consumer_components.all()
        
        self.assertEqual(consumers.count(), 1)
        self.assertNotIn(self.comp1, consumers)
```

---

## View Testing

### Testing View Rendering

```python
from django.test import TestCase, Client
from django.urls import reverse


class OreListViewTests(TestCase):
    """Test ore list view."""
    
    fixtures = ['sample_ores.json']
    
    def setUp(self):
        """Set up test client."""
        self.client = Client()
    
    def test_ore_list_view_renders(self):
        """Test that ore list view renders successfully."""
        response = self.client.get(reverse('ores:ore_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ores/ore_list.html')
    
    def test_ore_list_contains_ores(self):
        """Test that ore list displays all ores."""
        response = self.client.get(reverse('ores:ore_list'))
        
        # Check that ores are in context
        self.assertIn('object_list', response.context)
        ores = response.context['object_list']
        self.assertGreater(len(ores), 0)
    
    def test_ore_list_pagination(self):
        """Test pagination works correctly."""
        # Create 30 ores (assuming 25 per page)
        for i in range(30):
            Ore.objects.create(name=f"Ore{i}", mass=float(i))
        
        response = self.client.get(reverse('ores:ore_list'))
        
        self.assertIn('is_paginated', response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['object_list']), 25)
```

### Testing CRUD Operations

```python
class OreCreateViewTests(TestCase):
    """Test ore create view."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Client()
        self.url = reverse('ores:ore_create')
    
    def test_create_view_renders_form(self):
        """Test that create view shows form."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ores/ore_form.html')
        self.assertIn('form', response.context)
    
    def test_create_ore_with_valid_data(self):
        """Test creating ore with valid POST data."""
        data = {
            'name': 'New Ore',
            'mass': 75.0,
            'description': 'Test ore'
        }
        
        response = self.client.post(self.url, data)
        
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        
        # Verify ore was created
        ore = Ore.objects.get(name='New Ore')
        self.assertEqual(ore.mass, 75.0)
        self.assertEqual(ore.description, 'Test ore')
    
    def test_create_ore_with_invalid_data(self):
        """Test that invalid data shows errors."""
        data = {
            'name': '',  # Empty name (required)
            'mass': -10.0  # Negative mass
        }
        
        response = self.client.post(self.url, data)
        
        # Should stay on form with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        
        # Verify no ore was created
        self.assertEqual(Ore.objects.filter(mass=-10.0).count(), 0)


class OreUpdateViewTests(TestCase):
    """Test ore update view."""
    
    def setUp(self):
        """Create test ore."""
        self.ore = Ore.objects.create(
            name="Original Name",
            mass=50.0
        )
        self.url = reverse('ores:ore_update', args=[self.ore.ore_id])
        self.client = Client()
    
    def test_update_view_shows_existing_data(self):
        """Test update form pre-populates with existing data."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.initial['name'], 'Original Name')
        self.assertEqual(form.initial['mass'], 50.0)
    
    def test_update_ore_with_valid_data(self):
        """Test updating ore with valid data."""
        data = {
            'name': 'Updated Name',
            'mass': 75.0,
            'description': 'Updated description'
        }
        
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 302)
        
        # Refresh ore from database
        self.ore.refresh_from_db()
        self.assertEqual(self.ore.name, 'Updated Name')
        self.assertEqual(self.ore.mass, 75.0)


class OreDeleteViewTests(TestCase):
    """Test ore delete view."""
    
    def setUp(self):
        """Create test ore."""
        self.ore = Ore.objects.create(name="To Delete", mass=50.0)
        self.url = reverse('ores:ore_delete', args=[self.ore.ore_id])
        self.client = Client()
    
    def test_delete_confirmation_page(self):
        """Test delete confirmation page displays."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ores/ore_confirm_delete.html')
        self.assertContains(response, 'To Delete')
    
    def test_delete_ore(self):
        """Test deleting ore via POST."""
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, 302)
        
        # Verify ore was deleted
        self.assertEqual(Ore.objects.filter(ore_id=self.ore.ore_id).count(), 0)
```

---

## Form Testing

### Testing Form Validation

```python
from django.test import TestCase
from blocks.forms import BlockForm


class BlockFormTests(TestCase):
    """Test block form validation."""
    
    def setUp(self):
        """Create test components."""
        self.comp1 = Component.objects.create(name="Comp1")
        self.comp2 = Component.objects.create(name="Comp2")
    
    def test_form_with_valid_data(self):
        """Test form validation with valid data."""
        data = {
            'name': 'Test Block',
            'description': 'Test description',
            'consumer_components': [self.comp1.component_id],
            'producer_components': [self.comp2.component_id]
        }
        
        form = BlockForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_requires_name(self):
        """Test that name is required."""
        data = {
            'description': 'Test'
        }
        
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_form_requires_consumer_components(self):
        """Test that at least one consumer is required."""
        data = {
            'name': 'Test Block',
            'producer_components': [self.comp2.component_id]
        }
        
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('consumer_components', form.errors)
```

---

## Assertion Reference

### Common Assertions

```python
# Equality
self.assertEqual(a, b)              # a == b
self.assertNotEqual(a, b)           # a != b

# Truth
self.assertTrue(x)                  # bool(x) is True
self.assertFalse(x)                 # bool(x) is False

# Identity
self.assertIs(a, b)                 # a is b
self.assertIsNot(a, b)              # a is not b

# Membership
self.assertIn(a, b)                 # a in b
self.assertNotIn(a, b)              # a not in b

# None checks
self.assertIsNone(x)                # x is None
self.assertIsNotNone(x)             # x is not None

# Type checks
self.assertIsInstance(a, b)         # isinstance(a, b)
self.assertNotIsInstance(a, b)      # not isinstance(a, b)

# Exceptions
self.assertRaises(exc, func, *args) # func(*args) raises exc
with self.assertRaises(exc):        # Context manager version
    func()

# Django-specific
self.assertTemplateUsed(response, template_name)
self.assertRedirects(response, expected_url)
self.assertContains(response, text)
self.assertNotContains(response, text)
self.assertFormError(response, form, field, errors)
self.assertQuerysetEqual(qs1, qs2)
```

---

## Best Practices Summary

### Test Structure

✅ One test class per feature or component  
✅ One test method per specific behavior  
✅ Use descriptive test and method names  
✅ Follow Arrange-Act-Assert pattern  
✅ Add docstrings to test methods  

### Test Data

✅ Use setUp() for common test data  
✅ Use fixtures for complex scenarios  
✅ Create minimal test data needed  
✅ Clean up in tearDown() if necessary  
✅ Don't share mutable state between tests  

### Test Coverage

✅ Test both success and failure cases  
✅ Test edge cases and boundaries  
✅ Test validation logic thoroughly  
✅ Test all public methods  
✅ Don't test framework code  

### Test Independence

✅ Tests should not depend on each other  
✅ Tests should pass in any order  
✅ Use transactions for database isolation  
✅ Mock external dependencies  
✅ Reset state between tests  

---

## Running and Debugging

### Running Specific Tests

```bash
# Run all tests
uv run python manage.py test

# Run specific app
uv run python manage.py test ores

# Run specific file
uv run python manage.py test ores.tests.test_models

# Run specific class
uv run python manage.py test ores.tests.test_models.OreFieldValidationTests

# Run specific test
uv run python manage.py test ores.tests.test_models.OreFieldValidationTests.test_name_is_required
```

### Debugging Tests

```bash
# Keep database for inspection
uv run python manage.py test --keepdb

# Stop on first failure
uv run python manage.py test --failfast

# Verbose output
uv run python manage.py test -v 2

# Very verbose (shows why tests are skipped)
uv run python manage.py test -v 3
```

### Using pdb for Debugging

```python
def test_complex_logic(self):
    """Test complex logic."""
    import pdb; pdb.set_trace()  # Debugger will stop here
    
    result = complex_function()
    self.assertEqual(result, expected)
```

---

## Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Test-Driven Development Guide](https://testdriven.io/)

---

**Document Owner:** Development & QA Team  
**Last Updated:** January 30, 2026  
**Next Review:** April 30, 2026
