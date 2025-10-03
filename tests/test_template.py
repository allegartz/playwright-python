"""
Template for creating new tests.
Copy this file and modify for your specific test needs.
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.form_page import FormPage


# ============================================================================
# BASIC TEST EXAMPLES
# ============================================================================

@pytest.mark.smoke
def test_basic_navigation(page: Page):
    """
    Template: Basic navigation test.
    Replace URL and assertions with your needs.
    """
    # Navigate to page
    page.goto("https://example.com")
    
    # Wait for page to load
    page.wait_for_load_state("networkidle")
    
    # Assert page loaded correctly
    assert "Example" in page.title()


@pytest.mark.ui
def test_element_visibility(page: Page):
    """
    Template: Test element visibility.
    """
    page.goto("https://example.com")
    
    # Check if element is visible
    logo = page.locator(".logo")
    expect(logo).to_be_visible()
    
    # Check multiple elements
    navigation = page.locator("nav")
    expect(navigation).to_be_visible()


def test_click_and_navigate(page: Page):
    """
    Template: Click element and verify navigation.
    """
    page.goto("https://example.com")
    
    # Click a link
    page.click("a[href='/about']")
    
    # Wait for navigation
    page.wait_for_load_state("networkidle")
    
    # Verify new URL
    assert "/about" in page.url


# ============================================================================
# PAGE OBJECT EXAMPLES
# ============================================================================

@pytest.mark.login
def test_login_with_page_object(page: Page):
    """
    Template: Login test using Page Object.
    """
    login_page = LoginPage(page)
    
    # Navigate to login page
    login_page.navigate("https://example.com/login")
    
    # Perform login
    login_page.login("user@example.com", "password123")
    
    # Verify login success
    assert login_page.is_logged_in()


@pytest.mark.form
def test_form_submission(page: Page, sample_form_data: dict):
    """
    Template: Form submission using Page Object and fixture.
    """
    form_page = FormPage(page)
    
    # Navigate to form
    form_page.navigate("https://example.com/form")
    
    # Fill form
    form_page.fill_complete_form(sample_form_data)
    
    # Submit
    form_page.submit_form()
    
    # Verify success
    success_msg = form_page.get_success_message()
    assert success_msg or page.url != "https://example.com/form"


# ============================================================================
# TEST CLASS EXAMPLES
# ============================================================================

@pytest.mark.ui
class TestHomepage:
    """
    Template: Test class for grouping related tests.
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup before each test in this class."""
        self.base_url = "https://example.com"
        self.page = page
        page.goto(self.base_url)
    
    def test_title(self, page: Page):
        """Test page title."""
        assert "Example" in page.title()
    
    def test_logo_visible(self, page: Page):
        """Test logo is visible."""
        expect(page.locator(".logo")).to_be_visible()
    
    def test_navigation_menu(self, page: Page):
        """Test navigation menu."""
        nav_items = page.locator("nav a")
        assert nav_items.count() > 0


# ============================================================================
# PARAMETRIZED TEST EXAMPLES
# ============================================================================

@pytest.mark.parametrize("username,password,expected", [
    ("valid@example.com", "ValidPass123", True),
    ("invalid@example.com", "WrongPass", False),
    ("", "password", False),
    ("user@example.com", "", False),
])
def test_login_scenarios(page: Page, username, password, expected):
    """
    Template: Parametrized test for multiple scenarios.
    """
    login_page = LoginPage(page)
    login_page.navigate("https://example.com/login")
    
    login_page.login(username, password)
    page.wait_for_load_state("networkidle")
    
    if expected:
        assert login_page.is_logged_in()
    else:
        assert not login_page.is_logged_in()


@pytest.mark.parametrize("viewport", [
    {"width": 375, "height": 667},   # Mobile
    {"width": 768, "height": 1024},  # Tablet
    {"width": 1920, "height": 1080}, # Desktop
])
def test_responsive_design(page: Page, viewport):
    """
    Template: Test responsive design on different viewports.
    """
    page.set_viewport_size(viewport)
    page.goto("https://example.com")
    page.wait_for_load_state("networkidle")
    
    # Add assertions based on viewport
    assert page.url == "https://example.com"


# ============================================================================
# USER FLOW EXAMPLES
# ============================================================================

@pytest.mark.flow
def test_complete_user_flow(page: Page):
    """
    Template: Complete user flow test.
    """
    # Step 1: Navigate to homepage
    page.goto("https://example.com")
    page.wait_for_load_state("networkidle")
    
    # Step 2: Click on a link
    page.click("a:has-text('Login')")
    page.wait_for_load_state("networkidle")
    
    # Step 3: Fill login form
    page.fill("#email", "user@example.com")
    page.fill("#password", "password123")
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    
    # Step 4: Verify login and navigation
    assert "/dashboard" in page.url or "dashboard" in page.url.lower()
    
    # Step 5: Perform action on dashboard
    # Add your actions here
    
    # Step 6: Logout
    page.click("#logout")
    page.wait_for_load_state("networkidle")
    
    # Verify logout
    assert "/login" in page.url or "login" in page.url.lower()


# ============================================================================
# ADVANCED EXAMPLES
# ============================================================================

def test_with_screenshot_on_failure(page: Page):
    """
    Template: Test with screenshot on failure.
    """
    try:
        page.goto("https://example.com")
        
        # Your test assertions
        assert page.locator(".expected-element").is_visible()
        
    except Exception as e:
        # Take screenshot on failure
        page.screenshot(path="tests/test_data/failure_screenshot.png")
        raise e


def test_wait_for_specific_element(page: Page):
    """
    Template: Test with explicit waits.
    """
    page.goto("https://example.com")
    
    # Wait for specific element
    page.wait_for_selector(".dynamic-content", timeout=10000)
    
    # Verify element appeared
    content = page.locator(".dynamic-content")
    expect(content).to_be_visible()


def test_handle_dialog(page: Page):
    """
    Template: Test handling dialogs/alerts.
    """
    page.goto("https://example.com")
    
    # Set up dialog handler before triggering it
    page.on("dialog", lambda dialog: dialog.accept())
    
    # Trigger dialog
    page.click("button.show-alert")
    
    # Continue with test


def test_network_request_interception(page: Page):
    """
    Template: Test with network request monitoring.
    """
    # Monitor network requests
    requests = []
    page.on("request", lambda request: requests.append(request.url))
    
    page.goto("https://example.com")
    
    # Verify specific request was made
    assert any("api/data" in url for url in requests)


# ============================================================================
# CUSTOM FIXTURE EXAMPLES
# ============================================================================

@pytest.fixture
def custom_test_data():
    """Custom fixture for test data."""
    return {
        "field1": "value1",
        "field2": "value2",
        "field3": "value3"
    }


def test_with_custom_fixture(page: Page, custom_test_data):
    """
    Template: Test using custom fixture.
    """
    page.goto("https://example.com/form")
    
    # Use fixture data
    page.fill("#field1", custom_test_data["field1"])
    page.fill("#field2", custom_test_data["field2"])
    
    # Submit and verify
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    
    assert page.locator(".success").is_visible()


# ============================================================================
# NOTES FOR USERS
# ============================================================================

"""
HOW TO USE THIS TEMPLATE:

1. Copy this file to create your own test file:
   cp tests/test_template.py tests/test_my_feature.py

2. Modify the test functions for your specific needs:
   - Update URLs
   - Update selectors
   - Update assertions
   - Add your own logic

3. Add appropriate markers:
   @pytest.mark.login
   @pytest.mark.form
   @pytest.mark.ui
   @pytest.mark.flow
   @pytest.mark.smoke
   @pytest.mark.regression

4. Run your tests:
   pytest tests/test_my_feature.py -v

5. Tips:
   - Use descriptive test names
   - Add docstrings to explain what test does
   - Use Page Objects when possible
   - Add explicit waits instead of time.sleep()
   - Take screenshots on failures for debugging
   - Group related tests in classes
   - Use fixtures for reusable setup/data
"""
