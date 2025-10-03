"""
Example Login Page Object
"""

from framework.core.page_base import BasePage
from playwright.sync_api import Locator


class LoginPage(BasePage):
    """Login page object"""
    
    @property
    def url(self) -> str:
        return "/login"
    
    @property
    def username_input(self) -> Locator:
        """Username input field"""
        return self.page.locator("#username")
    
    @property
    def password_input(self) -> Locator:
        """Password input field"""
        return self.page.locator("#password")
    
    @property
    def login_button(self) -> Locator:
        """Login button"""
        return self.page.locator("button[type='submit']")
    
    @property
    def error_message(self) -> Locator:
        """Error message element"""
        return self.page.locator(".error-message")
    
    def login(self, username: str, password: str):
        """
        Perform login
        
        Args:
            username: Username
            password: Password
        """
        self.fill_input(self.username_input.first, username)
        self.fill_input(self.password_input.first, password)
        self.click_element(self.login_button.first)
        return self
    
    def is_error_visible(self) -> bool:
        """Check if error message is visible"""
        return self.is_visible(self.error_message.first)
