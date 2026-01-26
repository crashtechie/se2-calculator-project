"""
Tests for Block forms.

Tests JSONField component handling and validation.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from blocks.forms import BlockForm
from blocks.models import Block
from components.models import Component
from ores.models import Ore
import json


class BlockFormTest(TestCase):
    """Test BlockForm with comprehensive coverage."""
    
    fixtures = ['sample_ores.json', 'sample_components.json']
    
    def setUp(self):
        """Set up test data."""
        self.component = Component.objects.first()
        self.valid_data = {
            'name': 'Test Block',
            'description': 'Test description',
            'mass': 100.0,
            'health': 100.0,
            'pcu': 10,
            'snap_size': 0.5,
            'input_mass': None,
            'output_mass': None,
            'consumer_type': '',
            'consumer_rate': 0,
            'producer_type': '',
            'producer_rate': 0,
            'storage_capacity': 0,
            'components_json': json.dumps({str(self.component.component_id): 1})
        }
    
    def test_form_processes_components_json(self):
        """Test form processes components JSON correctly."""
        form = BlockForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)
        block = form.save()
        self.assertEqual(block.components, {str(self.component.component_id): 1})
    
    def test_form_with_existing_instance_populates_components_json(self):
        """Test form populates components_json for existing block."""
        block = Block.objects.create(
            name='Existing Block',
            description='Test',
            mass=10,
            health=10,
            pcu=1,
            snap_size=0.5,
            components={str(self.component.component_id): 5}
        )
        form = BlockForm(instance=block)
        self.assertEqual(
            form.initial['components_json'],
            json.dumps({str(self.component.component_id): 5})
        )
    
    def test_form_validates_unique_name(self):
        """Test form validates unique block name."""
        Block.objects.create(
            name='Duplicate Name',
            description='Test',
            mass=10,
            health=10,
            pcu=1,
            snap_size=0.5,
            components={}
        )
        data = self.valid_data.copy()
        data['name'] = 'Duplicate Name'
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_form_allows_same_name_for_same_instance(self):
        """Test form allows same name when updating existing block."""
        block = Block.objects.create(
            name='Update Test',
            description='Test',
            mass=10,
            health=10,
            pcu=1,
            snap_size=0.5,
            components={}
        )
        data = self.valid_data.copy()
        data['name'] = 'Update Test'
        form = BlockForm(data=data, instance=block)
        self.assertTrue(form.is_valid())
    
    def test_form_validates_empty_name(self):
        """Test form rejects empty name."""
        data = self.valid_data.copy()
        data['name'] = ''
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_form_validates_positive_mass(self):
        """Test form validates mass is positive."""
        data = self.valid_data.copy()
        data['mass'] = -1
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('mass', form.errors)
    
    def test_form_validates_non_negative_pcu_cost(self):
        """Test form validates PCU cost is not negative."""
        data = self.valid_data.copy()
        data['pcu'] = -5
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('pcu', form.errors)
    
    def test_form_requires_at_least_one_component(self):
        """Test form requires at least one component."""
        data = self.valid_data.copy()
        data['components_json'] = '{}'
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('components_json', form.errors)
    
    def test_form_rejects_invalid_json(self):
        """Test form rejects invalid JSON in components_json."""
        data = self.valid_data.copy()
        data['components_json'] = 'not valid json'
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('components_json', form.errors)
    
    def test_form_rejects_non_dict_components(self):
        """Test form rejects non-dict components."""
        data = self.valid_data.copy()
        data['components_json'] = '["not", "a", "dict"]'
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('components_json', form.errors)
    
    def test_form_validates_component_uuid_format(self):
        """Test form validates UUID format for component IDs."""
        data = self.valid_data.copy()
        data['components_json'] = json.dumps({'not-a-uuid': 1})
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('components_json', form.errors)
    
    def test_form_validates_positive_component_quantity(self):
        """Test form validates component quantities are positive."""
        data = self.valid_data.copy()
        data['components_json'] = json.dumps({str(self.component.component_id): 0})
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('components_json', form.errors)
    
    def test_form_validates_integer_component_quantity(self):
        """Test form validates component quantities are integers."""
        data = self.valid_data.copy()
        data['components_json'] = json.dumps({str(self.component.component_id): 'not-a-number'})
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('components_json', form.errors)
    
    def test_form_validates_component_exists(self):
        """Test form validates component IDs exist in database."""
        data = self.valid_data.copy()
        data['components_json'] = json.dumps({'00000000-0000-0000-0000-000000000000': 1})
        form = BlockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('components_json', form.errors)
    
    def test_form_accepts_multiple_components(self):
        """Test form accepts multiple components."""
        comp2 = Component.objects.last()
        data = self.valid_data.copy()
        data['components_json'] = json.dumps({
            str(self.component.component_id): 2,
            str(comp2.component_id): 3
        })
        form = BlockForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
    
    def test_form_with_optional_fields_empty(self):
        """Test form accepts empty optional fields."""
        data = self.valid_data.copy()
        data['input_mass'] = ''
        data['output_mass'] = ''
        data['consumer_type'] = ''
        data['producer_type'] = ''
        form = BlockForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
