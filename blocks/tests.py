from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from ores.models import Ore
from components.models import Component
from blocks.models import Block


# ---- Test helpers / factories ----
def create_ore(name="Iron", mass=1.0):
    return Ore.objects.create(name=name, mass=mass, description="")


def create_component(name="Steel Plate", materials=None):
    if materials is None:
        # Ensure unique ore names to avoid unique constraint violations across tests
        ore = create_ore(name=f"{name}-Ore")
        materials = {str(ore.ore_id): 1}
    return Component.objects.create(
        name=name,
        description="",
        materials=materials,
        fabricator_type="Assembler",
        crafting_time=1.0,
        mass=1.0,
    )


def component_entry(component: Component, quantity: int = 1):
    return {
        "component_id": str(component.component_id),
        "component_name": component.name,
        "quantity": quantity,
    }


def create_block(
    name="Test Block",
    components_list=None,
    consumer_type="",
    consumer_rate=0.0,
    producer_type="",
    producer_rate=0.0,
    storage_capacity=0.0,
    mass=10.0,
    health=100.0,
    pcu=50,
    snap_size=0.25,
    input_mass=5,
    output_mass=2,
):
    if components_list is None:
        components_list = []
    return Block.objects.create(
        name=name,
        description="",
        mass=mass,
        components=components_list,
        health=health,
        pcu=pcu,
        snap_size=snap_size,
        input_mass=input_mass,
        output_mass=output_mass,
        consumer_type=consumer_type,
        consumer_rate=consumer_rate,
        producer_type=producer_type,
        producer_rate=producer_rate,
        storage_capacity=storage_capacity,
    )


# ---- BlockModelCreationTests (7) ----
class BlockModelCreationTests(TestCase):
    def test_create_valid_block_minimal_fields(self):
        blk = create_block(name="Minimal Block")
        self.assertIsInstance(blk, Block)
        self.assertEqual(blk.name, "Minimal Block")

    def test_duplicate_name_not_allowed(self):
        create_block(name="Unique Block")
        with self.assertRaises(IntegrityError):
            create_block(name="Unique Block")

    def test_default_components_is_list(self):
        blk = create_block(name="Default Components Block")
        self.assertIsInstance(blk.components, list)
        self.assertEqual(blk.components, [])

    def test_str_returns_name(self):
        blk = create_block(name="Display Name Block")
        self.assertEqual(str(blk), "Display Name Block")

    def test_uuid_primary_key_assigned(self):
        blk = create_block(name="UUID Block")
        self.assertIsNotNone(blk.block_id)
        self.assertTrue(str(blk.block_id))

    def test_timestamps_auto_populated(self):
        blk = create_block(name="Timestamp Block")
        self.assertIsNotNone(blk.created_at)
        self.assertIsNotNone(blk.updated_at)

    def test_get_component_objects_empty_returns_none_queryset(self):
        blk = create_block(name="Empty Components Block")
        qs = blk.get_component_objects()
        self.assertEqual(qs.count(), 0)


# ---- BlockFieldValidationTests (8) ----
class BlockFieldValidationTests(TestCase):
    def test_blank_description_allowed(self):
        blk = create_block(name="No Description Block")
        self.assertEqual(blk.description, "")

    def test_assign_and_retrieve_mass(self):
        blk = create_block(name="Mass Block", mass=42.5)
        self.assertEqual(blk.mass, 42.5)

    def test_assign_and_retrieve_health(self):
        blk = create_block(name="Health Block", health=250.0)
        self.assertEqual(blk.health, 250.0)

    def test_assign_and_retrieve_pcu(self):
        blk = create_block(name="PCU Block", pcu=123)
        self.assertEqual(blk.pcu, 123)

    def test_assign_and_retrieve_snap_size(self):
        blk = create_block(name="Snap Block", snap_size=0.5)
        self.assertEqual(blk.snap_size, 0.5)

    def test_assign_and_retrieve_input_mass(self):
        blk = create_block(name="Input Mass Block", input_mass=99)
        self.assertEqual(blk.input_mass, 99)

    def test_assign_and_retrieve_output_mass(self):
        blk = create_block(name="Output Mass Block", output_mass=77)
        self.assertEqual(blk.output_mass, 77)

    def test_assign_and_retrieve_storage_capacity(self):
        blk = create_block(name="Storage Block", storage_capacity=10.0)
        self.assertEqual(blk.storage_capacity, 10.0)


