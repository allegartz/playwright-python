"""
Advanced Patterns Module

Design patterns and optimizations:
- Factory pattern for object creation
- Strategy pattern for algorithms
- Observer pattern for notifications
- Singleton pattern
- Builder pattern
"""

from .factory import PageFactory, TestDataFactory
from .strategy import RetryStrategy, LoadingStrategy
from .observer import TestObserver
from .builder import TestBuilder

__all__ = [
    'PageFactory',
    'TestDataFactory',
    'RetryStrategy',
    'LoadingStrategy',
    'TestObserver',
    'TestBuilder',
]
