"""
DOM Watcher

Monitors DOM changes and mutations:
- Element additions/removals
- Attribute changes
- Text content changes
"""

from typing import Callable, List, Dict, Any, Optional
from playwright.sync_api import Page
from loguru import logger
import threading


class DOMWatcher:
    """
    Watch DOM changes using MutationObserver
    
    Features:
    - Track element additions/removals
    - Monitor attribute changes
    - Detect text content changes
    - Callback support for custom handling
    
    Example:
        watcher = DOMWatcher(page)
        watcher.on_element_added(lambda el: print(f"Added: {el}"))
        watcher.start()
    """
    
    def __init__(self, page: Page):
        """
        Initialize DOM watcher
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.is_watching = False
        self._mutations: List[Dict[str, Any]] = []
        self._callbacks: Dict[str, List[Callable]] = {
            'element_added': [],
            'element_removed': [],
            'attribute_changed': [],
            'text_changed': [],
        }
        self._lock = threading.Lock()
    
    def start(self, target: str = "body", options: Optional[Dict] = None):
        """
        Start watching DOM changes
        
        Args:
            target: CSS selector for target element to watch
            options: MutationObserver options
        """
        if self.is_watching:
            logger.warning("DOM watcher already started")
            return
        
        # Default options
        default_options = {
            'childList': True,
            'attributes': True,
            'subtree': True,
            'characterData': True,
            'attributeOldValue': True,
            'characterDataOldValue': True,
        }
        
        if options:
            default_options.update(options)
        
        # Inject MutationObserver script
        self.page.evaluate(f"""
            (() => {{
                if (window.__domWatcher) {{
                    return; // Already initialized
                }}
                
                window.__domWatcher = {{
                    mutations: [],
                    observer: null
                }};
                
                const target = document.querySelector('{target}');
                if (!target) {{
                    console.error('Target element not found: {target}');
                    return;
                }}
                
                const callback = (mutationsList) => {{
                    for (const mutation of mutationsList) {{
                        const mutationData = {{
                            type: mutation.type,
                            target: {{
                                tagName: mutation.target.tagName,
                                id: mutation.target.id,
                                className: mutation.target.className
                            }},
                            timestamp: Date.now()
                        }};
                        
                        if (mutation.type === 'childList') {{
                            mutationData.addedNodes = Array.from(mutation.addedNodes).map(node => ({{
                                tagName: node.tagName,
                                id: node.id,
                                className: node.className
                            }}));
                            mutationData.removedNodes = Array.from(mutation.removedNodes).map(node => ({{
                                tagName: node.tagName,
                                id: node.id,
                                className: node.className
                            }}));
                        }} else if (mutation.type === 'attributes') {{
                            mutationData.attributeName = mutation.attributeName;
                            mutationData.oldValue = mutation.oldValue;
                            mutationData.newValue = mutation.target.getAttribute(mutation.attributeName);
                        }} else if (mutation.type === 'characterData') {{
                            mutationData.oldValue = mutation.oldValue;
                            mutationData.newValue = mutation.target.textContent;
                        }}
                        
                        window.__domWatcher.mutations.push(mutationData);
                    }}
                }};
                
                const observer = new MutationObserver(callback);
                observer.observe(target, {default_options});
                window.__domWatcher.observer = observer;
                
                console.log('DOM watcher started');
            }})();
        """)
        
        self.is_watching = True
        logger.info(f"DOM watcher started for: {target}")
    
    def stop(self):
        """Stop watching DOM changes"""
        if not self.is_watching:
            return
        
        self.page.evaluate("""
            (() => {
                if (window.__domWatcher && window.__domWatcher.observer) {
                    window.__domWatcher.observer.disconnect();
                    console.log('DOM watcher stopped');
                }
            })();
        """)
        
        self.is_watching = False
        logger.info("DOM watcher stopped")
    
    def get_mutations(self, clear: bool = True) -> List[Dict[str, Any]]:
        """
        Get collected mutations
        
        Args:
            clear: Clear mutations after retrieving
            
        Returns:
            List of mutation objects
        """
        mutations = self.page.evaluate(f"""
            (() => {{
                if (!window.__domWatcher) return [];
                const mutations = window.__domWatcher.mutations;
                {f"window.__domWatcher.mutations = [];" if clear else ""}
                return mutations;
            }})();
        """)
        
        with self._lock:
            self._mutations.extend(mutations or [])
        
        return mutations or []
    
    def on_element_added(self, callback: Callable):
        """
        Register callback for element additions
        
        Args:
            callback: Function to call when element is added
        """
        self._callbacks['element_added'].append(callback)
    
    def on_element_removed(self, callback: Callable):
        """
        Register callback for element removals
        
        Args:
            callback: Function to call when element is removed
        """
        self._callbacks['element_removed'].append(callback)
    
    def on_attribute_changed(self, callback: Callable):
        """
        Register callback for attribute changes
        
        Args:
            callback: Function to call when attribute changes
        """
        self._callbacks['attribute_changed'].append(callback)
    
    def on_text_changed(self, callback: Callable):
        """
        Register callback for text changes
        
        Args:
            callback: Function to call when text changes
        """
        self._callbacks['text_changed'].append(callback)
    
    def process_mutations(self):
        """Process mutations and trigger callbacks"""
        mutations = self.get_mutations()
        
        for mutation in mutations:
            mutation_type = mutation.get('type')
            
            if mutation_type == 'childList':
                added_nodes = mutation.get('addedNodes', [])
                removed_nodes = mutation.get('removedNodes', [])
                
                for node in added_nodes:
                    for callback in self._callbacks['element_added']:
                        try:
                            callback(node)
                        except Exception as e:
                            logger.error(f"Error in element_added callback: {e}")
                
                for node in removed_nodes:
                    for callback in self._callbacks['element_removed']:
                        try:
                            callback(node)
                        except Exception as e:
                            logger.error(f"Error in element_removed callback: {e}")
            
            elif mutation_type == 'attributes':
                for callback in self._callbacks['attribute_changed']:
                    try:
                        callback(mutation)
                    except Exception as e:
                        logger.error(f"Error in attribute_changed callback: {e}")
            
            elif mutation_type == 'characterData':
                for callback in self._callbacks['text_changed']:
                    try:
                        callback(mutation)
                    except Exception as e:
                        logger.error(f"Error in text_changed callback: {e}")
    
    def clear_mutations(self):
        """Clear all collected mutations"""
        with self._lock:
            self._mutations.clear()
        
        self.page.evaluate("""
            (() => {
                if (window.__domWatcher) {
                    window.__domWatcher.mutations = [];
                }
            })();
        """)
