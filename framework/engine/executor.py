"""
Parallel Executor

Manages parallel test execution with support for:
- Thread-based parallelism
- Process-based parallelism
- Dynamic worker scaling
- Result collection
"""

from typing import List, Callable, Any, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future, as_completed
from loguru import logger
import time
from datetime import datetime
from ..core.config_manager import ConfigManager


class ExecutionResult:
    """Container for execution results"""
    
    def __init__(self, task_id: str, success: bool, result: Any = None, error: Exception = None, duration: float = 0):
        self.task_id = task_id
        self.success = success
        self.result = result
        self.error = error
        self.duration = duration
        self.timestamp = datetime.now()
    
    def __repr__(self):
        status = "SUCCESS" if self.success else "FAILED"
        return f"ExecutionResult(task_id={self.task_id}, status={status}, duration={self.duration:.2f}s)"


class ParallelExecutor:
    """
    Execute tasks in parallel using thread or process pools
    
    Features:
    - Thread-based or process-based execution
    - Configurable worker count
    - Timeout support
    - Result aggregation
    - Error handling
    
    Example:
        executor = ParallelExecutor(workers=4, mode='thread')
        tasks = [task1, task2, task3]
        results = executor.execute_all(tasks)
    """
    
    def __init__(self, workers: Optional[int] = None, mode: str = 'thread'):
        """
        Initialize parallel executor
        
        Args:
            workers: Number of workers (defaults to config value)
            mode: Execution mode ('thread' or 'process')
        """
        self.config = ConfigManager.get_instance()
        self.workers = workers or self.config.get("execution.parallel_workers", 4)
        self.mode = mode
        
        self._executor = None
        self._futures: List[Future] = []
        self._results: List[ExecutionResult] = []
        
        logger.info(f"Parallel executor initialized: {self.workers} workers, mode={self.mode}")
    
    def _get_executor(self):
        """Get executor instance based on mode"""
        if self._executor is None:
            if self.mode == 'thread':
                self._executor = ThreadPoolExecutor(max_workers=self.workers)
            elif self.mode == 'process':
                self._executor = ProcessPoolExecutor(max_workers=self.workers)
            else:
                raise ValueError(f"Invalid execution mode: {self.mode}")
        return self._executor
    
    def submit(self, task: Callable, task_id: str = None, *args, **kwargs) -> Future:
        """
        Submit a task for execution
        
        Args:
            task: Callable to execute
            task_id: Optional task identifier
            *args: Positional arguments for task
            **kwargs: Keyword arguments for task
            
        Returns:
            Future object
        """
        task_id = task_id or f"task_{len(self._futures)}"
        executor = self._get_executor()
        
        future = executor.submit(task, *args, **kwargs)
        future.task_id = task_id
        self._futures.append(future)
        
        logger.debug(f"Task submitted: {task_id}")
        return future
    
    def execute_all(self, tasks: List[Dict[str, Any]], timeout: Optional[float] = None) -> List[ExecutionResult]:
        """
        Execute all tasks and wait for completion
        
        Args:
            tasks: List of task dictionaries with 'func', 'args', 'kwargs', 'task_id'
            timeout: Optional timeout in seconds for all tasks
            
        Returns:
            List of ExecutionResult objects
        """
        logger.info(f"Executing {len(tasks)} tasks in parallel")
        start_time = time.time()
        
        # Submit all tasks
        for task in tasks:
            func = task['func']
            args = task.get('args', [])
            kwargs = task.get('kwargs', {})
            task_id = task.get('task_id', f"task_{len(self._futures)}")
            
            self.submit(func, task_id, *args, **kwargs)
        
        # Wait for completion
        results = []
        for future in as_completed(self._futures, timeout=timeout):
            task_id = getattr(future, 'task_id', 'unknown')
            task_start = time.time()
            
            try:
                result = future.result()
                duration = time.time() - task_start
                execution_result = ExecutionResult(
                    task_id=task_id,
                    success=True,
                    result=result,
                    duration=duration
                )
                logger.info(f"Task completed: {task_id} ({duration:.2f}s)")
            except Exception as e:
                duration = time.time() - task_start
                execution_result = ExecutionResult(
                    task_id=task_id,
                    success=False,
                    error=e,
                    duration=duration
                )
                logger.error(f"Task failed: {task_id} - {str(e)}")
            
            results.append(execution_result)
        
        total_duration = time.time() - start_time
        logger.info(f"All tasks completed in {total_duration:.2f}s")
        
        self._results.extend(results)
        return results
    
    def execute_batch(self, tasks: List[Dict[str, Any]], batch_size: int) -> List[ExecutionResult]:
        """
        Execute tasks in batches
        
        Args:
            tasks: List of task dictionaries
            batch_size: Number of tasks per batch
            
        Returns:
            List of ExecutionResult objects
        """
        all_results = []
        
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            logger.info(f"Executing batch {i // batch_size + 1} ({len(batch)} tasks)")
            results = self.execute_all(batch)
            all_results.extend(results)
            
            # Clear futures for next batch
            self._futures.clear()
        
        return all_results
    
    def map(self, func: Callable, items: List[Any], timeout: Optional[float] = None) -> List[ExecutionResult]:
        """
        Map a function over items in parallel
        
        Args:
            func: Function to apply
            items: List of items to process
            timeout: Optional timeout in seconds
            
        Returns:
            List of ExecutionResult objects
        """
        tasks = [
            {
                'func': func,
                'args': [item],
                'task_id': f"map_item_{i}"
            }
            for i, item in enumerate(items)
        ]
        
        return self.execute_all(tasks, timeout=timeout)
    
    def get_results(self) -> List[ExecutionResult]:
        """Get all execution results"""
        return self._results
    
    def get_successful_results(self) -> List[ExecutionResult]:
        """Get only successful results"""
        return [r for r in self._results if r.success]
    
    def get_failed_results(self) -> List[ExecutionResult]:
        """Get only failed results"""
        return [r for r in self._results if not r.success]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get execution statistics
        
        Returns:
            Statistics dictionary
        """
        total = len(self._results)
        successful = len(self.get_successful_results())
        failed = len(self.get_failed_results())
        
        durations = [r.duration for r in self._results]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / total * 100 if total > 0 else 0,
            'average_duration': avg_duration,
            'total_duration': sum(durations)
        }
    
    def shutdown(self, wait: bool = True):
        """
        Shutdown executor
        
        Args:
            wait: Wait for pending tasks to complete
        """
        if self._executor:
            self._executor.shutdown(wait=wait)
            self._executor = None
            logger.info("Executor shutdown")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()
