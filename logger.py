import logging
import os
from typing import Optional

class Logger:
    """
    A wrapper class for Python's logging module that provides a simplified interface
    for logging messages with both console and file output capabilities.
    
    This class implements the singleton pattern to ensure only one logger instance
    exists per name.
    """
    _instances = {}

    def __new__(cls, name: str, log_file: Optional[str] = None,
                log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level: int = logging.DEBUG):
        """
        Create or retrieve a logger instance.

        Args:
            name: The name of the logger
            log_file: Optional path to the log file
            log_format: The format string for log messages
            level: The logging level (default: DEBUG)

        Returns:
            Logger instance
        """
        if name not in cls._instances:
            cls._instances[name] = super(Logger, cls).__new__(cls)
            cls._instances[name]._initialized = False
        return cls._instances[name]

    def __init__(self, name: str, log_file: Optional[str] = None,
                 log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                 level: int = logging.DEBUG) -> None:
        """
        Initialize the logger if it hasn't been initialized yet.
        """
        if getattr(self, '_initialized', False):
            return

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Remove existing handlers to avoid duplicates
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        self.logger.addHandler(console_handler)

        # Create file handler if log_file is specified
        if log_file:
            try:
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(logging.Formatter(log_format))
                self.logger.addHandler(file_handler)
            except Exception as e:
                self.logger.error(f"Failed to create log file handler: {str(e)}")

        self._initialized = True

    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)

    def critical(self, message: str) -> None:
        """Log a critical message."""
        self.logger.critical(message)

    def exception(self, message: str) -> None:
        """Log an exception message with traceback."""
        self.logger.exception(message)
