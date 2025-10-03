# Quick Start Guide - Playwright Python Testing

## 🚀 Cài đặt nhanh (5 phút)

### 1. Clone repository
```bash
git clone https://github.com/allegartz/playwright-python.git
cd playwright-python
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Cài đặt Playwright browsers
```bash
python -m playwright install chromium
```

### 4. Chạy smoke tests để kiểm tra
```bash
python run_tests.py smoke
```

## ✅ Chạy test đầu tiên

### Test example đơn giản
```bash
pytest tests/test_examples.py -v
```

### Chạy với browser hiển thị (để xem)
```bash
pytest tests/test_examples.py --headed -v
```

## 📝 Tùy chỉnh cho website của bạn

### Bước 1: Cập nhật URL trong config.py

```python
# config.py
ENVIRONMENTS = {
    "production": "https://your-website.com"
}

URLS = {
    "login": "/login",      # Đường dẫn login của bạn
    "form": "/contact",     # Đường dẫn form của bạn
}
```

### Bước 2: Cập nhật selectors trong pages/

```python
# pages/login_page.py
class LoginPage(BasePage):
    # Thay đổi selectors phù hợp với website của bạn
    USERNAME_INPUT = "#email"        # Selector của input username
    PASSWORD_INPUT = "#password"     # Selector của input password
    LOGIN_BUTTON = "button.login"    # Selector của button login
```

**Tip**: Sử dụng DevTools (F12) để tìm selectors:
1. Mở website
2. Right-click element → Inspect
3. Copy selector

### Bước 3: Viết test đầu tiên

Tạo file `tests/test_my_website.py`:

```python
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

@pytest.mark.smoke
def test_my_login(page: Page):
    """Test login vào website của tôi."""
    login_page = LoginPage(page)
    
    # Điều hướng đến trang login
    login_page.navigate("https://your-website.com/login")
    
    # Đăng nhập
    login_page.login("your-email@example.com", "your-password")
    
    # Verify đăng nhập thành công
    assert login_page.is_logged_in()
```

### Bước 4: Chạy test của bạn

```bash
pytest tests/test_my_website.py -v --headed
```

## 🎯 Các commands thường dùng

### Chạy tất cả tests
```bash
python run_tests.py all
```

### Chạy tests theo category
```bash
python run_tests.py login    # Login tests
python run_tests.py form     # Form tests
python run_tests.py ui       # UI tests
python run_tests.py flow     # User flow tests
```

### Chạy smoke tests (tests quan trọng nhất)
```bash
python run_tests.py smoke
```

### Chạy với browser hiển thị
```bash
python run_tests.py headed
```

### Xem reports
Sau khi chạy tests, mở file `reports/report.html` trong browser

## 📖 Ví dụ tests thường dùng

### Test 1: Login
```python
@pytest.mark.login
def test_login(page: Page):
    from pages.login_page import LoginPage
    
    login_page = LoginPage(page)
    login_page.navigate("https://example.com/login")
    login_page.login("user@example.com", "password123")
    
    assert login_page.is_logged_in()
```

### Test 2: Fill form
```python
@pytest.mark.form
def test_contact_form(page: Page):
    from pages.form_page import FormPage
    
    form_page = FormPage(page)
    form_page.navigate("https://example.com/contact")
    
    form_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    }
    
    form_page.fill_personal_info(
        form_data["first_name"],
        form_data["last_name"],
        form_data["email"]
    )
    form_page.submit_form()
    
    assert form_page.get_success_message()
```

### Test 3: UI elements
```python
@pytest.mark.ui
def test_homepage_elements(page: Page):
    page.goto("https://example.com")
    
    # Verify logo
    assert page.locator(".logo").is_visible()
    
    # Verify menu
    assert page.locator("nav").is_visible()
    
    # Verify title
    assert "Example" in page.title()
```

### Test 4: User flow
```python
@pytest.mark.flow
def test_complete_flow(page: Page):
    # Step 1: Go to homepage
    page.goto("https://example.com")
    
    # Step 2: Click login
    page.click("a[href='/login']")
    
    # Step 3: Login
    page.fill("#email", "user@example.com")
    page.fill("#password", "password123")
    page.click("button[type='submit']")
    
    # Step 4: Verify dashboard
    assert "dashboard" in page.url
```

## 🔍 Debug tips

### Chạy test chậm để xem rõ
```bash
pytest tests/test_my_website.py --headed --slowmo=1000
```

### Chụp screenshot
```python
def test_example(page: Page):
    page.goto("https://example.com")
    page.screenshot(path="screenshot.png")
```

### In ra element để debug
```python
def test_example(page: Page):
    page.goto("https://example.com")
    
    # Đếm số buttons
    buttons = page.locator("button")
    print(f"Found {buttons.count()} buttons")
    
    # In text của element
    text = page.locator("h1").text_content()
    print(f"Title: {text}")
```

## 💡 Tips

1. **Luôn chạy smoke tests trước** - Đảm bảo các chức năng chính hoạt động
2. **Sử dụng --headed khi debug** - Xem browser để hiểu test đang làm gì
3. **Sử dụng Page Objects** - Tổ chức code tốt hơn, dễ maintain
4. **Thêm markers** - Phân loại tests để dễ chạy từng nhóm
5. **Xem reports** - Reports HTML có nhiều thông tin hữu ích

## 🆘 Gặp vấn đề?

### Browser không được cài đặt
```bash
python -m playwright install chromium
```

### Selector không tìm thấy element
- Kiểm tra selector bằng DevTools (F12)
- Thử wait cho element: `page.wait_for_selector("your-selector")`
- Thử các selector khác: id, class, text, role

### Test timeout
- Tăng timeout: `page.wait_for_selector("element", timeout=60000)`
- Kiểm tra mạng có chậm không
- Kiểm tra website có load lâu không

### Tests fail ngẫu nhiên
- Thêm wait: `page.wait_for_load_state("networkidle")`
- Thêm explicit waits thay vì implicit waits
- Kiểm tra race conditions

## 📚 Đọc thêm

- `README.md` - Tổng quan dự án
- `GUIDE.md` - Hướng dẫn chi tiết
- [Playwright Python Docs](https://playwright.dev/python/)

## 🎉 Bắt đầu thôi!

```bash
# Clone và setup
git clone https://github.com/allegartz/playwright-python.git
cd playwright-python
pip install -r requirements.txt
python -m playwright install chromium

# Chạy test example
pytest tests/test_examples.py --headed -v

# Tạo test của bạn trong tests/test_my_website.py
# Chạy test của bạn
pytest tests/test_my_website.py --headed -v
```

Chúc bạn testing vui vẻ! 🚀
