# Playwright Python Test Framework

## Quick Start Guide

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/allegartz/playwright-python.git
   cd playwright-python
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

4. **Configure environment**
   ```bash
   cp config/.env.example .env
   # Edit .env with your settings
   ```

### Writing Your First Test

Create a test file in `tests/` directory:

```python
from framework.core.base_test import BaseTest

class TestMyApp(BaseTest):
    def test_homepage(self, page):
        # Navigate to your application
        page.goto("https://your-app.com")
        
        # Perform actions
        page.click("button[type='submit']")
        
        # Assertions
        self.assert_text_present(page, "Success")
```

### Using Page Objects

Create a page object in `tests/pages/`:

```python
from framework.core.page_base import BasePage

class HomePage(BasePage):
    @property
    def url(self) -> str:
        return "/"
    
    def search(self, query: str):
        self.fill_input("#search", query)
        self.click_element("button[type='submit']")
        return self
```

Use it in your test:

```python
def test_search(self, page):
    home = HomePage(page)
    home.navigate()
    home.search("playwright")
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_myapp.py

# Run tests with markers
pytest -m smoke

# Run in parallel (4 workers)
pytest -n 4

# Generate HTML report
pytest --html=reports/report.html --self-contained-html
```

### Using Watchers

```python
from framework.watchers.network_watcher import NetworkWatcher

def test_with_network_monitoring(self, page):
    watcher = NetworkWatcher(page)
    watcher.start()
    
    # Your test actions...
    page.goto("https://example.com")
    
    # Check network activity
    requests = watcher.get_requests()
    failed = watcher.get_failed_requests()
    
    watcher.stop()
```

### Parallel Execution

```python
from framework.engine.executor import ParallelExecutor

def my_test_function():
    # Your test logic
    pass

executor = ParallelExecutor(workers=4)
tasks = [
    {'func': my_test_function, 'task_id': 'test1'},
    {'func': my_test_function, 'task_id': 'test2'},
]
results = executor.execute_all(tasks)
```

### Configuration

Edit `config/config.yaml` for framework settings:

```yaml
browser:
  browser_type: chromium
  headless: true

timeouts:
  default_timeout: 30000

execution:
  parallel_workers: 4
```

### Best Practices

1. **Use Page Objects**: Organize page interactions into reusable page objects
2. **Leverage Watchers**: Monitor network, console, and performance
3. **Smart Element Handling**: Use ElementHandler for robust element interactions
4. **Flow Coordination**: Use FlowCoordinator for complex test scenarios
5. **Parallel Execution**: Run tests in parallel for faster feedback
6. **Proper Logging**: Use built-in logging for debugging
7. **Generate Reports**: Always generate test reports for analysis

### Troubleshooting

**Tests are slow**
- Enable parallel execution with `pytest -n 4`
- Check network timeouts in configuration

**Element not found**
- Use SmartLocator with multiple strategies
- Increase element timeout in configuration

**Tests are flaky**
- Use ElementHandler with auto-retry
- Implement proper wait strategies

### Next Steps

- Explore the `examples/` directory for more examples
- Read the full documentation in README.md
- Check out advanced patterns in `framework/patterns/`

### Getting Help

- Open an issue on GitHub
- Check the documentation
- Review example tests
