#!/usr/bin/env python
"""Integration tests for ores views and templates.

This script performs comprehensive testing of the CRUD workflow:
- Create ore via view
- Read detail page
- Update ore via view
- Read list page
- Delete ore via view
- Verify deletion
- Verify list update

Results are saved to ores/testResults/ directory with timestamp.

Usage:
    uv run python scripts/tests/integration/run_integration_tests.py
"""
import json
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Setup Django
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'se2CalcProject.settings')
django.setup()

from django.conf import settings
from django.test import Client
from django.urls import reverse
from ores.models import Ore

# Add testserver to ALLOWED_HOSTS if not present (for integration testing)
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver']


class IntegrationTestRunner:
    """Run integration tests for ores module with comprehensive error handling."""

    def __init__(self):
        """Initialize test runner."""
        self.client = Client()
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'environment': {
                'django_version': django.get_version(),
                'python_version': sys.version.split()[0],
                'db_engine': settings.DATABASES['default']['ENGINE'],
            },
            'tests': [],
            'summary': {
                'total': 7,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
            },
            'test_ore_id': None,
        }
        self.test_ore = None
        self.test_ore_id = None

    def log_result(self, test_name, passed, message="", error=None):
        """Log test result to internal structure and display output."""
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"  └─ {message}")
        if error:
            print(f"  └─ ERROR: {error}")

        # Track result
        result_entry = {
            'name': test_name,
            'passed': passed,
            'message': message,
            'error': error,
        }
        self.test_results['tests'].append(result_entry)

        # Update summary
        if passed:
            self.test_results['summary']['passed'] += 1
        elif test_name.startswith('[SKIPPED]'):
            self.test_results['summary']['skipped'] += 1
        else:
            self.test_results['summary']['failed'] += 1

    def cleanup(self):
        """Remove test data from previous runs."""
        print("\n[PRE-TEST] Cleaning up test data...")
        try:
            deleted_count, _ = Ore.objects.filter(
                name__startswith='Integration Test Ore'
            ).delete()
            print(f"✓ Removed {deleted_count} test ore(s)\n")
        except Exception as e:
            print(f"⚠ Warning during cleanup: {e}\n")

    def test_create(self):
        """TEST 1: Create ore via view."""
        print("[TEST 1] Creating ore via view...")
        try:
            create_data = {
                'name': 'Integration Test Ore',
                'mass': 999.99,
                'description': 'Created via integration test'
            }
            response = self.client.post(
                reverse('ores:ore_create'),
                create_data
            )

            # Validate status code
            if response.status_code != 302:
                raise AssertionError(
                    f"Expected status 302 (redirect), got {response.status_code}"
                )

            # Verify ore was created in database
            self.test_ore = Ore.objects.get(name='Integration Test Ore')
            self.test_ore_id = self.test_ore.ore_id
            self.test_results['test_ore_id'] = str(self.test_ore_id)

            # Validate created data
            if self.test_ore.mass != 999.99:
                raise AssertionError(
                    f"Expected mass 999.99, got {self.test_ore.mass}"
                )
            if self.test_ore.description != 'Created via integration test':
                raise AssertionError(
                    f"Unexpected description: {self.test_ore.description}"
                )

            self.log_result(
                "Create Ore",
                True,
                f"ID: {self.test_ore_id}, Mass: {self.test_ore.mass}"
            )
        except AssertionError as e:
            self.log_result("Create Ore", False, error=str(e))
        except Exception as e:
            self.log_result(
                "Create Ore",
                False,
                error=f"{type(e).__name__} - {str(e)}"
            )

    def test_read_detail(self):
        """TEST 2: Read ore detail page."""
        print("[TEST 2] Reading ore detail page...")
        if not self.test_ore_id:
            self.log_result("[SKIPPED] Read Detail", False, "Create test failed")
            return

        try:
            response = self.client.get(
                reverse('ores:ore_detail', kwargs={'pk': self.test_ore_id})
            )

            # Validate status code
            if response.status_code != 200:
                raise AssertionError(
                    f"Expected status 200, got {response.status_code}"
                )

            # Validate content
            content = response.content.decode()
            if 'Integration Test Ore' not in content:
                raise AssertionError(
                    "Ore name not found in detail page response"
                )

            self.log_result(
                "Read Detail",
                True,
                f"Status: {response.status_code}, Content verified"
            )
        except AssertionError as e:
            self.log_result("Read Detail", False, error=str(e))
        except Exception as e:
            self.log_result(
                "Read Detail",
                False,
                error=f"{type(e).__name__} - {str(e)}"
            )

    def test_update(self):
        """TEST 3: Update ore via view."""
        print("[TEST 3] Updating ore via view...")
        if not self.test_ore_id:
            self.log_result("[SKIPPED] Update Ore", False, "Create test failed")
            return

        try:
            update_data = {
                'name': 'Integration Test Ore Updated',
                'mass': 1111.11,
                'description': 'Updated via integration test'
            }
            response = self.client.post(
                reverse('ores:ore_update', kwargs={'pk': self.test_ore_id}),
                update_data
            )

            # Validate status code
            if response.status_code != 302:
                raise AssertionError(
                    f"Expected status 302 (redirect), got {response.status_code}"
                )

            # Refresh and validate
            if self.test_ore:
                self.test_ore.refresh_from_db()

                if self.test_ore.name != 'Integration Test Ore Updated':
                    raise AssertionError(f"Name not updated: {self.test_ore.name}")
                if self.test_ore.mass != 1111.11:
                    raise AssertionError(
                        f"Expected mass 1111.11, got {self.test_ore.mass}"
                    )
                if self.test_ore.description != 'Updated via integration test':
                    raise AssertionError(
                        f"Description not updated: {self.test_ore.description}"
                    )

                self.log_result(
                    "Update Ore",
                    True,
                    f"Name: {self.test_ore.name}, Mass: {self.test_ore.mass}"
                )
        except AssertionError as e:
            self.log_result("Update Ore", False, error=str(e))
        except Exception as e:
            self.log_result(
                "Update Ore",
                False,
                error=f"{type(e).__name__} - {str(e)}"
            )

    def test_read_list(self):
        """TEST 4: Read ore list page."""
        print("[TEST 4] Reading ore list page...")
        try:
            response = self.client.get(reverse('ores:ore_list'))

            # Validate status code
            if response.status_code != 200:
                raise AssertionError(
                    f"Expected status 200, got {response.status_code}"
                )

            # Validate content if ore was created
            if self.test_ore:
                content = response.content.decode()
                if 'Integration Test Ore Updated' not in content:
                    raise AssertionError(
                        "Updated ore not found in list view"
                    )

            self.log_result(
                "Read List",
                True,
                f"Status: {response.status_code}, Content verified"
            )
        except AssertionError as e:
            self.log_result("Read List", False, error=str(e))
        except Exception as e:
            self.log_result(
                "Read List",
                False,
                error=f"{type(e).__name__} - {str(e)}"
            )

    def test_delete(self):
        """TEST 5: Delete ore via view."""
        print("[TEST 5] Deleting ore via view...")
        if not self.test_ore_id:
            self.log_result("[SKIPPED] Delete Ore", False, "Create test failed")
            return

        try:
            response = self.client.post(
                reverse('ores:ore_delete', kwargs={'pk': self.test_ore_id})
            )

            # Validate status code
            if response.status_code != 302:
                raise AssertionError(
                    f"Expected status 302 (redirect), got {response.status_code}"
                )

            # Verify deletion
            exists = Ore.objects.filter(ore_id=self.test_ore_id).exists()
            if exists:
                raise AssertionError(
                    "Ore still exists in database after deletion"
                )

            self.log_result(
                "Delete Ore",
                True,
                "Ore successfully removed from database"
            )
        except AssertionError as e:
            self.log_result("Delete Ore", False, error=str(e))
        except Exception as e:
            self.log_result(
                "Delete Ore",
                False,
                error=f"{type(e).__name__} - {str(e)}"
            )

    def test_verify_deletion(self):
        """TEST 6: Verify deletion in database."""
        print("[TEST 6] Verifying deletion in database...")
        if not self.test_ore_id:
            self.log_result(
                "[SKIPPED] Verify Deletion",
                False,
                "Create test failed"
            )
            return

        try:
            exists = Ore.objects.filter(ore_id=self.test_ore_id).exists()

            if exists:
                raise AssertionError("Ore still exists in database")

            self.log_result(
                "Verify Deletion",
                True,
                "No ore record found in database"
            )
        except AssertionError as e:
            self.log_result("Verify Deletion", False, error=str(e))
        except Exception as e:
            self.log_result(
                "Verify Deletion",
                False,
                error=f"{type(e).__name__} - {str(e)}"
            )

    def test_verify_list_updated(self):
        """TEST 7: Verify ore removed from list."""
        print("[TEST 7] Verifying ore removed from list...")
        try:
            response = self.client.get(reverse('ores:ore_list'))

            # Validate status code
            if response.status_code != 200:
                raise AssertionError(
                    f"Expected status 200, got {response.status_code}"
                )

            # Validate test ore no longer in list
            content = response.content.decode()
            if 'Integration Test Ore Updated' in content:
                raise AssertionError("Deleted ore still appears in list view")

            self.log_result(
                "Verify List Updated",
                True,
                "Deleted ore no longer in list"
            )
        except AssertionError as e:
            self.log_result("Verify List Updated", False, error=str(e))
        except Exception as e:
            self.log_result(
                "Verify List Updated",
                False,
                error=f"{type(e).__name__} - {str(e)}"
            )

    def run_all_tests(self):
        """Run all integration tests."""
        print("=" * 70)
        print("CRUD Integration Test - Ores Module")
        print("=" * 70)

        self.cleanup()
        self.test_create()
        self.test_read_detail()
        self.test_update()
        self.test_read_list()
        self.test_delete()
        self.test_verify_deletion()
        self.test_verify_list_updated()

    def print_summary(self):
        """Print test summary."""
        summary = self.test_results['summary']
        passed = summary['passed']
        failed = summary['failed']
        total = summary['total']

        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests:  {total}")
        print(f"Passed:       {passed}")
        print(f"Failed:       {failed}")
        print(f"Pass Rate:    {(passed / total) * 100:.1f}%")

        if self.test_results['tests']:
            failed_tests = [
                t['name'] for t in self.test_results['tests']
                if not t['passed']
            ]
            if failed_tests:
                print("\nFailed Tests:")
                for test in failed_tests:
                    print(f"  ✗ {test}")

        if failed == 0:
            print("\n✓ All integration tests passed successfully!")
        else:
            print(f"\n✗ {failed} test(s) failed. Please review the errors above.")
            print("\nTroubleshooting Tips:")
            print("  1. Ensure the ores app is installed and migrations applied")
            print("  2. Check that URLs are configured in ores/urls.py")
            print("  3. Verify views are correctly implemented in ores/views.py")
            print("  4. Check form validation: add print(response.content)")
            print("  5. Review Django logs for detailed error messages")

        print("=" * 70 + "\n")

    def save_results(self):
        """Save test results to JSON file."""
        # Create testResults directory if it doesn't exist
        results_dir = Path('scripts/tests/testResults')
        results_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = results_dir / f'integration_test_results_{timestamp}.json'

        # Save results
        try:
            with open(results_file, 'w') as f:
                json.dump(self.test_results, f, indent=2, default=str)
            print(f"✓ Test results saved to: {results_file}")
            return results_file
        except Exception as e:
            print(f"✗ Failed to save results: {e}")
            return None

    def run(self):
        """Execute all tests and save results."""
        self.run_all_tests()
        self.print_summary()
        results_file = self.save_results()
        
        # Exit with appropriate code
        failed = self.test_results['summary']['failed']
        sys.exit(0 if failed == 0 else 1)


def main():
    """Main entry point."""
    runner = IntegrationTestRunner()
    runner.run()


if __name__ == '__main__':
    main()
