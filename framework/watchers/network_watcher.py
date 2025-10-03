"""
Network Watcher

Monitors network activity:
- HTTP requests/responses
- Request/response timing
- Failed requests
- Resource types
"""

from typing import Callable, List, Dict, Any, Optional
from playwright.sync_api import Page, Request, Response, Route
from loguru import logger
import threading
from datetime import datetime


class NetworkWatcher:
    """
    Monitor network requests and responses
    
    Features:
    - Track all network requests
    - Monitor response status codes
    - Measure request timing
    - Filter by resource type
    - Callback support
    
    Example:
        watcher = NetworkWatcher(page)
        watcher.on_request(lambda req: print(f"Request: {req.url}"))
        watcher.on_response(lambda res: print(f"Response: {res.status}"))
        watcher.start()
    """
    
    def __init__(self, page: Page):
        """
        Initialize network watcher
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.is_watching = False
        self._requests: List[Dict[str, Any]] = []
        self._responses: List[Dict[str, Any]] = []
        self._failed_requests: List[Dict[str, Any]] = []
        self._callbacks: Dict[str, List[Callable]] = {
            'request': [],
            'response': [],
            'request_finished': [],
            'request_failed': [],
        }
        self._lock = threading.Lock()
        self._filters: Dict[str, Any] = {}
    
    def start(self, filters: Optional[Dict[str, Any]] = None):
        """
        Start watching network activity
        
        Args:
            filters: Optional filters (resource_type, url_pattern, etc.)
        """
        if self.is_watching:
            logger.warning("Network watcher already started")
            return
        
        self._filters = filters or {}
        
        # Register event handlers
        self.page.on("request", self._handle_request)
        self.page.on("response", self._handle_response)
        self.page.on("requestfinished", self._handle_request_finished)
        self.page.on("requestfailed", self._handle_request_failed)
        
        self.is_watching = True
        logger.info("Network watcher started")
    
    def stop(self):
        """Stop watching network activity"""
        if not self.is_watching:
            return
        
        # Remove event handlers
        self.page.remove_listener("request", self._handle_request)
        self.page.remove_listener("response", self._handle_response)
        self.page.remove_listener("requestfinished", self._handle_request_finished)
        self.page.remove_listener("requestfailed", self._handle_request_failed)
        
        self.is_watching = False
        logger.info("Network watcher stopped")
    
    def _should_track(self, request: Request) -> bool:
        """
        Check if request should be tracked based on filters
        
        Args:
            request: Request object
            
        Returns:
            True if should track, False otherwise
        """
        if not self._filters:
            return True
        
        # Filter by resource type
        if 'resource_type' in self._filters:
            allowed_types = self._filters['resource_type']
            if isinstance(allowed_types, str):
                allowed_types = [allowed_types]
            if request.resource_type not in allowed_types:
                return False
        
        # Filter by URL pattern
        if 'url_pattern' in self._filters:
            pattern = self._filters['url_pattern']
            if pattern not in request.url:
                return False
        
        return True
    
    def _handle_request(self, request: Request):
        """Handle request event"""
        if not self._should_track(request):
            return
        
        request_data = {
            'url': request.url,
            'method': request.method,
            'resource_type': request.resource_type,
            'headers': request.headers,
            'timestamp': datetime.now().isoformat(),
        }
        
        with self._lock:
            self._requests.append(request_data)
        
        # Trigger callbacks
        for callback in self._callbacks['request']:
            try:
                callback(request)
            except Exception as e:
                logger.error(f"Error in request callback: {e}")
    
    def _handle_response(self, response: Response):
        """Handle response event"""
        request = response.request
        if not self._should_track(request):
            return
        
        response_data = {
            'url': response.url,
            'status': response.status,
            'status_text': response.status_text,
            'headers': response.headers,
            'request_method': request.method,
            'resource_type': request.resource_type,
            'timestamp': datetime.now().isoformat(),
        }
        
        with self._lock:
            self._responses.append(response_data)
        
        # Trigger callbacks
        for callback in self._callbacks['response']:
            try:
                callback(response)
            except Exception as e:
                logger.error(f"Error in response callback: {e}")
    
    def _handle_request_finished(self, request: Request):
        """Handle request finished event"""
        if not self._should_track(request):
            return
        
        # Trigger callbacks
        for callback in self._callbacks['request_finished']:
            try:
                callback(request)
            except Exception as e:
                logger.error(f"Error in request_finished callback: {e}")
    
    def _handle_request_failed(self, request: Request):
        """Handle request failed event"""
        if not self._should_track(request):
            return
        
        failure_data = {
            'url': request.url,
            'method': request.method,
            'resource_type': request.resource_type,
            'failure': request.failure,
            'timestamp': datetime.now().isoformat(),
        }
        
        with self._lock:
            self._failed_requests.append(failure_data)
        
        logger.warning(f"Request failed: {request.url}")
        
        # Trigger callbacks
        for callback in self._callbacks['request_failed']:
            try:
                callback(request)
            except Exception as e:
                logger.error(f"Error in request_failed callback: {e}")
    
    def get_requests(self, clear: bool = False) -> List[Dict[str, Any]]:
        """
        Get collected requests
        
        Args:
            clear: Clear requests after retrieving
            
        Returns:
            List of request objects
        """
        with self._lock:
            requests = self._requests.copy()
            if clear:
                self._requests.clear()
        return requests
    
    def get_responses(self, clear: bool = False) -> List[Dict[str, Any]]:
        """
        Get collected responses
        
        Args:
            clear: Clear responses after retrieving
            
        Returns:
            List of response objects
        """
        with self._lock:
            responses = self._responses.copy()
            if clear:
                self._responses.clear()
        return responses
    
    def get_failed_requests(self, clear: bool = False) -> List[Dict[str, Any]]:
        """
        Get failed requests
        
        Args:
            clear: Clear failed requests after retrieving
            
        Returns:
            List of failed request objects
        """
        with self._lock:
            failed = self._failed_requests.copy()
            if clear:
                self._failed_requests.clear()
        return failed
    
    def on_request(self, callback: Callable):
        """
        Register callback for requests
        
        Args:
            callback: Function to call on request
        """
        self._callbacks['request'].append(callback)
    
    def on_response(self, callback: Callable):
        """
        Register callback for responses
        
        Args:
            callback: Function to call on response
        """
        self._callbacks['response'].append(callback)
    
    def on_request_finished(self, callback: Callable):
        """
        Register callback for finished requests
        
        Args:
            callback: Function to call on request finished
        """
        self._callbacks['request_finished'].append(callback)
    
    def on_request_failed(self, callback: Callable):
        """
        Register callback for failed requests
        
        Args:
            callback: Function to call on request failed
        """
        self._callbacks['request_failed'].append(callback)
    
    def get_by_resource_type(self, resource_type: str) -> List[Dict[str, Any]]:
        """
        Get requests by resource type
        
        Args:
            resource_type: Resource type (document, stylesheet, image, etc.)
            
        Returns:
            List of matching requests
        """
        with self._lock:
            return [r for r in self._requests if r.get('resource_type') == resource_type]
    
    def get_by_status(self, status: int) -> List[Dict[str, Any]]:
        """
        Get responses by status code
        
        Args:
            status: HTTP status code
            
        Returns:
            List of matching responses
        """
        with self._lock:
            return [r for r in self._responses if r.get('status') == status]
    
    def clear_all(self):
        """Clear all collected data"""
        with self._lock:
            self._requests.clear()
            self._responses.clear()
            self._failed_requests.clear()
        logger.info("Network watcher data cleared")
