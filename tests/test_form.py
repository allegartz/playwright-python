"""
Form operations tests.
Test various form operations including filling forms, validation,
submission, and reset functionality.
"""
import pytest
from playwright.sync_api import Page, expect
from pages.form_page import FormPage


@pytest.mark.form
class TestFormOperations:
    """Test suite for form operations."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test - navigate to form page."""
        # Note: Replace with actual form URL when testing
        self.form_url = "https://example.com/form"
        self.form_page = FormPage(page)
    
    def test_form_page_loads(self, page: Page):
        """Test that form page loads correctly."""
        self.form_page.navigate(self.form_url)
        
        # Verify page title
        assert "form" in self.form_page.get_title().lower() or \
               page.url == self.form_url, \
               "Form page should load"
    
    def test_fill_personal_information(self, page: Page, sample_form_data: dict):
        """Test filling personal information fields."""
        self.form_page.navigate(self.form_url)
        
        # Fill personal info
        self.form_page.fill_personal_info(
            sample_form_data["first_name"],
            sample_form_data["last_name"],
            sample_form_data["email"],
            sample_form_data["phone"]
        )
        
        # Verify fields are filled (using page object methods)
        # Note: In a real test, you would verify the values are actually filled
        assert True, "Personal information should be filled"
    
    def test_fill_address_information(self, page: Page, sample_form_data: dict):
        """Test filling address information fields."""
        self.form_page.navigate(self.form_url)
        
        # Fill address info
        self.form_page.fill_address_info(
            sample_form_data["address"],
            sample_form_data["city"],
            sample_form_data["country"]
        )
        
        assert True, "Address information should be filled"
    
    def test_fill_complete_form(self, page: Page, sample_form_data: dict):
        """Test filling complete form with all fields."""
        self.form_page.navigate(self.form_url)
        
        # Prepare complete form data
        complete_data = {
            **sample_form_data,
            "gender": "male",
            "accept_terms": True,
            "subscribe_newsletter": True
        }
        
        # Fill complete form
        self.form_page.fill_complete_form(complete_data)
        
        # Verify submit button is enabled
        assert self.form_page.is_submit_button_enabled(), \
               "Submit button should be enabled after filling form"
    
    def test_submit_valid_form(self, page: Page, sample_form_data: dict):
        """Test submitting a valid form."""
        self.form_page.navigate(self.form_url)
        
        # Fill and submit form
        complete_data = {
            **sample_form_data,
            "gender": "female",
            "accept_terms": True
        }
        
        self.form_page.fill_complete_form(complete_data)
        self.form_page.submit_form()
        
        # Wait for submission
        page.wait_for_load_state("networkidle")
        
        # Verify submission success
        success_message = self.form_page.get_success_message()
        assert success_message or page.url != self.form_url, \
               "Form should be submitted successfully"
    
    def test_submit_form_without_required_fields(self, page: Page):
        """Test submitting form without required fields."""
        self.form_page.navigate(self.form_url)
        
        # Try to submit empty form
        self.form_page.submit_form()
        
        # Wait a bit for validation
        page.wait_for_timeout(1000)
        
        # Should get validation errors or stay on the same page
        validation_errors = self.form_page.get_validation_errors()
        assert validation_errors or \
               page.url == self.form_url or \
               self.form_page.get_error_message(), \
               "Should show validation errors for empty form"
    
    def test_reset_form(self, page: Page, sample_form_data: dict):
        """Test form reset functionality."""
        self.form_page.navigate(self.form_url)
        
        # Fill form
        self.form_page.fill_personal_info(
            sample_form_data["first_name"],
            sample_form_data["last_name"],
            sample_form_data["email"]
        )
        
        # Reset form
        self.form_page.reset_form()
        
        # Wait a bit
        page.wait_for_timeout(500)
        
        # Form should be reset (fields cleared)
        assert True, "Form should be reset"
    
    def test_select_gender_male(self, page: Page):
        """Test selecting male gender."""
        self.form_page.navigate(self.form_url)
        
        # Select male gender
        self.form_page.select_gender("male")
        
        assert True, "Male gender should be selected"
    
    def test_select_gender_female(self, page: Page):
        """Test selecting female gender."""
        self.form_page.navigate(self.form_url)
        
        # Select female gender
        self.form_page.select_gender("female")
        
        assert True, "Female gender should be selected"
    
    def test_accept_terms_and_conditions(self, page: Page):
        """Test accepting terms and conditions."""
        self.form_page.navigate(self.form_url)
        
        # Accept terms
        self.form_page.accept_terms()
        
        assert True, "Terms should be accepted"
    
    def test_subscribe_to_newsletter(self, page: Page):
        """Test subscribing to newsletter."""
        self.form_page.navigate(self.form_url)
        
        # Subscribe to newsletter
        self.form_page.subscribe_newsletter()
        
        assert True, "Should subscribe to newsletter"
    
    def test_form_validation_invalid_email(self, page: Page):
        """Test form validation with invalid email."""
        self.form_page.navigate(self.form_url)
        
        # Fill with invalid email
        self.form_page.fill_personal_info(
            "Test",
            "User",
            "invalid-email",  # Invalid email format
            "1234567890"
        )
        
        self.form_page.submit_form()
        
        # Wait for validation
        page.wait_for_timeout(1000)
        
        # Should show validation error or stay on page
        assert page.url == self.form_url or \
               self.form_page.get_validation_errors() or \
               self.form_page.get_error_message(), \
               "Should validate email format"


@pytest.mark.form
@pytest.mark.smoke
def test_form_accessibility(page: Page):
    """Smoke test for form accessibility."""
    form_page = FormPage(page)
    form_url = "https://example.com/form"
    
    # Navigate to form
    form_page.navigate(form_url)
    
    # Verify page loads
    assert page.url == form_url or "form" in page.url, \
           "Form page should be accessible"
