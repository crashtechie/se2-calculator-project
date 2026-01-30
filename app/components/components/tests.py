from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from components.models import Component
from ores.models import Ore
from datetime import timedelta
import time


class ComponentModelCreationTests(TestCase):
    """Test basic component creation with various field configurations."""
    
    def setUp(self):
        """Create test ores for use in components."""
        self.iron = Ore.objects.create(
            name="Test Iron Ore",
            mass=1.0
        )
        self.copper = Ore.objects.create(
            name="Test Copper Ore",
            mass=0.8
        )
    
    def test_create_component_with_all_fields(self):
        """Test creating a component with all fields populated."""
        component = Component.objects.create(
            name="Steel Plate",
            description="Basic building material",
            materials={str(self.iron.ore_id): 7},
            fabricator_type="Refinery",
            crafting_time=1.5,
            mass=7.0
        )
        
        self.assertEqual(component.name, "Steel Plate")
        self.assertEqual(component.description, "Basic building material")
        self.assertEqual(component.fabricator_type, "Refinery")
        self.assertEqual(component.crafting_time, 1.5)
        self.assertEqual(component.mass, 7.0)
        self.assertIsNotNone(component.component_id)
        self.assertIsNotNone(component.created_at)
        self.assertIsNotNone(component.updated_at)
    
    def test_create_component_minimal_fields(self):
        """Test creating a component with only required fields."""
        component = Component.objects.create(
            name="Minimal Component"
        )
        
        self.assertEqual(component.name, "Minimal Component")
        self.assertEqual(component.description, "")
        self.assertEqual(component.materials, {})
        self.assertEqual(component.fabricator_type, "")
        self.assertEqual(component.crafting_time, 0.0)
        self.assertEqual(component.mass, 0.0)
    
    def test_component_str_method(self):
        """Test the __str__ method returns the component name."""
        component = Component.objects.create(name="Motor")
        self.assertEqual(str(component), "Motor")
    
    def test_component_uuid_generation(self):
        """Test that UUIDv7 is automatically generated."""
        component = Component.objects.create(name="UUID Test")
        
        self.assertIsNotNone(component.component_id)
        # UUID should be a string representation
        uuid_str = str(component.component_id)
        self.assertEqual(len(uuid_str), 36)
        self.assertEqual(uuid_str.count('-'), 4)
    
    def test_component_uuid_uniqueness(self):
        """Test that each component gets a unique UUID."""
        comp1 = Component.objects.create(name="Component 1")
        comp2 = Component.objects.create(name="Component 2")
        
        self.assertNotEqual(comp1.component_id, comp2.component_id)
    
    def test_component_uuid_time_ordered(self):
        """Test that UUIDv7 generates time-ordered IDs."""
        components = []
        for i in range(5):
            comp = Component.objects.create(name=f"Ordered Component {i}")
            components.append(comp)
        
        uuids = [str(comp.component_id) for comp in components]
        self.assertEqual(uuids, sorted(uuids))


class ComponentFieldValidationTests(TestCase):
    """Test field validation and constraints."""
    
    def test_name_is_required(self):
        """Test that component name is required and cannot be blank."""
        component = Component(name="")
        with self.assertRaises(ValidationError):
            component.full_clean()
    
    def test_unique_name_constraint(self):
        """Test that duplicate component names are not allowed."""
        Component.objects.create(name="Unique Component")
        
        with self.assertRaises(IntegrityError):
            Component.objects.create(name="Unique Component")
    
    def test_name_max_length(self):
        """Test component name respects max_length constraint."""
        long_name = "A" * 100  # Exactly 100 characters
        component = Component.objects.create(name=long_name)
        self.assertEqual(len(component.name), 100)
    
    def test_description_can_be_blank(self):
        """Test that description field can be empty."""
        component = Component.objects.create(
            name="No Description",
            description=""
        )
        self.assertEqual(component.description, "")
    
    def test_fabricator_type_can_be_blank(self):
        """Test that fabricator_type field can be empty."""
        component = Component.objects.create(
            name="No Fabricator",
            fabricator_type=""
        )
        self.assertEqual(component.fabricator_type, "")
    
    def test_crafting_time_numeric_values(self):
        """Test crafting_time accepts various numeric values."""
        test_values = [0.0, 1.5, 10.0, 100.5]
        
        for i, value in enumerate(test_values):
            component = Component.objects.create(
                name=f"Time Test {i}",
                crafting_time=value
            )
            self.assertEqual(component.crafting_time, value)
    
    def test_mass_numeric_values(self):
        """Test mass accepts various numeric values."""
        test_values = [0.0, 0.5, 1.0, 10.5, 100.0]
        
        for i, value in enumerate(test_values):
            component = Component.objects.create(
                name=f"Mass Test {i}",
                mass=value
            )
            self.assertEqual(component.mass, value)


