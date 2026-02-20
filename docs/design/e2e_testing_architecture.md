# E2E Testing Architecture

**Document Version:** 1.0  
**Last Updated:** 2026-02-05  
**Status:** Active

## Overview

This document describes the architecture and design decisions for the end-to-end (E2E) testing infrastructure in the Space Engineers 2 Calculator project. The infrastructure supports both Selenium WebDriver and Playwright frameworks to provide comprehensive browser automation testing capabilities.

## Design Goals

1. **Maintainability:** Tests should be easy to update when UI changes
2. **Reliability:** Tests should be resilient to timing issues and flakiness
3. **Scalability:** Infrastructure should support growing test suite
4. **Flexibility:** Support multiple browsers and execution environments
5. **Developer Experience:** Easy to write, run, and debug tests

## Architectural Decisions

### 1. Dual Framework Approach

**Decision:** Support both Selenium and Playwright

**Rationale:**
- **Selenium:** Industry standard, mature ecosystem, familiar to most developers
- **Playwright:** Modern features, better reliability, auto-waiting mechanisms
- **Redundancy:** Both frameworks testing same functionality provides validation
- **Flexibility:** Teams can choose framework based on needs

**Trade-offs:**
- More maintenance (two sets of page objects)
- Larger dependency footprint
- Benefit: Comprehensive coverage and framework flexibility

### 2. Page Object Model Pattern

**Decision:** Use Page Object Model (POM) for all UI interactions

**Rationale:**
- Encapsulates page structure and behavior
- Reduces code duplication
- Isolates UI changes to page object classes
- Makes tests more readable and maintainable

**Implementation:**
```
page_objects/
├── base_page.py           # Abstract base class
├── selenium/              # Selenium implementations
│   ├── ore_pages.py
│   ├── component_pages.py
│   └── block_pages.py
└── playwright/            # Playwright implementations
    ├── ore_pages.py
    ├── component_pages.py
    └── block_pages.py
```

**Example:**
```python
# Instead of this in tests:
driver.find_element(By.ID, "create-btn").click()
driver.find_element(By.ID, "name").send_keys("Iron Ore")

# We do this:
list_page = OreListPage(driver)
list_page.click_create()
form_page = OreFormPage(driver)
form_page.fill_name("Iron Ore")
```

### 3. Factory Pattern for Test Data

**Decision:** Use factory utilities to generate test data

**Rationale:**
- Consistent test data generation
- Handles model relationships correctly
- Reduces boilerplate in tests
- Easy to create realistic scenarios

**Implementation:**
```python
class OreFactory:
    @staticmethod
    def create_ore(name=None, description=None, **kwargs):
        """Create a single ore with optional overrides."""
        if name is None:
            name = f"Test Ore {uuid.uuid4().hex[:8]}"
        if description is None:
            description = f"Description for {name}"
        
        return Ore.objects.create(
            name=name,
            description=description,
            **kwargs
        )
```

### 4. Configuration Management

**Decision:** Centralized configuration with multiple sources

**Configuration Priority:**
1. Environment variables (highest)
2. Command-line arguments
3. Default values (lowest)

**Rationale:**
- Flexible configuration for different environments
- Easy to override for specific test runs
- CI/CD can set environment variables
- Developers can use CLI for quick changes

**Implementation:**
```python
class E2EConfig:
    @property
    def base_url(self) -> str:
        return os.getenv('E2E_BASE_URL', 'http://localhost:8000')
    
    @property
    def headless(self) -> bool:
        # Auto-detect CI environment
        if os.getenv('CI'):
            return True
        return os.getenv('E2E_HEADLESS', 'false').lower() == 'true'
```

### 5. Test Isolation Strategy

**Decision:** Use database transactions with rollback

**Rationale:**
- Each test gets clean database state
- Tests don't interfere with each other
- Supports parallel execution
- Fast cleanup (rollback vs. delete)

**Implementation:**
```python
@pytest.fixture(scope="function")
def db_setup(transactional_db):
    """Provide clean database for each test."""
    yield
    # Automatic rollback by pytest-django
```

