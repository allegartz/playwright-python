"""
Logger Configuration

Configure logging for the framework
"""

import sys
from pathlib import Path
from loguru import logger
from datetime import datetime


def setup_logger(
    log_level: str = "INFO",
    log_file: str = None,
    rotation: str = "10 MB",
    retention: str = "7 days",
    format: str = None
):
    """
    Configure logger
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
        rotation: Log file rotation (e.g., "10 MB", "1 day")
        retention: Log file retention period
        format: Custom log format
    """
    # Remove default handler
    logger.remove()
    
    # Default format
    if format is None:
        format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Add console handler
    logger.add(
        sys.stdout,
        format=format,
        level=log_level,
        colorize=True
    )
    
    # Add file handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_file,
            format=format,
            level=log_level,
            rotation=rotation,
            retention=retention,
            compression="zip"
        )
        logger.info(f"Logging to file: {log_file}")
    
    logger.info(f"Logger configured with level: {log_level}")


def get_logger(name: str = None):
    """
    Get logger instance
    
    Args:
        name: Optional logger name
        
    Returns:
        Logger instance
    """
    if name:
        return logger.bind(name=name)
    return logger
