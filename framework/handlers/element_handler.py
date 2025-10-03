"""
Element Handler

Smart element interaction with retry logic and validation:
- Auto-retry on failure
- Element state validation
- Action chaining
- Screenshot on error
"""

from typing import Optional, Any, List
from playwright.sync_api import Page, Locator
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time

from .element_locator import SmartLocator
from ..core.config_manager import ConfigManager


class ElementHandler:
    """
    Handle element interactions with smart retry and validation
    
    Features:
    - Auto-retry on failure
    - Element state validation before actions
    - Action logging
    - Screenshot on error
    - Fluent interface
    
    Example:
        handler = ElementHandler(page)
        handler.click(css="#submit-btn")
        handler.fill(id="username", value="john")
    """
    
    def __init__(self, page: Page, max_retries: int = 3):
        """
        Initialize element handler
        
        Args:
            page: Playwright Page instance
            max_retries: Maximum retry attempts
        """
        self.page = page
        self.locator = SmartLocator(page)
        self.config = ConfigManager.get_instance()
        self.max_retries = max_retries
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception)
    )
    def click(
        self,
        css: Optional[str] = None,
        xpath: Optional[str] = None,
        text: Optional[str] = None,
        button: str = "left",
        click_count: int = 1,
        force: bool = False,
        **kwargs
    ):
        """
        Click element with retry
        
        Args:
            css: CSS selector
            xpath: XPath selector
            text: Text content
            button: Mouse button (left, right, middle)
            click_count: Number of clicks
            force: Force click even if element is not interactive
            **kwargs: Additional locator arguments
        """
        element = self.locator.find(css=css, xpath=xpath, text=text, **kwargs)
        
        # Validate element is clickable
        if not force:
            self._wait_for_clickable(element)
        
        element.click(button=button, click_count=click_count, force=force)
        logger.info(f"Clicked element: {css or xpath or text}")
        
        return self
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception)
    )
    def fill(
        self,
        value: str,
        css: Optional[str] = None,
        xpath: Optional[str] = None,
        placeholder: Optional[str] = None,
        clear_first: bool = True,
        **kwargs
    ):
        """
        Fill input field with retry
        
        Args:
            value: Value to fill
            css: CSS selector
            xpath: XPath selector
            placeholder: Placeholder text
            clear_first: Clear field before filling
            **kwargs: Additional locator arguments
        """
        element = self.locator.find(css=css, xpath=xpath, placeholder=placeholder, **kwargs)
        
        # Validate element is editable
        self._wait_for_editable(element)
        
        if clear_first:
            element.clear()
        
        element.fill(value)
        logger.info(f"Filled element with: {value}")
        
        return self
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception)
    )
    def type(
        self,
        text: str,
        css: Optional[str] = None,
        xpath: Optional[str] = None,
        delay: int = 0,
        **kwargs
    ):
        """
        Type text with delay between keystrokes
        
        Args:
            text: Text to type
            css: CSS selector
            xpath: XPath selector
            delay: Delay between keystrokes in milliseconds
            **kwargs: Additional locator arguments
        """
        element = self.locator.find(css=css, xpath=xpath, **kwargs)
        
        self._wait_for_editable(element)
        
        element.type(text, delay=delay)
        logger.info(f"Typed text: {text}")
        
        return self
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception)
    )
    def select_option(
        self,
        value: Optional[str] = None,
        label: Optional[str] = None,
        index: Optional[int] = None,
        css: Optional[str] = None,
        xpath: Optional[str] = None,
        **kwargs
    ):
        """
        Select option from dropdown
        
        Args:
            value: Option value
            label: Option label
            index: Option index
            css: CSS selector
            xpath: XPath selector
            **kwargs: Additional locator arguments
        """
        element = self.locator.find(css=css, xpath=xpath, **kwargs)
        
        if value:
            element.select_option(value=value)
        elif label:
            element.select_option(label=label)
        elif index is not None:
            element.select_option(index=index)
        else:
            raise ValueError("Must provide value, label, or index")
        
        logger.info(f"Selected option: {value or label or index}")
        
        return self
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception)
    )
    def check(self, css: Optional[str] = None, xpath: Optional[str] = None, force: bool = False, **kwargs):
        """
        Check checkbox/radio button
        
        Args:
            css: CSS selector
            xpath: XPath selector
            force: Force check even if not interactive
            **kwargs: Additional locator arguments
        """
        element = self.locator.find(css=css, xpath=xpath, **kwargs)
        
        if not force:
            self._wait_for_clickable(element)
        
        element.check(force=force)
        logger.info(f"Checked element: {css or xpath}")
        
        return self
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception)
    )
    def uncheck(self, css: Optional[str] = None, xpath: Optional[str] = None, force: bool = False, **kwargs):
        """
        Uncheck checkbox
        
        Args:
            css: CSS selector
            xpath: XPath selector
            force: Force uncheck even if not interactive
            **kwargs: Additional locator arguments
        """
        element = self.locator.find(css=css, xpath=xpath, **kwargs)
        
        if not force:
            self._wait_for_clickable(element)
        
        element.uncheck(force=force)
        logger.info(f"Unchecked element: {css or xpath}")
        
        return self
    
    def hover(self, css: Optional[str] = None, xpath: Optional[str] = None, **kwargs):
        """
        Hover over element
        
        Args:
            css: CSS selector
            xpath: XPath selector
            **kwargs: Additional locator arguments
        """
        element = self.locator.find(css=css, xpath=xpath, **kwargs)
        element.hover()
        logger.info(f"Hovered over element: {css or xpath}")
        
        return self
    
    def scroll_into_view(self, css: Optional[str] = None, xpath: Optional[str] = None, **kwargs):
        """
        Scroll element into view
        
        Args:
            css: CSS selector
            xpath: XPath selector
            **kwargs: Additional locator arguments
        """
        element = self.locator.find(css=css, xpath=xpath, **kwargs)
        element.scroll_into_view_if_needed()
        logger.info(f"Scrolled element into view: {css or xpath}")
        
        return self
    
    def get_text(self, css: Optional[str] = None, xpath: Optional[str] = None, **kwargs) -> str:
        """
        Get element text content
        
        Args:
            css: CSS selector
            xpath: XPath selector
            **kwargs: Additional locator arguments
            
        Returns:
            Text content
        """
        element = self.locator.find(css=css, xpath=xpath, **kwargs)
        text = element.text_content()
        logger.debug(f"Got text: {text}")
        return text or ""
    
    def get_value(self, css: Optional[str] = None, xpath: Optional[str] = None, **kwargs) -> str:
        """
        Get input element value
        
        Args:
            css: CSS selector
            xpath: XPath selector
            **kwargs: Additional locator arguments
            
        Returns:
            Input value
        """
        element = self.locator.find(css=css, xpath=xpath, **kwargs)
        value = element.input_value()
        logger.debug(f"Got value: {value}")
        return value
    
    def get_attribute(self, attribute: str, css: Optional[str] = None, xpath: Optional[str] = None, **kwargs) -> Optional[str]:
        """
        Get element attribute
        
        Args:
            attribute: Attribute name
            css: CSS selector
            xpath: XPath selector
            **kwargs: Additional locator arguments
            
        Returns:
            Attribute value
        """
        element = self.locator.find(css=css, xpath=xpath, **kwargs)
        value = element.get_attribute(attribute)
        logger.debug(f"Got attribute {attribute}: {value}")
        return value
    
    def is_visible(self, css: Optional[str] = None, xpath: Optional[str] = None, **kwargs) -> bool:
        """
        Check if element is visible
        
        Args:
            css: CSS selector
            xpath: XPath selector
            **kwargs: Additional locator arguments
            
        Returns:
            True if visible, False otherwise
        """
        try:
            element = self.locator.find(css=css, xpath=xpath, **kwargs)
            return element.is_visible()
        except:
            return False
    
    def is_enabled(self, css: Optional[str] = None, xpath: Optional[str] = None, **kwargs) -> bool:
        """
        Check if element is enabled
        
        Args:
            css: CSS selector
            xpath: XPath selector
            **kwargs: Additional locator arguments
            
        Returns:
            True if enabled, False otherwise
        """
        try:
            element = self.locator.find(css=css, xpath=xpath, **kwargs)
            return element.is_enabled()
        except:
            return False
    
    def wait_for(
        self,
        state: str = "visible",
        timeout: Optional[int] = None,
        css: Optional[str] = None,
        xpath: Optional[str] = None,
        **kwargs
    ):
        """
        Wait for element state
        
        Args:
            state: Element state (visible, hidden, attached, detached)
            timeout: Timeout in milliseconds
            css: CSS selector
            xpath: XPath selector
            **kwargs: Additional locator arguments
        """
        timeout = timeout or self.config.get("timeouts.element_timeout", 10000)
        element = self.locator.find(css=css, xpath=xpath, **kwargs)
        element.wait_for(state=state, timeout=timeout)
        logger.debug(f"Element {state}: {css or xpath}")
        
        return self
    
    def _wait_for_clickable(self, element: Locator):
        """Wait for element to be clickable"""
        element.wait_for(state="visible")
        if not element.is_enabled():
            raise Exception("Element is not enabled")
    
    def _wait_for_editable(self, element: Locator):
        """Wait for element to be editable"""
        element.wait_for(state="visible")
        if not element.is_editable():
            raise Exception("Element is not editable")
