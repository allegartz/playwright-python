"""
Flow Coordinator

Orchestrates test execution flow:
- Step sequencing
- Conditional execution
- Parallel flow management
- Error recovery
"""

from typing import List, Callable, Dict, Any, Optional
from loguru import logger
from enum import Enum
import time
from datetime import datetime

from .state_manager import StateManager
from .event_bus import EventBus


class StepStatus(Enum):
    """Step execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class FlowStep:
    """
    Represents a single step in the test flow
    
    Attributes:
        name: Step name
        action: Callable to execute
        condition: Optional condition to check before execution
        on_success: Callback on success
        on_failure: Callback on failure
        retry_on_failure: Whether to retry on failure
        max_retries: Maximum retry attempts
    """
    
    def __init__(
        self,
        name: str,
        action: Callable,
        condition: Optional[Callable[[], bool]] = None,
        on_success: Optional[Callable] = None,
        on_failure: Optional[Callable] = None,
        retry_on_failure: bool = False,
        max_retries: int = 2
    ):
        self.name = name
        self.action = action
        self.condition = condition
        self.on_success = on_success
        self.on_failure = on_failure
        self.retry_on_failure = retry_on_failure
        self.max_retries = max_retries
        self.status = StepStatus.PENDING
        self.result = None
        self.error = None
        self.retry_count = 0
        self.start_time = None
        self.end_time = None


class FlowCoordinator:
    """
    Coordinate test flow execution
    
    Features:
    - Sequential step execution
    - Conditional steps
    - Error handling and recovery
    - Flow state management
    - Event notifications
    
    Example:
        coordinator = FlowCoordinator()
        coordinator.add_step("login", login_func)
        coordinator.add_step("navigate", nav_func, condition=lambda: is_logged_in())
        coordinator.execute()
    """
    
    def __init__(self):
        """Initialize flow coordinator"""
        self.steps: List[FlowStep] = []
        self.state_manager = StateManager()
        self.event_bus = EventBus()
        self.current_step_index = 0
        
        logger.info("Flow coordinator initialized")
    
    def add_step(
        self,
        name: str,
        action: Callable,
        condition: Optional[Callable[[], bool]] = None,
        on_success: Optional[Callable] = None,
        on_failure: Optional[Callable] = None,
        retry_on_failure: bool = False,
        max_retries: int = 2
    ):
        """
        Add a step to the flow
        
        Args:
            name: Step name
            action: Callable to execute
            condition: Optional condition function
            on_success: Success callback
            on_failure: Failure callback
            retry_on_failure: Retry on failure
            max_retries: Maximum retries
        """
        step = FlowStep(
            name=name,
            action=action,
            condition=condition,
            on_success=on_success,
            on_failure=on_failure,
            retry_on_failure=retry_on_failure,
            max_retries=max_retries
        )
        
        self.steps.append(step)
        logger.debug(f"Added step: {name}")
    
    def execute(self, start_from: int = 0) -> bool:
        """
        Execute all steps in sequence
        
        Args:
            start_from: Step index to start from
            
        Returns:
            True if all steps succeeded, False otherwise
        """
        logger.info(f"Starting flow execution from step {start_from}")
        self.event_bus.publish("flow_started", {"start_from": start_from})
        
        self.current_step_index = start_from
        
        for i in range(start_from, len(self.steps)):
            step = self.steps[i]
            self.current_step_index = i
            
            # Execute step
            success = self._execute_step(step)
            
            if not success and not step.retry_on_failure:
                logger.error(f"Flow failed at step: {step.name}")
                self.event_bus.publish("flow_failed", {
                    "step": step.name,
                    "error": step.error
                })
                return False
        
        logger.info("Flow execution completed successfully")
        self.event_bus.publish("flow_completed", {})
        return True
    
    def _execute_step(self, step: FlowStep) -> bool:
        """
        Execute a single step
        
        Args:
            step: FlowStep to execute
            
        Returns:
            True if successful, False otherwise
        """
        # Check condition
        if step.condition and not step.condition():
            step.status = StepStatus.SKIPPED
            logger.info(f"Step skipped (condition not met): {step.name}")
            self.event_bus.publish("step_skipped", {"step": step.name})
            return True
        
        # Execute with retry
        while step.retry_count <= step.max_retries:
            try:
                logger.info(f"Executing step: {step.name} (attempt {step.retry_count + 1})")
                step.status = StepStatus.RUNNING
                step.start_time = datetime.now()
                
                self.event_bus.publish("step_started", {"step": step.name})
                
                # Execute action
                result = step.action()
                step.result = result
                
                # Success
                step.status = StepStatus.COMPLETED
                step.end_time = datetime.now()
                
                logger.info(f"Step completed: {step.name}")
                self.event_bus.publish("step_completed", {
                    "step": step.name,
                    "result": result
                })
                
                # Call success callback
                if step.on_success:
                    step.on_success(result)
                
                return True
                
            except Exception as e:
                step.error = e
                step.retry_count += 1
                
                logger.error(f"Step failed: {step.name} - {str(e)}")
                
                if step.retry_count <= step.max_retries and step.retry_on_failure:
                    logger.warning(f"Retrying step: {step.name} ({step.retry_count}/{step.max_retries})")
                    time.sleep(1)  # Wait before retry
                else:
                    # Final failure
                    step.status = StepStatus.FAILED
                    step.end_time = datetime.now()
                    
                    self.event_bus.publish("step_failed", {
                        "step": step.name,
                        "error": str(e)
                    })
                    
                    # Call failure callback
                    if step.on_failure:
                        step.on_failure(e)
                    
                    return False
        
        return False
    
    def execute_step(self, step_name: str) -> bool:
        """
        Execute a specific step by name
        
        Args:
            step_name: Name of step to execute
            
        Returns:
            True if successful, False otherwise
        """
        for step in self.steps:
            if step.name == step_name:
                return self._execute_step(step)
        
        logger.error(f"Step not found: {step_name}")
        return False
    
    def get_step_status(self, step_name: str) -> Optional[StepStatus]:
        """
        Get status of a step
        
        Args:
            step_name: Step name
            
        Returns:
            StepStatus or None
        """
        for step in self.steps:
            if step.name == step_name:
                return step.status
        return None
    
    def get_step_result(self, step_name: str) -> Any:
        """
        Get result of a step
        
        Args:
            step_name: Step name
            
        Returns:
            Step result or None
        """
        for step in self.steps:
            if step.name == step_name:
                return step.result
        return None
    
    def reset(self):
        """Reset all steps to pending state"""
        for step in self.steps:
            step.status = StepStatus.PENDING
            step.result = None
            step.error = None
            step.retry_count = 0
            step.start_time = None
            step.end_time = None
        
        self.current_step_index = 0
        logger.info("Flow coordinator reset")
    
    def clear(self):
        """Clear all steps"""
        self.steps.clear()
        self.current_step_index = 0
        logger.info("Flow coordinator cleared")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get flow execution statistics
        
        Returns:
            Statistics dictionary
        """
        total = len(self.steps)
        completed = sum(1 for s in self.steps if s.status == StepStatus.COMPLETED)
        failed = sum(1 for s in self.steps if s.status == StepStatus.FAILED)
        skipped = sum(1 for s in self.steps if s.status == StepStatus.SKIPPED)
        pending = sum(1 for s in self.steps if s.status == StepStatus.PENDING)
        
        return {
            'total_steps': total,
            'completed': completed,
            'failed': failed,
            'skipped': skipped,
            'pending': pending,
            'success_rate': completed / total * 100 if total > 0 else 0
        }
