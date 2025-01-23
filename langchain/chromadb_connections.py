from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from loguru import logger
from prettyformatter import pprint
from src import documents_loader
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
        DATASET_FILE = os.getenv('DATASET_FILE')
        CHROMA_DB_PATH = os.getenv('CHROMA_PATH', 'chroma_db')
        CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME')
        DATA_TO_QUERY = os.getenv('DATA_TO_QUERY')
        EMBEDDINGS_MODEL_NAME = os.getenv('EMBEDDINGS_MODEL_NAME')
        # logger.debug('preview environment variables data: ' + '\n' + DATASET_DIRECTORY + '\n' + CHROMA_DB_PATH + '\n' + CHROMA_COLLECTION_NAME + '\n' + DATA_TO_QUERY)
        return DATASET_DIRECTORY, DATASET_FILE, CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, DATA_TO_QUERY, EMBEDDINGS_MODEL_NAME

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def main():
    try:
        logger.info('starting main function')
        # vector store data ##
        # chroma_connection_string_data = vector_store.chroma_connection_string(chromadb_path=env_var[2])
        chroma_collection_connection_string_data = vector_store.chroma_collection_connection_string(
            chromadb_path=env_var[2], chroma_collection_name=env_var[3])

        # chroma_connection_string_data.reset_chromadb()
        # create_collection = chroma_connection_string_data.create_collection(chroma_collection_name=env_var[3])
        # print(create_collection)
        # chroma_connection_string_data.delete_collection(chroma_collection_name='test_collection')
        # list_collections = chroma_connection_string_data.list_collections()
        # print(list_collections)

        # collection_get_data = chroma_collection_connection_string_data.collection_get_data()
        # print(collection_get_data)
        collection_get_data = chroma_collection_connection_string_data.collection_search_data(
            document='invoice_information')
        print(collection_get_data)
        # chroma_collection_connection_string_data.collection_add_data()
        # collection_query_data = chroma_collection_connection_string_data.collection_query_data(query_data=env_var[4], number_results=1)
        # print(collection_query_data)
        # collection_query_data = chroma_collection_connection_string_data.collection_remove_data(ids=['id1'])
        # print(collection_query_data)
        # chroma_collection_connection_string_data.collection_delete()

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


if __name__ == '__main__':
    logger.remove()
    # TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
    logger.add(sys.stdout, level='DEBUG')
    # logger.info('Starting rag process PDF for bezetint invoices.')
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
