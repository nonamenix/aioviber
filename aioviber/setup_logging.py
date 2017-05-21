import logging
import os


def setup_logging():
    LOGGING_LEVEL = getattr(logging, os.environ.get('BOT_LOGGING_LEVEL', 'DEBUG'))
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='%(asctime)s | %(name)s | %(levelname)s - %(message)s'
    )
