# Hướng dẫn sử dụng Framework Kiểm thử Playwright Python

## Giới thiệu

Framework này cung cấp các công cụ và template để kiểm thử tự động ứng dụng web sử dụng Python và Playwright. Framework đã được cấu trúc theo mô hình Page Object Model (POM) để dễ bảo trì và mở rộng.

## Tính năng chính

### 1. Kiểm thử Đăng nhập (Login Tests)
- Test đăng nhập thành công với thông tin hợp lệ
- Test đăng nhập thất bại với thông tin không hợp lệ
- Test với username/password trống
- Test chức năng "Remember Me"
- Test chức năng đăng xuất
- Test bảo mật (SQL injection, XSS)

**File**: `tests/test_login.py`

### 2. Kiểm thử Form (Form Tests)
- Test điền thông tin cá nhân
- Test điền địa chỉ
- Test validation form
- Test submit form
- Test reset form
- Test các trường bắt buộc
- Test format email, số điện thoại

**File**: `tests/test_form.py`

### 3. Kiểm thử UI (UI Tests)
- Test các thành phần giao diện (navigation, footer, logo)
- Test responsive design (mobile, tablet, desktop)
- Test buttons và links
- Test accessibility (alt text cho images)
- Test hover effects
- Test keyboard navigation
- Test modals và tooltips
- Test scroll functionality

**File**: `tests/test_ui.py`

### 4. Kiểm thử Luồng người dùng (User Flow Tests)
- Test luồng đăng ký hoàn chỉnh
- Test luồng đăng nhập đến dashboard
- Test luồng submit form
- Test luồng đăng nhập -> thao tác -> đăng xuất
- Test navigation giữa các trang
- Test browser back/forward
- Test luồng tìm kiếm và filter
- Test luồng mua hàng (e-commerce)

**File**: `tests/test_user_flow.py`

## Page Objects

Framework sử dụng Page Object Model để tổ chức code:

### BasePage (`pages/base_page.py`)
Class cơ sở chứa các methods dùng chung:
- `navigate(url)` - Điều hướng đến URL
- `click_element(selector)` - Click vào element
- `fill_input(selector, text)` - Điền text vào input
- `is_visible(selector)` - Kiểm tra element có hiển thị
- `take_screenshot(filename)` - Chụp màn hình
- `select_option(selector, value)` - Chọn option từ dropdown
- `check_checkbox(selector)` - Check checkbox
- `hover_element(selector)` - Hover vào element

### LoginPage (`pages/login_page.py`)
Class cho trang login:
- `login(username, password, remember_me)` - Thực hiện login
- `logout()` - Thực hiện logout
- `is_logged_in()` - Kiểm tra đã login
- `get_error_message()` - Lấy error message
- `click_forgot_password()` - Click forgot password link

### FormPage (`pages/form_page.py`)
Class cho trang form:
- `fill_personal_info(...)` - Điền thông tin cá nhân
- `fill_address_info(...)` - Điền thông tin địa chỉ
- `fill_complete_form(data)` - Điền toàn bộ form
- `submit_form()` - Submit form
- `reset_form()` - Reset form
- `select_gender(gender)` - Chọn giới tính
- `accept_terms()` - Chấp nhận điều khoản
- `get_validation_errors()` - Lấy lỗi validation

## Cách sử dụng

### Chạy tests bằng Test Runner

```bash
# Chạy tất cả tests
python run_tests.py all

# Chạy theo category
python run_tests.py login
python run_tests.py form
python run_tests.py ui
python run_tests.py flow

# Chạy smoke tests (tests quan trọng nhất)
python run_tests.py smoke

# Chạy regression tests
python run_tests.py regression

# Chạy với browser hiển thị (để debug)
python run_tests.py headed

# Chạy một test cụ thể
python run_tests.py test tests/test_login.py::TestLogin::test_successful_login
```

### Chạy tests bằng pytest trực tiếp

```bash
# Chạy tất cả tests
pytest tests/ -v

# Chạy theo marker
pytest -m login -v
pytest -m form -v
pytest -m ui -v
pytest -m flow -v
pytest -m smoke -v

# Chạy một file cụ thể
pytest tests/test_login.py -v

# Chạy với nhiều workers (parallel)
pytest tests/ -n auto

# Chạy với browser cụ thể
pytest tests/ --browser chromium
pytest tests/ --browser firefox
pytest tests/ --browser webkit

# Chạy với headed mode
pytest tests/ --headed

# Slow motion (để xem rõ hơn)
pytest tests/ --headed --slowmo=1000
```

## Cấu hình

### pytest.ini
Cấu hình chính của pytest:
- Patterns để discover tests
- Output options
- Markers definition
- Report settings

### conftest.py
Fixtures và configuration:
- Browser context settings
- Viewport configuration
- Locale và timezone (Việt Nam)
- Test data fixtures

### config.py
Configuration cho test environment:
- Base URLs cho các môi trường (dev, staging, production)
- Test users
- Browser settings
- Timeout settings
- Screenshot settings

## Viết test mới

### Ví dụ 1: Test đơn giản

```python
import pytest
from playwright.sync_api import Page

@pytest.mark.smoke
def test_home_page_loads(page: Page):
    """Test trang chủ load thành công."""
    page.goto("https://example.com")
    assert "Example" in page.title()
```

### Ví dụ 2: Sử dụng Page Object

```python
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

@pytest.mark.login
def test_login_success(page: Page):
    """Test đăng nhập thành công."""
    login_page = LoginPage(page)
    login_page.navigate("https://example.com/login")
    login_page.login("user@example.com", "password123")
    assert login_page.is_logged_in()
```

