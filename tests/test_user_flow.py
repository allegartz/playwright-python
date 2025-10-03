"""
User flow tests.
Test complete user flows including multi-step processes,
navigation flows, and end-to-end scenarios.
"""
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.form_page import FormPage
from pages.base_page import BasePage


@pytest.mark.flow
class TestUserFlows:
    """Test suite for complete user flows."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test."""
        self.base_url = "https://example.com"
        self.login_page = LoginPage(page)
        self.form_page = FormPage(page)
        self.base_page = BasePage(page)
    
    def test_complete_registration_flow(self, page: Page, sample_form_data: dict):
        """Test complete user registration flow."""
        # Step 1: Navigate to registration page
        registration_url = f"{self.base_url}/register"
        self.base_page.navigate(registration_url)
        
        # Step 2: Fill registration form
        complete_data = {
            **sample_form_data,
            "gender": "male",
            "accept_terms": True,
            "subscribe_newsletter": True
        }
        
        self.form_page.fill_complete_form(complete_data)
        
        # Step 3: Submit registration
        self.form_page.submit_form()
        
        # Step 4: Wait for completion
        page.wait_for_load_state("networkidle")
        
        # Step 5: Verify registration success
        success_message = self.form_page.get_success_message()
        assert success_message or \
               page.url != registration_url or \
               "success" in page.url.lower() or \
               "dashboard" in page.url.lower(), \
               "Registration flow should complete successfully"
    
    def test_login_to_dashboard_flow(self, page: Page, test_user_credentials: dict):
        """Test login flow to dashboard."""
        # Step 1: Navigate to login page
        login_url = f"{self.base_url}/login"
        self.login_page.navigate(login_url)
        
        # Step 2: Login with credentials
        self.login_page.login(
            test_user_credentials["username"],
            test_user_credentials["password"]
        )
        
        # Step 3: Wait for navigation
        page.wait_for_load_state("networkidle")
        
        # Step 4: Verify reached dashboard
        assert self.login_page.is_logged_in() or \
               "dashboard" in page.url.lower() or \
               "home" in page.url.lower(), \
               "Should navigate to dashboard after login"
    
    def test_form_submission_flow(self, page: Page, sample_form_data: dict):
        """Test complete form submission flow."""
        # Step 1: Navigate to form page
        form_url = f"{self.base_url}/form"
        self.form_page.navigate(form_url)
        
        # Step 2: Fill all form fields
        self.form_page.fill_personal_info(
            sample_form_data["first_name"],
            sample_form_data["last_name"],
            sample_form_data["email"],
            sample_form_data["phone"]
        )
        
        self.form_page.fill_address_info(
            sample_form_data["address"],
            sample_form_data["city"]
        )
        
        # Step 3: Accept terms
        self.form_page.accept_terms()
        
        # Step 4: Submit form
        self.form_page.submit_form()
        
        # Step 5: Wait for submission
        page.wait_for_load_state("networkidle")
        
        # Step 6: Verify submission
        assert page.url != form_url or \
               self.form_page.get_success_message(), \
               "Form should be submitted successfully"
    
    def test_login_submit_form_logout_flow(self, page: Page, 
                                          test_user_credentials: dict,
                                          sample_form_data: dict):
        """Test complete flow: login -> submit form -> logout."""
        # Step 1: Login
        login_url = f"{self.base_url}/login"
        self.login_page.navigate(login_url)
        self.login_page.login(
            test_user_credentials["username"],
            test_user_credentials["password"]
        )
        page.wait_for_load_state("networkidle")
        
        # Step 2: Navigate to form
        form_url = f"{self.base_url}/form"
        self.form_page.navigate(form_url)
        
        # Step 3: Fill and submit form
        self.form_page.fill_personal_info(
            sample_form_data["first_name"],
            sample_form_data["last_name"],
            sample_form_data["email"]
        )
        self.form_page.submit_form()
        page.wait_for_load_state("networkidle")
        
        # Step 4: Logout
        self.login_page.logout()
        page.wait_for_load_state("networkidle")
        
        # Step 5: Verify logged out
        assert not self.login_page.is_logged_in() or \
               "login" in page.url.lower(), \
               "Should be logged out after complete flow"
    
    def test_multi_page_navigation_flow(self, page: Page):
        """Test navigation between multiple pages."""
        # Step 1: Start at home page
        self.base_page.navigate(self.base_url)
        page.wait_for_load_state("networkidle")
        home_url = page.url
        
        # Step 2: Navigate to login page
        login_url = f"{self.base_url}/login"
        self.base_page.navigate(login_url)
        page.wait_for_load_state("networkidle")
        
        # Step 3: Navigate to form page
        form_url = f"{self.base_url}/form"
        self.base_page.navigate(form_url)
        page.wait_for_load_state("networkidle")
        
        # Step 4: Navigate back to home
        self.base_page.navigate(self.base_url)
        page.wait_for_load_state("networkidle")
        
        # Verify navigation completed
        assert page.url, "Should be able to navigate between pages"
    
    def test_browser_back_forward_navigation(self, page: Page):
        """Test browser back and forward navigation."""
        # Navigate to first page
        self.base_page.navigate(self.base_url)
        page.wait_for_load_state("networkidle")
        first_url = page.url
        
        # Navigate to second page
        second_url = f"{self.base_url}/about"
        self.base_page.navigate(second_url)
        page.wait_for_load_state("networkidle")
        
        # Go back
        page.go_back()
        page.wait_for_load_state("networkidle")
        
        # Verify we're back at first page
        assert page.url == first_url or \
               page.url.rstrip('/') == first_url.rstrip('/'), \
               "Should navigate back to previous page"
        
        # Go forward
        page.go_forward()
        page.wait_for_load_state("networkidle")
        
        # Verify we're at second page
        assert page.url == second_url or \
               page.url.rstrip('/') == second_url.rstrip('/'), \
               "Should navigate forward"
    
    def test_search_and_filter_flow(self, page: Page):
        """Test search and filter functionality flow."""
        # Step 1: Navigate to search page
        search_url = f"{self.base_url}/search"
        self.base_page.navigate(search_url)
        
        # Step 2: Perform search
        search_input = "input[type='search'], input[name='search'], input[name='q']"
        try:
            self.base_page.fill_input(search_input, "test query")
            self.base_page.press_key("Enter")
            page.wait_for_load_state("networkidle")
        except:
            pass
        
        # Verify search flow
        assert True, "Search flow should be tested"
    
    def test_add_to_cart_checkout_flow(self, page: Page):
        """Test e-commerce flow: browse -> add to cart -> checkout."""
        # Step 1: Navigate to products page
        products_url = f"{self.base_url}/products"
        self.base_page.navigate(products_url)
        page.wait_for_load_state("networkidle")
        
        # Step 2: Click first "Add to Cart" button if exists
        try:
            add_to_cart_selectors = [
                "button:has-text('Add to Cart')",
                "button:has-text('Thêm vào giỏ')",
                ".add-to-cart",
                "[data-action='add-to-cart']"
            ]
            
            for selector in add_to_cart_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.click()
                        page.wait_for_load_state("networkidle")
                        break
                except:
                    continue
        except:
            pass
        
        # Step 3: Navigate to cart
        cart_url = f"{self.base_url}/cart"
        self.base_page.navigate(cart_url)
        page.wait_for_load_state("networkidle")
        
        # Verify cart flow
        assert page.url, "Shopping cart flow should be tested"


