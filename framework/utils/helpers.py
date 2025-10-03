"""
Helper Functions

Common utility functions
"""

import time
from typing import Callable, Any, Optional
from loguru import logger
from functools import wraps


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Retry decorator
    
    Args:
        max_attempts: Maximum retry attempts
        delay: Delay between retries in seconds
        exceptions: Tuple of exceptions to catch
        
    Example:
        @retry(max_attempts=3, delay=2.0)
        def flaky_function():
            # function that might fail
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed: {str(e)}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed")
            
            raise last_exception
        
        return wrapper
    return decorator


def wait_until(
    condition: Callable[[], bool],
    timeout: float = 30.0,
    poll_interval: float = 0.5,
    error_message: str = "Condition not met within timeout"
) -> bool:
    """
    Wait until condition is met
    
    Args:
        condition: Callable that returns bool
        timeout: Timeout in seconds
        poll_interval: Polling interval in seconds
        error_message: Error message if timeout
        
    Returns:
        True if condition met, False otherwise
        
    Example:
        wait_until(lambda: element.is_visible(), timeout=10)
    """
    end_time = time.time() + timeout
    
    while time.time() < end_time:
        try:
            if condition():
                return True
        except Exception as e:
            logger.debug(f"Condition check error: {e}")
        
        time.sleep(poll_interval)
    
    logger.error(error_message)
    return False


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
        
    Example:
        format_duration(3665)  # Returns "1h 1m 5s"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def safe_execute(func: Callable, default: Any = None, log_errors: bool = True) -> Any:
    """
    Safely execute function with error handling
    
    Args:
        func: Function to execute
        default: Default value on error
        log_errors: Whether to log errors
        
    Returns:
        Function result or default value
    """
    try:
        return func()
    except Exception as e:
        if log_errors:
            logger.error(f"Error executing {func.__name__}: {e}")
        return default


def timing(func: Callable) -> Callable:
    """
    Timing decorator
    
    Logs function execution time
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper
