"""
Form page object model.
"""
from pages.base_page import BasePage
from playwright.sync_api import Page


class FormPage(BasePage):
    """Form page object for handling various form operations."""
    
    # Common form locators
    FIRST_NAME_INPUT = "#firstName"
    LAST_NAME_INPUT = "#lastName"
    EMAIL_INPUT = "#email"
    PHONE_INPUT = "#phone"
    ADDRESS_INPUT = "#address"
    CITY_INPUT = "#city"
    COUNTRY_SELECT = "#country"
    GENDER_RADIO_MALE = "input[type='radio'][value='male']"
    GENDER_RADIO_FEMALE = "input[type='radio'][value='female']"
    TERMS_CHECKBOX = "#terms"
    NEWSLETTER_CHECKBOX = "#newsletter"
    SUBMIT_BUTTON = "button[type='submit']"
    RESET_BUTTON = "button[type='reset']"
    SUCCESS_MESSAGE = ".form-success"
    ERROR_MESSAGE = ".form-error"
    VALIDATION_ERROR = ".validation-error"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def fill_personal_info(self, first_name: str, last_name: str, email: str, phone: str = ""):
        """
        Fill personal information fields.
        
        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number (optional)
        """
        self.fill_input(self.FIRST_NAME_INPUT, first_name)
        self.fill_input(self.LAST_NAME_INPUT, last_name)
        self.fill_input(self.EMAIL_INPUT, email)
        
        if phone:
            self.fill_input(self.PHONE_INPUT, phone)
    
    def fill_address_info(self, address: str, city: str, country: str = ""):
        """
        Fill address information fields.
        
        Args:
            address: Street address
            city: City name
            country: Country (optional)
        """
        self.fill_input(self.ADDRESS_INPUT, address)
        self.fill_input(self.CITY_INPUT, city)
        
        if country:
            self.select_option(self.COUNTRY_SELECT, country)
    
    def select_gender(self, gender: str):
        """
        Select gender radio button.
        
        Args:
            gender: 'male' or 'female'
        """
        if gender.lower() == "male":
            self.click_element(self.GENDER_RADIO_MALE)
        elif gender.lower() == "female":
            self.click_element(self.GENDER_RADIO_FEMALE)
    
    def accept_terms(self):
        """Accept terms and conditions."""
        self.check_checkbox(self.TERMS_CHECKBOX)
    
    def subscribe_newsletter(self):
        """Subscribe to newsletter."""
        self.check_checkbox(self.NEWSLETTER_CHECKBOX)
    
    def submit_form(self):
        """Submit the form."""
        self.click_element(self.SUBMIT_BUTTON)
    
    def reset_form(self):
        """Reset the form."""
        self.click_element(self.RESET_BUTTON)
    
    def fill_complete_form(self, form_data: dict):
        """
        Fill complete form with all data.
        
        Args:
            form_data: Dictionary containing all form fields
        """
        self.fill_personal_info(
            form_data.get("first_name", ""),
            form_data.get("last_name", ""),
            form_data.get("email", ""),
            form_data.get("phone", "")
        )
        
        self.fill_address_info(
            form_data.get("address", ""),
            form_data.get("city", ""),
            form_data.get("country", "")
        )
        
        if form_data.get("gender"):
            self.select_gender(form_data.get("gender"))
        
        if form_data.get("accept_terms"):
            self.accept_terms()
        
        if form_data.get("subscribe_newsletter"):
            self.subscribe_newsletter()
    
    def get_success_message(self) -> str:
        """Get form success message."""
        if self.is_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""
    
    def get_error_message(self) -> str:
        """Get form error message."""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def get_validation_errors(self) -> list:
        """Get all validation error messages."""
        errors = []
        error_count = self.get_element_count(self.VALIDATION_ERROR)
        
        for i in range(error_count):
            error_text = self.page.locator(self.VALIDATION_ERROR).nth(i).text_content()
            errors.append(error_text)
        
        return errors
    
    def is_submit_button_enabled(self) -> bool:
        """Check if submit button is enabled."""
        return self.page.locator(self.SUBMIT_BUTTON).is_enabled()
