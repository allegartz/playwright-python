"""
State Manager

Manages test state across steps and flows:
- State storage and retrieval
- State persistence
- State validation
- State snapshots
"""

from typing import Any, Dict, Optional, List
from loguru import logger
import json
from pathlib import Path
from datetime import datetime
import threading


class StateManager:
    """
    Manage test execution state
    
    Features:
    - Thread-safe state storage
    - State persistence to disk
    - State history and snapshots
    - Nested state access
    
    Example:
        state = StateManager()
        state.set("user.name", "John")
        name = state.get("user.name")
        state.save("state.json")
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
        """Initialize state manager"""
        if not hasattr(self, '_initialized'):
            self._state: Dict[str, Any] = {}
            self._history: List[Dict[str, Any]] = []
            self._lock = threading.Lock()
            self._initialized = True
            logger.info("State manager initialized")
    
    def set(self, key: str, value: Any):
        """
        Set state value (supports dot notation)
        
        Args:
            key: State key (use dot notation for nested: "user.profile.name")
            value: Value to set
        """
        with self._lock:
            keys = key.split('.')
            current = self._state
            
            # Navigate to nested dict
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            # Set value
            current[keys[-1]] = value
            logger.debug(f"State set: {key} = {value}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get state value (supports dot notation)
        
        Args:
            key: State key
            default: Default value if not found
            
        Returns:
            State value or default
        """
        with self._lock:
            keys = key.split('.')
            current = self._state
            
            try:
                for k in keys:
                    current = current[k]
                return current
            except (KeyError, TypeError):
                return default
    
    def has(self, key: str) -> bool:
        """
        Check if state key exists
        
        Args:
            key: State key
            
        Returns:
            True if exists, False otherwise
        """
        return self.get(key) is not None
    
    def delete(self, key: str):
        """
        Delete state key
        
        Args:
            key: State key to delete
        """
        with self._lock:
            keys = key.split('.')
            current = self._state
            
            try:
                for k in keys[:-1]:
                    current = current[k]
                del current[keys[-1]]
                logger.debug(f"State deleted: {key}")
            except (KeyError, TypeError):
                logger.warning(f"State key not found: {key}")
    
    def update(self, updates: Dict[str, Any]):
        """
        Update multiple state values
        
        Args:
            updates: Dictionary of key-value pairs
        """
        for key, value in updates.items():
            self.set(key, value)
        logger.debug(f"State updated with {len(updates)} values")
    
    def clear(self):
        """Clear all state"""
        with self._lock:
            self._state.clear()
            logger.info("State cleared")
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all state
        
        Returns:
            State dictionary copy
        """
        with self._lock:
            return self._state.copy()
    
    def snapshot(self):
        """Create a snapshot of current state"""
        with self._lock:
            snapshot = {
                'timestamp': datetime.now().isoformat(),
                'state': self._state.copy()
            }
            self._history.append(snapshot)
            logger.debug("State snapshot created")
    
    def restore_snapshot(self, index: int = -1):
        """
        Restore state from snapshot
        
        Args:
            index: Snapshot index (-1 for latest)
        """
        with self._lock:
            if not self._history:
                logger.warning("No snapshots available")
                return
            
            snapshot = self._history[index]
            self._state = snapshot['state'].copy()
            logger.info(f"State restored from snapshot: {snapshot['timestamp']}")
    
    def save(self, filepath: str):
        """
        Save state to file
        
        Args:
            filepath: Path to save file
        """
        with self._lock:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w') as f:
                json.dump(self._state, f, indent=2, default=str)
            
            logger.info(f"State saved to: {filepath}")
    
    def load(self, filepath: str):
        """
        Load state from file
        
        Args:
            filepath: Path to load file
        """
        with self._lock:
            path = Path(filepath)
            
            if not path.exists():
                logger.warning(f"State file not found: {filepath}")
                return
            
            with open(path, 'r') as f:
                self._state = json.load(f)
            
            logger.info(f"State loaded from: {filepath}")
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get state history
        
        Returns:
            List of state snapshots
        """
        with self._lock:
            return self._history.copy()
    
    def clear_history(self):
        """Clear state history"""
        with self._lock:
            self._history.clear()
            logger.info("State history cleared")
