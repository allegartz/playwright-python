"""
Base Test Class

Provides common test setup and teardown functionality:
- Browser initialization
- Context management
- Screenshot capture on failure
- Logging integration
"""

import pytest
from typing import Generator, Optional
from playwright.sync_api import Page, BrowserContext
from loguru import logger
import traceback

from .browser_manager import BrowserManager
from .config_manager import ConfigManager


class BaseTest:
    """
    Base test class that all test classes should inherit from
    
    Features:
    - Automatic browser setup/teardown
    - Screenshot on failure
    - Logging
    - Configuration access
    
    Example:
        class TestLogin(BaseTest):
            def test_login_success(self, page):
                page.goto("https://example.com")
                # test logic here
    """
    
    config: ConfigManager = None
    browser_manager: BrowserManager = None
    
    @classmethod
    def setup_class(cls):
        """Setup before all tests in class"""
        cls.config = ConfigManager.get_instance()
        cls.browser_manager = BrowserManager()
        logger.info(f"Setting up test class: {cls.__name__}")
    
    @classmethod
    def teardown_class(cls):
        """Teardown after all tests in class"""
        if cls.browser_manager:
            cls.browser_manager.cleanup()
        logger.info(f"Tearing down test class: {cls.__name__}")
    
    def setup_method(self, method):
        """Setup before each test method"""
        logger.info(f"Starting test: {method.__name__}")
        self.test_name = method.__name__
    
    def teardown_method(self, method):
        """Teardown after each test method"""
        logger.info(f"Finished test: {method.__name__}")
    
    @pytest.fixture
    def context(self) -> Generator[BrowserContext, None, None]:
        """
        Pytest fixture for browser context
        
        Yields:
            BrowserContext instance
        """
        context = self.browser_manager.create_context()
        yield context
        context.close()
    
    @pytest.fixture
    def page(self, context: BrowserContext) -> Generator[Page, None, None]:
        """
        Pytest fixture for page
        
        Yields:
            Page instance
        """
        page = context.new_page()
        
        # Setup failure screenshot
        failed = False
        
        yield page
        
        # Capture screenshot on failure
        if hasattr(self, '_test_failed') and self._test_failed:
            try:
                screenshot_name = f"failure_{self.test_name}"
                self.browser_manager.take_screenshot(page, screenshot_name)
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {e}")
        
        page.close()
    
    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Hook to capture test failures"""
        outcome = yield
        rep = outcome.get_result()
        
        if rep.when == "call" and rep.failed:
            self._test_failed = True
    
    def navigate(self, page: Page, url: str):
        """
        Navigate to URL with logging
        
        Args:
            page: Page instance
            url: URL to navigate to
        """
        full_url = url if url.startswith('http') else f"{self.config.get('base_url', '')}{url}"
        logger.info(f"Navigating to: {full_url}")
        page.goto(full_url)
    
    def assert_element_visible(self, page: Page, selector: str, timeout: Optional[int] = None):
        """
        Assert element is visible
        
        Args:
            page: Page instance
            selector: Element selector
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.config.get("timeouts.element_timeout", 10000)
        element = page.wait_for_selector(selector, state="visible", timeout=timeout)
        assert element is not None, f"Element not visible: {selector}"
        logger.info(f"Element visible: {selector}")
    
    def assert_text_present(self, page: Page, text: str):
        """
        Assert text is present on page
        
        Args:
            page: Page instance
            text: Text to find
        """
        assert page.get_by_text(text).is_visible(), f"Text not found: {text}"
        logger.info(f"Text found: {text}")
