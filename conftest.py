"""
Pytest configuration and fixtures
"""

import pytest
from pathlib import Path
from framework.core.browser_manager import BrowserManager
from framework.core.config_manager import ConfigManager
from framework.utils.logger import setup_logger


def pytest_configure(config):
    """Configure pytest"""
    # Setup logging
    log_file = Path("logs/test.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    setup_logger(log_level="INFO", log_file=str(log_file))
    
    # Register custom markers
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "regression: regression tests")
    config.addinivalue_line("markers", "integration: integration tests")


def pytest_sessionstart(session):
    """Called before test session starts"""
    # Initialize Playwright
    BrowserManager.initialize_playwright()


def pytest_sessionfinish(session, exitstatus):
    """Called after test session finishes"""
    # Cleanup Playwright
    BrowserManager.cleanup_playwright()


@pytest.fixture(scope="session")
def config():
    """Provide configuration instance"""
    return ConfigManager.get_instance()


@pytest.fixture(scope="function")
def browser_manager():
    """Provide browser manager instance"""
    manager = BrowserManager()
    yield manager
    manager.cleanup()


# Playwright-pytest integration happens automatically via pytest-playwright plugin
# The 'page' fixture is provided by pytest-playwright
