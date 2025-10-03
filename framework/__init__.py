"""
Playwright Python Test Automation Framework

A comprehensive test automation framework featuring:
- Core testing infrastructure
- Advanced monitoring with watchers
- Parallel execution engine
- Smart element handling
- Flow coordination
- Design patterns and optimizations
- Production-ready utilities
"""

__version__ = "1.0.0"
__author__ = "Playwright Test Team"

# Core imports
from framework.core import BaseTest, BasePage, ConfigManager, BrowserManager

# Watchers
from framework.watchers import (
    DOMWatcher,
    NetworkWatcher,
    ConsoleWatcher,
    PerformanceWatcher,
)

# Execution engine
from framework.engine import ParallelExecutor, TaskManager, WorkerPool

# Handlers
from framework.handlers import SmartLocator, ElementHandler, WaitStrategy

# Coordinator
from framework.coordinator import FlowCoordinator, StateManager, EventBus

# Patterns
from framework.patterns import (
    PageFactory,
    TestDataFactory,
    RetryStrategy,
    LoadingStrategy,
    TestObserver,
    TestBuilder,
)

# Utils
from framework.utils import setup_logger, get_logger, TestReporter, HTMLReporter

__all__ = [
    # Core
    "BaseTest",
    "BasePage",
    "ConfigManager",
    "BrowserManager",
    # Watchers
    "DOMWatcher",
    "NetworkWatcher",
    "ConsoleWatcher",
    "PerformanceWatcher",
    # Engine
    "ParallelExecutor",
    "TaskManager",
    "WorkerPool",
    # Handlers
    "SmartLocator",
    "ElementHandler",
    "WaitStrategy",
    # Coordinator
    "FlowCoordinator",
    "StateManager",
    "EventBus",
    # Patterns
    "PageFactory",
    "TestDataFactory",
    "RetryStrategy",
    "LoadingStrategy",
    "TestObserver",
    "TestBuilder",
    # Utils
    "setup_logger",
    "get_logger",
    "TestReporter",
    "HTMLReporter",
]
