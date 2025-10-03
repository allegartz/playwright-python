"""
Login functionality tests.
Test various login scenarios including valid/invalid credentials,
remember me functionality, and logout.
"""
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


@pytest.mark.login
class TestLogin:
    """Test suite for login functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test - navigate to login page."""
        # Note: Replace with actual login URL when testing
        self.login_url = "https://example.com/login"
        self.login_page = LoginPage(page)
    
    def test_login_page_elements(self, page: Page):
        """Test that all login page elements are visible."""
        self.login_page.navigate(self.login_url)
        
        # Verify page title
        assert "login" in self.login_page.get_title().lower() or \
               "sign in" in self.login_page.get_title().lower(), \
               "Login page title should contain 'login' or 'sign in'"
        
        # Verify form elements are visible
        assert self.login_page.is_username_field_visible(), \
               "Username field should be visible"
        assert self.login_page.is_password_field_visible(), \
               "Password field should be visible"
        assert self.login_page.is_login_button_enabled(), \
               "Login button should be enabled"
    
    def test_successful_login(self, page: Page, test_user_credentials: dict):
        """Test successful login with valid credentials."""
        self.login_page.navigate(self.login_url)
        
        # Perform login
        self.login_page.login(
            test_user_credentials["username"],
            test_user_credentials["password"]
        )
        
        # Wait for navigation after successful login
        page.wait_for_load_state("networkidle")
        
        # Verify successful login
        # Note: This assertion should be customized based on actual application
        # For example, check if redirected to dashboard or if logout button is visible
        assert self.login_page.is_logged_in() or \
               "dashboard" in page.url.lower() or \
               "home" in page.url.lower(), \
               "Should be redirected after successful login"
    
    def test_login_with_invalid_credentials(self, page: Page):
        """Test login with invalid credentials."""
        self.login_page.navigate(self.login_url)
        
        # Attempt login with invalid credentials
        self.login_page.login("invalid_user@example.com", "wrongpassword")
        
        # Wait a bit for error message
        page.wait_for_timeout(1000)
        
        # Verify error message is displayed
        error_message = self.login_page.get_error_message()
        assert error_message or page.url == self.login_url, \
               "Should show error message or stay on login page"
    
    def test_login_with_empty_username(self, page: Page):
        """Test login with empty username field."""
        self.login_page.navigate(self.login_url)
        
        # Attempt login with empty username
        self.login_page.login("", "password123")
        
        # Should stay on login page
        assert page.url == self.login_url or \
               self.login_page.get_error_message(), \
               "Should not login with empty username"
    
    def test_login_with_empty_password(self, page: Page):
        """Test login with empty password field."""
        self.login_page.navigate(self.login_url)
        
        # Attempt login with empty password
        self.login_page.login("user@example.com", "")
        
        # Should stay on login page
        assert page.url == self.login_url or \
               self.login_page.get_error_message(), \
               "Should not login with empty password"
    
    def test_login_with_remember_me(self, page: Page, test_user_credentials: dict):
        """Test login with remember me checkbox."""
        self.login_page.navigate(self.login_url)
        
        # Perform login with remember me
        self.login_page.login(
            test_user_credentials["username"],
            test_user_credentials["password"],
            remember_me=True
        )
        
        page.wait_for_load_state("networkidle")
        
        # Verify login was successful
        assert self.login_page.is_logged_in() or \
               page.url != self.login_url, \
               "Should be logged in"
    
    def test_logout_functionality(self, page: Page, test_user_credentials: dict):
        """Test logout functionality."""
        self.login_page.navigate(self.login_url)
        
        # Login first
        self.login_page.login(
            test_user_credentials["username"],
            test_user_credentials["password"]
        )
        
        page.wait_for_load_state("networkidle")
        
        # Perform logout
        self.login_page.logout()
        
        page.wait_for_load_state("networkidle")
        
        # Verify redirected to login page or logged out
        assert not self.login_page.is_logged_in() or \
               "login" in page.url.lower(), \
               "Should be logged out"


@pytest.mark.login
@pytest.mark.smoke
def test_login_page_loads(page: Page):
    """Smoke test to verify login page loads properly."""
    login_page = LoginPage(page)
    login_url = "https://example.com/login"
    
    # Navigate to login page
    login_page.navigate(login_url)
    
    # Verify page loaded
    assert page.url == login_url or "login" in page.url, \
           "Should navigate to login page"
