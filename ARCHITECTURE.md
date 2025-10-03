# Framework Architecture

## Overview

This document describes the architecture of the Playwright Python Test Automation Framework.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Test Layer                                       │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐            │
│  │   Unit Tests   │  │Integration Tests│  │  Example Tests │            │
│  └────────────────┘  └────────────────┘  └────────────────┘            │
└─────────────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Page Object Layer                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐            │
│  │   LoginPage    │  │   HomePage     │  │  Custom Pages  │            │
│  └────────────────┘  └────────────────┘  └────────────────┘            │
└─────────────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       Core Framework                                     │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                    Base Components                            │      │
│  │  • BaseTest      • BasePage      • ConfigManager             │      │
│  │  • BrowserManager                                            │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                  Smart Handlers                               │      │
│  │  • SmartLocator  • ElementHandler  • WaitStrategy            │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                   Watchers                                    │      │
│  │  • DOMWatcher    • NetworkWatcher  • ConsoleWatcher          │      │
│  │  • PerformanceWatcher                                        │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │              Execution Engine                                 │      │
│  │  • ParallelExecutor  • TaskManager  • WorkerPool             │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                  Coordinator                                  │      │
│  │  • FlowCoordinator  • StateManager  • EventBus               │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │              Design Patterns                                  │      │
│  │  • Factory  • Strategy  • Observer  • Builder                │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                   Utilities                                   │      │
│  │  • Logger  • Reporter  • Helpers                             │      │
│  └──────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Playwright API                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Core Components (`framework/core/`)

#### BaseTest
- Base class for all tests
- Automatic browser setup/teardown
- Screenshot on failure
- Pytest fixtures integration

#### BasePage
- Base Page Object Model class
- Common element interaction methods
- Smart waiting strategies
- Reusable page actions

#### ConfigManager
- Singleton configuration manager
- YAML and environment variable support
- Nested configuration access
- Runtime configuration updates

#### BrowserManager
- Browser lifecycle management
- Context pooling
- Thread-safe operations
- Video and screenshot capture

### 2. Watchers (`framework/watchers/`)

#### DOMWatcher
- Monitor DOM mutations
- Track element additions/removals
- Attribute change detection
- Text content monitoring

#### NetworkWatcher
- Track HTTP requests/responses
- Request/response timing
- Failed request detection
- Resource type filtering

#### ConsoleWatcher
- Capture console messages
- Error/warning detection
- Message filtering
- Event callbacks

#### PerformanceWatcher
- Navigation timing metrics
- Resource performance
- Custom performance marks
- Performance budgets

### 3. Execution Engine (`framework/engine/`)

#### ParallelExecutor
- Thread/process-based execution
- Task submission and tracking
- Result aggregation
- Statistics collection

#### TaskManager
- Task lifecycle management
- Dependency tracking
- Priority queuing
- Retry logic

#### WorkerPool
- Dynamic worker scaling
- Work distribution
- Health monitoring
- Graceful shutdown

### 4. Smart Handlers (`framework/handlers/`)

#### SmartLocator
- Multiple locator strategies
- Auto-healing locators
- Fallback mechanisms
- Cache support

#### ElementHandler
- Auto-retry on failure
- Element state validation
- Fluent interface
- Error handling

#### WaitStrategy
- Flexible wait conditions
- Custom polling
- Multiple wait types
- Timeout management

### 5. Coordinator (`framework/coordinator/`)

#### FlowCoordinator
- Step sequencing
- Conditional execution
- Error recovery
- Flow statistics

#### StateManager
- Thread-safe state storage
- State persistence
- State history
- Nested access

#### EventBus
- Publish-subscribe pattern
- Event filtering
- Event history
- Async handling

### 6. Design Patterns (`framework/patterns/`)

#### Factory
- Page object creation
- Test data generation
- Reusable factories

#### Strategy
- Retry strategies
- Loading strategies
- Pluggable algorithms

#### Observer
- Event monitoring
- Test observation
- Notification system

#### Builder
- Fluent test building
- Configuration construction
- Step-by-step creation

### 7. Utilities (`framework/utils/`)

#### Logger
- Structured logging
- File and console output
- Log rotation
- Custom formatting

#### Reporter
- HTML report generation
- JSON report export
- Test statistics
- Result aggregation

#### Helpers
- Retry decorator
- Wait utilities
- Duration formatting
- Safe execution

## Data Flow

```
Test Execution Flow:
┌──────────┐
│  pytest  │
└────┬─────┘
     ▼
┌──────────────┐
│  BaseTest    │ ◄─── ConfigManager
└────┬─────────┘
     ▼
┌──────────────┐
│BrowserManager│
└────┬─────────┘
     ▼
┌──────────────┐
│   Page       │
└────┬─────────┘
     ▼
┌──────────────┐
│ BasePage/    │ ◄─── SmartLocator
│ ElementHandler│ ◄─── WaitStrategy
└────┬─────────┘
     ▼
┌──────────────┐
│  Watchers    │ ◄─── DOM/Network/Console/Performance
└────┬─────────┘
     ▼
┌──────────────┐
│  Reporter    │ ─────► HTML/JSON Reports
└──────────────┘
```

## Extension Points

### Adding New Page Objects
```python
from framework.core.page_base import BasePage

class NewPage(BasePage):
    @property
    def url(self) -> str:
        return "/new-page"
    
    # Add custom methods
```

### Adding New Watchers
```python
from framework.watchers.base_watcher import BaseWatcher

class CustomWatcher(BaseWatcher):
    def start(self):
        # Implementation
        pass
```

### Adding New Patterns
```python
from framework.patterns.base_pattern import BasePattern

class NewPattern(BasePattern):
    # Implementation
    pass
```

## Configuration Flow

```
Environment Variables (.env)
         ▼
YAML Config (config.yaml)
         ▼
ConfigManager (singleton)
         ▼
Framework Components
```

## Thread Safety

- ConfigManager: Singleton with thread lock
- StateManager: Thread-safe with locks
- EventBus: Thread-safe operations
- BrowserManager: Thread-local browser instances

## Best Practices

1. **Modularity**: Keep components independent
2. **Reusability**: Use Page Objects and Factories
3. **Observability**: Enable watchers for debugging
4. **Parallelism**: Use execution engine for performance
5. **Configuration**: Externalize configuration
6. **Logging**: Use structured logging
7. **Testing**: Write tests for new features

## Performance Considerations

- Browser instance pooling reduces startup overhead
- Parallel execution for faster test runs
- Smart waiting reduces unnecessary delays
- Element caching for repeated lookups
- Worker pool for concurrent tasks

## Security

- No secrets in code
- Environment variables for sensitive data
- Screenshot sanitization
- Log redaction options

## Scalability

- Horizontal scaling with parallel execution
- Vertical scaling with worker pool
- Distributed execution ready
- Cloud deployment compatible
