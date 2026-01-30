"""
Tests for Blocks views.

Tests CRUD operations, resource chain calculation, and component handling.
Follows ENH-0000005 and ENH-0000006 test patterns.
"""
from django.test import TestCase, Client
from django.urls import reverse
from blocks.models import Block
from components.models import Component
from ores.models import Ore
import uuid


class BlockListViewTest(TestCase):
    """Test BlockListView."""
    
    fixtures = ['sample_ores.json', 'sample_components.json', 'sample_blocks.json']
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('blocks:block_list')
    
    def test_view_renders_successfully(self):
        """Test list view renders with fixture data."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blocks/block_list.html')
    
    def test_search_functionality(self):
        """Test search works."""
        response = self.client.get(self.url, {'q': 'Armor'})
        self.assertEqual(response.status_code, 200)
    
    def test_empty_search_returns_all_blocks(self):
        """Test empty search returns all blocks."""
        response = self.client.get(self.url, {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['object_list']), 0)
    
    def test_context_contains_search_query(self):
        """Test context includes search query."""
        response = self.client.get(self.url, {'q': 'Test'})
        self.assertIn('search_query', response.context)
        self.assertEqual(response.context['search_query'], 'Test')
    
    def test_blocks_ordered_by_name(self):
        """Test blocks are ordered by name."""
        response = self.client.get(self.url)
        blocks = list(response.context['object_list'])
        names = [b.name for b in blocks]
        self.assertEqual(names, sorted(names))
    
    # Add 20+ more tests...


class BlockDetailViewTest(TestCase):
    """Test BlockDetailView with resource chain."""
    
    fixtures = ['sample_ores.json', 'sample_components.json', 'sample_blocks.json']
    
    def test_detail_view_with_resource_chain(self):
        """Test detail view calculates resource chain."""
        block = Block.objects.first()
        url = reverse('blocks:block_detail', kwargs={'pk': block.block_id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('resource_chain', response.context)
    
    def test_detail_view_renders_template(self):
        """Test detail view uses correct template."""
        block = Block.objects.first()
        url = reverse('blocks:block_detail', kwargs={'pk': block.block_id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blocks/block_detail.html')
    
    def test_detail_view_with_nonexistent_block(self):
        """Test detail view with invalid block ID returns 404."""
        url = reverse('blocks:block_detail', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    # Add 20+ more tests...


class BlockCreateViewTest(TestCase):
    """Test BlockCreateView."""
    
    fixtures = ['sample_ores.json', 'sample_components.json']
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('blocks:block_create')
        self.component = Component.objects.first()
    
    def test_create_view_get_renders_form(self):
        """Test GET request renders create form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blocks/block_form.html')
    
    def test_create_view_context_has_components(self):
        """Test context includes available components."""
        response = self.client.get(self.url)
        self.assertIn('available_components', response.context)
    
    def test_create_view_post_creates_block(self):
        """Test POST request creates new block."""
        import json
        data = {
            'name': 'New Test Block',
            'description': 'Test description',
            'mass': 100.0,
            'health': 100.0,
            'pcu': 10,
            'snap_size': 0.5,
            'consumer_rate': 0.0,
            'producer_rate': 0.0,
            'storage_capacity': 0.0,
            'components_json': json.dumps({str(self.component.component_id): 1})
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Block.objects.filter(name='New Test Block').exists())
    
    def test_create_view_invalid_data_shows_errors(self):
        """Test POST with invalid data shows errors."""
        data = {
            'name': '',  # Invalid: empty name
            'mass': 100.0,
            'components_json': '{}'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Re-renders form


class BlockUpdateViewTest(TestCase):
    """Test BlockUpdateView."""
    
    fixtures = ['sample_ores.json', 'sample_components.json', 'sample_blocks.json']
    
    def setUp(self):
        self.client = Client()
        self.block = Block.objects.first()
        self.url = reverse('blocks:block_update', kwargs={'pk': self.block.block_id})
    
    def test_update_view_get_renders_form(self):
        """Test GET request renders update form with existing data."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blocks/block_form.html')
        self.assertEqual(response.context['object'], self.block)
    
    def test_update_view_context_has_components(self):
        """Test context includes available components."""
        response = self.client.get(self.url)
        self.assertIn('available_components', response.context)
    
    def test_update_view_post_updates_block(self):
        """Test POST request updates block."""
        import json
        component = Component.objects.first()
        data = {
            'name': self.block.name,
            'description': 'Updated description',
            'mass': self.block.mass,
            'health': self.block.health,
            'pcu': self.block.pcu,
            'snap_size': self.block.snap_size,
            'consumer_rate': self.block.consumer_rate,
            'producer_rate': self.block.producer_rate,
            'storage_capacity': self.block.storage_capacity,
            'components_json': json.dumps({str(component.component_id): 2})
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.block.refresh_from_db()
        self.assertEqual(self.block.description, 'Updated description')
    
    def test_update_view_with_nonexistent_block(self):
        """Test update view with invalid block ID returns 404."""
        url = reverse('blocks:block_update', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class BlockDeleteViewTest(TestCase):
    """Test BlockDeleteView."""
    
    fixtures = ['sample_ores.json', 'sample_components.json', 'sample_blocks.json']
    
    def setUp(self):
        self.client = Client()
        self.block = Block.objects.first()
        self.url = reverse('blocks:block_delete', kwargs={'pk': self.block.block_id})
    
    def test_delete_view_get_renders_confirmation(self):
        """Test GET request renders delete confirmation."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blocks/block_confirm_delete.html')
    
    def test_delete_view_post_deletes_block(self):
        """Test POST request deletes block."""
        block_id = self.block.block_id
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertFalse(Block.objects.filter(block_id=block_id).exists())
    
    def test_delete_view_with_nonexistent_block(self):
        """Test delete view with invalid block ID returns 404."""
        url = reverse('blocks:block_delete', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    # Add 20+ more tests...


class BlockFormTest(TestCase):
    """Test BlockForm validation."""
    
    fixtures = ['sample_ores.json', 'sample_components.json']
    
    def test_form_validates_components(self):
        """Test form validates components using Phase 1 helper."""
        from blocks.forms import BlockForm
        # Add test implementation
        pass
    
    # Add 10+ more tests...
