"""
Browser Manager

Handles browser lifecycle and context management with support for:
- Multiple browser types
- Browser context pooling
- Video recording
- Screenshots
"""

from typing import Optional, Dict, Any
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
from pathlib import Path
import threading
from loguru import logger

from .config_manager import ConfigManager


class BrowserManager:
    """
    Manages browser instances and contexts
    
    Features:
    - Browser instance pooling
    - Context management
    - Video and screenshot capture
    - Thread-safe operations
    """
    
    _lock = threading.Lock()
    _browsers: Dict[str, Browser] = {}
    _playwright: Optional[Playwright] = None
    
    def __init__(self):
        """Initialize browser manager"""
        self.config = ConfigManager.get_instance()
        self._current_browser: Optional[Browser] = None
        self._current_context: Optional[BrowserContext] = None
        self._current_page: Optional[Page] = None
    
    @classmethod
    def initialize_playwright(cls) -> Playwright:
        """Initialize Playwright instance (singleton)"""
        with cls._lock:
            if cls._playwright is None:
                cls._playwright = sync_playwright().start()
                logger.info("Playwright initialized")
            return cls._playwright
    
    @classmethod
    def cleanup_playwright(cls):
        """Cleanup Playwright instance"""
        with cls._lock:
            if cls._playwright is not None:
                cls._playwright.stop()
                cls._playwright = None
                cls._browsers.clear()
                logger.info("Playwright cleaned up")
    
    def launch_browser(self, browser_type: Optional[str] = None, **kwargs) -> Browser:
        """
        Launch a new browser instance
        
        Args:
            browser_type: Type of browser (chromium, firefox, webkit)
            **kwargs: Additional browser launch options
            
        Returns:
            Browser instance
        """
        if self._playwright is None:
            self.initialize_playwright()
        
        browser_type = browser_type or self.config.get("browser.browser_type", "chromium")
        
        # Prepare launch options
        launch_options = {
            "headless": self.config.get("browser.headless", True),
            "slow_mo": self.config.get("browser.slow_mo", 0),
        }
        launch_options.update(kwargs)
        
        # Get browser launcher
        browser_launcher = getattr(self._playwright, browser_type)
        
        # Launch browser
        browser = browser_launcher.launch(**launch_options)
        self._current_browser = browser
        
        logger.info(f"Browser launched: {browser_type}, headless={launch_options['headless']}")
        return browser
    
    def create_context(self, **kwargs) -> BrowserContext:
        """
        Create a new browser context
        
        Args:
            **kwargs: Context options
            
        Returns:
            BrowserContext instance
        """
        if self._current_browser is None:
            self.launch_browser()
        
        # Prepare context options
        context_options = {
            "viewport": {
                "width": self.config.get("browser.viewport_width", 1920),
                "height": self.config.get("browser.viewport_height", 1080),
            },
        }
        
        # Add video recording if configured
        video_dir = self.config.get("browser.video_dir")
        if video_dir:
            Path(video_dir).mkdir(parents=True, exist_ok=True)
            context_options["record_video_dir"] = video_dir
        
        context_options.update(kwargs)
        
        # Create context
        context = self._current_browser.new_context(**context_options)
        self._current_context = context
        
        # Set default timeouts
        context.set_default_timeout(self.config.get("timeouts.default_timeout", 30000))
        context.set_default_navigation_timeout(
            self.config.get("timeouts.navigation_timeout", 30000)
        )
        
        logger.info("Browser context created")
        return context
    
    def create_page(self, context: Optional[BrowserContext] = None) -> Page:
        """
        Create a new page
        
        Args:
            context: Browser context (creates new if not provided)
            
        Returns:
            Page instance
        """
        if context is None:
            if self._current_context is None:
                context = self.create_context()
            else:
                context = self._current_context
        
        page = context.new_page()
        self._current_page = page
        
        logger.info("New page created")
        return page
    
    def close_page(self, page: Optional[Page] = None):
        """Close page"""
        page = page or self._current_page
        if page:
            page.close()
            logger.info("Page closed")
    
    def close_context(self, context: Optional[BrowserContext] = None):
        """Close browser context"""
        context = context or self._current_context
        if context:
            context.close()
            logger.info("Context closed")
            self._current_context = None
    
    def close_browser(self, browser: Optional[Browser] = None):
        """Close browser"""
        browser = browser or self._current_browser
        if browser:
            browser.close()
            logger.info("Browser closed")
            self._current_browser = None
    
    def cleanup(self):
        """Cleanup all resources"""
        if self._current_page:
            self.close_page()
        if self._current_context:
            self.close_context()
        if self._current_browser:
            self.close_browser()
    
    def take_screenshot(self, page: Page, name: str, full_page: bool = True) -> str:
        """
        Take screenshot
        
        Args:
            page: Page to screenshot
            name: Screenshot name
            full_page: Capture full page
            
        Returns:
            Path to screenshot file
        """
        screenshot_dir = Path(self.config.get("browser.screenshot_dir", "screenshots"))
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        screenshot_path = screenshot_dir / f"{name}.png"
        page.screenshot(path=str(screenshot_path), full_page=full_page)
        
        logger.info(f"Screenshot saved: {screenshot_path}")
        return str(screenshot_path)
    
    @property
    def current_browser(self) -> Optional[Browser]:
        """Get current browser"""
        return self._current_browser
    
    @property
    def current_context(self) -> Optional[BrowserContext]:
        """Get current context"""
        return self._current_context
    
    @property
    def current_page(self) -> Optional[Page]:
        """Get current page"""
        return self._current_page
