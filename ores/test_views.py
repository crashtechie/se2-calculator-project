"""
Unit tests for Ores app views.
Tests CRUD operations, filtering, sorting, pagination, and form validation.
"""
from django.test import TestCase, Client
from django.urls import reverse
from ores.models import Ore
from ores.forms import OreForm


class OreViewsTestCase(TestCase):
    """Test case for Ore CRUD views."""
    
    fixtures = ['sample_ores.json']
    
    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.test_ore = Ore.objects.first()
    
    # ========== OreListView Tests ==========
    
    def test_ore_list_view_renders(self):
        """Test that ore list view renders successfully."""
        response = self.client.get(reverse('ores:ore_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ores/ore_list.html')
        self.assertIn('ore_list', response.context)
    
    def test_ore_list_view_displays_fixture_data(self):
        """Test that list view displays ores from fixtures."""
        response = self.client.get(reverse('ores:ore_list'))
        ore_count = Ore.objects.count()
        self.assertGreater(ore_count, 0)
        self.assertContains(response, self.test_ore.name)
    
    def test_ore_list_view_search_by_name(self):
        """Test filtering ores by name."""
        response = self.client.get(reverse('ores:ore_list'), {'search': 'Iron'})
        self.assertEqual(response.status_code, 200)
        # Verify search was applied
        self.assertEqual(response.context['search_query'], 'Iron')
    
    def test_ore_list_view_sort_by_mass_ascending(self):
        """Test sorting ores by mass (ascending)."""
        response = self.client.get(
            reverse('ores:ore_list'),
            {'sort_by': 'mass', 'order': 'asc'}
        )
        self.assertEqual(response.status_code, 200)
        ore_list = list(response.context['ore_list'])
        # Verify sorting
        if len(ore_list) > 1:
            self.assertLessEqual(ore_list[0].mass, ore_list[1].mass)
    
    def test_ore_list_view_sort_by_mass_descending(self):
        """Test sorting ores by mass (descending)."""
        response = self.client.get(
            reverse('ores:ore_list'),
            {'sort_by': 'mass', 'order': 'desc'}
        )
        self.assertEqual(response.status_code, 200)
        ore_list = list(response.context['ore_list'])
        # Verify sorting
        if len(ore_list) > 1:
            self.assertGreaterEqual(ore_list[0].mass, ore_list[1].mass)
    
    def test_ore_list_view_pagination(self):
        """Test pagination when more than 25 ores exist."""
        # Create additional ores if needed
        current_count = Ore.objects.count()
        if current_count < 30:
            for i in range(30 - current_count):
                Ore.objects.create(
                    name=f'Test Ore {i}',
                    mass=100.0 + i,
                    description=f'Test ore number {i}'
                )
        
        response = self.client.get(reverse('ores:ore_list'))
        self.assertEqual(response.status_code, 200)
        # Check if pagination exists
        if Ore.objects.count() > 25:
            self.assertTrue(response.context['is_paginated'])
    
    # ========== OreDetailView Tests ==========
    
    def test_ore_detail_view_renders(self):
        """Test that ore detail view renders successfully."""
        response = self.client.get(
            reverse('ores:ore_detail', kwargs={'pk': self.test_ore.ore_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ores/ore_detail.html')
        self.assertEqual(response.context['ore'], self.test_ore)
    
    def test_ore_detail_view_invalid_uuid(self):
        """Test that detail view returns 404 for invalid UUID."""
        invalid_uuid = '00000000-0000-0000-0000-000000000000'
        response = self.client.get(
            reverse('ores:ore_detail', kwargs={'pk': invalid_uuid})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_ore_detail_view_displays_all_fields(self):
        """Test that detail view displays all ore properties."""
        response = self.client.get(
            reverse('ores:ore_detail', kwargs={'pk': self.test_ore.ore_id})
        )
        self.assertContains(response, self.test_ore.name)
        self.assertContains(response, str(self.test_ore.ore_id))
        self.assertContains(response, f'{self.test_ore.mass:.2f}')
    
    # ========== OreCreateView Tests ==========
    
    def test_ore_create_view_get(self):
        """Test that create view GET request renders form."""
        response = self.client.get(reverse('ores:ore_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ores/ore_form.html')
        self.assertIsInstance(response.context['form'], OreForm)
        self.assertEqual(response.context['form_action'], 'Create')
    
    def test_ore_create_view_post_valid_data(self):
        """Test creating ore with valid data."""
        initial_count = Ore.objects.count()
        data = {
            'name': 'New Test Ore',
            'mass': 150.50,
            'description': 'This is a new test ore'
        }
        response = self.client.post(reverse('ores:ore_create'), data)
        
        # Should redirect to detail page
        self.assertEqual(response.status_code, 302)
        
        # Verify ore was created
        self.assertEqual(Ore.objects.count(), initial_count + 1)
        
        # Verify ore data
        new_ore = Ore.objects.get(name='New Test Ore')
        self.assertEqual(new_ore.mass, 150.50)
        self.assertEqual(new_ore.description, 'This is a new test ore')
    
    def test_ore_create_view_post_invalid_data(self):
        """Test creating ore with invalid data shows errors."""
        initial_count = Ore.objects.count()
        data = {
            'name': '',  # Invalid: empty name
            'mass': -10,  # Invalid: negative mass
        }
        response = self.client.post(reverse('ores:ore_create'), data)
        
        # Should not redirect (form has errors)
        self.assertEqual(response.status_code, 200)
        
        # Verify ore was NOT created
        self.assertEqual(Ore.objects.count(), initial_count)
        
        # Verify form has errors
        self.assertFormError(response.context['form'], 'name', 'This field is required.')
    
    def test_ore_create_view_duplicate_name(self):
        """Test that creating ore with duplicate name fails."""
        initial_count = Ore.objects.count()
        data = {
            'name': self.test_ore.name,  # Duplicate name
            'mass': 100.0,
        }
        response = self.client.post(reverse('ores:ore_create'), data)
        
        # Should not redirect (form has errors)
        self.assertEqual(response.status_code, 200)
        
        # Verify ore was NOT created
        self.assertEqual(Ore.objects.count(), initial_count)
    
    # ========== OreUpdateView Tests ==========
    
    def test_ore_update_view_get(self):
        """Test that update view GET request renders form with existing data."""
        response = self.client.get(
            reverse('ores:ore_update', kwargs={'pk': self.test_ore.ore_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ores/ore_form.html')
        self.assertIsInstance(response.context['form'], OreForm)
        self.assertEqual(response.context['form_action'], 'Update')
        
        # Verify form is pre-populated
        form = response.context['form']
        self.assertEqual(form.initial['name'], self.test_ore.name)
    
    def test_ore_update_view_post_valid_data(self):
        """Test updating ore with valid data."""
        data = {
            'name': 'Updated Ore Name',
            'mass': 200.00,
            'description': 'Updated description'
        }
        response = self.client.post(
            reverse('ores:ore_update', kwargs={'pk': self.test_ore.ore_id}),
            data
        )
        
        # Should redirect to detail page
        self.assertEqual(response.status_code, 302)
        
        # Verify ore was updated
        self.test_ore.refresh_from_db()
        self.assertEqual(self.test_ore.name, 'Updated Ore Name')
        self.assertEqual(self.test_ore.mass, 200.00)
    
    def test_ore_update_view_invalid_data(self):
        """Test updating ore with invalid data."""
        original_name = self.test_ore.name
        data = {
            'name': '',  # Invalid
            'mass': -50,  # Invalid
        }
        response = self.client.post(
            reverse('ores:ore_update', kwargs={'pk': self.test_ore.ore_id}),
            data
        )
        
        # Should not redirect
        self.assertEqual(response.status_code, 200)
        
        # Verify ore was NOT updated
        self.test_ore.refresh_from_db()
        self.assertEqual(self.test_ore.name, original_name)
    
    # ========== OreDeleteView Tests ==========
    
    def test_ore_delete_view_get(self):
        """Test that delete view GET request renders confirmation page."""
        response = self.client.get(
            reverse('ores:ore_delete', kwargs={'pk': self.test_ore.ore_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ores/ore_confirm_delete.html')
        self.assertEqual(response.context['ore'], self.test_ore)
    
    def test_ore_delete_view_post(self):
        """Test that DELETE request deletes ore."""
        initial_count = Ore.objects.count()
        ore_id = self.test_ore.ore_id
        
        response = self.client.post(
            reverse('ores:ore_delete', kwargs={'pk': ore_id})
        )
        
        # Should redirect to list page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('ores:ore_list'))
        
        # Verify ore was deleted
        self.assertEqual(Ore.objects.count(), initial_count - 1)
        self.assertFalse(Ore.objects.filter(ore_id=ore_id).exists())


class OreFormTestCase(TestCase):
    """Test case for OreForm validation."""
    
    def test_ore_form_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'name': 'Test Ore',
            'mass': 100.0,
            'description': 'Test description'
        }
        form = OreForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_ore_form_missing_name(self):
        """Test form with missing name."""
        form_data = {
            'mass': 100.0,
        }
        form = OreForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_ore_form_negative_mass(self):
        """Test form with negative mass."""
        form_data = {
            'name': 'Test Ore',
            'mass': -10.0,
        }
        form = OreForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mass', form.errors)
    
    def test_ore_form_zero_mass(self):
        """Test form with zero mass."""
        form_data = {
            'name': 'Test Ore',
            'mass': 0.0,
        }
        form = OreForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mass', form.errors)