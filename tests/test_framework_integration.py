"""
Sample integration test demonstrating framework capabilities
"""

import pytest
from framework.core.base_test import BaseTest
from framework.watchers.network_watcher import NetworkWatcher
from framework.watchers.console_watcher import ConsoleWatcher
from framework.handlers.element_handler import ElementHandler
from framework.coordinator.flow_coordinator import FlowCoordinator


class TestFrameworkIntegration(BaseTest):
    """Integration tests for framework components"""
    
    @pytest.mark.smoke
    def test_basic_navigation(self, page):
        """Test basic page navigation"""
        # Navigate to a page
        page.goto("https://playwright.dev")
        
        # Verify page loaded
        assert "Playwright" in page.title()
    
    @pytest.mark.smoke
    def test_element_handler(self, page):
        """Test smart element handler"""
        handler = ElementHandler(page)
        
        page.goto("https://playwright.dev")
        
        # Test element visibility
        assert handler.is_visible(css="nav")
    
    def test_network_monitoring(self, page):
        """Test network monitoring capabilities"""
        watcher = NetworkWatcher(page)
        watcher.start()
        
        # Navigate and trigger requests
        page.goto("https://playwright.dev")
        
        # Get network data
        requests = watcher.get_requests()
        responses = watcher.get_responses()
        
        assert len(requests) > 0, "Should capture network requests"
        assert len(responses) > 0, "Should capture network responses"
        
        # Check for failed requests
        failed = watcher.get_failed_requests()
        assert len(failed) == 0, "Should not have failed requests"
        
        watcher.stop()
    
    def test_console_monitoring(self, page):
        """Test console monitoring"""
        watcher = ConsoleWatcher(page)
        watcher.start()
        
        # Navigate to page
        page.goto("https://playwright.dev")
        
        # Get console messages
        messages = watcher.get_messages()
        
        # Verify no console errors
        assert not watcher.has_errors(), "Should not have console errors"
        
        watcher.stop()
    
    def test_flow_coordination(self, page):
        """Test flow coordinator"""
        coordinator = FlowCoordinator()
        
        # Define flow
        coordinator.add_step(
            "navigate",
            lambda: page.goto("https://playwright.dev")
        )
        coordinator.add_step(
            "verify_title",
            lambda: "Playwright" in page.title()
        )
        
        # Execute flow
        success = coordinator.execute()
        assert success, "Flow should execute successfully"
        
        # Check statistics
        stats = coordinator.get_statistics()
        assert stats['completed'] == 2
        assert stats['failed'] == 0


class TestConfigurationManagement(BaseTest):
    """Test configuration management"""
    
    def test_config_loading(self):
        """Test configuration is loaded"""
        assert self.config is not None
        
        # Test config access
        browser_type = self.config.get("browser.browser_type")
        assert browser_type in ["chromium", "firefox", "webkit"]
    
    def test_timeout_config(self):
        """Test timeout configurations"""
        default_timeout = self.config.get("timeouts.default_timeout")
        assert default_timeout > 0