### 6. Wait Strategy

**Decision:** Explicit waits with retry logic

**Rationale:**
- More reliable than implicit waits or sleep()
- Waits only as long as necessary
- Clear timeout errors
- Handles dynamic content

**Selenium Implementation:**
```python
def wait_for_element(self, locator, timeout=10):
    return WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located(locator)
    )
```

**Playwright Implementation:**
```python
# Playwright has built-in auto-waiting
def click_button(self):
    self.page.locator("#button").click()  # Automatically waits
```

### 7. Screenshot and Artifact Capture

**Decision:** Automatic screenshot capture on test failure

**Rationale:**
- Essential for debugging CI failures
- No need to reproduce failures locally
- Organized by test name and timestamp

**Implementation:**
```python
def teardown_method(self, method):
    """Capture screenshot on failure and quit driver."""
    if hasattr(self, '_test_failed') and self._test_failed:
        self.take_screenshot(f"{method.__name__}_failure")
    self.driver.quit()
```

### 8. Parallel Execution

**Decision:** Support parallel test execution with pytest-xdist

**Rationale:**
- Reduces total test execution time
- Better resource utilization
- Scales with available CPU cores

**Considerations:**
- Each worker needs separate browser instance
- Database isolation must be maintained
- Worker ID included in logs for debugging

## Component Architecture

### Base Test Classes

**Purpose:** Provide common setup, teardown, and utilities

**Selenium Base:**
```python
class SeleniumBaseTest:
    driver: WebDriver
    config: E2EConfig
    wait: WebDriverWait
    
    def setup_method(self, method):
        # Initialize WebDriver
        # Navigate to base URL
    
    def teardown_method(self, method):
        # Capture screenshot on failure
        # Quit driver
    
    def navigate_to(self, path: str):
        # Navigate to path
    
    def wait_for_element(self, locator: tuple):
        # Wait for element
```

**Playwright Base:**
```python
class PlaywrightBaseTest:
    browser: Browser
    context: BrowserContext
    page: Page
    config: E2EConfig
    
    def setup_method(self, method):
        # Initialize browser, context, page
    
    def teardown_method(self, method):
        # Capture screenshot on failure
        # Close browser
    
    def navigate_to(self, path: str):
        # Navigate to path
```

### Page Objects

**Structure:**
- One class per page or major page section
- Locators defined as class attributes or properties
- Methods for user actions (click, fill, submit)
- No assertions in page objects

**Selenium Example:**
```python
class OreListPage:
    CREATE_BUTTON = (By.ID, "create-ore-btn")
    SEARCH_INPUT = (By.ID, "search-input")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click_create(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.CREATE_BUTTON)
        )
        button.click()
```

**Playwright Example:**
```python
class OreListPage:
    def __init__(self, page: Page):
        self.page = page
    
    @property
    def create_button(self):
        return self.page.locator("#create-ore-btn")
    
    def click_create(self):
        self.create_button.click()
```

### Utilities

**Wait Helpers:**
- `wait_for_element_visible()`
- `wait_for_element_clickable()`
- `wait_for_text_present()`
- `wait_for_url_change()`
- `retry_on_stale_element()`

**Screenshot Utilities:**
- `capture_selenium()`
- `capture_playwright()`
- `capture_full_page()`
- `organize_by_test_run()`

**Database Helpers:**
- `clear_all_data()`
- `load_fixtures()`
- `verify_object_exists()`
- `get_object_count()`

## Test Organization

### Directory Structure

```
tests/e2e/
├── base/                  # Base test classes
├── page_objects/          # Page object implementations
│   ├── selenium/
│   └── playwright/
├── factories/             # Test data factories
├── utils/                 # Utility modules
├── selenium_tests/        # Selenium E2E tests
├── playwright_tests/      # Playwright E2E tests
├── unit/                  # Infrastructure unit tests
└── properties/            # Property-based tests
```

### Test Naming Convention

- Test files: `test_<feature>_<operation>.py`
- Test classes: `Test<Feature><Operation>`
- Test methods: `test_<specific_behavior>`

