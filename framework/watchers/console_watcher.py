"""
Console Watcher

Monitors browser console messages:
- Log messages
- Warnings
- Errors
- Custom messages
"""

from typing import Callable, List, Dict, Any
from playwright.sync_api import Page, ConsoleMessage
from loguru import logger
import threading
from datetime import datetime


class ConsoleWatcher:
    """
    Monitor browser console messages
    
    Features:
    - Track console logs, warnings, errors
    - Filter by message type
    - Callback support
    - Message history
    
    Example:
        watcher = ConsoleWatcher(page)
        watcher.on_error(lambda msg: print(f"Error: {msg.text}"))
        watcher.start()
    """
    
    def __init__(self, page: Page):
        """
        Initialize console watcher
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.is_watching = False
        self._messages: List[Dict[str, Any]] = []
        self._callbacks: Dict[str, List[Callable]] = {
            'log': [],
            'warning': [],
            'error': [],
            'info': [],
            'debug': [],
        }
        self._lock = threading.Lock()
    
    def start(self):
        """Start watching console messages"""
        if self.is_watching:
            logger.warning("Console watcher already started")
            return
        
        self.page.on("console", self._handle_console_message)
        self.is_watching = True
        logger.info("Console watcher started")
    
    def stop(self):
        """Stop watching console messages"""
        if not self.is_watching:
            return
        
        self.page.remove_listener("console", self._handle_console_message)
        self.is_watching = False
        logger.info("Console watcher stopped")
    
    def _handle_console_message(self, message: ConsoleMessage):
        """
        Handle console message event
        
        Args:
            message: ConsoleMessage object
        """
        message_data = {
            'type': message.type,
            'text': message.text,
            'location': message.location,
            'timestamp': datetime.now().isoformat(),
        }
        
        with self._lock:
            self._messages.append(message_data)
        
        # Log to our logger
        msg_type = message.type
        if msg_type == 'error':
            logger.error(f"Browser console error: {message.text}")
        elif msg_type == 'warning':
            logger.warning(f"Browser console warning: {message.text}")
        else:
            logger.debug(f"Browser console {msg_type}: {message.text}")
        
        # Trigger callbacks
        callbacks = self._callbacks.get(msg_type, [])
        for callback in callbacks:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error in console callback: {e}")
    
    def get_messages(self, msg_type: str = None, clear: bool = False) -> List[Dict[str, Any]]:
        """
        Get collected console messages
        
        Args:
            msg_type: Filter by message type (log, warning, error, etc.)
            clear: Clear messages after retrieving
            
        Returns:
            List of console message objects
        """
        with self._lock:
            if msg_type:
                messages = [m for m in self._messages if m['type'] == msg_type]
            else:
                messages = self._messages.copy()
            
            if clear:
                if msg_type:
                    self._messages = [m for m in self._messages if m['type'] != msg_type]
                else:
                    self._messages.clear()
        
        return messages
    
    def get_errors(self, clear: bool = False) -> List[Dict[str, Any]]:
        """
        Get error messages
        
        Args:
            clear: Clear errors after retrieving
            
        Returns:
            List of error messages
        """
        return self.get_messages('error', clear)
    
    def get_warnings(self, clear: bool = False) -> List[Dict[str, Any]]:
        """
        Get warning messages
        
        Args:
            clear: Clear warnings after retrieving
            
        Returns:
            List of warning messages
        """
        return self.get_messages('warning', clear)
    
    def has_errors(self) -> bool:
        """
        Check if there are any error messages
        
        Returns:
            True if errors exist, False otherwise
        """
        with self._lock:
            return any(m['type'] == 'error' for m in self._messages)
    
    def has_warnings(self) -> bool:
        """
        Check if there are any warning messages
        
        Returns:
            True if warnings exist, False otherwise
        """
        with self._lock:
            return any(m['type'] == 'warning' for m in self._messages)
    
    def on_log(self, callback: Callable):
        """
        Register callback for log messages
        
        Args:
            callback: Function to call on log message
        """
        self._callbacks['log'].append(callback)
    
    def on_warning(self, callback: Callable):
        """
        Register callback for warning messages
        
        Args:
            callback: Function to call on warning message
        """
        self._callbacks['warning'].append(callback)
    
    def on_error(self, callback: Callable):
        """
        Register callback for error messages
        
        Args:
            callback: Function to call on error message
        """
        self._callbacks['error'].append(callback)
    
    def on_info(self, callback: Callable):
        """
        Register callback for info messages
        
        Args:
            callback: Function to call on info message
        """
        self._callbacks['info'].append(callback)
    
    def on_debug(self, callback: Callable):
        """
        Register callback for debug messages
        
        Args:
            callback: Function to call on debug message
        """
        self._callbacks['debug'].append(callback)
    
    def clear_messages(self):
        """Clear all collected messages"""
        with self._lock:
            self._messages.clear()
        logger.info("Console messages cleared")
