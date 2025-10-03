"""
Base Page Class

Page Object Model base class with common page operations:
- Element interactions
- Waiting strategies
- Custom actions
"""

from typing import Optional, List, Any
from playwright.sync_api import Page, Locator, expect
from loguru import logger
from abc import ABC, abstractmethod

from .config_manager import ConfigManager


class BasePage(ABC):
    """
    Base Page Object Model class
    
    All page objects should inherit from this class.
    
    Features:
    - Common element interaction methods
    - Smart waiting
    - Logging
    - Reusable actions
    
    Example:
        class LoginPage(BasePage):
            def __init__(self, page: Page):
                super().__init__(page)
                self.url = "/login"
                
            @property
            def username_input(self) -> Locator:
                return self.page.locator("#username")
    """
    
    def __init__(self, page: Page):
        """
        Initialize page object
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.config = ConfigManager.get_instance()
        self.timeout = self.config.get("timeouts.element_timeout", 10000)
    
    @property
    @abstractmethod
    def url(self) -> str:
        """Page URL (relative or absolute)"""
        pass
    
    def navigate(self):
        """Navigate to page URL"""
        full_url = self.url if self.url.startswith('http') else f"{self.config.get('base_url', '')}{self.url}"
        logger.info(f"Navigating to: {full_url}")
        self.page.goto(full_url)
        return self
    
    def wait_for_load(self, timeout: Optional[int] = None):
        """
        Wait for page to load
        
        Args:
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        self.page.wait_for_load_state("load", timeout=timeout)
        logger.info(f"Page loaded: {self.page.url}")
        return self
    
    def wait_for_selector(self, selector: str, state: str = "visible", timeout: Optional[int] = None) -> Locator:
        """
        Wait for element by selector
        
        Args:
            selector: Element selector
            state: Element state (visible, hidden, attached, detached)
            timeout: Optional timeout in milliseconds
            
        Returns:
            Locator instance
        """
        timeout = timeout or self.timeout
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=timeout)
        return locator
    
    def click_element(self, selector: str, timeout: Optional[int] = None):
        """
        Click element
        
        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self.wait_for_selector(selector, timeout=timeout)
        element.click()
        logger.info(f"Clicked element: {selector}")
        return self
    
    def fill_input(self, selector: str, value: str, timeout: Optional[int] = None):
        """
        Fill input field
        
        Args:
            selector: Element selector
            value: Value to fill
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self.wait_for_selector(selector, timeout=timeout)
        element.fill(value)
        logger.info(f"Filled input {selector} with: {value}")
        return self
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get element text
        
        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
            
        Returns:
            Element text
        """
        timeout = timeout or self.timeout
        element = self.wait_for_selector(selector, timeout=timeout)
        text = element.text_content()
        logger.info(f"Got text from {selector}: {text}")
        return text
    
    def get_attribute(self, selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        Get element attribute
        
        Args:
            selector: Element selector
            attribute: Attribute name
            timeout: Optional timeout in milliseconds
            
        Returns:
            Attribute value
        """
        timeout = timeout or self.timeout
        element = self.wait_for_selector(selector, timeout=timeout)
        value = element.get_attribute(attribute)
        logger.info(f"Got attribute {attribute} from {selector}: {value}")
        return value
    
    def is_visible(self, selector: str) -> bool:
        """
        Check if element is visible
        
        Args:
            selector: Element selector
            
        Returns:
            True if visible, False otherwise
        """
        try:
            element = self.page.locator(selector)
            return element.is_visible()
        except Exception:
            return False
    
    def is_enabled(self, selector: str) -> bool:
        """
        Check if element is enabled
        
        Args:
            selector: Element selector
            
        Returns:
            True if enabled, False otherwise
        """
        try:
            element = self.page.locator(selector)
            return element.is_enabled()
        except Exception:
            return False
    
    def select_option(self, selector: str, value: str, timeout: Optional[int] = None):
        """
        Select option from dropdown
        
        Args:
            selector: Select element selector
            value: Option value
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self.wait_for_selector(selector, timeout=timeout)
        element.select_option(value)
        logger.info(f"Selected option {value} in {selector}")
        return self
    
    def check_checkbox(self, selector: str, timeout: Optional[int] = None):
        """
        Check checkbox
        
        Args:
            selector: Checkbox selector
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self.wait_for_selector(selector, timeout=timeout)
        element.check()
        logger.info(f"Checked checkbox: {selector}")
        return self
    
    def uncheck_checkbox(self, selector: str, timeout: Optional[int] = None):
        """
        Uncheck checkbox
        
        Args:
            selector: Checkbox selector
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self.wait_for_selector(selector, timeout=timeout)
        element.uncheck()
        logger.info(f"Unchecked checkbox: {selector}")
        return self
    
    def hover(self, selector: str, timeout: Optional[int] = None):
        """
        Hover over element
        
        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        element = self.wait_for_selector(selector, timeout=timeout)
        element.hover()
        logger.info(f"Hovered over: {selector}")
        return self
    
    def scroll_to(self, selector: str):
        """
        Scroll to element
        
        Args:
            selector: Element selector
        """
        element = self.page.locator(selector)
        element.scroll_into_view_if_needed()
        logger.info(f"Scrolled to: {selector}")
        return self
    
    def get_elements(self, selector: str) -> List[Locator]:
        """
        Get all elements matching selector
        
        Args:
            selector: Element selector
            
        Returns:
            List of Locator instances
        """
        elements = self.page.locator(selector).all()
        logger.info(f"Found {len(elements)} elements: {selector}")
        return elements
    
    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript
        
        Args:
            script: JavaScript code
            *args: Arguments to pass to script
            
        Returns:
            Script result
        """
        result = self.page.evaluate(script, *args)
        logger.info(f"Executed script: {script[:50]}...")
        return result
