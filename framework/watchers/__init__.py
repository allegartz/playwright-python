"""
Watchers Module

Advanced monitoring and event tracking:
- DOM change detection
- Network request monitoring
- Console message tracking
- Performance monitoring
"""

from .dom_watcher import DOMWatcher
from .network_watcher import NetworkWatcher
from .console_watcher import ConsoleWatcher
from .performance_watcher import PerformanceWatcher

__all__ = [
    'DOMWatcher',
    'NetworkWatcher',
    'ConsoleWatcher',
    'PerformanceWatcher',
]
