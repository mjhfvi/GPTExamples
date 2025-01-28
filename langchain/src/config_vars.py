from __future__ import annotations

import datetime
import getpass
import os
import sys

from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

from . import local_tools

load_dotenv(dotenv_path='.env', verbose=True)

# set llm model config ##
OLLAMA_MODEL_CONFIG = local_tools.ollama_llm_config(
    model='llama3.2:1b', temperature=0.0)
OLLAMA_CHAT_CONFIG = local_tools.chat_ollama_config(
    model='llama3.2:1b', temperature=0.0)
TODAY = datetime.datetime.now().strftime('%Y-%m-%d')


# logger.debug('loading variables')
logger.debug('loading DATASET_DIRECTORY key')
if not os.environ.get('DATASET_DIRECTORY'):
    logger.warning('cant find DATASET_DIRECTORY in environment variables')
if os.environ.get('DATASET_DIRECTORY') is not None:
    os.environ['DATASET_DIRECTORY'] = os.environ.get('DATASET_DIRECTORY')
if not os.getenv('DATASET_DIRECTORY'):
    logger.warning('cant find DATASET_DIRECTORY in .env file')
if os.getenv('DATASET_DIRECTORY') is not None:
    os.environ['DATASET_DIRECTORY'] = os.getenv('DATASET_DIRECTORY')
if not os.environ.get('DATASET_DIRECTORY') and not os.getenv('DATASET_DIRECTORY'):
    logger.warning(
        'cant find DATASET_DIRECTORY in environment variables and .env file')
    os.environ['DATASET_DIRECTORY'] = getpass.getpass(
        'please enter DATASET_DIRECTORY:\n')
    if os.environ['DATASET_DIRECTORY'] is not None:
        logger.success('successfully loading DATASET_DIRECTORY key.')
else:
    logger.success('successfully loading DATASET_DIRECTORY key.')

logger.debug('loading DATASET_FILE key')
if not os.environ.get('DATASET_FILE'):
    logger.warning('cant find DATASET_FILE in environment variables')
if os.environ.get('DATASET_FILE') is not None:
    os.environ['DATASET_FILE'] = os.environ.get('DATASET_FILE')
if not os.getenv('DATASET_FILE'):
    logger.warning('cant find DATASET_FILE in .env file')
if os.getenv('DATASET_FILE') is not None:
    os.environ['DATASET_FILE'] = os.getenv('DATASET_FILE')
if not os.environ.get('DATASET_FILE') and not os.getenv('DATASET_FILE'):
    logger.warning(
        'cant find DATASET_FILE in environment variables and .env file')
    os.environ['DATASET_FILE'] = getpass.getpass(
        'please enter DATASET_FILE:\n')
    if os.environ['DATASET_FILE'] is not None:
        logger.success('successfully loading DATASET_FILE key.')
else:
    logger.success('successfully loading DATASET_FILE key.')

logger.debug('loading CHROMA_DB_PATH key')
if not os.environ.get('CHROMA_DB_PATH'):
    logger.warning('cant find CHROMA_DB_PATH in environment variables')
if os.environ.get('CHROMA_DB_PATH') is not None:
    os.environ['CHROMA_DB_PATH'] = os.environ.get('CHROMA_DB_PATH')
if not os.getenv('CHROMA_DB_PATH'):
    logger.warning('cant find CHROMA_DB_PATH in .env file')
if os.getenv('CHROMA_DB_PATH') is not None:
    os.environ['CHROMA_DB_PATH'] = os.getenv('CHROMA_DB_PATH')
if not os.environ.get('CHROMA_DB_PATH') and not os.getenv('CHROMA_DB_PATH'):
    logger.warning(
        'cant find CHROMA_DB_PATH in environment variables and .env file')
    os.environ['CHROMA_DB_PATH'] = getpass.getpass(
        'please enter CHROMA_DB_PATH:\n')
    if os.environ['CHROMA_DB_PATH'] is not None:
        logger.success('successfully loading CHROMA_DB_PATH key.')
else:
    logger.success('successfully loading CHROMA_DB_PATH key.')

logger.debug('loading CHROMA_COLLECTION_NAME key')
if not os.environ.get('CHROMA_COLLECTION_NAME'):
    logger.warning('cant find CHROMA_COLLECTION_NAME in environment variables')
if os.environ.get('CHROMA_COLLECTION_NAME') is not None:
    os.environ['CHROMA_COLLECTION_NAME'] = os.environ.get(
        'CHROMA_COLLECTION_NAME')
if not os.getenv('CHROMA_COLLECTION_NAME'):
    logger.warning('cant find CHROMA_COLLECTION_NAME in .env file')
if os.getenv('CHROMA_COLLECTION_NAME') is not None:
    os.environ['CHROMA_COLLECTION_NAME'] = os.getenv('CHROMA_COLLECTION_NAME')
if not os.environ.get('CHROMA_COLLECTION_NAME') and not os.getenv('CHROMA_COLLECTION_NAME'):
    logger.warning(
        'cant find CHROMA_COLLECTION_NAME in environment variables and .env file')
    os.environ['CHROMA_COLLECTION_NAME'] = getpass.getpass(
        'please enter CHROMA_COLLECTION_NAME:\n')
    if os.environ['CHROMA_COLLECTION_NAME'] is not None:
        logger.success('successfully loading CHROMA_COLLECTION_NAME key.')
