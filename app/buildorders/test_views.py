"""
Integration tests for BuildOrder CRUD views.

Tests complete workflows including create → view → update → delete sequences,
search → sort → paginate workflows, form validation workflows, and cache invalidation.
Follows patterns from app/blocks/test_views.py and app/components/test_views.py.
"""

import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.core.cache import cache

from buildorders.models import BuildOrder
from blocks.models import Block
from components.models import Component
from ores.models import Ore


class BuildOrderIntegrationTestCase(TestCase):
    """Integration tests for complete CRUD workflows."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all integration tests."""
        cls.client = Client()

        # Create test ores
        cls.ore_iron = Ore.objects.create(name="Iron", mass=1.0)
        cls.ore_silicon = Ore.objects.create(name="Silicon", mass=0.5)

        # Create test components
        cls.comp_steel = Component.objects.create(
            name="Steel Plate",
            description="Basic steel plate",
            materials={str(cls.ore_iron.ore_id): 7.0},
            mass=20.0,
            crafting_time=3.2,
            fabricator_type="Assembler",
        )
        cls.comp_computer = Component.objects.create(
            name="Computer",
            description="Basic computer",
            materials={
                str(cls.ore_iron.ore_id): 1.0,
                str(cls.ore_silicon.ore_id): 2.0,
            },
            mass=5.0,
            crafting_time=5.0,
            fabricator_type="Assembler",
        )

        # Create test blocks
        cls.block_armor = Block.objects.create(
            name="Armor Block",
            description="Heavy armor block",
            mass=150.0,
            components={str(cls.comp_steel.component_id): 25},
            health=100.0,
            pcu=50,
            snap_size=0.25,
            input_mass=0,
            output_mass=0,
        )
        cls.block_computer = Block.objects.create(
            name="Computer Block",
            description="Computer block",
            mass=50.0,
            components={str(cls.comp_computer.component_id): 10},
            health=50.0,
            pcu=25,
            snap_size=0.25,
            input_mass=0,
            output_mass=0,
        )

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    # ---- Test 18.1: Complete CRUD workflow ----
    def test_complete_crud_workflow_create_view_update_delete(self):
        """
        Test complete CRUD workflow: create → view → update → delete.
        Validates: Requirements 15.7
        """
        # Step 1: Create a build order
        create_url = reverse("buildorders:create")
        create_data = {
            "name": "Test Build Order",
            "blocks_json": json.dumps({str(self.block_armor.block_id): 5}),
        }
        create_response = self.client.post(create_url, create_data, follow=True)

        # Verify creation
        self.assertEqual(create_response.status_code, 200)
        self.assertTrue(BuildOrder.objects.filter(name="Test Build Order").exists())
        build_order = BuildOrder.objects.get(name="Test Build Order")

        # Verify redirect to detail view
        self.assertRedirects(
            create_response,
            reverse("buildorders:detail", kwargs={"pk": build_order.order_id}),
        )

        # Verify success message
        messages = list(get_messages(create_response.wsgi_request))
        self.assertTrue(
            any("created successfully" in str(m) for m in messages),
            "Create success message not found",
        )

        # Verify database state after creation
        self.assertEqual(build_order.blocks[str(self.block_armor.block_id)], 5)

        # Step 2: View the build order detail
        detail_url = reverse("buildorders:detail", kwargs={"pk": build_order.order_id})
        detail_response = self.client.get(detail_url)

        # Verify detail view renders
        self.assertEqual(detail_response.status_code, 200)
        self.assertTemplateUsed(detail_response, "buildorders/buildorder_detail.html")
        self.assertContains(detail_response, "Test Build Order")

        # Verify calculation summary is displayed
        self.assertIn("calculation_summary", detail_response.context)
        summary = detail_response.context["calculation_summary"]
        self.assertIn("total_mass", summary)
        self.assertEqual(summary["total_mass"], 750.0)  # 150 kg * 5 blocks

        # Step 3: Update the build order
        update_url = reverse("buildorders:update", kwargs={"pk": build_order.order_id})
        update_data = {
            "name": "Updated Build Order",
            "blocks_json": json.dumps({str(self.block_armor.block_id): 10}),
        }
        update_response = self.client.post(update_url, update_data, follow=True)

        # Verify update
        self.assertEqual(update_response.status_code, 200)
        build_order.refresh_from_db()
        self.assertEqual(build_order.name, "Updated Build Order")
        self.assertEqual(build_order.blocks[str(self.block_armor.block_id)], 10)

        # Verify redirect to detail view
        self.assertRedirects(
            update_response,
            reverse("buildorders:detail", kwargs={"pk": build_order.order_id}),
        )

        # Verify success message
        messages = list(get_messages(update_response.wsgi_request))
        self.assertTrue(
            any("updated successfully" in str(m) for m in messages),
            "Update success message not found",
        )

        # Step 4: Delete the build order
        delete_url = reverse("buildorders:delete", kwargs={"pk": build_order.order_id})
        delete_response = self.client.post(delete_url, follow=True)

        # Verify deletion
        self.assertEqual(delete_response.status_code, 200)
        self.assertFalse(
            BuildOrder.objects.filter(order_id=build_order.order_id).exists()
        )

        # Verify redirect to list view
        self.assertRedirects(delete_response, reverse("buildorders:list"))

        # Verify success message
        messages = list(get_messages(delete_response.wsgi_request))
        self.assertTrue(
            any("deleted successfully" in str(m) for m in messages),
            "Delete success message not found",
        )

    # ---- Test 18.2: Search → sort → paginate workflow ----
    def test_search_sort_paginate_workflow_preserves_parameters(self):
        """
        Test search → sort → paginate workflow with query parameter preservation.
        Validates: Requirements 15.7
        """
        # Create multiple build orders for testing
        for i in range(30):
            BuildOrder.objects.create(
                name=f"Build Order {i:02d}",
                description=f"Test order {i}",
                blocks={str(self.block_armor.block_id): i + 1},
            )

        # Create some orders with "Alpha" in the name for search testing
        BuildOrder.objects.create(
            name="Alpha Order 1",
            blocks={str(self.block_armor.block_id): 5},
        )
        BuildOrder.objects.create(
            name="Alpha Order 2",
            blocks={str(self.block_computer.block_id): 3},
        )

        list_url = reverse("buildorders:list")

        # Step 1: Search for "Alpha"
        search_response = self.client.get(list_url, {"q": "Alpha"})
        self.assertEqual(search_response.status_code, 200)

        # Verify search results
        build_orders = list(search_response.context["buildorder_list"])
        self.assertTrue(all("Alpha" in order.name for order in build_orders))
        self.assertEqual(search_response.context["search_query"], "Alpha")

        # Step 2: Add sorting to search results
        search_sort_response = self.client.get(
            list_url, {"q": "Alpha", "sort": "name", "order": "asc"}
        )
        self.assertEqual(search_sort_response.status_code, 200)

        # Verify query parameters are preserved
        self.assertEqual(search_sort_response.context["search_query"], "Alpha")
        self.assertEqual(search_sort_response.context["current_sort"], "name")
        self.assertEqual(search_sort_response.context["current_order"], "asc")

        # Verify sorting is applied
        build_orders = list(search_sort_response.context["buildorder_list"])
        names = [order.name for order in build_orders]
        self.assertEqual(names, sorted(names))

        # Step 3: Test pagination with search and sort
        # Create enough "Alpha" orders to trigger pagination
        for i in range(30):
            BuildOrder.objects.create(
                name=f"Alpha Order {i + 10}",
                blocks={str(self.block_armor.block_id): 1},
            )

        page2_response = self.client.get(
            list_url, {"q": "Alpha", "sort": "name", "order": "asc", "page": 2}
        )
        self.assertEqual(page2_response.status_code, 200)

        # Verify query parameters are preserved in pagination
        self.assertEqual(page2_response.context["search_query"], "Alpha")
        self.assertEqual(page2_response.context["current_sort"], "name")
        self.assertEqual(page2_response.context["current_order"], "asc")
        self.assertTrue(page2_response.context["page_obj"].has_previous())

        # Verify query_string context for pagination links
        query_string = page2_response.context.get("query_string", "")
        self.assertIn("q=Alpha", query_string)
        self.assertIn("sort=name", query_string)
        self.assertIn("order=asc", query_string)

    # ---- Test 18.3: Form validation → error → correction → success ----
    def test_form_validation_error_correction_success_workflow(self):
        """
        Test form validation → error display → correction → success workflow.
        Validates: Requirements 15.7, 15.8
        """
        create_url = reverse("buildorders:create")

        # Step 1: Submit form with invalid data (empty name)
        invalid_data = {
            "name": "",  # Invalid: empty name
            "blocks_json": json.dumps({str(self.block_armor.block_id): 5}),
        }
        error_response = self.client.post(create_url, invalid_data)

        # Verify form validation error
        self.assertEqual(error_response.status_code, 200)  # Re-renders form
        self.assertTemplateUsed(error_response, "buildorders/buildorder_form.html")
        self.assertFormError(
            error_response.context["form"], "name", "This field is required."
        )

        # Verify no build order was created
        self.assertFalse(BuildOrder.objects.filter(name="").exists())

        # Step 2: Submit form with invalid blocks_json (non-existent block ID)
        invalid_blocks_data = {
            "name": "Invalid Blocks Order",
            "blocks_json": json.dumps({"00000000-0000-0000-0000-000000000000": 5}),
        }
        blocks_error_response = self.client.post(create_url, invalid_blocks_data)

        # Verify blocks validation error
        self.assertEqual(blocks_error_response.status_code, 200)
        self.assertIn("form", blocks_error_response.context)
        form_errors = blocks_error_response.context["form"].errors
        self.assertTrue(
            any("does not exist" in str(error) for error in form_errors.values())
        )

        # Verify no build order was created
        self.assertFalse(
            BuildOrder.objects.filter(name="Invalid Blocks Order").exists()
        )

        # Step 3: Submit form with invalid quantity (negative)
        invalid_quantity_data = {
            "name": "Invalid Quantity Order",
            "blocks_json": json.dumps({str(self.block_armor.block_id): -5}),
        }
        quantity_error_response = self.client.post(create_url, invalid_quantity_data)

        # Verify quantity validation error
        self.assertEqual(quantity_error_response.status_code, 200)
        form_errors = quantity_error_response.context["form"].errors
        self.assertTrue(
            any("Invalid quantity" in str(error) for error in form_errors.values())
        )

        # Verify no build order was created
        self.assertFalse(
            BuildOrder.objects.filter(name="Invalid Quantity Order").exists()
        )

        # Step 4: Correct the data and submit successfully
        valid_data = {
            "name": "Corrected Build Order",
            "blocks_json": json.dumps({str(self.block_armor.block_id): 5}),
        }
        success_response = self.client.post(create_url, valid_data, follow=True)

        # Verify successful creation
        self.assertEqual(success_response.status_code, 200)
        self.assertTrue(
            BuildOrder.objects.filter(name="Corrected Build Order").exists()
        )

        # Verify database state after correction
        build_order = BuildOrder.objects.get(name="Corrected Build Order")
        self.assertEqual(build_order.blocks[str(self.block_armor.block_id)], 5)

        # Verify success message
        messages = list(get_messages(success_response.wsgi_request))
        self.assertTrue(any("created successfully" in str(m) for m in messages))

    # ---- Test 18.4: Cache invalidation on update ----
    def test_cache_invalidation_on_update_workflow(self):
        """
        Test cache invalidation when build order is updated.
        Validates: Requirements 14.3, 14.4
        """
        # Step 1: Create a build order
        build_order = BuildOrder.objects.create(
            name="Cache Test Order",
            blocks={str(self.block_armor.block_id): 5},
        )

        # Step 2: View detail to cache calculation
        detail_url = reverse("buildorders:detail", kwargs={"pk": build_order.order_id})
        detail_response1 = self.client.get(detail_url)

        # Verify calculation is cached
        self.assertEqual(detail_response1.status_code, 200)
        summary1 = detail_response1.context["calculation_summary"]
        self.assertEqual(summary1["total_mass"], 750.0)  # 150 kg * 5 blocks

        # Verify cache was set
        cache_key = f"buildorder_calc_{build_order.order_id}"
        cached_data = cache.get(cache_key)
        self.assertIsNotNone(cached_data)
        self.assertEqual(cached_data["total_mass"], 750.0)

        # Step 3: Update the build order
        update_url = reverse("buildorders:update", kwargs={"pk": build_order.order_id})
        update_data = {
            "name": "Cache Test Order",
            "blocks_json": json.dumps({str(self.block_armor.block_id): 10}),
        }
        update_response = self.client.post(update_url, update_data, follow=True)

        # Verify update succeeded
        self.assertEqual(update_response.status_code, 200)
        build_order.refresh_from_db()
        self.assertEqual(build_order.blocks[str(self.block_armor.block_id)], 10)

        # Step 4: View detail again and verify cache was invalidated
        detail_response2 = self.client.get(detail_url)
        self.assertEqual(detail_response2.status_code, 200)
        summary2 = detail_response2.context["calculation_summary"]

        # Verify new calculation reflects updated quantity
        self.assertEqual(summary2["total_mass"], 1500.0)  # 150 kg * 10 blocks
        self.assertNotEqual(summary1["total_mass"], summary2["total_mass"])

        # Verify cache was updated with new values
        cached_data_after = cache.get(cache_key)
        self.assertIsNotNone(cached_data_after)
        self.assertEqual(cached_data_after["total_mass"], 1500.0)

    # ---- Additional integration test: Multiple blocks workflow ----
    def test_create_with_multiple_blocks_and_verify_calculations(self):
        """
        Test creating a build order with multiple blocks and verify all calculations.
        """
        create_url = reverse("buildorders:create")
        create_data = {
            "name": "Multi-Block Order",
            "blocks_json": json.dumps(
                {
                    str(self.block_armor.block_id): 3,
                    str(self.block_computer.block_id): 5,
                }
            ),
        }
        create_response = self.client.post(create_url, create_data, follow=True)

        # Verify creation
        self.assertEqual(create_response.status_code, 200)
        build_order = BuildOrder.objects.get(name="Multi-Block Order")

        # View detail and verify calculations
        detail_url = reverse("buildorders:detail", kwargs={"pk": build_order.order_id})
        detail_response = self.client.get(detail_url)

        summary = detail_response.context["calculation_summary"]

        # Verify total mass: (150 * 3) + (50 * 5) = 450 + 250 = 700 kg
        self.assertEqual(summary["total_mass"], 700.0)

        # Verify required components
        required_components = summary["required_components"]
        # Steel: 25 plates/armor * 3 = 75
        self.assertEqual(required_components[str(self.comp_steel.component_id)], 75)
        # Computer: 10 computers/block * 5 = 50
        self.assertEqual(required_components[str(self.comp_computer.component_id)], 50)

        # Verify required ores
        required_ores = summary["required_ores"]
        # Iron: (7 * 75) + (1 * 50) = 525 + 50 = 575
        self.assertEqual(required_ores[str(self.ore_iron.ore_id)], 575.0)
        # Silicon: 2 * 50 = 100
        self.assertEqual(required_ores[str(self.ore_silicon.ore_id)], 100.0)

        # Verify fabricator times
        fabricator_times = summary["fabricator_times"]
        # Assembler: (3.2 * 75) + (5.0 * 50) = 240 + 250 = 490 seconds
        self.assertEqual(fabricator_times["Assembler"], 490.0)

    # ---- Additional integration test: Update with different blocks ----
    def test_update_changes_block_composition_and_recalculates(self):
        """
        Test updating a build order to change block composition and verify recalculation.
        """
        # Create initial build order with armor blocks
        build_order = BuildOrder.objects.create(
            name="Composition Test Order",
            blocks={str(self.block_armor.block_id): 5},
        )

        # Get initial calculation
        initial_summary = build_order.get_cached_calculation_summary()
        self.assertEqual(initial_summary["total_mass"], 750.0)

        # Update to use computer blocks instead
        update_url = reverse("buildorders:update", kwargs={"pk": build_order.order_id})
        update_data = {
            "name": "Composition Test Order",
            "blocks_json": json.dumps({str(self.block_computer.block_id): 8}),
        }
        update_response = self.client.post(update_url, update_data, follow=True)

        # Verify update
        self.assertEqual(update_response.status_code, 200)
        build_order.refresh_from_db()

        # Get new calculation
        new_summary = build_order.get_cached_calculation_summary()

        # Verify mass changed: 50 kg * 8 = 400 kg
        self.assertEqual(new_summary["total_mass"], 400.0)

        # Verify components changed to computer components
        self.assertNotIn(
            str(self.comp_steel.component_id), new_summary["required_components"]
        )
        self.assertIn(
            str(self.comp_computer.component_id), new_summary["required_components"]
        )
        self.assertEqual(
            new_summary["required_components"][str(self.comp_computer.component_id)], 80
        )

    # ---- Additional integration test: Delete confirmation workflow ----
    def test_delete_confirmation_displays_before_deletion(self):
        """
        Test that delete confirmation page displays before actual deletion.
        """
        # Create a build order
        build_order = BuildOrder.objects.create(
            name="Delete Confirmation Test",
            blocks={str(self.block_armor.block_id): 3},
        )

        delete_url = reverse("buildorders:delete", kwargs={"pk": build_order.order_id})

        # Step 1: GET request shows confirmation page
        get_response = self.client.get(delete_url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(
            get_response, "buildorders/buildorder_confirm_delete.html"
        )
        self.assertContains(get_response, "Delete Confirmation Test")

        # Verify build order still exists
        self.assertTrue(
            BuildOrder.objects.filter(order_id=build_order.order_id).exists()
        )

        # Step 2: POST request performs deletion
        post_response = self.client.post(delete_url, follow=True)
        self.assertEqual(post_response.status_code, 200)

        # Verify build order was deleted
        self.assertFalse(
            BuildOrder.objects.filter(order_id=build_order.order_id).exists()
        )

        # Verify redirect to list view
        self.assertRedirects(post_response, reverse("buildorders:list"))
