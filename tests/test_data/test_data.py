"""
Sample test data for tests.
"""

# Sample user data
SAMPLE_USERS = [
    {
        "first_name": "Nguyễn",
        "last_name": "Văn A",
        "email": "nguyenvana@example.com",
        "phone": "0901234567",
        "address": "123 Đường ABC, Quận 1",
        "city": "Hồ Chí Minh",
        "country": "Việt Nam"
    },
    {
        "first_name": "Trần",
        "last_name": "Thị B",
        "email": "tranthib@example.com",
        "phone": "0912345678",
        "address": "456 Đường XYZ, Quận 2",
        "city": "Hà Nội",
        "country": "Việt Nam"
    },
    {
        "first_name": "Lê",
        "last_name": "Văn C",
        "email": "levanc@example.com",
        "phone": "0923456789",
        "address": "789 Đường DEF, Quận 3",
        "city": "Đà Nẵng",
        "country": "Việt Nam"
    }
]

# Sample form data with different scenarios
FORM_SCENARIOS = {
    "valid_complete": {
        "first_name": "Phạm",
        "last_name": "Văn D",
        "email": "phamvand@example.com",
        "phone": "0934567890",
        "address": "321 Đường GHI",
        "city": "Cần Thơ",
        "country": "Việt Nam",
        "gender": "male",
        "accept_terms": True,
        "subscribe_newsletter": True
    },
    "missing_required": {
        "first_name": "",
        "last_name": "",
        "email": "",
        "phone": "0945678901"
    },
    "invalid_email": {
        "first_name": "Test",
        "last_name": "User",
        "email": "invalid-email",
        "phone": "0956789012"
    },
    "invalid_phone": {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "phone": "123"  # Invalid phone format
    }
}

# Login credentials for different scenarios
LOGIN_SCENARIOS = {
    "valid_login": {
        "username": "valid_user@example.com",
        "password": "ValidPass@123"
    },
    "invalid_username": {
        "username": "nonexistent@example.com",
        "password": "SomePassword123"
    },
    "invalid_password": {
        "username": "valid_user@example.com",
        "password": "WrongPassword"
    },
    "empty_username": {
        "username": "",
        "password": "SomePassword123"
    },
    "empty_password": {
        "username": "valid_user@example.com",
        "password": ""
    },
    "sql_injection": {
        "username": "admin' OR '1'='1",
        "password": "' OR '1'='1"
    },
    "xss_attempt": {
        "username": "<script>alert('XSS')</script>",
        "password": "password"
    }
}

# Search queries
SEARCH_QUERIES = [
    "Playwright",
    "Python testing",
    "Automation",
    "Test framework",
    "Kiểm thử tự động"
]

# Product data for e-commerce tests
PRODUCT_DATA = [
    {
        "name": "Sản phẩm 1",
        "quantity": 1,
        "price": 100000
    },
    {
        "name": "Sản phẩm 2",
        "quantity": 2,
        "price": 250000
    }
]
