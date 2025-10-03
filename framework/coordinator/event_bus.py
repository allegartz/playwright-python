"""
Event Bus

Event-driven communication system:
- Publish-subscribe pattern
- Event filtering
- Async event handling
- Event history
"""

from typing import Callable, Dict, List, Any
from loguru import logger
from datetime import datetime
import threading


class Event:
    """Represents an event"""
    
    def __init__(self, name: str, data: Any = None):
        self.name = name
        self.data = data
        self.timestamp = datetime.now()
    
    def __repr__(self):
        return f"Event(name={self.name}, timestamp={self.timestamp})"


class EventBus:
    """
    Event bus for publish-subscribe communication
    
    Features:
    - Subscribe to events
    - Publish events
    - Event filtering
    - Event history
    
    Example:
        bus = EventBus()
        bus.subscribe("test_started", lambda event: print(event.data))
        bus.publish("test_started", {"test_name": "login_test"})
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize event bus"""
        if not hasattr(self, '_initialized'):
            self._subscribers: Dict[str, List[Callable]] = {}
            self._history: List[Event] = []
            self._lock = threading.Lock()
            self._initialized = True
            logger.info("Event bus initialized")
    
    def subscribe(self, event_name: str, callback: Callable):
        """
        Subscribe to an event
        
        Args:
            event_name: Name of event to subscribe to
            callback: Function to call when event is published
        """
        with self._lock:
            if event_name not in self._subscribers:
                self._subscribers[event_name] = []
            
            self._subscribers[event_name].append(callback)
            logger.debug(f"Subscribed to event: {event_name}")
    
    def unsubscribe(self, event_name: str, callback: Callable):
        """
        Unsubscribe from an event
        
        Args:
            event_name: Event name
            callback: Callback to remove
        """
        with self._lock:
            if event_name in self._subscribers:
                try:
                    self._subscribers[event_name].remove(callback)
                    logger.debug(f"Unsubscribed from event: {event_name}")
                except ValueError:
                    logger.warning(f"Callback not found for event: {event_name}")
    
    def publish(self, event_name: str, data: Any = None):
        """
        Publish an event
        
        Args:
            event_name: Event name
            data: Event data
        """
        event = Event(event_name, data)
        
        with self._lock:
            self._history.append(event)
        
        # Notify subscribers
        subscribers = self._subscribers.get(event_name, [])
        
        for callback in subscribers:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Error in event callback for {event_name}: {e}")
        
        logger.debug(f"Event published: {event_name}")
    
    def get_history(self, event_name: str = None) -> List[Event]:
        """
        Get event history
        
        Args:
            event_name: Optional filter by event name
            
        Returns:
            List of events
        """
        with self._lock:
            if event_name:
                return [e for e in self._history if e.name == event_name]
            return self._history.copy()
    
    def clear_history(self):
        """Clear event history"""
        with self._lock:
            self._history.clear()
            logger.info("Event history cleared")
    
    def clear_subscribers(self, event_name: str = None):
        """
        Clear subscribers
        
        Args:
            event_name: Optional event name (clears all if not provided)
        """
        with self._lock:
            if event_name:
                if event_name in self._subscribers:
                    self._subscribers[event_name].clear()
                    logger.info(f"Cleared subscribers for: {event_name}")
            else:
                self._subscribers.clear()
                logger.info("All subscribers cleared")
