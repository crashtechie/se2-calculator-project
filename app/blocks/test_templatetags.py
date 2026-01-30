"""
Tests for Block template tags.

Tests custom template filters for block rendering.
"""
from django.test import TestCase
from blocks.models import Block
from blocks.templatetags.block_filters import get_component_name, get_component_mass, multiply
from components.models import Component
from ores.models import Ore


class BlockTemplateTagsTest(TestCase):
    """Test block_filters template tags."""
    
    fixtures = ['sample_ores.json', 'sample_components.json', 'sample_blocks.json']
    
    def test_get_component_name_with_valid_id(self):
        """Test get_component_name returns component name."""
        component = Component.objects.first()
        result = get_component_name(str(component.component_id))
        self.assertEqual(result, component.name)
    
    def test_get_component_name_with_invalid_id(self):
        """Test get_component_name with invalid ID returns 'Unknown'."""
        result = get_component_name('invalid-id')
        self.assertIn('Unknown Component', result)
    
    def test_get_component_name_with_nonexistent_id(self):
        """Test get_component_name with nonexistent ID returns 'Unknown'."""
        result = get_component_name('00000000-0000-0000-0000-000000000000')
        self.assertIn('Unknown Component', result)
    
    def test_get_component_name_with_none(self):
        """Test get_component_name with None returns 'Unknown'."""
        result = get_component_name(None)
        self.assertEqual(result, 'Unknown Component')
    
    def test_get_component_name_with_empty_string(self):
        """Test get_component_name with empty string."""
        result = get_component_name('')
        self.assertEqual(result, 'Unknown Component')
    
    def test_get_component_mass_with_valid_id(self):
        """Test get_component_mass returns component mass."""
        component = Component.objects.first()
        result = get_component_mass(str(component.component_id))
        self.assertEqual(result, component.mass)
    
    def test_get_component_mass_with_invalid_id(self):
        """Test get_component_mass with invalid ID returns 0."""
        result = get_component_mass('invalid-id')
        self.assertEqual(result, 0.0)
    
    def test_get_component_mass_with_nonexistent_id(self):
        """Test get_component_mass with nonexistent ID returns 0."""
        result = get_component_mass('00000000-0000-0000-0000-000000000000')
        self.assertEqual(result, 0.0)
    
    def test_get_component_mass_with_none(self):
        """Test get_component_mass with None returns 0."""
        result = get_component_mass(None)
        self.assertEqual(result, 0.0)
    
    def test_get_component_mass_with_empty_string(self):
        """Test get_component_mass with empty string."""
        result = get_component_mass('')
        self.assertEqual(result, 0.0)
    
    def test_multiply_filter_with_integers(self):
        """Test multiply filter with integers."""
        result = multiply(5, 3)
        self.assertEqual(result, 15)
    
    def test_multiply_filter_with_floats(self):
        """Test multiply filter with floats."""
        result = multiply(5.5, 2.0)
        self.assertEqual(result, 11.0)
    
    def test_multiply_filter_with_zero(self):
        """Test multiply filter with zero."""
        result = multiply(5, 0)
        self.assertEqual(result, 0)
    
    def test_multiply_filter_with_negative(self):
        """Test multiply filter with negative numbers."""
        result = multiply(-5, 3)
        self.assertEqual(result, -15)
    
    def test_multiply_filter_with_invalid_value(self):
        """Test multiply filter with invalid value."""
        result = multiply('not-a-number', 3)
        self.assertEqual(result, 0)
    
    def test_multiply_filter_with_invalid_arg(self):
        """Test multiply filter with invalid arg."""
        result = multiply(5, 'not-a-number')
        self.assertEqual(result, 0)
