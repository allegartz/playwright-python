"""
Worker Pool

Dynamic worker pool management:
- Worker lifecycle
- Work distribution
- Health monitoring
"""

from typing import Optional, Callable, Any
from threading import Thread, Event
from queue import Queue
import time
from loguru import logger


class Worker(Thread):
    """
    Worker thread for task execution
    
    Features:
    - Task execution
    - Health monitoring
    - Graceful shutdown
    """
    
    def __init__(self, worker_id: int, task_queue: Queue, result_queue: Queue, stop_event: Event):
        """
        Initialize worker
        
        Args:
            worker_id: Unique worker identifier
            task_queue: Queue to get tasks from
            result_queue: Queue to put results in
            stop_event: Event to signal shutdown
        """
        super().__init__()
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.stop_event = stop_event
        self.tasks_processed = 0
        self.daemon = True
        
        logger.debug(f"Worker {self.worker_id} initialized")
    
    def run(self):
        """Worker main loop"""
        logger.info(f"Worker {self.worker_id} started")
        
        while not self.stop_event.is_set():
            try:
                # Get task with timeout
                task = self.task_queue.get(timeout=1)
                
                if task is None:  # Poison pill
                    break
                
                # Execute task
                result = self._execute_task(task)
                
                # Put result
                self.result_queue.put(result)
                
                self.tasks_processed += 1
                self.task_queue.task_done()
                
            except Exception as e:
                if not self.stop_event.is_set():
                    logger.error(f"Worker {self.worker_id} error: {e}")
        
        logger.info(f"Worker {self.worker_id} stopped (processed {self.tasks_processed} tasks)")
    
    def _execute_task(self, task: dict) -> dict:
        """
        Execute a task
        
        Args:
            task: Task dictionary
            
        Returns:
            Result dictionary
        """
        task_id = task.get('task_id', 'unknown')
        func = task.get('func')
        args = task.get('args', [])
        kwargs = task.get('kwargs', {})
        
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            return {
                'task_id': task_id,
                'worker_id': self.worker_id,
                'success': True,
                'result': result,
                'duration': duration
            }
        except Exception as e:
            duration = time.time() - start_time
            
            return {
                'task_id': task_id,
                'worker_id': self.worker_id,
                'success': False,
                'error': str(e),
                'duration': duration
            }


class WorkerPool:
    """
    Manage a pool of worker threads
    
    Features:
    - Dynamic worker scaling
    - Task distribution
    - Result collection
    - Health monitoring
    
    Example:
        pool = WorkerPool(size=4)
        pool.start()
        pool.submit_task(my_func, args=[1, 2])
        results = pool.get_results()
        pool.stop()
    """
    
    def __init__(self, size: int = 4):
        """
        Initialize worker pool
        
        Args:
            size: Number of workers
        """
        self.size = size
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.stop_event = Event()
        self.workers = []
        self._started = False
        
        logger.info(f"Worker pool initialized with {size} workers")
    
    def start(self):
        """Start all workers"""
        if self._started:
            logger.warning("Worker pool already started")
            return
        
        for i in range(self.size):
            worker = Worker(i, self.task_queue, self.result_queue, self.stop_event)
            worker.start()
            self.workers.append(worker)
        
        self._started = True
        logger.info(f"Worker pool started with {self.size} workers")
    
    def submit_task(self, func: Callable, task_id: str = None, *args, **kwargs):
        """
        Submit a task to the pool
        
        Args:
            func: Callable to execute
            task_id: Optional task identifier
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        if not self._started:
            self.start()
        
        task = {
            'func': func,
            'task_id': task_id or f"task_{time.time()}",
            'args': args,
            'kwargs': kwargs
        }
        
        self.task_queue.put(task)
    
    def get_result(self, timeout: Optional[float] = None) -> Optional[dict]:
        """
        Get a result from the queue
        
        Args:
            timeout: Optional timeout in seconds
            
        Returns:
            Result dictionary or None
        """
        try:
            return self.result_queue.get(timeout=timeout)
        except:
            return None
    
    def get_all_results(self, timeout: Optional[float] = None) -> list:
        """
        Get all available results
        
        Args:
            timeout: Optional timeout in seconds
            
        Returns:
            List of result dictionaries
        """
        results = []
        
        while True:
            result = self.get_result(timeout=0.1)
            if result is None:
                break
            results.append(result)
        
        return results
    
    def wait_for_completion(self):
        """Wait for all tasks to complete"""
        self.task_queue.join()
    
    def stop(self, wait: bool = True):
        """
        Stop all workers
        
        Args:
            wait: Wait for workers to finish
        """
        if not self._started:
            return
        
        logger.info("Stopping worker pool...")
        
        # Signal workers to stop
        self.stop_event.set()
        
        # Send poison pills
        for _ in self.workers:
            self.task_queue.put(None)
        
        if wait:
            # Wait for workers to finish
            for worker in self.workers:
                worker.join(timeout=5)
        
        self.workers.clear()
        self._started = False
        
        logger.info("Worker pool stopped")
    
    def resize(self, new_size: int):
        """
        Resize the worker pool
        
        Args:
            new_size: New pool size
        """
        if new_size == self.size:
            return
        
        if new_size > self.size:
            # Add workers
            for i in range(self.size, new_size):
                worker = Worker(i, self.task_queue, self.result_queue, self.stop_event)
                worker.start()
                self.workers.append(worker)
            logger.info(f"Worker pool expanded to {new_size} workers")
        else:
            # Remove workers
            workers_to_remove = self.size - new_size
            for _ in range(workers_to_remove):
                self.task_queue.put(None)
            logger.info(f"Worker pool reduced to {new_size} workers")
        
        self.size = new_size
    
    def get_statistics(self) -> dict:
        """
        Get pool statistics
        
        Returns:
            Statistics dictionary
        """
        total_processed = sum(w.tasks_processed for w in self.workers)
        alive_workers = sum(1 for w in self.workers if w.is_alive())
        
        return {
            'pool_size': self.size,
            'alive_workers': alive_workers,
            'total_tasks_processed': total_processed,
            'pending_tasks': self.task_queue.qsize(),
            'pending_results': self.result_queue.qsize()
        }
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
