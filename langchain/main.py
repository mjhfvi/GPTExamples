from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from loguru import logger
from prettyformatter import pprint
from rich import print_json
from src import ollama_chat
from src import vector_store


def load_local_env_var() -> os.getenv:
    try:
        logger.info('loading environment variables from .env file')
        load_dotenv(dotenv_path='.env', verbose=True)
        if not os.getenv('DATASET_DIRECTORY') and not os.getenv('CHROMA_PATH') and not os.getenv('CHROMA_COLLECTION_NAME'):
            logger.error('env values are empty')
        else:
            logger.success(
                'successfully loading environment variables from .env file.')
        DATASET_DIRECTORY = os.getenv('DATASET_DIRECTORY')
        CHROMA_DB_PATH = os.getenv('CHROMA_PATH', 'chroma_db')
        CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME')
        DATA_TO_QUERY = os.getenv('DATA_TO_QUERY')
        EMBEDDINGS_MODEL_NAME = os.getenv('EMBEDDINGS_MODEL_NAME')
        logger.debug('preview environment variables data: ' + '\n' + DATASET_DIRECTORY +
                     '\n' + CHROMA_DB_PATH + '\n' + CHROMA_COLLECTION_NAME + '\n' + DATA_TO_QUERY)
        return DATASET_DIRECTORY, CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, DATA_TO_QUERY, EMBEDDINGS_MODEL_NAME

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def main() -> None:
    try:
        logger.info('query chroma db for data.')
        query_embedding = vector_store.query_data_from_vector_store(
            chroma_collection_name=env_var[2], query_data=env_var[3])
        logger.debug('query chroma db for data.')
        query_question = 'what is the total amount of the invoice? and what is the VAT amount to pay? and list the extra service i received'
        logger.info('Starting LLM chat.')
        ollama_chat.start_ollama_chat(
            query_question=query_question,
            chroma_collection_name=env_var[2],
            query_data=env_var[3],
            retriever=query_embedding,
            temperature='0',
            EMBEDDINGS_MODEL_NAME=env_var[4])
        # ollama_chat.start_ollama_chat(query_question, chroma_collection_name, query_data, EMBEDDINGS_MODEL_NAME=EMBEDDINGS_MODEL_NAME):

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


if __name__ == '__main__':
    logger.remove()
    # TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
    logger.add(sys.stdout, level='INFO')
    env_var = load_local_env_var()
    main()

    # TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
    # logger.trace("This is a trace message.")
    # logger.debug("This is a debug message")
    # logger.info("This is an info message.")
    # logger.success("This is a success message.")
    # logger.warning("This is a warning message.")
    # logger.error("This is an error message.")
    # logger.critical("This is a critical message.")