### Ví dụ 3: Sử dụng fixture

```python
import pytest
from playwright.sync_api import Page

@pytest.mark.form
def test_submit_form(page: Page, sample_form_data: dict):
    """Test submit form với data từ fixture."""
    from pages.form_page import FormPage
    
    form_page = FormPage(page)
    form_page.navigate("https://example.com/form")
    form_page.fill_complete_form(sample_form_data)
    form_page.submit_form()
    
    assert form_page.get_success_message()
```

### Ví dụ 4: Test class

```python
import pytest
from playwright.sync_api import Page

@pytest.mark.ui
class TestNavigation:
    """Test suite cho navigation."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup trước mỗi test."""
        self.base_url = "https://example.com"
        page.goto(self.base_url)
    
    def test_menu_visible(self, page: Page):
        """Test menu hiển thị."""
        assert page.locator("nav").is_visible()
    
    def test_logo_clickable(self, page: Page):
        """Test logo có thể click."""
        page.click(".logo")
        assert page.url == self.base_url
```

## Tùy chỉnh cho dự án của bạn

### Bước 1: Cập nhật URLs

Sửa file `config.py`:

```python
ENVIRONMENTS = {
    "dev": "https://dev.yoursite.com",
    "staging": "https://staging.yoursite.com",
    "production": "https://yoursite.com"
}
```

### Bước 2: Cập nhật selectors

Sửa các Page Objects trong thư mục `pages/`:

```python
# Ví dụ: pages/login_page.py
class LoginPage(BasePage):
    # Cập nhật selectors theo website của bạn
    USERNAME_INPUT = "#email"  # thay vì #username
    PASSWORD_INPUT = "#pass"   # thay vì #password
    LOGIN_BUTTON = "button.login-btn"  # thay vì button[type='submit']
```

### Bước 3: Thêm Page Objects mới

Tạo file mới trong `pages/`:

```python
# pages/dashboard_page.py
from pages.base_page import BasePage

class DashboardPage(BasePage):
    # Định nghĩa selectors
    WELCOME_MESSAGE = ".welcome"
    USER_MENU = "#user-menu"
    
    def get_welcome_message(self):
        return self.get_text(self.WELCOME_MESSAGE)
    
    def click_user_menu(self):
        self.click_element(self.USER_MENU)
```

### Bước 4: Thêm test data

Sửa file `tests/test_data/test_data.py` hoặc `conftest.py`:

```python
@pytest.fixture
def my_test_data():
    return {
        "field1": "value1",
        "field2": "value2"
    }
```

## Reports

Sau khi chạy tests, reports được tạo trong thư mục `reports/`:

- `report.html` - Báo cáo tổng hợp
- `login_report.html` - Báo cáo login tests
- `form_report.html` - Báo cáo form tests
- `ui_report.html` - Báo cáo UI tests
- `flow_report.html` - Báo cáo flow tests

Mở file HTML trong browser để xem báo cáo chi tiết với:
- Kết quả từng test case
- Thời gian chạy
- Error messages
- Screenshots (nếu có)

## Debug

### Xem browser khi chạy test

```bash
pytest tests/ --headed --slowmo=1000
```

### Chạy một test cụ thể với debug

```bash
pytest tests/test_login.py::test_successful_login -v --headed --slowmo=500
```

### Sử dụng Python debugger

```bash
pytest tests/test_login.py --pdb
```

### Chụp screenshot khi lỗi

Thêm vào test:

```python
def test_example(page: Page):
    try:
        # test code
        pass
    except Exception as e:
        page.screenshot(path="error_screenshot.png")
        raise e
```

## Best Practices

1. **Sử dụng Page Object Model** - Tách logic tương tác với UI vào Page Objects
2. **Sử dụng markers** - Phân loại tests để dễ chạy nhóm cụ thể
3. **Sử dụng fixtures** - Tái sử dụng setup code và test data
4. **Wait cho elements** - Sử dụng `wait_for_selector()` thay vì `time.sleep()`
5. **Assertions rõ ràng** - Viết assertions với messages mô tả lỗi
6. **Smoke tests** - Đánh dấu tests quan trọng nhất bằng marker `@pytest.mark.smoke`
7. **Independent tests** - Mỗi test nên độc lập, không phụ thuộc vào test khác
8. **Clean up** - Đảm bảo logout/cleanup sau mỗi test
9. **Readable test names** - Đặt tên test mô tả rõ ràng chức năng được test
10. **Screenshots** - Chụp screenshots khi test fail để debug

## CI/CD

Framework đã được cấu hình với GitHub Actions. Workflow sẽ tự động chạy khi:
- Push code lên branch main hoặc develop
- Tạo Pull Request
- Trigger manually

Workflow file: `.github/workflows/playwright-tests.yml`

## Troubleshooting

### Lỗi: Browser not found

```bash
python -m playwright install chromium
```

### Lỗi: Timeout

Tăng timeout trong test:

```python
page.wait_for_selector("element", timeout=60000)  # 60 seconds
```

### Lỗi: Element not found

Kiểm tra selector:

```python
# In ra tất cả elements matching
elements = page.locator("your-selector").all()
print(f"Found {len(elements)} elements")
```

### Lỗi: Tests chạy chậm

Chạy parallel:

```bash
pytest tests/ -n auto
```

## Tài liệu tham khảo

- [Playwright Python Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model](https://playwright.dev/python/docs/pom)
- [Selectors Guide](https://playwright.dev/python/docs/selectors)
- [Best Practices](https://playwright.dev/python/docs/best-practices)
