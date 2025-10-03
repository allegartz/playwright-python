# Playwright Python Test Automation Framework

Advanced test automation framework built with Playwright and Python, featuring intelligent element handling, parallel execution, comprehensive monitoring, and production-ready patterns.

## 🎯 Features

### 1. Core Concept
- **Base Test Class**: Foundation for all tests with automatic setup/teardown
- **Page Object Model**: Structured page object pattern with reusable components
- **Configuration Management**: Flexible configuration with YAML/environment variables
- **Browser Management**: Smart browser lifecycle and context pooling

### 2. Advanced Watcher Implementation
- **DOM Watcher**: Monitor DOM changes and mutations in real-time
- **Network Watcher**: Track HTTP requests/responses with filtering
- **Console Watcher**: Capture and analyze browser console messages
- **Performance Watcher**: Measure page load times and resource performance

### 3. Concurrent Execution Engine
- **Parallel Executor**: Thread and process-based parallel test execution
- **Task Manager**: Advanced task scheduling with dependencies and priorities
- **Worker Pool**: Dynamic worker pool with health monitoring

### 4. Smart Element Handling
- **Smart Locator**: Multiple fallback strategies for element location
- **Element Handler**: Auto-retry mechanisms with intelligent waiting
- **Wait Strategies**: Flexible waiting conditions and custom strategies

### 5. Coordination with Main Flow
- **Flow Coordinator**: Orchestrate complex test flows with conditional steps
- **State Manager**: Thread-safe state management with persistence
- **Event Bus**: Publish-subscribe event system for component communication

### 6. Advanced Patterns & Optimizations
- **Factory Pattern**: Page and test data factories
- **Strategy Pattern**: Pluggable retry and loading strategies
- **Observer Pattern**: Event-driven test monitoring
- **Builder Pattern**: Fluent test configuration builders

### 7. Production-Ready Implementation
- **Logging**: Structured logging with Loguru
- **Reporting**: HTML and JSON test reports
- **Error Handling**: Comprehensive error recovery mechanisms
- **CI/CD**: GitHub Actions workflow configuration

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/allegartz/playwright-python.git
cd playwright-python

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## 🚀 Quick Start

### Basic Test Example

```python
from framework.core.base_test import BaseTest
from examples.pages.login_page import LoginPage

class TestLogin(BaseTest):
    def test_login(self, page):
        # Create page object
        login_page = LoginPage(page)
        
        # Navigate and interact
        login_page.navigate()
        login_page.login("user@example.com", "password123")
        
        # Assertions
        self.assert_text_present(page, "Dashboard")
```

### Smart Element Handling

```python
from framework.handlers.element_handler import ElementHandler

handler = ElementHandler(page)

# Auto-retry with multiple locator strategies
handler.fill("john@example.com", id="email", placeholder="Email")
handler.click(text="Submit", role="button")
```

### Network Monitoring

```python
from framework.watchers.network_watcher import NetworkWatcher

watcher = NetworkWatcher(page)
watcher.start()

# Perform actions...
page.goto("https://example.com")

# Analyze requests
requests = watcher.get_requests()
failed = watcher.get_failed_requests()
```

### Flow Coordination

```python
from framework.coordinator.flow_coordinator import FlowCoordinator

coordinator = FlowCoordinator()

coordinator.add_step("login", login_action)
coordinator.add_step("navigate", nav_action, condition=lambda: is_logged_in())
coordinator.add_step("verify", verify_action, retry_on_failure=True)

success = coordinator.execute()
```

## 📁 Project Structure

```
playwright-python/
├── framework/
│   ├── core/              # Core framework components
│   │   ├── base_test.py
│   │   ├── page_base.py
│   │   ├── config_manager.py
│   │   └── browser_manager.py
│   ├── watchers/          # Monitoring components
│   │   ├── dom_watcher.py
│   │   ├── network_watcher.py
│   │   ├── console_watcher.py
│   │   └── performance_watcher.py
│   ├── engine/            # Parallel execution
│   │   ├── executor.py
│   │   ├── task_manager.py
│   │   └── worker_pool.py
│   ├── handlers/          # Smart element handling
│   │   ├── element_locator.py
│   │   ├── element_handler.py
│   │   └── wait_strategies.py
│   ├── coordinator/       # Flow coordination
│   │   ├── flow_coordinator.py
│   │   ├── state_manager.py
│   │   └── event_bus.py
│   ├── patterns/          # Design patterns
│   │   ├── factory.py
│   │   ├── strategy.py
│   │   ├── observer.py
│   │   └── builder.py
│   └── utils/             # Utilities
│       ├── logger.py
│       ├── reporter.py
│       └── helpers.py
├── config/                # Configuration files
│   ├── config.yaml
│   └── .env.example
├── examples/              # Example tests
│   ├── pages/
│   └── test_login.py
├── tests/                 # Your tests here
├── .github/workflows/     # CI/CD configuration
├── requirements.txt
├── setup.py
└── pytest.ini
```

## ⚙️ Configuration

### YAML Configuration (`config/config.yaml`)

```yaml
browser:
  browser_type: chromium
  headless: true
  viewport_width: 1920
  viewport_height: 1080

timeouts:
  default_timeout: 30000
  element_timeout: 10000

execution:
  parallel_workers: 4
  retry_failed: 2
```

### Environment Variables (`.env`)

```bash
BROWSER_TYPE=chromium
HEADLESS=true
BASE_URL=https://example.com
PARALLEL_WORKERS=4
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest examples/test_login.py

# Run with markers
pytest -m smoke

# Run in parallel
pytest -n 4

# Generate HTML report
pytest --html=reports/report.html
```

## 📊 Reporting

The framework generates comprehensive test reports:

- **HTML Reports**: Interactive test results with statistics
- **JSON Reports**: Machine-readable test data
- **Logs**: Detailed execution logs with Loguru
- **Screenshots**: Automatic screenshots on test failures

## 🔧 Advanced Usage

### Custom Page Object

```python
from framework.core.page_base import BasePage

class MyPage(BasePage):
    @property
    def url(self) -> str:
        return "/my-page"
    
    def custom_action(self):
        self.click_element("#button")
        self.wait_for_selector(".result")
        return self.get_text(".result")
```

### Parallel Test Execution

```python
from framework.engine.executor import ParallelExecutor

executor = ParallelExecutor(workers=4, mode='thread')

tasks = [
    {'func': test1, 'task_id': 'test1'},
    {'func': test2, 'task_id': 'test2'},
]

results = executor.execute_all(tasks)
```

### Test Data Generation

```python
from framework.patterns.factory import TestDataFactory

factory = TestDataFactory()
user = factory.create_user()
address = factory.create_address()
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Built with:
- [Playwright](https://playwright.dev/) - Browser automation
- [Pytest](https://pytest.org/) - Testing framework
- [Loguru](https://github.com/Delgan/loguru) - Logging
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation

## 📧 Contact

For questions or issues, please open an issue on GitHub.
