from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from ores.models import Ore
import time
import uuid


class OreModelCreationTests(TestCase):
    """Test suite for basic Ore model creation and validation."""

    def test_create_ore_with_all_fields(self):
        """Test creating an Ore with all fields specified."""
        ore = Ore.objects.create(
            name="Iron Ore",
            description="Common ore used for steel production",
            mass=1.5
        )
        
        self.assertIsNotNone(ore.ore_id)
        self.assertEqual(ore.name, "Iron Ore")
        self.assertEqual(ore.description, "Common ore used for steel production")
        self.assertEqual(ore.mass, 1.5)
        self.assertIsNotNone(ore.created_at)
        self.assertIsNotNone(ore.updated_at)

    def test_create_ore_minimal_fields(self):
        """Test creating an Ore with only required fields."""
        ore = Ore.objects.create(name="Silicon", mass=0.8)
        
        self.assertEqual(ore.name, "Silicon")
        self.assertEqual(ore.mass, 0.8)
        self.assertEqual(ore.description, "")  # blank=True
        self.assertIsNotNone(ore.ore_id)

    def test_create_ore_with_float_mass(self):
        """Test that mass field correctly stores float values."""
        test_values = [0.1, 1.0, 2.5, 100.999]
        
        for mass in test_values:
            ore = Ore.objects.create(name=f"Test Ore {mass}", mass=mass)
            self.assertEqual(ore.mass, mass)

    def test_ore_string_representation(self):
        """Test that __str__ returns the ore name."""
        ore = Ore.objects.create(name="Cobalt Ore", mass=1.2)
        self.assertEqual(str(ore), "Cobalt Ore")


class OreModelFieldValidationTests(TestCase):
    """Test suite for Ore model field constraints and validation."""

    def test_unique_name_constraint(self):
        """Test that ore names must be unique."""
        Ore.objects.create(name="Unique Ore", mass=1.0)
        
        with self.assertRaises(IntegrityError):
            Ore.objects.create(name="Unique Ore", mass=2.0)

    def test_unique_name_case_sensitive(self):
        """Test that unique constraint is case sensitive."""
        Ore.objects.create(name="Iron Ore", mass=1.0)
        # Different case should be allowed (database dependent)
        ore2 = Ore.objects.create(name="iron ore", mass=1.0)
        self.assertIsNotNone(ore2)

    def test_name_max_length(self):
        """Test that name field respects max_length constraint."""
        # Create a name exactly at the limit
        name_100_chars = "A" * 100
        ore = Ore.objects.create(name=name_100_chars, mass=1.0)
        self.assertEqual(len(ore.name), 100)

    def test_name_exceeds_max_length(self):
        """Test that names exceeding max_length are rejected."""
        name_101_chars = "A" * 101
        with self.assertRaises(ValidationError):
            ore = Ore(name=name_101_chars, mass=1.0)
            ore.full_clean()

    def test_description_blank_allowed(self):
        """Test that description is optional."""
        ore = Ore.objects.create(name="Test Ore", mass=1.0)
        self.assertEqual(ore.description, "")

    def test_description_long_text(self):
        """Test that description can store long text."""
        long_description = "A" * 10000
        ore = Ore.objects.create(
            name="Long Description Ore",
            description=long_description,
            mass=1.0
        )
        self.assertEqual(ore.description, long_description)


