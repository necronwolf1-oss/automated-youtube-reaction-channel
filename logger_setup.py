"""Centralized logging configuration."""
import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from colorama import Fore, Style, init
from config import get_config

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support."""
    
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


def setup_logging(name: str = "automation") -> logging.Logger:
    """Setup logging configuration with file and console handlers.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    config = get_config()
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.logging.level))
    
    # Create logs directory if it doesn't exist
    log_path = Path(config.logging.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # File Handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        config.logging.log_file,
        maxBytes=config.logging.max_log_size_mb * 1024 * 1024,
        backupCount=config.logging.backup_count
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console Handler with colors
    if config.logging.console_output:
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger


# Create a global logger instance
logger: Optional[logging.Logger] = None


def get_logger(name: str = "automation") -> logging.Logger:
    """Get or create the global logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    global logger
    if logger is None:
        logger = setup_logging(name)
    return logger
