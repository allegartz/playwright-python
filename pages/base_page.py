"""
Base page object model for all page objects.
"""
from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str):
        """Navigate to a specific URL."""
        self.page.goto(url)
    
    def get_title(self) -> str:
        """Get the page title."""
        return self.page.title()
    
    def get_url(self) -> str:
        """Get the current page URL."""
        return self.page.url
    
    def click_element(self, selector: str):
        """Click an element by selector."""
        self.page.click(selector)
    
    def fill_input(self, selector: str, text: str):
        """Fill an input field with text."""
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """Get text content from an element."""
        return self.page.locator(selector).text_content()
    
    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        return self.page.locator(selector).is_visible()
    
    def wait_for_selector(self, selector: str, timeout: int = 30000):
        """Wait for an element to appear."""
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def take_screenshot(self, filename: str):
        """Take a screenshot of the current page."""
        self.page.screenshot(path=filename)
    
    def select_option(self, selector: str, value: str):
        """Select an option from a dropdown."""
        self.page.select_option(selector, value)
    
    def check_checkbox(self, selector: str):
        """Check a checkbox."""
        self.page.check(selector)
    
    def uncheck_checkbox(self, selector: str):
        """Uncheck a checkbox."""
        self.page.uncheck(selector)
    
    def get_element_count(self, selector: str) -> int:
        """Get the count of elements matching selector."""
        return self.page.locator(selector).count()
    
    def hover_element(self, selector: str):
        """Hover over an element."""
        self.page.hover(selector)
    
    def press_key(self, key: str):
        """Press a keyboard key."""
        self.page.keyboard.press(key)
