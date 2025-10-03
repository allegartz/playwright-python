"""
Framework Core Module

This module contains the fundamental classes and structures for the test framework.
"""

from .base_test import BaseTest
from .page_base import BasePage
from .config_manager import ConfigManager
from .browser_manager import BrowserManager

__all__ = [
    'BaseTest',
    'BasePage',
    'ConfigManager',
    'BrowserManager',
]