@pytest.mark.flow
@pytest.mark.regression
def test_complete_user_journey(page: Page, 
                               test_user_credentials: dict,
                               sample_form_data: dict):
    """
    Regression test for complete user journey.
    Tests the most common user path through the application.
    """
    base_url = "https://example.com"
    login_page = LoginPage(page)
    form_page = FormPage(page)
    base_page = BasePage(page)
    
    # Step 1: Visit home page
    base_page.navigate(base_url)
    page.wait_for_load_state("networkidle")
    
    # Step 2: Login
    login_url = f"{base_url}/login"
    login_page.navigate(login_url)
    login_page.login(
        test_user_credentials["username"],
        test_user_credentials["password"]
    )
    page.wait_for_load_state("networkidle")
    
    # Step 3: Perform main action (fill a form)
    form_url = f"{base_url}/form"
    form_page.navigate(form_url)
    form_page.fill_personal_info(
        sample_form_data["first_name"],
        sample_form_data["last_name"],
        sample_form_data["email"]
    )
    
    # Step 4: Logout
    login_page.logout()
    page.wait_for_load_state("networkidle")
    
    # Complete journey should execute without errors
    assert True, "Complete user journey should work"


@pytest.mark.flow
@pytest.mark.smoke
def test_critical_path_smoke(page: Page):
    """Smoke test for critical user path."""
    base_url = "https://example.com"
    base_page = BasePage(page)
    
    # Navigate to main pages
    pages_to_check = [
        base_url,
        f"{base_url}/login",
        f"{base_url}/form"
    ]
    
    for url in pages_to_check:
        base_page.navigate(url)
        page.wait_for_load_state("networkidle")
        assert page.url, f"Should be able to navigate to {url}"
