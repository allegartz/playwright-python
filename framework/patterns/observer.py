"""
Observer Pattern

Observer classes for monitoring and notifications
"""

from typing import List, Callable, Any
from loguru import logger
from abc import ABC, abstractmethod


class Observer(ABC):
    """Base observer interface"""
    
    @abstractmethod
    def update(self, subject: 'Subject', event: str, data: Any = None):
        """Update observer with event"""
        pass


class Subject:
    """Subject being observed"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Attach observer"""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.debug(f"Observer attached: {observer.__class__.__name__}")
    
    def detach(self, observer: Observer):
        """Detach observer"""
        try:
            self._observers.remove(observer)
            logger.debug(f"Observer detached: {observer.__class__.__name__}")
        except ValueError:
            pass
    
    def notify(self, event: str, data: Any = None):
        """Notify all observers"""
        for observer in self._observers:
            observer.update(self, event, data)


class TestObserver(Observer):
    """Observer for test execution"""
    
    def __init__(self):
        self.events = []
    
    def update(self, subject: Subject, event: str, data: Any = None):
        """Record test event"""
        self.events.append({
            'event': event,
            'data': data,
            'subject': subject.__class__.__name__
        })
        logger.info(f"Test event: {event}")
    
    def get_events(self) -> List[dict]:
        """Get recorded events"""
        return self.events
    
    def clear_events(self):
        """Clear event history"""
        self.events.clear()
