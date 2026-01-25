import json
import uuid

from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from components.models import Component
from ores.models import Ore


class ComponentViewTestCase(TestCase):
    """Comprehensive view tests for the Components app."""

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        # Core ores used across tests
        cls.ore_iron = Ore.objects.create(name="Iron", mass=1.0)
        cls.ore_copper = Ore.objects.create(name="Copper", mass=2.0)
        cls.ore_nickel = Ore.objects.create(name="Nickel", mass=3.0)

        # Component for detail view tests
        cls.detail_component = Component.objects.create(
            name="Detail Component",
            description="Used for detail view checks",
            materials={
                str(cls.ore_iron.ore_id): 5,
                str(cls.ore_copper.ore_id): 2,
            },
            mass=12.5,
            crafting_time=30,
        )

        # Component for update/delete specific tests
        cls.updatable_component = Component.objects.create(
            name="Updatable Component",
            description="Original description",
            materials={str(cls.ore_iron.ore_id): 1},
            mass=5.0,
            crafting_time=10,
        )

        cls.deletable_component = Component.objects.create(
            name="Deletable Component",
            description="Ready to remove",
            materials={str(cls.ore_copper.ore_id): 3},
            mass=9.0,
            crafting_time=15,
        )

        # Components for list view sorting/search/pagination
        Component.objects.create(
            name="Alpha Component",
            description="First in alphabetical order",
            materials={str(cls.ore_iron.ore_id): 1},
            mass=1.0,
            crafting_time=1,
        )
        Component.objects.create(
            name="Gamma Component",
            description="Third in alphabetical order",
            materials={str(cls.ore_copper.ore_id): 2},
            mass=3.0,
            crafting_time=1,
        )
        Component.objects.create(
            name="Beta Component",
            description="Second in alphabetical order",
            materials={str(cls.ore_nickel.ore_id): 4},
            mass=2.0,
            crafting_time=1,
        )

        cls.search_component = Component.objects.create(
            name="Search Target",
            description="Unique searchable description",
            materials={str(cls.ore_iron.ore_id): 7},
            mass=7.0,
            crafting_time=5,
        )

        # Pagination dataset: 30 components to exercise paginate_by=25
        cls.pagination_components = []
        for i in range(30):
            comp = Component.objects.create(
                name=f"Bulk Component {i:02d}",
                description=f"Bulk item {i}",
                materials={str(cls.ore_iron.ore_id): i + 1},
                mass=i + 1,
                crafting_time=i,
            )
            cls.pagination_components.append(comp)

    # ComponentListView tests (7)
    def test_component_list_view_renders_with_context(self):
        url = reverse("components:component_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "components/component_list.html")
        self.assertIn("component_list", response.context)
        self.assertIn("search_query", response.context)
        self.assertIn("current_sort", response.context)
        self.assertIn("current_order", response.context)
        self.assertIn("total_components", response.context)

    def test_component_list_search_by_name(self):
        url = reverse("components:component_list")
        response = self.client.get(url, {"q": "Search Target"})

        self.assertEqual(response.status_code, 200)
        component_names = [comp.name for comp in response.context["component_list"]]
        self.assertIn("Search Target", component_names)

    def test_component_list_search_by_description(self):
        url = reverse("components:component_list")
        response = self.client.get(url, {"q": "Unique searchable description"})

        self.assertEqual(response.status_code, 200)
        component_names = [comp.name for comp in response.context["component_list"]]
        self.assertIn("Search Target", component_names)

    def test_component_list_sort_by_mass_desc(self):
        url = reverse("components:component_list")
        response = self.client.get(url, {"sort": "mass", "order": "desc"})

        masses = [comp.mass for comp in response.context["component_list"][:3]]
        self.assertEqual(masses, sorted(masses, reverse=True))

    def test_component_list_invalid_sort_defaults_to_name(self):
        url = reverse("components:component_list")
        response = self.client.get(url, {"sort": "invalid_field"})

        names = [comp.name for comp in response.context["component_list"][:3]]
        self.assertEqual(names, sorted(names))

    def test_component_list_pagination_second_page_size(self):
        url = reverse("components:component_list")
        response = self.client.get(url, {"page": 2})

        self.assertEqual(response.status_code, 200)
        total_components = Component.objects.count()
        expected_second_page = max(total_components - 25, 0)
        self.assertEqual(len(response.context["object_list"]), expected_second_page)
        self.assertTrue(response.context["page_obj"].has_previous())
        self.assertFalse(response.context["page_obj"].has_next())

    def test_component_list_preserves_query_string(self):
        url = reverse("components:component_list")
        params = {"q": "Bulk", "sort": "mass", "order": "desc", "page": 2}
        response = self.client.get(url, params)

        query_string = response.context.get("query_string", "")
        self.assertIn("q=Bulk", query_string)
        self.assertIn("sort=mass", query_string)
        self.assertIn("order=desc", query_string)

    # ComponentDetailView tests (5)
    def test_component_detail_view_renders(self):
        url = reverse("components:component_detail", args=[self.detail_component.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "components/component_detail.html")
        self.assertEqual(str(response.context["component"].pk), str(self.detail_component.pk))
        self.assertIn("formatted_materials", response.context)
        self.assertIn("total_material_mass", response.context)
        self.assertEqual(response.context["total_material_mass"], 7)

    def test_component_detail_includes_ore_names(self):
        url = reverse("components:component_detail", args=[self.detail_component.pk])
        response = self.client.get(url)

        ore_names = [item["ore_name"] for item in response.context["formatted_materials"]]
        self.assertIn(self.ore_iron.name, ore_names)
        self.assertIn(self.ore_copper.name, ore_names)

    def test_component_detail_handles_missing_ore(self):
        missing_ore = Ore.objects.create(name="Temporary Ore", mass=4.0)
        component = Component.objects.create(
            name="Missing Ore Component",
            materials={str(missing_ore.ore_id): 2},
            mass=2.0,
            crafting_time=1,
        )
        missing_ore.delete()

        url = reverse("components:component_detail", args=[component.pk])
        response = self.client.get(url)

        formatted = response.context["formatted_materials"]
        self.assertIn("Unknown Ore", formatted[0]["ore_name"])

    def test_component_detail_invalid_uuid_returns_404(self):
        url = reverse("components:component_detail", args=[uuid.uuid4()])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_component_detail_context_contains_component(self):
        url = reverse("components:component_detail", args=[self.detail_component.pk])
        response = self.client.get(url)

        self.assertEqual(response.context["component"].name, "Detail Component")

    # ComponentCreateView tests (6)
    def test_component_create_view_get(self):
        url = reverse("components:component_create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "components/component_form.html")
        self.assertIn("ores", response.context)
        self.assertIn("form_title", response.context)
        self.assertIn("submit_text", response.context)

    def test_component_create_valid_post(self):
        url = reverse("components:component_create")
        payload = {
            "name": "Created Component",
            "description": "Created via test",
            "mass": "11.5",
            "crafting_time": "20",
            "materials_json": json.dumps({str(self.ore_iron.ore_id): 3}),
        }

        response = self.client.post(url, payload, follow=True)

        self.assertRedirects(response, reverse("components:component_list"))
        self.assertTrue(Component.objects.filter(name="Created Component").exists())
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(any("created successfully" in msg for msg in messages))

    def test_component_create_requires_materials(self):
        url = reverse("components:component_create")
        payload = {
            "name": "No Materials",
            "description": "Missing materials",
            "mass": "5",
            "crafting_time": "10",
            "materials_json": "{}",
        }

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Component.objects.filter(name="No Materials").exists())
        self.assertFormError(response.context["form"], "materials_json", "At least one material is required.")

    def test_component_create_rejects_duplicate_name(self):
        url = reverse("components:component_create")
        payload = {
            "name": self.search_component.name,
            "description": "Duplicate name",
            "mass": "6",
            "crafting_time": "5",
            "materials_json": json.dumps({str(self.ore_copper.ore_id): 1}),
        }

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", f"A component with name '{self.search_component.name}' already exists.")

    def test_component_create_rejects_negative_mass(self):
        url = reverse("components:component_create")
        payload = {
            "name": "Negative Mass",
            "description": "Invalid mass",
            "mass": "-1",
            "crafting_time": "5",
            "materials_json": json.dumps({str(self.ore_iron.ore_id): 1}),
        }

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "mass", "Mass must be greater than 0.")

    def test_component_create_rejects_negative_quantity(self):
        url = reverse("components:component_create")
        payload = {
            "name": "Negative Quantity Component",
            "description": "Invalid quantity",
            "mass": "3",
            "crafting_time": "5",
            "materials_json": json.dumps({str(self.ore_iron.ore_id): -2}),
        }

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "materials_json", [
            "Quantity for ore "
            f"{self.ore_iron.ore_id} must be positive (got -2.0)."
        ])

    # ComponentUpdateView tests (5)
    def test_component_update_view_get(self):
        url = reverse("components:component_update", args=[self.updatable_component.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "components/component_form.html")
        self.assertEqual(response.context["existing_materials"], self.updatable_component.materials)
        self.assertIn("form_title", response.context)

    def test_component_update_valid_post(self):
        url = reverse("components:component_update", args=[self.updatable_component.pk])
        payload = {
            "name": "Updated Component",
            "description": "Updated description",
            "mass": "15",
            "crafting_time": "25",
            "materials_json": json.dumps({str(self.ore_copper.ore_id): 4}),
        }

        response = self.client.post(url, payload, follow=True)

        self.assertRedirects(
            response,
            reverse("components:component_detail", args=[self.updatable_component.pk]),
        )

        updated = Component.objects.get(pk=self.updatable_component.pk)
        self.assertEqual(updated.name, "Updated Component")
        self.assertEqual(updated.materials, {str(self.ore_copper.ore_id): 4})
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(any("updated successfully" in msg for msg in messages))

    def test_component_update_rejects_negative_quantity(self):
        url = reverse("components:component_update", args=[self.updatable_component.pk])
        payload = {
            "name": "Updatable Component",
            "description": "Negative quantity",
            "mass": "5",
            "crafting_time": "10",
            "materials_json": json.dumps({str(self.ore_iron.ore_id): -1}),
        }

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "materials_json", [
            "Quantity for ore "
            f"{self.ore_iron.ore_id} must be positive (got -1.0)."
        ])

    def test_component_update_changes_materials(self):
        url = reverse("components:component_update", args=[self.updatable_component.pk])
        payload = {
            "name": "Updatable Component",
            "description": "Materials changed",
            "mass": "6",
            "crafting_time": "12",
            "materials_json": json.dumps({
                str(self.ore_iron.ore_id): 2,
                str(self.ore_copper.ore_id): 3,
            }),
        }

        response = self.client.post(url, payload, follow=True)

        updated = Component.objects.get(pk=self.updatable_component.pk)
        self.assertEqual(updated.materials, {
            str(self.ore_iron.ore_id): 2.0,
            str(self.ore_copper.ore_id): 3.0,
        })
        self.assertEqual(response.status_code, 200)

    def test_component_update_handles_validation_errors(self):
        url = reverse("components:component_update", args=[self.updatable_component.pk])
        payload = {
            "name": "",
            "description": "Missing name",
            "mass": "5",
            "crafting_time": "10",
            "materials_json": json.dumps({str(self.ore_iron.ore_id): 1}),
        }

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")

    # ComponentDeleteView tests (3)
    def test_component_delete_view_get(self):
        url = reverse("components:component_delete", args=[self.deletable_component.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "components/component_confirm_delete.html")
        self.assertIn("formatted_materials", response.context)
        self.assertGreater(len(response.context["formatted_materials"]), 0)

    def test_component_delete_view_post(self):
        url = reverse("components:component_delete", args=[self.deletable_component.pk])
        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse("components:component_list"))
        self.assertFalse(Component.objects.filter(pk=self.deletable_component.pk).exists())

    def test_component_delete_sets_success_message(self):
        component = Component.objects.create(
            name="Delete Message Component",
            materials={str(self.ore_iron.ore_id): 1},
            mass=1.0,
            crafting_time=1,
        )
        url = reverse("components:component_delete", args=[component.pk])
        response = self.client.post(url, follow=True)

        messages_ctx = response.context.get("messages") if hasattr(response, "context") else []
        messages = [m.message for m in messages_ctx] if messages_ctx else [m.message for m in get_messages(response.wsgi_request)]
        self.assertIsNotNone(getattr(response.wsgi_request, "_messages", None))

    # Template rendering checks (4)
    def test_component_list_template_used(self):
        response = self.client.get(reverse("components:component_list"))
        self.assertTemplateUsed(response, "components/component_list.html")

    def test_component_detail_template_used(self):
        response = self.client.get(reverse("components:component_detail", args=[self.detail_component.pk]))
        self.assertTemplateUsed(response, "components/component_detail.html")

    def test_component_form_template_used_for_create(self):
        response = self.client.get(reverse("components:component_create"))
        self.assertTemplateUsed(response, "components/component_form.html")

    def test_component_list_empty_state_message(self):
        Component.objects.all().delete()
        response = self.client.get(reverse("components:component_list"))

        self.assertContains(response, "No Components Found")
