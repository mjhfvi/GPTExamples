from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv(dotenv_path='.env', verbose=True)
logger.remove()    # TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
logger.add(sys.stdout, level='DEBUG')
logger.info(f"LLM Langchain Project: v{os.environ.get('VERSION')}")

# TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
# logger.trace("This is a trace message.")
# logger.debug("This is a debug message")
# logger.info("This is an info message.")
# logger.success("This is a success message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
# logger.critical("This is a critical message.")
