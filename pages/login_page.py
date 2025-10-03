"""
Login page object model.
"""
from pages.base_page import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):
    """Login page object with login functionality."""
    
    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    SUCCESS_MESSAGE = ".success-message"
    LOGOUT_BUTTON = "#logout"
    REMEMBER_ME_CHECKBOX = "#remember-me"
    FORGOT_PASSWORD_LINK = "a[href*='forgot-password']"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def login(self, username: str, password: str, remember_me: bool = False):
        """
        Perform login action.
        
        Args:
            username: User's username or email
            password: User's password
            remember_me: Whether to check the remember me checkbox
        """
        self.fill_input(self.USERNAME_INPUT, username)
        self.fill_input(self.PASSWORD_INPUT, password)
        
        if remember_me:
            self.check_checkbox(self.REMEMBER_ME_CHECKBOX)
        
        self.click_element(self.LOGIN_BUTTON)
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in by checking logout button visibility."""
        return self.is_visible(self.LOGOUT_BUTTON)
    
    def logout(self):
        """Perform logout action."""
        if self.is_visible(self.LOGOUT_BUTTON):
            self.click_element(self.LOGOUT_BUTTON)
    
    def get_error_message(self) -> str:
        """Get the error message text."""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def get_success_message(self) -> str:
        """Get the success message text."""
        if self.is_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""
    
    def click_forgot_password(self):
        """Click on forgot password link."""
        self.click_element(self.FORGOT_PASSWORD_LINK)
    
    def is_username_field_visible(self) -> bool:
        """Check if username field is visible."""
        return self.is_visible(self.USERNAME_INPUT)
    
    def is_password_field_visible(self) -> bool:
        """Check if password field is visible."""
        return self.is_visible(self.PASSWORD_INPUT)
    
    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled."""
        return self.page.locator(self.LOGIN_BUTTON).is_enabled()