else:
    logger.success('successfully loading CHROMA_COLLECTION_NAME key.')

logger.debug('loading LLM_MODEL key')
if not os.environ.get('LLM_MODEL'):
    logger.warning('cant find LLM_MODEL in environment variables')
if os.environ.get('LLM_MODEL') is not None:
    os.environ['LLM_MODEL'] = os.environ.get('LLM_MODEL')
if not os.getenv('LLM_MODEL'):
    logger.warning('cant find LLM_MODEL in .env file')
if os.getenv('LLM_MODEL') is not None:
    os.environ['LLM_MODEL'] = os.getenv('LLM_MODEL')
if not os.environ.get('LLM_MODEL') and not os.getenv('LLM_MODEL'):
    logger.warning(
        'cant find LLM_MODEL in environment variables and .env file')
    os.environ['LLM_MODEL'] = getpass.getpass('please enter LLM_MODEL:\n')
    if os.environ['LLM_MODEL'] is not None:
        logger.success('successfully loading LLM_MODEL key.')
else:
    logger.success('successfully loading LLM_MODEL key.')

logger.debug('loading EMBEDDINGS_MODEL_NAME key')
if not os.environ.get('EMBEDDINGS_MODEL_NAME'):
    logger.warning('cant find EMBEDDINGS_MODEL_NAME in environment variables')
if os.environ.get('EMBEDDINGS_MODEL_NAME') is not None:
    os.environ['EMBEDDINGS_MODEL_NAME'] = os.environ.get(
        'EMBEDDINGS_MODEL_NAME')
if not os.getenv('EMBEDDINGS_MODEL_NAME'):
    logger.warning('cant find EMBEDDINGS_MODEL_NAME in .env file')
if os.getenv('EMBEDDINGS_MODEL_NAME') is not None:
    os.environ['EMBEDDINGS_MODEL_NAME'] = os.getenv('EMBEDDINGS_MODEL_NAME')
if not os.environ.get('EMBEDDINGS_MODEL_NAME') and not os.getenv('EMBEDDINGS_MODEL_NAME'):
    logger.warning(
        'cant find EMBEDDINGS_MODEL_NAME in environment variables and .env file')
    os.environ['EMBEDDINGS_MODEL_NAME'] = getpass.getpass(
        'please enter EMBEDDINGS_MODEL_NAME:\n')
    if os.environ['EMBEDDINGS_MODEL_NAME'] is not None:
        logger.success('successfully loading EMBEDDINGS_MODEL_NAME key.')
else:
    logger.success('successfully loading EMBEDDINGS_MODEL_NAME key.')

logger.debug('loading DATA_TO_QUERY key')
if not os.environ.get('DATA_TO_QUERY'):
    logger.warning('cant find DATA_TO_QUERY in environment variables')
if os.environ.get('DATA_TO_QUERY') is not None:
    os.environ['DATA_TO_QUERY'] = os.environ.get('DATA_TO_QUERY')
if not os.getenv('DATA_TO_QUERY'):
    logger.warning('cant find DATA_TO_QUERY in .env file')
if os.getenv('DATA_TO_QUERY') is not None:
    os.environ['DATA_TO_QUERY'] = os.getenv('DATA_TO_QUERY')
if not os.environ.get('DATA_TO_QUERY') and not os.getenv('DATA_TO_QUERY'):
    logger.warning(
        'cant find DATA_TO_QUERY in environment variables and .env file')
    os.environ['DATA_TO_QUERY'] = getpass.getpass(
        'please enter DATA_TO_QUERY:\n')
    if os.environ['DATA_TO_QUERY'] is not None:
        logger.success('successfully loading DATA_TO_QUERY key.')
else:
    logger.success('successfully loading DATA_TO_QUERY key.')

logger.debug('loading TAVILY_API_KEY key')
if not os.environ.get('TAVILY_API_KEY'):
    logger.warning('cant find TAVILY_API_KEY in environment variables')
if os.environ.get('TAVILY_API_KEY') is not None:
    os.environ['TAVILY_API_KEY'] = os.environ.get('TAVILY_API_KEY')
if not os.getenv('TAVILY_API_KEY'):
    logger.warning('cant find TAVILY_API_KEY in .env file')
if os.getenv('TAVILY_API_KEY') is not None:
    os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
if not os.environ.get('TAVILY_API_KEY') and not os.getenv('TAVILY_API_KEY'):
    logger.warning(
        'cant find TAVILY_API_KEY in environment variables and .env file')
    os.environ['TAVILY_API_KEY'] = getpass.getpass(
        'please enter TAVILY_API_KEY:\n')
    if os.environ['TAVILY_API_KEY'] is not None:
        logger.success('successfully loading TAVILY_API_KEY key.')
else:
    logger.success('successfully loading TAVILY_API_KEY key.')


def Error_Handler(func):
    def Inner_Function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            logger.exception(
                f'An error occurred while running function: {func.__name__}, please check the logs for more information. ')
            # inspect(func)   # for more information set all=True
        except KeyboardInterrupt:
            logger.error('program terminated by user.')
    return Inner_Function


if __name__ == '__main__':
    print('this is not the main script, exiting ...')
    sys.exit()
