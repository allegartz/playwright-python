"""
Configuration Manager

Handles all framework configuration including:
- Environment variables
- Test settings
- Browser configurations
- Timeout values
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv


class BrowserConfig(BaseModel):
    """Browser configuration settings"""
    browser_type: str = Field(default="chromium", description="Browser type: chromium, firefox, webkit")
    headless: bool = Field(default=True, description="Run browser in headless mode")
    slow_mo: int = Field(default=0, description="Slow down operations by specified milliseconds")
    viewport_width: int = Field(default=1920, description="Viewport width")
    viewport_height: int = Field(default=1080, description="Viewport height")
    video_dir: Optional[str] = Field(default=None, description="Directory to save videos")
    screenshot_dir: str = Field(default="screenshots", description="Directory to save screenshots")


class TimeoutConfig(BaseModel):
    """Timeout configuration settings"""
    default_timeout: int = Field(default=30000, description="Default timeout in milliseconds")
    navigation_timeout: int = Field(default=30000, description="Navigation timeout in milliseconds")
    element_timeout: int = Field(default=10000, description="Element interaction timeout in milliseconds")


class ExecutionConfig(BaseModel):
    """Test execution configuration"""
    parallel_workers: int = Field(default=4, description="Number of parallel workers")
    retry_failed: int = Field(default=2, description="Number of retries for failed tests")
    capture_trace: bool = Field(default=True, description="Capture trace on failure")


class FrameworkConfig(BaseModel):
    """Main framework configuration"""
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    timeouts: TimeoutConfig = Field(default_factory=TimeoutConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    base_url: str = Field(default="", description="Base URL for tests")
    environment: str = Field(default="dev", description="Test environment")


class ConfigManager:
    """
    Singleton configuration manager for the framework
    
    Usage:
        config = ConfigManager.get_instance()
        browser_type = config.get("browser.browser_type")
    """
    
    _instance: Optional['ConfigManager'] = None
    _config: FrameworkConfig = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'ConfigManager':
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """Initialize configuration manager"""
        if self._config is None:
            self._load_config()
    
    def _load_config(self):
        """Load configuration from environment and files"""
        # Load environment variables
        load_dotenv()
        
        # Try to load from YAML config file
        config_path = Path(os.getenv("CONFIG_PATH", "config/config.yaml"))
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
                self._config = FrameworkConfig(**config_data)
        else:
            # Use default configuration
            self._config = FrameworkConfig()
        
        # Override with environment variables
        self._override_from_env()
    
    def _override_from_env(self):
        """Override configuration with environment variables"""
        env_mappings = {
            "BROWSER_TYPE": ("browser", "browser_type"),
            "HEADLESS": ("browser", "headless"),
            "BASE_URL": ("base_url",),
            "ENVIRONMENT": ("environment",),
            "PARALLEL_WORKERS": ("execution", "parallel_workers"),
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                self._set_nested_value(config_path, value)
    
    def _set_nested_value(self, path: tuple, value: Any):
        """Set nested configuration value"""
        current = self._config
        for key in path[:-1]:
            current = getattr(current, key)
        
        # Convert value to appropriate type
        field_type = type(getattr(current, path[-1]))
        if field_type == bool:
            value = value.lower() in ('true', '1', 'yes')
        elif field_type == int:
            value = int(value)
        
        setattr(current, path[-1], value)
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation path
        
        Args:
            path: Dot-notation path (e.g., "browser.browser_type")
            default: Default value if path not found
            
        Returns:
            Configuration value
        """
        keys = path.split('.')
        current = self._config
        
        try:
            for key in keys:
                current = getattr(current, key)
            return current
        except AttributeError:
            return default
    
    def set(self, path: str, value: Any):
        """
        Set configuration value by dot-notation path
        
        Args:
            path: Dot-notation path (e.g., "browser.browser_type")
            value: Value to set
        """
        keys = path.split('.')
        self._set_nested_value(tuple(keys), value)
    
    @property
    def config(self) -> FrameworkConfig:
        """Get raw configuration object"""
        return self._config
    
    def reload(self):
        """Reload configuration"""
        self._config = None
        self._load_config()