class ComponentTimestampTests(TestCase):
    """Test automatic timestamp management."""
    
    def test_created_at_auto_populated(self):
        """Test that created_at is automatically set on creation."""
        component = Component.objects.create(name="Timestamp Test")
        self.assertIsNotNone(component.created_at)
    
    def test_updated_at_auto_populated(self):
        """Test that updated_at is automatically set on creation."""
        component = Component.objects.create(name="Timestamp Test")
        self.assertIsNotNone(component.updated_at)
    
    def test_created_and_updated_match_on_creation(self):
        """Test that created_at and updated_at are the same on creation."""
        component = Component.objects.create(name="Timestamp Test")
        self.assertAlmostEqual(
            component.created_at,
            component.updated_at,
            delta=timedelta(milliseconds=1)
        )
    
    def test_updated_at_changes_on_save(self):
        """Test that updated_at is updated when the component is saved."""
        component = Component.objects.create(name="Update Test")
        original_updated = component.updated_at
        
        time.sleep(0.01)  # Ensure time difference
        component.mass = 5.0
        component.save()
        
        component.refresh_from_db()
        self.assertGreater(component.updated_at, original_updated)
    
    def test_created_at_immutable(self):
        """Test that created_at doesn't change on subsequent saves."""
        component = Component.objects.create(name="Immutable Test")
        original_created = component.created_at
        
        time.sleep(0.01)
        component.mass = 5.0
        component.save()
        
        component.refresh_from_db()
        self.assertEqual(component.created_at, original_created)


class ComponentMaterialsJSONFieldTests(TestCase):
    """Test JSONField functionality for materials."""
    
    def setUp(self):
        """Create test ores."""
        self.iron = Ore.objects.create(name="JSON Iron", mass=1.0)
        self.copper = Ore.objects.create(name="JSON Copper", mass=0.8)
    
    def test_materials_default_empty_dict(self):
        """Test that materials defaults to empty dict."""
        component = Component.objects.create(name="Empty Materials")
        self.assertEqual(component.materials, {})
    
    def test_materials_stores_single_ore(self):
        """Test storing a single ore in materials."""
        component = Component.objects.create(
            name="Single Material",
            materials={str(self.iron.ore_id): 10}
        )
        self.assertEqual(len(component.materials), 1)
        self.assertEqual(component.materials[str(self.iron.ore_id)], 10)
    
    def test_materials_stores_multiple_ores(self):
        """Test storing multiple ores in materials."""
        component = Component.objects.create(
            name="Multiple Materials",
            materials={
                str(self.iron.ore_id): 7,
                str(self.copper.ore_id): 3
            }
        )
        self.assertEqual(len(component.materials), 2)
        self.assertEqual(component.materials[str(self.iron.ore_id)], 7)
        self.assertEqual(component.materials[str(self.copper.ore_id)], 3)
    
    def test_materials_persist_after_save(self):
        """Test that materials JSON persists correctly to database."""
        component = Component.objects.create(
            name="Persist Test",
            materials={str(self.iron.ore_id): 5}
        )
        
        component.refresh_from_db()
        self.assertEqual(component.materials[str(self.iron.ore_id)], 5)
    
    def test_materials_can_be_updated(self):
        """Test that materials can be updated."""
        component = Component.objects.create(
            name="Update Materials",
            materials={str(self.iron.ore_id): 5}
        )
        
        component.materials[str(self.copper.ore_id)] = 3
        component.save()
        
        component.refresh_from_db()
        self.assertEqual(len(component.materials), 2)