class OreModelUUIDTests(TestCase):
    """Test suite for UUIDv7 primary key generation."""

    def test_ore_id_auto_generated(self):
        """Test that ore_id is automatically generated on creation."""
        ore = Ore.objects.create(name="Auto UUID Ore", mass=1.0)
        self.assertIsNotNone(ore.ore_id)
        # ore_id is stored as string due to lambda conversion
        self.assertIsInstance(ore.ore_id, str)

    def test_ore_id_is_uuid(self):
        """Test that ore_id is a valid UUID."""
        ore = Ore.objects.create(name="UUID Format Ore", mass=1.0)
        # ore_id is stored as string, but should be a valid UUID string
        uuid_str = str(ore.ore_id)
        # Should be able to recreate UUID from string
        uuid_obj = uuid.UUID(uuid_str)
        # String form should match
        self.assertEqual(ore.ore_id, str(uuid_obj))

    def test_ore_id_unique(self):
        """Test that each ore gets a unique ore_id."""
        ores = []
        for i in range(10):
            ore = Ore.objects.create(name=f"UUID Test Ore {i}", mass=1.0)
            ores.append(ore.ore_id)
        
        # All UUIDs should be unique
        self.assertEqual(len(ores), len(set(ores)))

    def test_ore_id_not_editable(self):
        """Test that ore_id cannot be manually changed after creation."""
        ore = Ore.objects.create(name="Non-editable UUID Ore", mass=1.0)
        original_id = ore.ore_id
        
        # Since the field is editable=False, attempting to change it in the form
        # won't be allowed. We can verify the field property is set correctly.
        field = Ore._meta.get_field('ore_id')
        self.assertFalse(field.editable)

    def test_uuid7_time_ordered(self):
        """Test that UUIDv7 primary keys are time-ordered."""
        ores = []
        for i in range(5):
            ore = Ore.objects.create(name=f"Time Order Test {i}", mass=1.0)
            ores.append(ore)
            # Small delay to ensure different timestamps
            time.sleep(0.01)
        
        # Extract UUIDs
        uuids = [ore.ore_id for ore in ores]
        # UUIDv7 should be sequentially ordered by time
        # Compare string representations (UUIDv7 encodes time in first part)
        uuid_strs = [str(uuid) for uuid in uuids]
        self.assertEqual(uuid_strs, sorted(uuid_strs))


class OreModelTimestampTests(TestCase):
    """Test suite for automatic timestamp handling."""

    def test_created_at_auto_populated(self):
        """Test that created_at is automatically populated on creation."""
        before = timezone.now()
        ore = Ore.objects.create(name="Timestamp Ore", mass=1.0)
        after = timezone.now()
        
        self.assertIsNotNone(ore.created_at)
        self.assertGreaterEqual(ore.created_at, before)
        self.assertLessEqual(ore.created_at, after)

    def test_updated_at_auto_populated(self):
        """Test that updated_at is automatically populated on creation."""
        before = timezone.now()
        ore = Ore.objects.create(name="Updated Timestamp Ore", mass=1.0)
        after = timezone.now()
        
        self.assertIsNotNone(ore.updated_at)
        self.assertGreaterEqual(ore.updated_at, before)
        self.assertLessEqual(ore.updated_at, after)

    def test_created_at_unchanged_on_update(self):
        """Test that created_at doesn't change when ore is updated."""
        ore = Ore.objects.create(name="Creation Time Test", mass=1.0)
        original_created_at = ore.created_at
        
        # Wait a bit and update
        time.sleep(0.1)
        ore.mass = 2.0
        ore.save()
        
        ore.refresh_from_db()
        self.assertEqual(ore.created_at, original_created_at)

    def test_updated_at_changes_on_update(self):
        """Test that updated_at changes when ore is updated."""
        ore = Ore.objects.create(name="Update Time Test", mass=1.0)
        original_updated_at = ore.updated_at
        
        # Wait and update
        time.sleep(0.1)
        ore.mass = 2.0
        ore.save()
        
        ore.refresh_from_db()
        self.assertGreater(ore.updated_at, original_updated_at)

    def test_timestamps_are_timezone_aware(self):
        """Test that timestamps include timezone information."""
        ore = Ore.objects.create(name="Timezone Ore", mass=1.0)
        
        # Should have timezone info
        self.assertIsNotNone(ore.created_at.tzinfo)
        self.assertIsNotNone(ore.updated_at.tzinfo)


class OreModelQueryTests(TestCase):
    """Test suite for Ore model queries and ordering."""

    def setUp(self):
        """Create test ores for query testing."""
        self.ores = [
            Ore.objects.create(name="Zinc", mass=1.1),
            Ore.objects.create(name="Iron", mass=1.0),
            Ore.objects.create(name="Silver", mass=0.9),
            Ore.objects.create(name="Gold", mass=1.2),
        ]

    def test_ores_ordered_by_name(self):
        """Test that ores are returned ordered by name."""
        ores = Ore.objects.all()
        names = [ore.name for ore in ores]
        expected_names = ["Gold", "Iron", "Silver", "Zinc"]
        self.assertEqual(names, expected_names)

    def test_get_ore_by_name(self):
        """Test retrieving an ore by name."""
        ore = Ore.objects.get(name="Iron")
        self.assertEqual(ore.name, "Iron")
        self.assertEqual(ore.mass, 1.0)

    def test_get_ore_by_mass(self):
        """Test querying ores by mass."""
        ores = Ore.objects.filter(mass__gt=1.0)
        self.assertEqual(ores.count(), 2)  # Zinc (1.1) and Gold (1.2)

    def test_count_ores(self):
        """Test counting ores."""
        self.assertEqual(Ore.objects.count(), 4)

    def test_delete_ore(self):
        """Test deleting an ore."""
        ore = Ore.objects.get(name="Silver")
        ore.delete()
        self.assertEqual(Ore.objects.count(), 3)
        with self.assertRaises(Ore.DoesNotExist):
            Ore.objects.get(name="Silver")


