import logging
import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))

logger = logging.getLogger("kwebmon-producer")
logger.setLevel(logging.DEBUG)

_console_handler = logging.StreamHandler()
_console_handler.setLevel(logging.INFO)

_log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

_console_handler.setFormatter(_log_formatter)
logger.addHandler(_console_handler)
