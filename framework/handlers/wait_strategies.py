"""
Wait Strategies

Different waiting strategies for elements and conditions:
- Explicit waits
- Implicit waits
- Custom conditions
- Polling strategies
"""

from typing import Callable, Any, Optional
from playwright.sync_api import Page, Locator
from loguru import logger
import time
from enum import Enum


class WaitCondition(Enum):
    """Predefined wait conditions"""
    VISIBLE = "visible"
    HIDDEN = "hidden"
    ATTACHED = "attached"
    DETACHED = "detached"
    ENABLED = "enabled"
    DISABLED = "disabled"
    EDITABLE = "editable"
    CHECKED = "checked"
    UNCHECKED = "unchecked"


class WaitStrategy:
    """
    Flexible wait strategies for different conditions
    
    Features:
    - Predefined wait conditions
    - Custom condition functions
    - Configurable timeout and polling
    - Multiple element waiting
    
    Example:
        wait = WaitStrategy(page)
        wait.for_element_visible("#submit-btn")
        wait.for_condition(lambda: page.title == "Home")
    """
    
    def __init__(self, page: Page, default_timeout: int = 30000, poll_interval: int = 500):
        """
        Initialize wait strategy
        
        Args:
            page: Playwright Page instance
            default_timeout: Default timeout in milliseconds
            poll_interval: Polling interval in milliseconds
        """
        self.page = page
        self.default_timeout = default_timeout
        self.poll_interval = poll_interval
    
    def for_element_visible(
        self,
        selector: str,
        timeout: Optional[int] = None
    ) -> Locator:
        """
        Wait for element to be visible
        
        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
            
        Returns:
            Locator instance
        """
        timeout = timeout or self.default_timeout
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        logger.debug(f"Element visible: {selector}")
        return locator
    
    def for_element_hidden(
        self,
        selector: str,
        timeout: Optional[int] = None
    ) -> Locator:
        """
        Wait for element to be hidden
        
        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
            
        Returns:
            Locator instance
        """
        timeout = timeout or self.default_timeout
        locator = self.page.locator(selector)
        locator.wait_for(state="hidden", timeout=timeout)
        logger.debug(f"Element hidden: {selector}")
        return locator
    
    def for_element_attached(
        self,
        selector: str,
        timeout: Optional[int] = None
    ) -> Locator:
        """
        Wait for element to be attached to DOM
        
        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
            
        Returns:
            Locator instance
        """
        timeout = timeout or self.default_timeout
        locator = self.page.locator(selector)
        locator.wait_for(state="attached", timeout=timeout)
        logger.debug(f"Element attached: {selector}")
        return locator
    
    def for_element_detached(
        self,
        selector: str,
        timeout: Optional[int] = None
    ) -> Locator:
        """
        Wait for element to be detached from DOM
        
        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
            
        Returns:
            Locator instance
        """
        timeout = timeout or self.default_timeout
        locator = self.page.locator(selector)
        locator.wait_for(state="detached", timeout=timeout)
        logger.debug(f"Element detached: {selector}")
        return locator
    
    def for_element_count(
        self,
        selector: str,
        count: int,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for specific element count
        
        Args:
            selector: Element selector
            count: Expected element count
            timeout: Optional timeout in milliseconds
            
        Returns:
            True if count matches, False otherwise
        """
        timeout = timeout or self.default_timeout
        end_time = time.time() + (timeout / 1000)
        
        while time.time() < end_time:
            current_count = self.page.locator(selector).count()
            if current_count == count:
                logger.debug(f"Element count matches {count}: {selector}")
                return True
            time.sleep(self.poll_interval / 1000)
        
        logger.warning(f"Element count timeout: {selector}")
        return False
    
    def for_text_visible(
        self,
        text: str,
        exact: bool = False,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for text to be visible on page
        
        Args:
            text: Text to wait for
            exact: Exact text matching
            timeout: Optional timeout in milliseconds
            
        Returns:
            True if text visible, False otherwise
        """
        timeout = timeout or self.default_timeout
        
        try:
            locator = self.page.get_by_text(text, exact=exact)
            locator.wait_for(state="visible", timeout=timeout)
            logger.debug(f"Text visible: {text}")
            return True
        except:
            logger.warning(f"Text not visible: {text}")
            return False
    
    def for_url(
        self,
        url: str,
        exact: bool = False,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for URL to match
        
        Args:
            url: URL or URL pattern to wait for
            exact: Exact URL matching
            timeout: Optional timeout in milliseconds
            
        Returns:
            True if URL matches, False otherwise
        """
        timeout = timeout or self.default_timeout
        end_time = time.time() + (timeout / 1000)
        
        while time.time() < end_time:
            current_url = self.page.url
            
            if exact:
                if current_url == url:
                    logger.debug(f"URL matches: {url}")
                    return True
            else:
                if url in current_url:
                    logger.debug(f"URL contains: {url}")
                    return True
            
            time.sleep(self.poll_interval / 1000)
        
        logger.warning(f"URL timeout: {url}")
        return False
    
    def for_title(
        self,
        title: str,
        exact: bool = False,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for page title to match
        
        Args:
            title: Title or title pattern to wait for
            exact: Exact title matching
            timeout: Optional timeout in milliseconds
            
        Returns:
            True if title matches, False otherwise
        """
        timeout = timeout or self.default_timeout
        end_time = time.time() + (timeout / 1000)
        
        while time.time() < end_time:
            current_title = self.page.title()
            
            if exact:
                if current_title == title:
                    logger.debug(f"Title matches: {title}")
                    return True
            else:
                if title in current_title:
                    logger.debug(f"Title contains: {title}")
                    return True
            
            time.sleep(self.poll_interval / 1000)
        
        logger.warning(f"Title timeout: {title}")
        return False
    
    def for_condition(
        self,
        condition: Callable[[], bool],
        timeout: Optional[int] = None,
        message: str = "Condition not met"
    ) -> bool:
        """
        Wait for custom condition
        
        Args:
            condition: Callable that returns bool
            timeout: Optional timeout in milliseconds
            message: Error message if condition not met
            
        Returns:
            True if condition met, False otherwise
        """
        timeout = timeout or self.default_timeout
        end_time = time.time() + (timeout / 1000)
        
        while time.time() < end_time:
            try:
                if condition():
                    logger.debug(f"Condition met: {message}")
                    return True
            except Exception as e:
                logger.debug(f"Condition check error: {e}")
            
            time.sleep(self.poll_interval / 1000)
        
        logger.warning(f"Condition timeout: {message}")
        return False
    
    def for_network_idle(
        self,
        timeout: Optional[int] = None
    ):
        """
        Wait for network to be idle
        
        Args:
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.default_timeout
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        logger.debug("Network idle")
    
    def for_load(
        self,
        timeout: Optional[int] = None
    ):
        """
        Wait for page load
        
        Args:
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.default_timeout
        self.page.wait_for_load_state("load", timeout=timeout)
        logger.debug("Page loaded")
    
    def for_dom_content_loaded(
        self,
        timeout: Optional[int] = None
    ):
        """
        Wait for DOM content loaded
        
        Args:
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.default_timeout
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        logger.debug("DOM content loaded")
    
    def for_selector(
        self,
        selector: str,
        state: str = "visible",
        timeout: Optional[int] = None
    ) -> Locator:
        """
        Generic wait for selector with state
        
        Args:
            selector: Element selector
            state: Element state
            timeout: Optional timeout in milliseconds
            
        Returns:
            Locator instance
        """
        timeout = timeout or self.default_timeout
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=timeout)
        logger.debug(f"Element {state}: {selector}")
        return locator
    
    def for_function(
        self,
        page_function: str,
        timeout: Optional[int] = None
    ) -> Any:
        """
        Wait for function to return truthy value
        
        Args:
            page_function: JavaScript function string
            timeout: Optional timeout in milliseconds
            
        Returns:
            Function result
        """
        timeout = timeout or self.default_timeout
        result = self.page.wait_for_function(page_function, timeout=timeout)
        logger.debug(f"Function returned truthy: {page_function[:50]}...")
        return result
