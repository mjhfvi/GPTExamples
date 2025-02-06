from __future__ import annotations

import getpass
import os
import sys

from dotenv import load_dotenv
from loguru import logger

logger.remove()    # TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
logger.add(sys.stdout, level='DEBUG')
load_dotenv(dotenv_path='.env', verbose=True)
logger.info(f"LLM Langchain Project: v{os.environ.get('VERSION')}")

env_list = ['DATASET_DIRECTORY', 'DATASET_FILE', 'CHROMA_DB_PATH', 'CHROMA_TENANT_NAME', 'CHROMA_DATABASE_NAME', 'CHROMA_COLLECTION_NAME', 'LLM_MODEL',
            # , 'TAVILY_API_KEY', 'GIT_HUB_TOKEN'
            'EMBEDDINGS_MODEL_NAME', 'OLLAMA_URL']

logger.debug('loading environment variables')
for env in env_list:
    logger.debug(f'loading {env} key')
    if os.environ.get(env) is None:
        logger.debug(f'{env} is NOT set in environment variables.')
        if not os.environ.get(env) and not os.getenv(env):
            logger.warning(
                f'cant find {env} in environment variables or in .env file')
            if 'API' in env or 'KEY' in env or 'TOKEN' in env:
                os.environ[env] = getpass.getpass(
                    f'Enter {env} value: (input will be hidden): ')
            else:
                os.environ[env] = input(f"Enter {env} value: ")
            if os.environ[env] is not None:
                logger.success('successfully load key from user input.')
                continue
    if os.environ.get(env) is not None:
        logger.success(
            f'successfully load {env} key from environment variables.')

# TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
# logger.trace("This is a trace message.")
# logger.debug("This is a debug message")
# logger.info("This is an info message.")
# logger.success("This is a success message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
# logger.critical("This is a critical message.")
