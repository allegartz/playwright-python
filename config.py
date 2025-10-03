"""
Configuration file for test settings.
Customize URLs and test data here.
"""

# Base URLs for different environments
ENVIRONMENTS = {
    "dev": "https://dev.example.com",
    "staging": "https://staging.example.com",
    "production": "https://example.com"
}

# Default environment
DEFAULT_ENV = "production"

# Page URLs
URLS = {
    "home": "/",
    "login": "/login",
    "register": "/register",
    "form": "/form",
    "dashboard": "/dashboard",
    "products": "/products",
    "cart": "/cart",
    "search": "/search",
    "about": "/about"
}

# Test users
TEST_USERS = {
    "valid_user": {
        "username": "test_user@example.com",
        "password": "Test@123456"
    },
    "invalid_user": {
        "username": "invalid@example.com",
        "password": "wrongpassword"
    }
}

# Browser settings
BROWSER_CONFIG = {
    "headless": True,
    "slow_mo": 0,  # Slow down operations by specified milliseconds
    "viewport": {
        "width": 1920,
        "height": 1080
    },
    "locale": "vi-VN",
    "timezone_id": "Asia/Ho_Chi_Minh"
}

# Timeout settings (in milliseconds)
TIMEOUTS = {
    "default": 30000,
    "long": 60000,
    "short": 5000
}

# Screenshot settings
SCREENSHOT_CONFIG = {
    "on_failure": True,
    "path": "screenshots/"
}


def get_base_url(environment=None):
    """Get base URL for specified environment."""
    env = environment or DEFAULT_ENV
    return ENVIRONMENTS.get(env, ENVIRONMENTS[DEFAULT_ENV])


def get_url(page_name, environment=None):
    """Get full URL for a specific page."""
    base_url = get_base_url(environment)
    page_path = URLS.get(page_name, "/")
    return f"{base_url}{page_path}"
