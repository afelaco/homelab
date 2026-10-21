import logging
import sys


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Returns a singleton logger instance with consistent formatting.
    """
    logger = logging.getLogger(name)

    # Only add handlers if they are not already configured
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # Avoid logging duplication in root logger
        logger.propagate = False

    return logger
