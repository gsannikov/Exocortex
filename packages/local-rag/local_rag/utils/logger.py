"""
Centralized logging configuration for local RAG.

Provides structured logging with:
- Rotating file handlers
- Separate error log
- Console + file output
- Configurable log levels
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Cache of configured loggers to avoid duplicate setup
_configured_loggers = set()


def setup_logging(
    log_dir: Path,
    log_level: str = "INFO",
    rotation_mb: int = 10,
    backup_count: int = 5,
    console: bool = True
) -> None:
    """
    Configure root logger with file rotation.
    
    Args:
        log_dir: Directory for log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        rotation_mb: Max size of each log file in MB
        backup_count: Number of backup files to keep
        console: Whether to also log to console
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Main log file (all levels)
    main_log = log_dir / "indexing.log"
    main_handler = RotatingFileHandler(
        main_log,
        maxBytes=rotation_mb * 1024 * 1024,
        backupCount=backup_count
    )
    main_handler.setLevel(getattr(logging, log_level.upper()))
    main_handler.setFormatter(detailed_formatter)
    
    # Error log file (errors only)
    error_log = log_dir / "errors.log"
    error_handler = RotatingFileHandler(
        error_log,
        maxBytes=rotation_mb * 1024 * 1024,
        backupCount=backup_count
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Add handlers
    root_logger.addHandler(main_handler)
    root_logger.addHandler(error_handler)
    
    # Console output (optional) - MUST use stderr for MCP compatibility
    # MCP servers communicate via JSON-RPC on stdout, so logs must go to stderr
    if console:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
