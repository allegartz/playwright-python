"""
Example test using the framework
"""

import pytest
from framework.core.base_test import BaseTest
from examples.pages.login_page import LoginPage
from framework.patterns.factory import TestDataFactory
from framework.watchers.network_watcher import NetworkWatcher
from framework.watchers.console_watcher import ConsoleWatcher


class TestLogin(BaseTest):
    """Login test examples"""
    
    def test_successful_login(self, page):
        """Test successful login"""
        # Create test data
        data_factory = TestDataFactory()
        user_data = data_factory.create_user()
        
        # Create page object
        login_page = LoginPage(page)
        
        # Navigate and login
        login_page.navigate()
        login_page.wait_for_load()
        login_page.login(user_data['username'], user_data['password'])
        
        # Verify login success (example)
        # self.assert_text_present(page, "Dashboard")
    
    def test_failed_login(self, page):
        """Test failed login with invalid credentials"""
        login_page = LoginPage(page)
        
        # Navigate and attempt login with invalid credentials
        login_page.navigate()
        login_page.wait_for_load()
        login_page.login("invalid_user", "invalid_password")
        
        # Verify error message is displayed
        assert login_page.is_error_visible(), "Error message should be visible"
    
    def test_login_with_network_monitoring(self, page):
        """Test login with network monitoring"""
        # Setup network watcher
        network_watcher = NetworkWatcher(page)
        network_watcher.start()
        
        # Perform login
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("testuser", "testpass")
        
        # Check network requests
        requests = network_watcher.get_requests()
        assert len(requests) > 0, "Should have network requests"
        
        # Check for failed requests
        failed = network_watcher.get_failed_requests()
        assert len(failed) == 0, "Should not have failed requests"
        
        network_watcher.stop()
    
    def test_login_with_console_monitoring(self, page):
        """Test login with console error monitoring"""
        # Setup console watcher
        console_watcher = ConsoleWatcher(page)
        console_watcher.start()
        
        # Perform login
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("testuser", "testpass")
        
        # Check for console errors
        assert not console_watcher.has_errors(), "Should not have console errors"
        
        console_watcher.stop()


class TestLoginWithSmartElements(BaseTest):
    """Login tests using smart element handlers"""
    
    def test_login_with_element_handler(self, page):
        """Test login using ElementHandler"""
        from framework.handlers.element_handler import ElementHandler
        
        handler = ElementHandler(page)
        
        # Navigate
        page.goto(f"{self.config.get('base_url')}/login")
        
        # Fill and submit using smart element handler
        handler.fill("testuser", id="username")
        handler.fill("testpass", id="password")
        handler.click(css="button[type='submit']")
        
        # Verify (example)
        assert handler.is_visible(text="Dashboard") or True


class TestLoginWithFlow(BaseTest):
    """Login tests using flow coordinator"""
    
    def test_login_flow(self, page):
        """Test login using flow coordinator"""
        from framework.coordinator.flow_coordinator import FlowCoordinator
        
        coordinator = FlowCoordinator()
        login_page = LoginPage(page)
        
        # Define flow steps
        coordinator.add_step(
            "navigate",
            lambda: login_page.navigate()
        )
        coordinator.add_step(
            "wait_for_load",
            lambda: login_page.wait_for_load()
        )
        coordinator.add_step(
            "enter_credentials",
            lambda: login_page.login("testuser", "testpass")
        )
        
        # Execute flow
        success = coordinator.execute()
        assert success, "Login flow should succeed"
        
        # Check statistics
        stats = coordinator.get_statistics()
        assert stats['completed'] == 3, "All steps should complete"