# ---- BlockTimestampTests (5) ----
class BlockTimestampTests(TestCase):
    def test_created_at_set_on_create(self):
        blk = create_block(name="CreatedAt Block")
        self.assertIsNotNone(blk.created_at)

    def test_updated_at_updates_on_save(self):
        blk = create_block(name="UpdatedAt Block")
        original_updated = blk.updated_at
        blk.description = "Updated"
        blk.save()
        self.assertGreaterEqual(blk.updated_at, original_updated)

    def test_updated_at_greater_or_equal_to_created_at(self):
        blk = create_block(name="Timestamp Compare Block")
        self.assertGreaterEqual(blk.updated_at, blk.created_at)

    def test_multiple_updates_change_updated_at(self):
        blk = create_block(name="Multi Update Block")
        first = blk.updated_at
        blk.description = "A"
        blk.save()
        second = blk.updated_at
        blk.description = "B"
        blk.save()
        third = blk.updated_at
        self.assertGreaterEqual(second, first)
        self.assertGreaterEqual(third, second)

    def test_datetime_types(self):
        blk = create_block(name="Datetime Type Block")
        from datetime import datetime
        self.assertIsInstance(blk.created_at, datetime)
        self.assertIsInstance(blk.updated_at, datetime)


# ---- BlockComponentsJSONFieldTests (5) ----
class BlockComponentsJSONFieldTests(TestCase):
    def test_empty_components_valid(self):
        blk = create_block(name="Empty Components Valid Block")
        is_valid, errors = blk.validate_components()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_non_dict_component_item_invalid(self):
        blk = Block(
            name="NonDict Component Block",
            description="",
            mass=10.0,
            components=["not-a-dict"],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
        )
        is_valid, errors = blk.validate_components()
        self.assertFalse(is_valid)
        self.assertTrue(any("must be dict" in e for e in errors))

    def test_missing_keys_in_component_item_invalid(self):
        blk = Block(
            name="Missing Keys Block",
            description="",
            mass=10.0,
            components=[{"component_id": "x"}],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
        )
        is_valid, errors = blk.validate_components()
        self.assertFalse(is_valid)
        self.assertTrue(any("missing keys" in e for e in errors))

    def test_invalid_quantity_in_component_item_invalid(self):
        comp = create_component(name="Motor")
        blk = Block(
            name="Invalid Quantity Block",
            description="",
            mass=10.0,
            components=[component_entry(comp, quantity=0)],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
        )
        is_valid, errors = blk.validate_components()
        self.assertFalse(is_valid)
        self.assertTrue(any("Invalid quantity" in e for e in errors))

    def test_nonexistent_component_id_invalid(self):
        blk = Block(
            name="Nonexistent Component ID Block",
            description="",
            mass=10.0,
            components=[
                {
                    "component_id": "00000000-0000-0000-0000-000000000000",
                    "component_name": "Ghost",
                    "quantity": 1,
                }
            ],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
        )
        is_valid, errors = blk.validate_components()
        self.assertFalse(is_valid)
        self.assertTrue(any("does not exist" in e for e in errors))


