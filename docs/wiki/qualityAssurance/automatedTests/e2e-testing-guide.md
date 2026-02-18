# E2E Testing Guide

**Last Updated:** 2026-02-05  
**Status:** Active  
**Audience:** Developers, QA Engineers

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Architecture Overview](#architecture-overview)
4. [Writing Tests](#writing-tests)
5. [Running Tests](#running-tests)
6. [Debugging Tests](#debugging-tests)
7. [Best Practices](#best-practices)
8. [CI/CD Integration](#cicd-integration)
9. [Troubleshooting](#troubleshooting)

## Introduction

The Space Engineers 2 Calculator project uses a dual-framework approach for end-to-end (E2E) testing:

- **Selenium WebDriver:** Industry-standard browser automation for Chrome, Firefox, and Edge
- **Playwright:** Modern browser automation for Chromium, Firefox, and WebKit

Both frameworks test the same functionality to ensure comprehensive coverage and provide redundancy in test validation.

### Why E2E Testing?

E2E tests verify that the application works correctly from a user's perspective by:
- Testing complete user workflows through the UI
- Validating interactions between frontend and backend
- Ensuring cross-browser compatibility
- Catching integration issues that unit tests miss

## Quick Start

### Prerequisites

```bash
# Ensure you have Python 3.13+ and UV installed
uv --version

# Install project dependencies
uv sync

# Install Playwright browsers
uv run playwright install
```

### Run Your First Test

```bash
# Run all E2E tests
uv run pytest tests/e2e/

# Run only Selenium tests
uv run pytest tests/e2e/selenium_tests/ -m selenium

# Run only Playwright tests
uv run pytest tests/e2e/playwright_tests/ -m playwright

# Run with headed browser (see what's happening)
uv run pytest tests/e2e/ --headed

# Run specific test file
uv run pytest tests/e2e/selenium_tests/test_ores_crud.py
```

## Architecture Overview

### Directory Structure

```
tests/e2e/
├── __init__.py
├── conftest.py                 # Shared pytest fixtures
├── config.py                   # Configuration management
├── base/
│   ├── selenium_base.py        # Base Selenium test class
│   └── playwright_base.py      # Base Playwright test class
├── page_objects/
│   ├── selenium/               # Selenium page objects
│   │   ├── navigation.py
│   │   ├── ore_pages.py
│   │   ├── component_pages.py
│   │   └── block_pages.py
│   └── playwright/             # Playwright page objects
│       ├── navigation.py
│       ├── ore_pages.py
│       ├── component_pages.py
│       └── block_pages.py
├── factories/
│   ├── ore_factory.py          # Test data factories
│   ├── component_factory.py
│   └── block_factory.py
├── utils/
│   ├── wait_helpers.py         # Wait and retry utilities
│   ├── screenshot.py           # Screenshot capture
│   └── db_helpers.py           # Database utilities
├── selenium_tests/             # Selenium E2E tests
│   ├── test_ores_crud.py
│   ├── test_components_crud.py
│   ├── test_blocks_crud.py
│   └── test_navigation.py
└── playwright_tests/           # Playwright E2E tests
    ├── test_ores_crud.py
    ├── test_components_crud.py
    ├── test_blocks_crud.py
    └── test_navigation.py
```

### Key Concepts

**Page Object Model (POM):**
- Encapsulates page elements and interactions
- Makes tests more maintainable
- Reduces code duplication
- Isolates UI changes to page object classes

**Test Fixtures:**
- Reusable setup and teardown logic
- Browser initialization
- Database setup and cleanup
- Test data creation

**Factory Pattern:**
- Generates realistic test data
- Handles model relationships
- Ensures data validity

## Writing Tests

### Selenium Test Example

```python
import pytest
from tests.e2e.base.selenium_base import SeleniumBaseTest
from tests.e2e.page_objects.selenium.ore_pages import OreListPage, OreFormPage
from tests.e2e.factories.ore_factory import OreFactory


@pytest.mark.selenium
class TestOresCRUD(SeleniumBaseTest):
    """E2E tests for Ore CRUD operations using Selenium."""
    
    def test_create_ore(self, db_setup):
        """Test creating a new ore through the UI."""
        # Navigate to ore list page
        self.navigate_to('/ores/')
        list_page = OreListPage(self.driver)
        
        # Click create button
        list_page.click_create()
        
        # Fill out form
        form_page = OreFormPage(self.driver)
        form_page.fill_name("Iron Ore")
        form_page.fill_description("Basic ore for steel production")
        form_page.submit()
        
        # Verify ore appears in list
        assert list_page.is_ore_present("Iron Ore")
        
        # Verify ore exists in database
        from app.ores.models import Ore
        assert Ore.objects.filter(name="Iron Ore").exists()
    
    def test_update_ore(self, db_setup):
        """Test updating an existing ore."""
        # Create test ore using factory
        ore = OreFactory.create_ore(name="Test Ore")
        
        # Navigate to ore list
        self.navigate_to('/ores/')
        list_page = OreListPage(self.driver)
        
        # Click edit button
        list_page.click_edit("Test Ore")
        
        # Update the name
        form_page = OreFormPage(self.driver)
        form_page.fill_name("Updated Ore")
        form_page.submit()
        
        # Verify update
        assert list_page.is_ore_present("Updated Ore")
        assert not list_page.is_ore_present("Test Ore")
```

### Playwright Test Example

```python
import pytest
from tests.e2e.base.playwright_base import PlaywrightBaseTest
from tests.e2e.page_objects.playwright.ore_pages import OreListPage, OreFormPage
from tests.e2e.factories.ore_factory import OreFactory


@pytest.mark.playwright
class TestOresCRUD(PlaywrightBaseTest):
    """E2E tests for Ore CRUD operations using Playwright."""
    
    def test_create_ore(self, db_setup):
        """Test creating a new ore through the UI."""
        # Navigate to ore list page
        self.navigate_to('/ores/')
        list_page = OreListPage(self.page)
        
        # Click create button
        list_page.click_create()
        
        # Fill out form
        form_page = OreFormPage(self.page)
        form_page.fill_name("Iron Ore")
        form_page.fill_description("Basic ore for steel production")
        form_page.submit()
        
        # Verify ore appears in list
        assert list_page.is_ore_present("Iron Ore")
        
        # Verify ore exists in database
        from app.ores.models import Ore
        assert Ore.objects.filter(name="Iron Ore").exists()
```

### Creating Page Objects

**Selenium Page Object:**

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OreListPage:
    """Page object for ore list view."""
    
    # Locators
    CREATE_BUTTON = (By.ID, "create-ore-btn")
    SEARCH_INPUT = (By.ID, "search-input")
    TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click_create(self):
        """Click the create new ore button."""
        button = self.wait.until(
            EC.element_to_be_clickable(self.CREATE_BUTTON)
        )
        button.click()
    
    def is_ore_present(self, ore_name: str) -> bool:
        """Check if ore is present in the list."""
        try:
            locator = (By.XPATH, f"//td[text()='{ore_name}']")
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except:
            return False
```

**Playwright Page Object:**

```python
from playwright.sync_api import Page, Locator


class OreListPage:
    """Page object for ore list view."""
    
    def __init__(self, page: Page):
        self.page = page
    
    @property
    def create_button(self) -> Locator:
        return self.page.locator("#create-ore-btn")
    
    @property
    def search_input(self) -> Locator:
        return self.page.locator("#search-input")
    
    def click_create(self):
        """Click the create new ore button."""
        self.create_button.click()
    
    def is_ore_present(self, ore_name: str) -> bool:
        """Check if ore is present in the list."""
        return self.page.locator(f"text={ore_name}").is_visible()
```

## Running Tests

### Basic Commands

```bash
# Run all E2E tests
uv run pytest tests/e2e/

# Run with verbose output
uv run pytest tests/e2e/ -v

# Run specific test class
uv run pytest tests/e2e/selenium_tests/test_ores_crud.py::TestOresCRUD

# Run specific test method
uv run pytest tests/e2e/selenium_tests/test_ores_crud.py::TestOresCRUD::test_create_ore
```

### Browser Selection

```bash
# Run with Chrome (default)
uv run pytest tests/e2e/ --browser=chrome

# Run with Firefox
uv run pytest tests/e2e/ --browser=firefox

# Run with Edge
uv run pytest tests/e2e/ --browser=edge

# Run with Chromium (Playwright)
uv run pytest tests/e2e/playwright_tests/ --browser=chromium

# Run with WebKit (Playwright)
uv run pytest tests/e2e/playwright_tests/ --browser=webkit
```

### Execution Modes

```bash
# Headless mode (default in CI)
uv run pytest tests/e2e/ --headless

# Headed mode (see browser)
uv run pytest tests/e2e/ --headed

# Slow motion (for debugging)
uv run pytest tests/e2e/ --headed --slow-mo=1000
```

### Parallel Execution

```bash
# Run with 4 parallel workers
uv run pytest tests/e2e/ -n 4

# Run with auto-detected CPU count
uv run pytest tests/e2e/ -n auto
```

### Filtering Tests

```bash
# Run only Selenium tests
uv run pytest tests/e2e/ -m selenium

# Run only Playwright tests
uv run pytest tests/e2e/ -m playwright

# Run only property tests
uv run pytest tests/e2e/ -m property_test

# Run tests matching pattern
uv run pytest tests/e2e/ -k "create"
```

### Generating Reports

```bash
# Generate HTML report
uv run pytest tests/e2e/ --html=reports/e2e-report.html --self-contained-html

# Generate coverage report
uv run pytest tests/e2e/ --cov=tests/e2e --cov-report=html
```

## Debugging Tests

### Visual Debugging

```bash
# Run in headed mode with slow motion
uv run pytest tests/e2e/ --headed --slow-mo=1000

# Run single test in headed mode
uv run pytest tests/e2e/selenium_tests/test_ores_crud.py::TestOresCRUD::test_create_ore --headed
```

### Screenshots

Screenshots are automatically captured on test failures and saved to `tests/e2e/screenshots/`.

To manually capture screenshots in tests:

```python
# Selenium
self.take_screenshot("my_screenshot")

# Playwright
self.take_screenshot("my_screenshot")
```

### Debugging with pdb

```python
def test_create_ore(self, db_setup):
    self.navigate_to('/ores/')
    
    # Add breakpoint
    import pdb; pdb.set_trace()
    
    list_page = OreListPage(self.driver)
    list_page.click_create()
```

### Playwright Inspector

```bash
# Run with Playwright inspector
PWDEBUG=1 uv run pytest tests/e2e/playwright_tests/test_ores_crud.py
```

### Common Issues

**Element not found:**
- Check if element locator is correct
- Verify element is visible on page
- Increase wait timeout if needed
- Check for dynamic content loading

**Stale element reference:**
- Re-locate element after page updates
- Use wait helpers with retry logic

**Test timeout:**
- Increase timeout in config
- Check for slow page loads
- Verify application is running

## Best Practices

### Test Design

1. **One assertion per test:** Focus each test on a single behavior
2. **Use factories:** Generate test data with factories, not fixtures
3. **Clean up:** Ensure tests clean up after themselves
4. **Independent tests:** Tests should not depend on each other
5. **Descriptive names:** Use clear, descriptive test names

### Page Objects

1. **Encapsulate locators:** Keep all locators in page object classes
2. **Return page objects:** Methods that navigate should return new page objects
3. **No assertions:** Page objects should not contain assertions
4. **Reusable methods:** Create reusable methods for common actions

### Wait Strategies

1. **Explicit waits:** Always use explicit waits, never sleep()
2. **Wait for conditions:** Wait for specific conditions (visible, clickable)
3. **Reasonable timeouts:** Use appropriate timeouts (default 10 seconds)
4. **Retry logic:** Implement retry for operations that may fail temporarily

### Test Data

1. **Use factories:** Generate test data with factory utilities
2. **Minimal data:** Create only the data needed for the test
3. **Realistic data:** Use realistic values that match production
4. **Clean up:** Ensure test data is cleaned up after tests

## CI/CD Integration

### GitHub Actions

E2E tests run automatically in CI/CD on:
- Pull requests
- Pushes to main branch
- Scheduled nightly runs

Configuration: `.github/workflows/e2e-tests.yml`

### Running Locally Like CI

```bash
# Set CI environment variable
export CI=true

# Run tests in headless mode
uv run pytest tests/e2e/ --headless -n 4
```

### Viewing CI Artifacts

When tests fail in CI:
1. Go to GitHub Actions run
2. Click on failed job
3. Download "e2e-test-artifacts" artifact
4. Extract and view screenshots

## Troubleshooting

### Browser Driver Issues

**Problem:** Browser driver not found

**Solution:**
```bash
# For Playwright
uv run playwright install

# For Selenium, ensure browser is installed
# Chrome: https://www.google.com/chrome/
# Firefox: https://www.mozilla.org/firefox/
```

### Application Not Running

**Problem:** Tests fail because application is not accessible

**Solution:**
```bash
# Start Django development server
uv run python app/manage.py runserver

# Or start Docker stack
docker compose up -d
```

### Database Issues

**Problem:** Tests fail with database errors

**Solution:**
```bash
# Run migrations
uv run python app/manage.py migrate

# Clear test database
uv run python app/manage.py flush --no-input
```

### Flaky Tests

**Problem:** Tests pass sometimes and fail other times

**Solutions:**
1. Increase wait timeouts
2. Use more specific locators
3. Wait for specific conditions, not just presence
4. Check for race conditions
5. Ensure proper test isolation

### Performance Issues

**Problem:** Tests run too slowly

**Solutions:**
1. Run tests in parallel: `-n 4`
2. Use headless mode
3. Optimize test data creation
4. Skip unnecessary waits
5. Use Playwright (generally faster)

## Additional Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Page Object Model Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)

## Support

For questions or issues:
1. Check this guide and troubleshooting section
2. Review test examples in `tests/e2e/`
3. Check spec documentation in `.kiro/specs/e2e-testing-infrastructure/`
4. Ask in team chat or create an issue

---

**Maintained by:** QA Team  
**Last Review:** 2026-02-05
