import json
import re
from pathlib import Path

from django.test import TestCase


UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


class ComponentFixtureValidationTests(TestCase):
    """Validate component fixture structure and references."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.components = json.loads(Path("components/fixtures/sample_components.json").read_text())
        cls.ores = json.loads(Path("ores/fixtures/sample_ores.json").read_text())
        cls.ore_ids = {entry["pk"] for entry in cls.ores}

    def test_minimum_component_count(self):
        self.assertGreaterEqual(len(self.components), 10)

    def test_all_components_have_required_fields(self):
        for comp in self.components:
            self.assertIn("model", comp)
            self.assertIn("pk", comp)
            self.assertIn("fields", comp)
            fields = comp["fields"]
            self.assertIn("name", fields)
            self.assertIn("materials", fields)
            self.assertIsInstance(fields.get("materials", {}), dict)

    def test_material_references_use_known_ores(self):
        for comp in self.components:
            materials = comp["fields"].get("materials", {})
            for ore_id, qty in materials.items():
                self.assertIn(ore_id, self.ore_ids)
                self.assertGreater(qty, 0)


class ComponentFixtureUUIDTests(TestCase):
    """Validate UUID format and uniqueness for component fixtures."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.components = json.loads(Path("components/fixtures/sample_components.json").read_text())
        cls.component_ids = [entry["pk"] for entry in cls.components]

    def test_all_component_uuids_valid_v7(self):
        for comp_id in self.component_ids:
            self.assertRegex(comp_id, UUID_PATTERN)

    def test_component_uuid_uniqueness(self):
        self.assertEqual(len(self.component_ids), len(set(self.component_ids)))

    def test_no_placeholder_uuids(self):
        self.assertFalse(any("REPLACE_WITH" in comp_id for comp_id in self.component_ids))