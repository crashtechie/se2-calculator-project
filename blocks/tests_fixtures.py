import json
import re
from pathlib import Path

from django.test import TestCase


UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


class BlockFixtureValidationTests(TestCase):
    """Validate block fixture integrity and references."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blocks = json.loads(Path("blocks/fixtures/sample_blocks.json").read_text())
        cls.components = json.loads(Path("components/fixtures/sample_components.json").read_text())
        cls.component_ids = {entry["pk"] for entry in cls.components}

    def test_minimum_block_count(self):
        self.assertGreaterEqual(len(self.blocks), 15)

    def test_block_required_fields_present(self):
        for block in self.blocks:
            self.assertIn("model", block)
            self.assertIn("pk", block)
            self.assertIn("fields", block)
            fields = block["fields"]
            self.assertIn("name", fields)
            self.assertIn("components", fields)
            self.assertIsInstance(fields.get("components", []), list)

    def test_block_component_references_valid(self):
        for block in self.blocks:
            for comp_ref in block["fields"].get("components", []):
                self.assertIn("component_id", comp_ref)
                self.assertIn("component_name", comp_ref)
                self.assertIn("quantity", comp_ref)
                self.assertIn(comp_ref["component_id"], self.component_ids)
                self.assertGreater(comp_ref["quantity"], 0)


class BlockFixtureUUIDTests(TestCase):
    """Validate UUID format and uniqueness for block fixtures."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blocks = json.loads(Path("blocks/fixtures/sample_blocks.json").read_text())
        cls.block_ids = [entry["pk"] for entry in cls.blocks]

    def test_all_block_uuids_valid_v7(self):
        for block_id in self.block_ids:
            self.assertRegex(block_id, UUID_PATTERN)

    def test_block_uuid_uniqueness(self):
        self.assertEqual(len(self.block_ids), len(set(self.block_ids)))

    def test_no_placeholder_uuids(self):
        self.assertFalse(any("REPLACE_WITH" in block_id for block_id in self.block_ids))