# ---- BlockConsumerValidationTests (5) ----
class BlockConsumerValidationTests(TestCase):
    def test_consumer_valid_when_type_empty_and_rate_zero(self):
        blk = create_block(name="Consumer OK Empty", consumer_type="", consumer_rate=0.0)
        is_valid, errors = blk.validate_consumer()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_consumer_invalid_when_type_set_and_rate_zero(self):
        blk = Block(
            name="Consumer Invalid Zero",
            description="",
            mass=10.0,
            components=[],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
            consumer_type="Power",
            consumer_rate=0.0,
        )
        is_valid, errors = blk.validate_consumer()
        self.assertFalse(is_valid)
        self.assertTrue(any("requires consumer_rate > 0" in e for e in errors))

    def test_consumer_invalid_when_rate_negative(self):
        blk = Block(
            name="Consumer Invalid Negative",
            description="",
            mass=10.0,
            components=[],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
            consumer_type="Power",
            consumer_rate=-1.0,
        )
        is_valid, errors = blk.validate_consumer()
        self.assertFalse(is_valid)
        self.assertTrue(any("cannot be negative" in e for e in errors))

    def test_consumer_valid_when_type_set_and_rate_positive(self):
        blk = create_block(name="Consumer Valid", consumer_type="Power", consumer_rate=5.0)
        is_valid, errors = blk.validate_consumer()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_consumer_error_message_contains_type(self):
        blk = Block(
            name="Consumer Msg",
            description="",
            mass=10.0,
            components=[],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
            consumer_type="Oxygen",
            consumer_rate=0.0,
        )
        is_valid, errors = blk.validate_consumer()
        self.assertFalse(is_valid)
        self.assertTrue(any("Oxygen" in e for e in errors))


# ---- BlockProducerValidationTests (5) ----
class BlockProducerValidationTests(TestCase):
    def test_producer_valid_when_type_empty_and_rate_zero(self):
        blk = create_block(name="Producer OK Empty", producer_type="", producer_rate=0.0)
        is_valid, errors = blk.validate_producer()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_producer_invalid_when_type_set_and_rate_zero(self):
        blk = Block(
            name="Producer Invalid Zero",
            description="",
            mass=10.0,
            components=[],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
            producer_type="Hydrogen",
            producer_rate=0.0,
        )
        is_valid, errors = blk.validate_producer()
        self.assertFalse(is_valid)
        self.assertTrue(any("requires producer_rate > 0" in e for e in errors))

    def test_producer_invalid_when_rate_negative(self):
        blk = Block(
            name="Producer Invalid Negative",
            description="",
            mass=10.0,
            components=[],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
            producer_type="Hydrogen",
            producer_rate=-1.0,
        )
        is_valid, errors = blk.validate_producer()
        self.assertFalse(is_valid)
        self.assertTrue(any("cannot be negative" in e for e in errors))

    def test_producer_valid_when_type_set_and_rate_positive(self):
        blk = create_block(name="Producer Valid", producer_type="Hydrogen", producer_rate=3.0)
        is_valid, errors = blk.validate_producer()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_producer_error_message_contains_type(self):
        blk = Block(
            name="Producer Msg",
            description="",
            mass=10.0,
            components=[],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
            producer_type="Power",
            producer_rate=0.0,
        )
        is_valid, errors = blk.validate_producer()
        self.assertFalse(is_valid)
        self.assertTrue(any("Power" in e for e in errors))


# ---- BlockComponentRelationshipTests (4) ----
class BlockComponentRelationshipTests(TestCase):
    def test_get_component_objects_returns_correct_queryset(self):
        comp1 = create_component(name="Motor")
        comp2 = create_component(name="Computer")
        blk = create_block(
            name="Relationship Block",
            components_list=[component_entry(comp1, 2), component_entry(comp2, 3)],
        )
        qs = blk.get_component_objects()
        names = set(qs.values_list("name", flat=True))
        self.assertEqual(names, {"Motor", "Computer"})

    def test_get_component_objects_with_duplicate_ids_returns_unique(self):
        comp = create_component(name="Display")
        blk = create_block(
            name="Duplicate IDs Block",
            components_list=[component_entry(comp, 1), component_entry(comp, 2)],
        )
        qs = blk.get_component_objects()
        self.assertEqual(qs.count(), 1)

    def test_validate_components_success_with_existing_components(self):
        comp = create_component(name="Steel Plate")
        blk = create_block(
            name="Validate Components Success",
            components_list=[component_entry(comp, 10)],
        )
        is_valid, errors = blk.validate_components()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_save_with_valid_components_succeeds(self):
        comp = create_component(name="Interior Plate")
        blk = create_block(
            name="Save Valid Components",
            components_list=[component_entry(comp, 1)],
        )
        # save() runs clean(); should succeed
        blk.description = "OK"
        blk.save()
        self.assertEqual(Block.objects.get(pk=blk.block_id).description, "OK")


