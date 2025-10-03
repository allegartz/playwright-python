"""
Concurrent Execution Engine

Parallel test execution with:
- Thread pool management
- Process pool management
- Task queue
- Result aggregation
"""

from .executor import ParallelExecutor
from .task_manager import TaskManager
from .worker_pool import WorkerPool

__all__ = [
    'ParallelExecutor',
    'TaskManager',
    'WorkerPool',
]
