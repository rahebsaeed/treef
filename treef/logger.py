# treef/logger.py
import logging
import sys

def configure_logger():
    """
    Performs the initial, one-time configuration for the 'treef' logger.
    """
    # Get the root logger for our application
    log = logging.getLogger("treef")

    # The key fix: only add handlers if none exist. This makes the
    # function idempotent (safe to call multiple times).
    if not log.handlers:
        log.setLevel(logging.INFO)  # Set the default level
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] - %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        log.addHandler(handler)