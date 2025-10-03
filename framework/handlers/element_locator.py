"""
Smart Locator

Intelligent element location strategies:
- Multiple selector strategies
- Auto-healing locators
- Fuzzy matching
- AI-powered element detection
"""

from typing import Optional, List, Dict, Any, Union
from playwright.sync_api import Page, Locator
from loguru import logger
from enum import Enum


class LocatorStrategy(Enum):
    """Element locator strategies"""
    CSS = "css"
    XPATH = "xpath"
    TEXT = "text"
    ID = "id"
    NAME = "name"
    CLASS = "class"
    PLACEHOLDER = "placeholder"
    ROLE = "role"
    TEST_ID = "test_id"
    LABEL = "label"


class SmartLocator:
    """
    Intelligent element locator with multiple fallback strategies
    
    Features:
    - Multiple locator strategies
    - Auto-healing when elements change
    - Fuzzy text matching
    - Priority-based fallback
    
    Example:
        locator = SmartLocator(page)
        element = locator.find(
            css="#submit-btn",
            text="Submit",
            role="button"
        )
    """
    
    def __init__(self, page: Page):
        """
        Initialize smart locator
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self._cache: Dict[str, Locator] = {}
    
    def find(
        self,
        css: Optional[str] = None,
        xpath: Optional[str] = None,
        text: Optional[str] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        class_name: Optional[str] = None,
        placeholder: Optional[str] = None,
        role: Optional[str] = None,
        test_id: Optional[str] = None,
        label: Optional[str] = None,
        exact: bool = False,
        timeout: int = 10000
    ) -> Locator:
        """
        Find element using multiple strategies with fallback
        
        Args:
            css: CSS selector
            xpath: XPath selector
            text: Text content
            id: Element ID
            name: Element name
            class_name: CSS class name
            placeholder: Placeholder text
            role: ARIA role
            test_id: Test ID attribute
            label: Associated label text
            exact: Exact text matching
            timeout: Timeout in milliseconds
            
        Returns:
            Locator instance
            
        Raises:
            Exception: If no element found with any strategy
        """
        strategies = []
        
        # Build strategy list in priority order
        if test_id:
            strategies.append(('test_id', lambda: self.page.get_by_test_id(test_id)))
        
        if id:
            strategies.append(('id', lambda: self.page.locator(f"#{id}")))
        
        if role:
            strategies.append(('role', lambda: self.page.get_by_role(role)))
        
        if label:
            strategies.append(('label', lambda: self.page.get_by_label(label, exact=exact)))
        
        if placeholder:
            strategies.append(('placeholder', lambda: self.page.get_by_placeholder(placeholder, exact=exact)))
        
        if text:
            strategies.append(('text', lambda: self.page.get_by_text(text, exact=exact)))
        
        if name:
            strategies.append(('name', lambda: self.page.locator(f"[name='{name}']")))
        
        if class_name:
            strategies.append(('class', lambda: self.page.locator(f".{class_name}")))
        
        if css:
            strategies.append(('css', lambda: self.page.locator(css)))
        
        if xpath:
            strategies.append(('xpath', lambda: self.page.locator(f"xpath={xpath}")))
        
        # Try each strategy
        last_error = None
        for strategy_name, strategy_func in strategies:
            try:
                locator = strategy_func()
                # Verify element exists
                locator.wait_for(state="attached", timeout=timeout)
                logger.debug(f"Element found using strategy: {strategy_name}")
                return locator
            except Exception as e:
                last_error = e
                logger.debug(f"Strategy {strategy_name} failed: {str(e)}")
                continue
        
        # All strategies failed
        error_msg = f"Could not locate element with any strategy. Last error: {last_error}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    def find_all(
        self,
        css: Optional[str] = None,
        xpath: Optional[str] = None,
        text: Optional[str] = None,
        role: Optional[str] = None
    ) -> List[Locator]:
        """
        Find all matching elements
        
        Args:
            css: CSS selector
            xpath: XPath selector
            text: Text content
            role: ARIA role
            
        Returns:
            List of Locator instances
        """
        if css:
            return self.page.locator(css).all()
        elif xpath:
            return self.page.locator(f"xpath={xpath}").all()
        elif text:
            return self.page.get_by_text(text).all()
        elif role:
            return self.page.get_by_role(role).all()
        else:
            raise ValueError("At least one selector must be provided")
    
    def find_by_attributes(self, **attributes) -> Locator:
        """
        Find element by multiple attributes
        
        Args:
            **attributes: Attribute key-value pairs
            
        Returns:
            Locator instance
        """
        selectors = []
        for key, value in attributes.items():
            selectors.append(f"[{key}='{value}']")
        
        css_selector = "".join(selectors)
        return self.page.locator(css_selector)
    
    def find_by_contains_text(self, text: str) -> Locator:
        """
        Find element containing text (case-insensitive)
        
        Args:
            text: Text to search for
            
        Returns:
            Locator instance
        """
        xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"
        return self.page.locator(f"xpath={xpath}")
    
    def find_parent(self, locator: Locator) -> Locator:
        """
        Find parent element
        
        Args:
            locator: Child element locator
            
        Returns:
            Parent element locator
        """
        return locator.locator('..')
    
    def find_sibling(self, locator: Locator, selector: str) -> Locator:
        """
        Find sibling element
        
        Args:
            locator: Reference element locator
            selector: Sibling selector
            
        Returns:
            Sibling element locator
        """
        parent = self.find_parent(locator)
        return parent.locator(selector)
    
    def find_child(self, locator: Locator, selector: str) -> Locator:
        """
        Find child element
        
        Args:
            locator: Parent element locator
            selector: Child selector
            
        Returns:
            Child element locator
        """
        return locator.locator(selector)
    
    def is_visible(self, locator: Locator) -> bool:
        """
        Check if element is visible
        
        Args:
            locator: Element locator
            
        Returns:
            True if visible, False otherwise
        """
        try:
            return locator.is_visible()
        except:
            return False
    
    def is_enabled(self, locator: Locator) -> bool:
        """
        Check if element is enabled
        
        Args:
            locator: Element locator
            
        Returns:
            True if enabled, False otherwise
        """
        try:
            return locator.is_enabled()
        except:
            return False
    
    def get_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        """
        Get element attribute value
        
        Args:
            locator: Element locator
            attribute: Attribute name
            
        Returns:
            Attribute value or None
        """
        try:
            return locator.get_attribute(attribute)
        except:
            return None
    
    def clear_cache(self):
        """Clear locator cache"""
        self._cache.clear()
        logger.debug("Locator cache cleared")
