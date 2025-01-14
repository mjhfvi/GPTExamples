from __future__ import annotations

import os
import sys

import rag_pdf_bezeqint
from dotenv import load_dotenv
from loguru import logger
from prettyformatter import pprint
from src import ollama_chat
from src import vector_store


def load_local_env_var():
    try:
        logger.debug('loading environment variables from .env file')
        load_dotenv(dotenv_path='.env', verbose=True)
        if not os.getenv('DATASET_DIRECTORY') and not os.getenv('CHROMA_PATH') and not os.getenv('CHROMA_COLLECTION_NAME'):
            logger.error('env values are empty')
        else:
            logger.success(
                'successfully loading environment variables from .env file.')
        DATASET_DIRECTORY = os.getenv('DATASET_DIRECTORY')
        CHROMA_DB_PATH = os.getenv('CHROMA_PATH', 'chroma_db')
        CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME')
        return DATASET_DIRECTORY, CHROMA_DB_PATH, CHROMA_COLLECTION_NAME
    except Exception as error:
        logger.exception(
            'An Error Occurred while loading files from disk', error)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


if __name__ == '__main__':
    logger.info('Starting ollama chat.')
    env_var = load_local_env_var()

    # query data from vector store
    # chroma_collection_name = "Invoice_2024-01-01"
    data_to_query = 'Invoice'
    query_embedding = rag_pdf_bezeqint.query_data_from_vector_store(
        chroma_collection_name=env_var[2], query_data=data_to_query)
    pprint(query_embedding)

    # run ollama model
    response_message = 'how much is the total amount of the invoice?'
    ollama_chat.start_ollama_chat(
        response_message=response_message, data=query_embedding)

# logger.trace("This is a trace message.")
# logger.debug("This is a debug message")
# logger.info("This is an info message.")
# logger.success("This is a success message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
# logger.critical("This is a critical message.")
