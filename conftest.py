"""
Pytest configuration and fixtures for Playwright tests.
"""
import pytest
from playwright.sync_api import Page, BrowserContext, Browser


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context arguments.
    """
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "locale": "vi-VN",  # Vietnamese locale
        "timezone_id": "Asia/Ho_Chi_Minh",
    }


@pytest.fixture(scope="function")
def context(browser: Browser):
    """
    Create a new browser context for each test.
    """
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """
    Create a new page for each test.
    """
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def test_user_credentials():
    """
    Sample user credentials for testing.
    """
    return {
        "username": "test_user@example.com",
        "password": "Test@123456",
    }


@pytest.fixture
def sample_form_data():
    """
    Sample form data for testing.
    """
    return {
        "first_name": "Nguyễn",
        "last_name": "Văn A",
        "email": "nguyenvana@example.com",
        "phone": "0901234567",
        "address": "123 Đường ABC, Quận 1, TP.HCM",
        "city": "Hồ Chí Minh",
        "country": "Việt Nam",
    }