class ComponentMaterialValidationTests(TestCase):
    """Test material validation helper methods."""
    
    def setUp(self):
        """Create test ores."""
        self.iron = Ore.objects.create(name="Valid Iron", mass=1.0)
        self.copper = Ore.objects.create(name="Valid Copper", mass=0.8)
    
    def test_validate_materials_with_valid_ores(self):
        """Test validation passes with valid ore references."""
        component = Component.objects.create(
            name="Valid Component",
            materials={str(self.iron.ore_id): 10}
        )
        
        is_valid, errors = component.validate_materials()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])
    
    def test_validate_materials_with_invalid_ore_id(self):
        """Test validation fails with non-existent ore ID."""
        component = Component(
            name="Invalid Ore",
            materials={"00000000-0000-0000-0000-000000000000": 10}
        )
        
        is_valid, errors = component.validate_materials()
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("does not exist", errors[0])
    
    def test_validate_materials_with_negative_quantity(self):
        """Test validation fails with negative quantity."""
        component = Component(
            name="Negative Quantity",
            materials={str(self.iron.ore_id): -5}
        )
        
        is_valid, errors = component.validate_materials()
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("positive number", errors[0])
    
    def test_validate_materials_with_zero_quantity(self):
        """Test validation fails with zero quantity."""
        component = Component(
            name="Zero Quantity",
            materials={str(self.iron.ore_id): 0}
        )
        
        is_valid, errors = component.validate_materials()
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_validate_materials_empty_materials(self):
        """Test validation passes with empty materials."""
        component = Component.objects.create(
            name="Empty Materials",
            materials={}
        )
        
        is_valid, errors = component.validate_materials()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])
    
    def test_validate_materials_multiple_invalid_ores(self):
        """Test validation reports multiple errors."""
        component = Component(
            name="Multiple Errors",
            materials={
                "00000000-0000-0000-0000-000000000000": 10,
                "11111111-1111-1111-1111-111111111111": -5
            }
        )
        
        is_valid, errors = component.validate_materials()
        self.assertFalse(is_valid)
        self.assertGreaterEqual(len(errors), 2)
    
    def test_clean_raises_validation_error(self):
        """Test that clean() raises ValidationError for invalid materials."""
        component = Component(
            name="Clean Test",
            materials={"00000000-0000-0000-0000-000000000000": 10}
        )
        
        with self.assertRaises(ValidationError):
            component.clean()
    
    def test_save_validates_materials(self):
        """Test that save() calls validation."""
        component = Component(
            name="Save Validation",
            materials={"00000000-0000-0000-0000-000000000000": 10}
        )
        
        with self.assertRaises(ValidationError):
            component.save()


class ComponentMaterialOresRelationshipTests(TestCase):
    """Test get_material_ores() helper method."""
    
    def setUp(self):
        """Create test ores."""
        self.iron = Ore.objects.create(name="Rel Iron", mass=1.0)
        self.copper = Ore.objects.create(name="Rel Copper", mass=0.8)
        self.nickel = Ore.objects.create(name="Rel Nickel", mass=0.9)
    
    def test_get_material_ores_single_ore(self):
        """Test getting a single ore from materials."""
        component = Component.objects.create(
            name="Single Ore",
            materials={str(self.iron.ore_id): 10}
        )
        
        ores = component.get_material_ores()
        self.assertEqual(ores.count(), 1)
        ore_ids = {str(ore.ore_id) for ore in ores}
        self.assertIn(str(self.iron.ore_id), ore_ids)
    
    def test_get_material_ores_multiple_ores(self):
        """Test getting multiple ores from materials."""
        component = Component.objects.create(
            name="Multiple Ores",
            materials={
                str(self.iron.ore_id): 7,
                str(self.copper.ore_id): 3
            }
        )
        
        ores = component.get_material_ores()
        self.assertEqual(ores.count(), 2)
        ore_ids = {str(ore.ore_id) for ore in ores}
        self.assertIn(str(self.iron.ore_id), ore_ids)
        self.assertIn(str(self.copper.ore_id), ore_ids)
    
    def test_get_material_ores_empty_materials(self):
        """Test getting ores with empty materials returns empty queryset."""
        component = Component.objects.create(
            name="No Materials",
            materials={}
        )
        
        ores = component.get_material_ores()
        self.assertEqual(ores.count(), 0)
    
    def test_get_material_ores_preserves_quantities(self):
        """Test that material quantities are accessible after getting ores."""
        component = Component.objects.create(
            name="Quantity Test",
            materials={
                str(self.iron.ore_id): 7,
                str(self.copper.ore_id): 3
            }
        )
        
        ores = component.get_material_ores()
        for ore in ores:
            quantity = component.materials[str(ore.ore_id)]
            self.assertGreater(quantity, 0)


