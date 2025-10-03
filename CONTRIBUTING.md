# Contributing to Playwright Python Framework

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/playwright-python.git
   cd playwright-python
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

## Development Workflow

### Creating a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### Code Style

We follow PEP 8 guidelines with some exceptions:

- Maximum line length: 100 characters
- Use double quotes for strings
- Use type hints where appropriate

Format your code:
```bash
black framework/ tests/ examples/
isort framework/ tests/ examples/
```

Lint your code:
```bash
flake8 framework/ tests/ examples/
```

### Writing Tests

- Add tests for new features in `tests/`
- Follow existing test patterns
- Use descriptive test names
- Add docstrings to test classes and methods

Example:
```python
class TestNewFeature(BaseTest):
    """Tests for new feature"""
    
    def test_feature_works_correctly(self, page):
        """Test that feature behaves as expected"""
        # Arrange
        # Act
        # Assert
        pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_framework_integration.py

# Run with coverage
pytest --cov=framework --cov-report=html
```

### Documentation

- Update README.md for significant changes
- Add docstrings to all public functions and classes
- Include examples in docstrings
- Update QUICKSTART.md if adding user-facing features

Example docstring:
```python
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description of function
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Example:
        result = my_function("test", 42)
    """
    pass
```

### Committing Changes

- Write clear, concise commit messages
- Use present tense ("Add feature" not "Added feature")
- Reference issues when applicable

```bash
git add .
git commit -m "Add smart retry mechanism for element interactions

- Implement exponential backoff
- Add configurable max attempts
- Include logging for retry attempts

Fixes #123"
```

### Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md (if exists)
5. Submit pull request with clear description

Pull request template:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Documentation updated

## Related Issues
Fixes #(issue number)
```

## Architecture Guidelines

### Framework Structure

```
framework/
├── core/          # Base classes and core functionality
├── watchers/      # Monitoring components
├── engine/        # Parallel execution
├── handlers/      # Element handling
├── coordinator/   # Flow coordination
├── patterns/      # Design patterns
└── utils/         # Utilities
```

### Design Principles

1. **Modularity**: Keep components independent and reusable
2. **Extensibility**: Design for easy extension without modification
3. **Simplicity**: Prefer simple solutions over complex ones
4. **Documentation**: Code should be self-documenting with clear names
5. **Testing**: All features should be testable

### Adding New Features

1. **Core Components**: Add to appropriate module in `framework/`
2. **Tests**: Add integration tests in `tests/`
3. **Examples**: Add usage examples in `examples/`
4. **Documentation**: Update README and add docstrings

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No breaking changes (or clearly documented)
- [ ] Performance impact considered
- [ ] Error handling is appropriate
- [ ] Logging is informative

## Questions?

Feel free to:
- Open an issue for bugs
- Start a discussion for feature requests
- Ask questions in pull request comments

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing! 🎉