# ---- BlockMetaTests (4) ----
class BlockMetaTests(TestCase):
    def test_verbose_names(self):
        self.assertEqual(Block._meta.verbose_name, "Block")
        self.assertEqual(Block._meta.verbose_name_plural, "Blocks")

    def test_db_table_name(self):
        self.assertEqual(Block._meta.db_table, "blocks_block")

    def test_ordering_by_name(self):
        b1 = create_block(name="A")
        b2 = create_block(name="B")
        names = list(Block.objects.values_list("name", flat=True))
        self.assertEqual(names, ["A", "B"])  # ordered by name

    def test_model_fields_exist(self):
        field_names = {f.name for f in Block._meta.get_fields()}
        for expected in [
            "block_id",
            "name",
            "description",
            "mass",
            "components",
            "health",
            "pcu",
            "snap_size",
            "input_mass",
            "output_mass",
            "consumer_type",
            "consumer_rate",
            "producer_type",
            "producer_rate",
            "storage_capacity",
            "created_at",
            "updated_at",
        ]:
            self.assertIn(expected, field_names)


# ---- BlockIntegrationTests (6) ----
class BlockIntegrationTests(TestCase):
    def test_save_raises_validation_error_for_invalid_components(self):
        blk = Block(
            name="Invalid Components Save",
            description="Try save",
            mass=10.0,
            components=[{"bad": "structure"}],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
        )
        with self.assertRaises(ValidationError):
            blk.save()

    def test_save_raises_validation_error_for_consumer_and_producer_invalid(self):
        blk = Block(
            name="Invalid Consumer Producer",
            description="",
            mass=10.0,
            components=[],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
            consumer_type="Power",
            consumer_rate=0.0,
            producer_type="Hydrogen",
            producer_rate=0.0,
        )
        with self.assertRaises(ValidationError) as ctx:
            blk.save()
        msg = str(ctx.exception)
        self.assertIn("consumer_rate > 0", msg)
        self.assertIn("producer_rate > 0", msg)

    def test_save_success_with_valid_consumer_and_producer(self):
        blk = create_block(
            name="Valid Consumer Producer",
            consumer_type="Power",
            consumer_rate=1.5,
            producer_type="Hydrogen",
            producer_rate=2.0,
        )
        blk.description = "OK"
        blk.save()
        self.assertEqual(Block.objects.get(pk=blk.block_id).description, "OK")

    def test_multiple_errors_aggregated_in_validation_error_message(self):
        blk = Block(
            name="Multiple Errors",
            description="",
            mass=10.0,
            components=[{"not": "valid"}],
            health=100.0,
            pcu=1,
            snap_size=0.25,
            input_mass=1,
            output_mass=1,
            consumer_type="Power",
            consumer_rate=0.0,
        )
        with self.assertRaises(ValidationError) as ctx:
            blk.save()
        msg = str(ctx.exception)
        self.assertIn("Validation failed:", msg)
        self.assertIn("consumer_rate > 0", msg)
        self.assertIn("missing keys", msg)

    def test_full_cycle_create_update_save_updates_timestamp(self):
        blk = create_block(name="Full Cycle")
        before = blk.updated_at
        blk.description = "Cycle"
        blk.save()
        after = blk.updated_at
        self.assertGreaterEqual(after, before)

    def test_query_filtering_by_name_and_ordering(self):
        create_block(name="Alpha")
        create_block(name="Beta")
        names = list(Block.objects.filter(name__in=["Alpha", "Beta"]).values_list("name", flat=True))
        self.assertEqual(names, ["Alpha", "Beta"])  # ordering by name
