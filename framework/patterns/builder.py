"""
Builder Pattern

Builder classes for constructing complex objects
"""

from typing import Any, Dict, Optional, List
from loguru import logger


class TestBuilder:
    """
    Builder for constructing test configurations
    
    Example:
        test = TestBuilder() \\
            .with_name("Login Test") \\
            .with_timeout(30000) \\
            .with_retry(3) \\
            .build()
    """
    
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._steps: List[Dict[str, Any]] = []
    
    def with_name(self, name: str) -> 'TestBuilder':
        """Set test name"""
        self._config['name'] = name
        return self
    
    def with_timeout(self, timeout: int) -> 'TestBuilder':
        """Set test timeout"""
        self._config['timeout'] = timeout
        return self
    
    def with_retry(self, max_retries: int) -> 'TestBuilder':
        """Set retry count"""
        self._config['max_retries'] = max_retries
        return self
    
    def with_tags(self, *tags: str) -> 'TestBuilder':
        """Set test tags"""
        self._config['tags'] = list(tags)
        return self
    
    def add_step(self, name: str, action: Any, **kwargs) -> 'TestBuilder':
        """Add test step"""
        step = {'name': name, 'action': action}
        step.update(kwargs)
        self._steps.append(step)
        return self
    
    def with_setup(self, setup_func: Any) -> 'TestBuilder':
        """Set setup function"""
        self._config['setup'] = setup_func
        return self
    
    def with_teardown(self, teardown_func: Any) -> 'TestBuilder':
        """Set teardown function"""
        self._config['teardown'] = teardown_func
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build test configuration"""
        config = self._config.copy()
        config['steps'] = self._steps.copy()
        logger.debug(f"Built test config: {config.get('name', 'unnamed')}")
        return config
