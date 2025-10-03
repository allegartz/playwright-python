"""
Strategy Pattern

Strategy classes for different behaviors:
- Retry strategies
- Loading strategies
- Wait strategies
"""

from typing import Callable, Any, Optional
from loguru import logger
import time
from abc import ABC, abstractmethod


class RetryStrategy(ABC):
    """Base retry strategy"""
    
    @abstractmethod
    def should_retry(self, attempt: int, error: Exception) -> bool:
        """Determine if should retry"""
        pass
    
    @abstractmethod
    def get_delay(self, attempt: int) -> float:
        """Get delay before retry"""
        pass


class FixedRetryStrategy(RetryStrategy):
    """Fixed interval retry strategy"""
    
    def __init__(self, max_attempts: int = 3, delay: float = 1.0):
        self.max_attempts = max_attempts
        self.delay = delay
    
    def should_retry(self, attempt: int, error: Exception) -> bool:
        return attempt < self.max_attempts
    
    def get_delay(self, attempt: int) -> float:
        return self.delay


class ExponentialRetryStrategy(RetryStrategy):
    """Exponential backoff retry strategy"""
    
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def should_retry(self, attempt: int, error: Exception) -> bool:
        return attempt < self.max_attempts
    
    def get_delay(self, attempt: int) -> float:
        delay = self.base_delay * (2 ** attempt)
        return min(delay, self.max_delay)


class LoadingStrategy(ABC):
    """Base loading strategy"""
    
    @abstractmethod
    def wait_for_load(self, page: Any):
        """Wait for page to load"""
        pass


class NetworkIdleStrategy(LoadingStrategy):
    """Wait for network idle"""
    
    def __init__(self, timeout: int = 30000):
        self.timeout = timeout
    
    def wait_for_load(self, page: Any):
        page.wait_for_load_state("networkidle", timeout=self.timeout)
        logger.debug("Page loaded (network idle)")


class DOMContentLoadedStrategy(LoadingStrategy):
    """Wait for DOM content loaded"""
    
    def __init__(self, timeout: int = 30000):
        self.timeout = timeout
    
    def wait_for_load(self, page: Any):
        page.wait_for_load_state("domcontentloaded", timeout=self.timeout)
        logger.debug("Page loaded (DOM content loaded)")


class CustomElementStrategy(LoadingStrategy):
    """Wait for custom element"""
    
    def __init__(self, selector: str, timeout: int = 30000):
        self.selector = selector
        self.timeout = timeout
    
    def wait_for_load(self, page: Any):
        page.wait_for_selector(self.selector, state="visible", timeout=self.timeout)
        logger.debug(f"Page loaded (element visible: {self.selector})")