class OreModelMetaTests(TestCase):
    """Test suite for Ore model Meta configuration."""

    def test_model_verbose_name(self):
        """Test that verbose_name is set correctly."""
        self.assertEqual(Ore._meta.verbose_name, "Ore")

    def test_model_verbose_name_plural(self):
        """Test that verbose_name_plural is set correctly."""
        self.assertEqual(Ore._meta.verbose_name_plural, "Ores")

    def test_model_table_name(self):
        """Test that custom table name is used."""
        self.assertEqual(Ore._meta.db_table, "ores_ore")

    def test_model_ordering(self):
        """Test that model has correct ordering."""
        self.assertEqual(Ore._meta.ordering, ["name"])


class OreModelPrimaryKeyTests(TestCase):
    """Test suite for primary key configuration."""

    def test_ore_id_is_primary_key(self):
        """Test that ore_id is configured as primary key."""
        self.assertTrue(Ore._meta.get_field("ore_id").primary_key)

    def test_cannot_create_ore_with_duplicate_id(self):
        """Test that duplicate ore_ids cannot be created."""
        ore1 = Ore.objects.create(name="Ore 1", mass=1.0)
        
        # Manually try to create with same ID (shouldn't happen in normal operation)
        with self.assertRaises(IntegrityError):
            Ore.objects.create(ore_id=ore1.ore_id, name="Ore 2", mass=1.0)


class OreModelIntegrationTests(TestCase):
    """Integration tests for complete Ore model workflows."""

    def test_create_read_update_delete(self):
        """Test complete CRUD operation cycle."""
        # Create
        ore = Ore.objects.create(
            name="CRUD Test Ore",
            description="Initial description",
            mass=1.0
        )
        self.assertIsNotNone(ore.ore_id)
        
        # Read
        retrieved = Ore.objects.get(ore_id=ore.ore_id)
        self.assertEqual(retrieved.name, "CRUD Test Ore")
        
        # Update
        retrieved.description = "Updated description"
        retrieved.mass = 2.0
        retrieved.save()
        
        # Verify update
        ore.refresh_from_db()
        self.assertEqual(ore.description, "Updated description")
        self.assertEqual(ore.mass, 2.0)
        
        # Delete
        ore.delete()
        self.assertEqual(Ore.objects.filter(ore_id=ore.ore_id).count(), 0)

    def test_bulk_create_ores(self):
        """Test creating multiple ores at once."""
        ores_to_create = [
            Ore(name=f"Bulk Ore {i}", mass=float(i))
            for i in range(1, 6)
        ]
        
        created_ores = Ore.objects.bulk_create(ores_to_create)
        self.assertEqual(len(created_ores), 5)
        self.assertEqual(Ore.objects.filter(name__startswith="Bulk").count(), 5)

    def test_search_ores_by_name(self):
        """Test searching ores by partial name match."""
        Ore.objects.create(name="Iron Ore", mass=1.0)
        Ore.objects.create(name="Iron Oxide", mass=1.5)
        Ore.objects.create(name="Copper", mass=1.2)
        
        iron_ores = Ore.objects.filter(name__icontains="Iron")
        self.assertEqual(iron_ores.count(), 2)

    def test_update_multiple_ores(self):
        """Test updating multiple ores at once."""
        for i in range(5):
            Ore.objects.create(name=f"Update Test {i}", mass=1.0)
        
        # Update all created ores
        Ore.objects.filter(name__startswith="Update Test").update(mass=2.0)
        
        updated = Ore.objects.filter(name__startswith="Update Test")
        for ore in updated:
            self.assertEqual(ore.mass, 2.0)
