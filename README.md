# Playwright Python - Automated Web Testing

Dự án kiểm thử tự động cho ứng dụng web sử dụng Python và Playwright. Hỗ trợ kiểm thử đăng nhập, thao tác form, kiểm tra UI và luồng người dùng.

## 📋 Tính năng

- ✅ **Kiểm thử đăng nhập**: Test các kịch bản đăng nhập với thông tin hợp lệ/không hợp lệ, remember me, logout
- ✅ **Kiểm thử form**: Test điền form, validation, submit, reset
- ✅ **Kiểm thử UI**: Test các thành phần giao diện, responsive design, accessibility
- ✅ **Kiểm thử luồng người dùng**: Test các luồng nghiệp vụ end-to-end
- 📊 Báo cáo HTML chi tiết
- 🎯 Test markers để phân loại và chạy test theo nhóm
- 🔧 Page Object Model để tổ chức code tốt hơn

## 🚀 Cài đặt

### Yêu cầu hệ thống
- Python 3.8+
- pip

### Các bước cài đặt

1. Clone repository:
```bash
git clone https://github.com/allegartz/playwright-python.git
cd playwright-python
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Cài đặt Playwright browsers:
```bash
python -m playwright install chromium
# Hoặc cài đặt tất cả browsers
python -m playwright install
```

## 📁 Cấu trúc dự án

```
playwright-python/
├── pages/                      # Page Object Models
│   ├── __init__.py
│   ├── base_page.py           # Base page với các methods chung
│   ├── login_page.py          # Login page object
│   └── form_page.py           # Form page object
├── tests/                      # Test cases
│   ├── __init__.py
│   ├── test_login.py          # Login tests
│   ├── test_form.py           # Form tests
│   ├── test_ui.py             # UI tests
│   ├── test_user_flow.py      # User flow tests
│   └── test_data/             # Test data files
├── reports/                    # Test reports (auto-generated)
├── conftest.py                # Pytest fixtures và configuration
├── pytest.ini                 # Pytest configuration
├── run_tests.py              # Test runner script
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation

```

## 🎯 Chạy tests

### Sử dụng test runner script

```bash
# Chạy tất cả tests
python run_tests.py all

# Chạy login tests
python run_tests.py login

# Chạy form tests
python run_tests.py form

# Chạy UI tests
python run_tests.py ui

# Chạy user flow tests
python run_tests.py flow

# Chạy smoke tests
python run_tests.py smoke

# Chạy regression tests
python run_tests.py regression

# Chạy tests với browser hiển thị
python run_tests.py headed

# Chạy một test cụ thể
python run_tests.py test tests/test_login.py
python run_tests.py test tests/test_login.py::TestLogin::test_successful_login

# Hiển thị help
python run_tests.py help
```

### Sử dụng pytest trực tiếp

```bash
# Chạy tất cả tests
pytest tests/ -v

# Chạy tests theo marker
pytest -m login -v
pytest -m form -v
pytest -m ui -v
pytest -m flow -v

# Chạy một file test cụ thể
pytest tests/test_login.py -v

# Chạy một test function cụ thể
pytest tests/test_login.py::TestLogin::test_successful_login -v

# Chạy với browser hiển thị
pytest tests/ --headed -v

# Chạy với browser cụ thể
pytest tests/ --browser chromium -v
pytest tests/ --browser firefox -v
pytest tests/ --browser webkit -v

# Tạo báo cáo HTML
pytest tests/ --html=reports/report.html --self-contained-html
```

## 📊 Test Markers

Tests được phân loại bằng markers:

- `login`: Tests liên quan đến chức năng đăng nhập
- `form`: Tests liên quan đến thao tác form
- `ui`: Tests liên quan đến UI elements
- `flow`: Tests liên quan đến user flows
- `smoke`: Smoke tests cho các chức năng quan trọng
- `regression`: Regression tests

## 📝 Viết tests mới

### Sử dụng Page Object Model

```python
from playwright.sync_api import Page
from pages.login_page import LoginPage

def test_my_login(page: Page):
    login_page = LoginPage(page)
    login_page.navigate("https://example.com/login")
    login_page.login("user@example.com", "password123")
    assert login_page.is_logged_in()
```

### Sử dụng fixtures

```python
import pytest

def test_with_credentials(page: Page, test_user_credentials: dict):
    # test_user_credentials fixture được định nghĩa trong conftest.py
    username = test_user_credentials["username"]
    password = test_user_credentials["password"]
    # ... test code
```

### Thêm markers

```python
import pytest

@pytest.mark.login
@pytest.mark.smoke
def test_critical_login(page: Page):
    # Test code here
    pass
```

## 🔧 Configuration

### pytest.ini
Cấu hình pytest nằm trong file `pytest.ini`:
- Test discovery patterns
- Output options
- Markers definition
- Report settings

### conftest.py
Fixtures và configuration:
- Browser context settings
- Viewport size
- Locale và timezone
- Test data fixtures

## 📈 Báo cáo

Sau khi chạy tests, báo cáo HTML được tạo trong thư mục `reports/`:
- `reports/report.html`: Báo cáo tổng hợp
- `reports/login_report.html`: Báo cáo login tests
- `reports/form_report.html`: Báo cáo form tests
- `reports/ui_report.html`: Báo cáo UI tests
- `reports/flow_report.html`: Báo cáo flow tests

## 🛠️ Tùy chỉnh

### Thay đổi URLs
Update URLs trong các test files hoặc tạo configuration file:

```python
# Trong test file
self.base_url = "https://your-website.com"
self.login_url = f"{self.base_url}/login"
```

### Thêm Page Objects mới
Tạo file mới trong thư mục `pages/`:

```python
from pages.base_page import BasePage

class MyPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
    
    def my_method(self):
        # Implementation
        pass
```

## 🐛 Debugging

### Chạy tests với browser hiển thị
```bash
pytest --headed --slowmo=1000
```

### Chạy với debugger
```bash
pytest --pdb
```

### Xem chi tiết lỗi
```bash
pytest -v --tb=long
```

## 🤝 Đóng góp

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 📞 Liên hệ

- GitHub: [@allegartz](https://github.com/allegartz)

## 🎓 Tài liệu tham khảo

- [Playwright Python Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://playwright.dev/python/docs/pom)