class ComponentMetaTests(TestCase):
    """Test model Meta configuration."""
    
    def test_components_ordered_by_name(self):
        """Test that components are ordered by name."""
        Component.objects.create(name="Zebra Component")
        Component.objects.create(name="Alpha Component")
        Component.objects.create(name="Bravo Component")
        
        components = list(Component.objects.all())
        names = [c.name for c in components]
        
        self.assertEqual(names, sorted(names))
    
    def test_verbose_name_singular(self):
        """Test verbose name is set correctly."""
        self.assertEqual(Component._meta.verbose_name, 'Component')
    
    def test_verbose_name_plural(self):
        """Test verbose name plural is set correctly."""
        self.assertEqual(Component._meta.verbose_name_plural, 'Components')
    
    def test_db_table_name(self):
        """Test custom database table name is set."""
        self.assertEqual(Component._meta.db_table, 'components_component')


class ComponentIntegrationTests(TestCase):
    """Integration tests for complete component workflows."""
    
    def setUp(self):
        """Create test ores."""
        self.iron = Ore.objects.create(name="Int Iron", mass=1.0)
        self.copper = Ore.objects.create(name="Int Copper", mass=0.8)
        self.silicon = Ore.objects.create(name="Int Silicon", mass=0.7)
    
    def test_complete_component_creation_workflow(self):
        """Test complete workflow from creation to validation."""
        component = Component.objects.create(
            name="Complete Workflow Component",
            description="Comprehensive test component",
            materials={
                str(self.iron.ore_id): 10,
                str(self.copper.ore_id): 5
            },
            fabricator_type="Assembler",
            crafting_time=2.5,
            mass=15.0
        )
        
        # Verify creation
        self.assertIsNotNone(component.component_id)
        
        # Verify validation
        is_valid, errors = component.validate_materials()
        self.assertTrue(is_valid)
        
        # Verify relationships
        ores = component.get_material_ores()
        self.assertEqual(ores.count(), 2)
        
        # Verify persistence
        component.refresh_from_db()
        self.assertEqual(component.name, "Complete Workflow Component")
    
    def test_bulk_component_creation(self):
        """Test creating multiple components at once."""
        components_data = [
            {"name": "Bulk Component 1", "materials": {str(self.iron.ore_id): 5}},
            {"name": "Bulk Component 2", "materials": {str(self.copper.ore_id): 3}},
            {"name": "Bulk Component 3", "materials": {str(self.silicon.ore_id): 2}},
        ]
        
        for data in components_data:
            Component.objects.create(**data)
        
        self.assertEqual(Component.objects.count(), 3)
    
    def test_component_update_preserves_relationships(self):
        """Test that updating component preserves ore relationships."""
        component = Component.objects.create(
            name="Update Relationship Test",
            materials={str(self.iron.ore_id): 10}
        )
        
        # Update materials to add another ore
        component.materials[str(self.copper.ore_id)] = 5
        component.save()
        
        # Verify both ores are still referenced
        ores = component.get_material_ores()
        self.assertEqual(ores.count(), 2)
    
    def test_component_with_complex_materials_recipe(self):
        """Test component with all available ores."""
        component = Component.objects.create(
            name="Complex Recipe",
            materials={
                str(self.iron.ore_id): 10,
                str(self.copper.ore_id): 5,
                str(self.silicon.ore_id): 2
            },
            fabricator_type="Advanced Assembler",
            crafting_time=5.0,
            mass=25.0
        )
        
        is_valid, errors = component.validate_materials()
        self.assertTrue(is_valid)
        
        ores = component.get_material_ores()
        self.assertEqual(ores.count(), 3)
    
    def test_component_deletion_does_not_affect_ores(self):
        """Test that deleting component doesn't delete referenced ores."""
        component = Component.objects.create(
            name="Delete Test",
            materials={str(self.iron.ore_id): 10}
        )
        
        component.delete()
        
        # Verify ore still exists
        self.assertTrue(Ore.objects.filter(ore_id=self.iron.ore_id).exists())