**Examples:**
- `test_ores_crud.py::TestOresCRUD::test_create_ore`
- `test_navigation.py::TestNavigation::test_main_menu_links`

## Browser Support Matrix

| Framework | Chrome | Firefox | Edge | Safari/WebKit |
|-----------|--------|---------|------|---------------|
| Selenium  | ✅     | ✅      | ✅   | ❌            |
| Playwright| ✅     | ✅      | ❌   | ✅            |

**Notes:**
- Selenium uses WebDriver for each browser
- Playwright uses built-in browser binaries
- WebKit support only via Playwright
- Edge support only via Selenium

## Execution Environments

### Local Development

**Characteristics:**
- Headed or headless mode
- Single browser
- Fast feedback loop
- Interactive debugging

**Configuration:**
```bash
E2E_BASE_URL=http://localhost:8000
E2E_HEADLESS=false
E2E_BROWSER=chrome
```

### CI/CD (GitHub Actions)

**Characteristics:**
- Headless mode only
- Multiple browsers in parallel
- Artifact upload on failure
- Build failure on test failure

**Configuration:**
```yaml
env:
  E2E_BASE_URL: http://localhost:8000
  E2E_HEADLESS: true
  CI: true
```

### Docker

**Characteristics:**
- Isolated environment
- Consistent with production
- Headless mode
- Health checks before tests

**Configuration:**
```yaml
services:
  e2e-tests:
    build: .
    environment:
      - E2E_BASE_URL=http://web:8000
      - E2E_HEADLESS=true
```

## Performance Considerations

### Test Execution Time

**Targets:**
- Single test: < 10 seconds
- Full suite (sequential): < 15 minutes
- Full suite (parallel, 4 workers): < 5 minutes

**Optimization Strategies:**
1. Parallel execution with pytest-xdist
2. Headless mode (faster than headed)
3. Minimal test data creation
4. Efficient wait strategies
5. Playwright (generally faster than Selenium)

### Resource Usage

**Browser Instances:**
- Each worker needs separate browser
- Memory: ~200MB per browser instance
- CPU: Varies by test complexity

**Database:**
- Separate database per worker
- Transaction-based isolation
- Minimal disk I/O

## Error Handling

### Browser Initialization Errors

**Strategy:** Skip tests for unavailable browsers

**Implementation:**
```python
try:
    driver = webdriver.Chrome()
except WebDriverException as e:
    pytest.skip(f"Chrome not available: {e}")
```

### Element Not Found Errors

**Strategy:** Explicit waits with clear error messages

**Implementation:**
```python
try:
    element = self.wait_for_element(locator, timeout=10)
except TimeoutException:
    self.take_screenshot("element_not_found")
    raise AssertionError(
        f"Element {locator} not found after {timeout}s"
    )
```

### Stale Element Errors

**Strategy:** Automatic retry with re-location

**Implementation:**
```python
@retry_on_stale_element(max_attempts=3)
def click_element(self, locator):
    element = self.driver.find_element(*locator)
    element.click()
```

## Security Considerations

1. **No Sensitive Data:** Test data should not contain real user information
2. **Isolated Environment:** Tests run in isolated test database
3. **Clean Up:** All test data cleaned up after execution
4. **Screenshot Sanitization:** Ensure screenshots don't capture sensitive data

## Future Enhancements

1. **Visual Regression Testing:** Compare screenshots for UI changes
2. **Performance Testing:** Measure page load times and interactions
3. **Accessibility Testing:** Automated accessibility checks
4. **Mobile Testing:** Support for mobile browsers
5. **API Mocking:** Mock external API calls for faster tests

## References

- [Selenium Best Practices](https://www.selenium.dev/documentation/test_practices/)
- [Playwright Best Practices](https://playwright.dev/python/docs/best-practices)
- [Page Object Model](https://martinfowler.com/bliki/PageObject.html)
- [pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)

---

**Document Owner:** QA Team  
**Review Cycle:** Quarterly  
**Next Review:** 2026-05-05
