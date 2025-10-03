"""
Task Manager

Manages test task lifecycle:
- Task registration
- Dependency tracking
- Priority queuing
- Retry logic
"""

from typing import List, Dict, Any, Optional, Callable
from queue import PriorityQueue, Queue
from dataclasses import dataclass, field
from enum import Enum
import uuid
from loguru import logger
from datetime import datetime


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 3
    NORMAL = 2
    HIGH = 1
    CRITICAL = 0


@dataclass
class Task:
    """
    Represents a test task
    
    Attributes:
        func: Callable to execute
        task_id: Unique task identifier
        priority: Task priority
        args: Positional arguments
        kwargs: Keyword arguments
        dependencies: List of task IDs this task depends on
        max_retries: Maximum retry attempts
        timeout: Task timeout in seconds
    """
    func: Callable
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    priority: TaskPriority = TaskPriority.NORMAL
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    max_retries: int = 2
    timeout: Optional[float] = None
    status: TaskStatus = TaskStatus.PENDING
    retry_count: int = 0
    result: Any = None
    error: Optional[Exception] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __lt__(self, other):
        """Compare tasks by priority for queue ordering"""
        return self.priority.value < other.priority.value


class TaskManager:
    """
    Manage task execution lifecycle
    
    Features:
    - Task queuing with priority
    - Dependency resolution
    - Retry logic
    - Task history
    
    Example:
        manager = TaskManager()
        task = Task(func=my_test, priority=TaskPriority.HIGH)
        manager.add_task(task)
        next_task = manager.get_next_task()
    """
    
    def __init__(self):
        """Initialize task manager"""
        self._task_queue = PriorityQueue()
        self._tasks: Dict[str, Task] = {}
        self._completed_tasks: List[Task] = []
        self._failed_tasks: List[Task] = []
        
        logger.info("Task manager initialized")
    
    def add_task(self, task: Task) -> str:
        """
        Add task to queue
        
        Args:
            task: Task object
            
        Returns:
            Task ID
        """
        self._tasks[task.task_id] = task
        self._task_queue.put(task)
        
        logger.debug(f"Task added: {task.task_id} (priority={task.priority.name})")
        return task.task_id
    
    def create_task(
        self,
        func: Callable,
        priority: TaskPriority = TaskPriority.NORMAL,
        dependencies: List[str] = None,
        max_retries: int = 2,
        timeout: Optional[float] = None,
        *args,
        **kwargs
    ) -> str:
        """
        Create and add a new task
        
        Args:
            func: Callable to execute
            priority: Task priority
            dependencies: Task dependencies
            max_retries: Maximum retry attempts
            timeout: Task timeout
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Task ID
        """
        task = Task(
            func=func,
            priority=priority,
            args=args,
            kwargs=kwargs,
            dependencies=dependencies or [],
            max_retries=max_retries,
            timeout=timeout
        )
        
        return self.add_task(task)
    
    def get_next_task(self) -> Optional[Task]:
        """
        Get next task from queue
        
        Returns:
            Next task or None if queue is empty
        """
        if self._task_queue.empty():
            return None
        
        while not self._task_queue.empty():
            task = self._task_queue.get()
            
            # Check dependencies
            if self._check_dependencies(task):
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now()
                logger.debug(f"Task ready: {task.task_id}")
                return task
            else:
                # Re-queue if dependencies not met
                self._task_queue.put(task)
                logger.debug(f"Task dependencies not met: {task.task_id}")
                return None
        
        return None
    
    def _check_dependencies(self, task: Task) -> bool:
        """
        Check if all task dependencies are completed
        
        Args:
            task: Task to check
            
        Returns:
            True if all dependencies completed, False otherwise
        """
        if not task.dependencies:
            return True
        
        for dep_id in task.dependencies:
            dep_task = self._tasks.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        
        return True
    
    def mark_completed(self, task: Task, result: Any = None):
        """
        Mark task as completed
        
        Args:
            task: Task object
            result: Task result
        """
        task.status = TaskStatus.COMPLETED
        task.result = result
        task.completed_at = datetime.now()
        
        self._completed_tasks.append(task)
        logger.info(f"Task completed: {task.task_id}")
    
    def mark_failed(self, task: Task, error: Exception):
        """
        Mark task as failed or retry
        
        Args:
            task: Task object
            error: Exception that caused failure
        """
        task.error = error
        
        if task.retry_count < task.max_retries:
            task.retry_count += 1
            task.status = TaskStatus.RETRYING
            self._task_queue.put(task)
            logger.warning(f"Task retry {task.retry_count}/{task.max_retries}: {task.task_id}")
        else:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            self._failed_tasks.append(task)
            logger.error(f"Task failed: {task.task_id} - {str(error)}")
    
    def cancel_task(self, task_id: str):
        """
        Cancel a task
        
        Args:
            task_id: Task ID to cancel
        """
        task = self._tasks.get(task_id)
        if task:
            task.status = TaskStatus.CANCELLED
            logger.info(f"Task cancelled: {task_id}")
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get task by ID
        
        Args:
            task_id: Task ID
            
        Returns:
            Task object or None
        """
        return self._tasks.get(task_id)
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks"""
        return [t for t in self._tasks.values() if t.status == TaskStatus.PENDING]
    
    def get_running_tasks(self) -> List[Task]:
        """Get all running tasks"""
        return [t for t in self._tasks.values() if t.status == TaskStatus.RUNNING]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks"""
        return self._completed_tasks
    
    def get_failed_tasks(self) -> List[Task]:
        """Get all failed tasks"""
        return self._failed_tasks
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get task statistics
        
        Returns:
            Statistics dictionary
        """
        total = len(self._tasks)
        pending = len(self.get_pending_tasks())
        running = len(self.get_running_tasks())
        completed = len(self._completed_tasks)
        failed = len(self._failed_tasks)
        
        return {
            'total': total,
            'pending': pending,
            'running': running,
            'completed': completed,
            'failed': failed,
            'success_rate': completed / total * 100 if total > 0 else 0
        }
    
    def clear(self):
        """Clear all tasks"""
        while not self._task_queue.empty():
            try:
                self._task_queue.get_nowait()
            except:
                break
        
        self._tasks.clear()
        self._completed_tasks.clear()
        self._failed_tasks.clear()
        
        logger.info("Task manager cleared")
