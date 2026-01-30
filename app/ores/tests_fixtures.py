import json
import re
from pathlib import Path

from django.test import TestCase


UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


class OreFixtureFileValidationTests(TestCase):
    """Validate ore fixture structure and content."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture_path = Path("ores/fixtures/sample_ores.json")
        cls.fixture_data = json.loads(fixture_path.read_text())

    def test_fixture_exists_and_is_list(self):
        self.assertIsInstance(self.fixture_data, list)
        self.assertGreater(len(self.fixture_data), 0)

    def test_minimum_ore_count(self):
        self.assertGreaterEqual(len(self.fixture_data), 5)

    def test_required_fields_present(self):
        for entry in self.fixture_data:
            self.assertIn("model", entry)
            self.assertIn("pk", entry)
            self.assertIn("fields", entry)
            self.assertIn("name", entry["fields"])
            self.assertIn("mass", entry["fields"])


class OreFixtureUUIDTests(TestCase):
    """Validate UUID format and uniqueness for ore fixtures."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture_path = Path("ores/fixtures/sample_ores.json")
        cls.fixture_data = json.loads(fixture_path.read_text())
        cls.uuids = [entry["pk"] for entry in cls.fixture_data]

    def test_all_uuids_valid_v7(self):
        for uuid in self.uuids:
            self.assertRegex(uuid, UUID_PATTERN)

    def test_uuid_uniqueness(self):
        self.assertEqual(len(self.uuids), len(set(self.uuids)))

    def test_no_placeholder_uuids(self):
        self.assertFalse(any("REPLACE_WITH" in uuid for uuid in self.uuids))