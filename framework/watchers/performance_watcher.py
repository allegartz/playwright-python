"""
Performance Watcher

Monitors performance metrics:
- Page load time
- Resource timing
- Navigation timing
- Custom performance marks
"""

from typing import Dict, Any, List, Optional
from playwright.sync_api import Page
from loguru import logger
import threading
from datetime import datetime


class PerformanceWatcher:
    """
    Monitor page performance metrics
    
    Features:
    - Page load timing
    - Resource performance
    - Navigation timing
    - Custom performance marks
    - Performance budgets
    
    Example:
        watcher = PerformanceWatcher(page)
        watcher.start()
        # ... perform actions ...
        metrics = watcher.get_metrics()
    """
    
    def __init__(self, page: Page):
        """
        Initialize performance watcher
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.is_watching = False
        self._metrics: Dict[str, Any] = {}
        self._marks: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
    
    def start(self):
        """Start watching performance"""
        if self.is_watching:
            logger.warning("Performance watcher already started")
            return
        
        # Inject performance monitoring script
        self.page.evaluate("""
            (() => {
                if (!window.__performanceWatcher) {
                    window.__performanceWatcher = {
                        marks: [],
                        measures: []
                    };
                }
            })();
        """)
        
        self.is_watching = True
        logger.info("Performance watcher started")
    
    def stop(self):
        """Stop watching performance"""
        if not self.is_watching:
            return
        
        self.is_watching = False
        logger.info("Performance watcher stopped")
    
    def get_navigation_timing(self) -> Dict[str, Any]:
        """
        Get navigation timing metrics
        
        Returns:
            Navigation timing data
        """
        timing = self.page.evaluate("""
            (() => {
                const timing = performance.timing;
                const navigation = performance.navigation;
                
                return {
                    navigationStart: timing.navigationStart,
                    domainLookupStart: timing.domainLookupStart,
                    domainLookupEnd: timing.domainLookupEnd,
                    connectStart: timing.connectStart,
                    connectEnd: timing.connectEnd,
                    requestStart: timing.requestStart,
                    responseStart: timing.responseStart,
                    responseEnd: timing.responseEnd,
                    domLoading: timing.domLoading,
                    domInteractive: timing.domInteractive,
                    domContentLoadedEventStart: timing.domContentLoadedEventStart,
                    domContentLoadedEventEnd: timing.domContentLoadedEventEnd,
                    domComplete: timing.domComplete,
                    loadEventStart: timing.loadEventStart,
                    loadEventEnd: timing.loadEventEnd,
                    navigationType: navigation.type,
                    redirectCount: navigation.redirectCount
                };
            })();
        """)
        
        # Calculate derived metrics
        if timing:
            nav_start = timing.get('navigationStart', 0)
            timing['dnsTime'] = timing.get('domainLookupEnd', 0) - timing.get('domainLookupStart', 0)
            timing['tcpTime'] = timing.get('connectEnd', 0) - timing.get('connectStart', 0)
            timing['requestTime'] = timing.get('responseStart', 0) - timing.get('requestStart', 0)
            timing['responseTime'] = timing.get('responseEnd', 0) - timing.get('responseStart', 0)
            timing['domLoadingTime'] = timing.get('domComplete', 0) - timing.get('domLoading', 0)
            timing['totalLoadTime'] = timing.get('loadEventEnd', 0) - nav_start
        
        with self._lock:
            self._metrics['navigation'] = timing
        
        return timing
    
    def get_resource_timing(self) -> List[Dict[str, Any]]:
        """
        Get resource timing metrics
        
        Returns:
            List of resource timing entries
        """
        resources = self.page.evaluate("""
            (() => {
                const resources = performance.getEntriesByType('resource');
                return resources.map(entry => ({
                    name: entry.name,
                    initiatorType: entry.initiatorType,
                    duration: entry.duration,
                    startTime: entry.startTime,
                    responseEnd: entry.responseEnd,
                    transferSize: entry.transferSize || 0,
                    encodedBodySize: entry.encodedBodySize || 0,
                    decodedBodySize: entry.decodedBodySize || 0
                }));
            })();
        """)
        
        with self._lock:
            self._metrics['resources'] = resources
        
        return resources or []
    
    def get_paint_timing(self) -> Dict[str, Any]:
        """
        Get paint timing metrics (First Paint, First Contentful Paint)
        
        Returns:
            Paint timing data
        """
        paint_timing = self.page.evaluate("""
            (() => {
                const paints = performance.getEntriesByType('paint');
                const result = {};
                paints.forEach(paint => {
                    result[paint.name] = paint.startTime;
                });
                return result;
            })();
        """)
        
        with self._lock:
            self._metrics['paint'] = paint_timing
        
        return paint_timing or {}
    
    def mark(self, name: str):
        """
        Create a performance mark
        
        Args:
            name: Mark name
        """
        self.page.evaluate(f"""
            (() => {{
                performance.mark('{name}');
                window.__performanceWatcher.marks.push({{
                    name: '{name}',
                    timestamp: Date.now()
                }});
            }})();
        """)
        
        logger.info(f"Performance mark created: {name}")
    
    def measure(self, name: str, start_mark: str, end_mark: str) -> float:
        """
        Measure duration between two marks
        
        Args:
            name: Measure name
            start_mark: Start mark name
            end_mark: End mark name
            
        Returns:
            Duration in milliseconds
        """
        duration = self.page.evaluate(f"""
            (() => {{
                performance.measure('{name}', '{start_mark}', '{end_mark}');
                const measure = performance.getEntriesByName('{name}', 'measure')[0];
                window.__performanceWatcher.measures.push({{
                    name: '{name}',
                    duration: measure.duration,
                    timestamp: Date.now()
                }});
                return measure.duration;
            }})();
        """)
        
        logger.info(f"Performance measure '{name}': {duration}ms")
        return duration
    
    def get_marks(self) -> List[Dict[str, Any]]:
        """
        Get all performance marks
        
        Returns:
            List of marks
        """
        marks = self.page.evaluate("""
            (() => {
                return window.__performanceWatcher.marks;
            })();
        """)
        
        return marks or []
    
    def get_measures(self) -> List[Dict[str, Any]]:
        """
        Get all performance measures
        
        Returns:
            List of measures
        """
        measures = self.page.evaluate("""
            (() => {
                return window.__performanceWatcher.measures;
            })();
        """)
        
        return measures or []
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all performance metrics
        
        Returns:
            Combined metrics object
        """
        metrics = {
            'navigation': self.get_navigation_timing(),
            'resources': self.get_resource_timing(),
            'paint': self.get_paint_timing(),
            'marks': self.get_marks(),
            'measures': self.get_measures(),
        }
        
        with self._lock:
            self._metrics.update(metrics)
        
        return metrics
    
    def check_budget(self, budget: Dict[str, float]) -> Dict[str, bool]:
        """
        Check if performance metrics meet budget constraints
        
        Args:
            budget: Dictionary of metric names and max values (in ms)
            
        Returns:
            Dictionary of metric names and pass/fail status
        """
        metrics = self.get_metrics()
        results = {}
        
        for metric_name, max_value in budget.items():
            actual_value = None
            
            # Check navigation timing
            if metric_name in metrics.get('navigation', {}):
                actual_value = metrics['navigation'][metric_name]
            
            # Check paint timing
            elif metric_name in metrics.get('paint', {}):
                actual_value = metrics['paint'][metric_name]
            
            if actual_value is not None:
                results[metric_name] = actual_value <= max_value
                if not results[metric_name]:
                    logger.warning(
                        f"Performance budget exceeded for {metric_name}: "
                        f"{actual_value}ms > {max_value}ms"
                    )
        
        return results
    
    def clear_metrics(self):
        """Clear all collected metrics"""
        with self._lock:
            self._metrics.clear()
        
        self.page.evaluate("""
            (() => {
                if (window.__performanceWatcher) {
                    window.__performanceWatcher.marks = [];
                    window.__performanceWatcher.measures = [];
                }
            })();
        """)
        
        logger.info("Performance metrics cleared")
