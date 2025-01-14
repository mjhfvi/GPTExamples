from __future__ import annotations

import os
import sys

from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger
from prettyformatter import pprint
from rich import print_json
from src import vector_store

from langchain.docstore.document import Document


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
        logger.debug('preview environment variables data: ' + '\n' + DATASET_DIRECTORY +
                     '\n' + CHROMA_DB_PATH + '\n' + CHROMA_COLLECTION_NAME + '\n' + DATA_TO_QUERY)
        return DATASET_DIRECTORY, CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, DATA_TO_QUERY

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def load_files(dataset_directory) -> PyPDFDirectoryLoader:
    try:
        logger.info('loading files from path: ')
        logger.debug('using directory path: ' + dataset_directory)
        loader = PyPDFDirectoryLoader(dataset_directory)
        loader_data = loader.load()
        logger.success('successfully loading date from files')
        logger.debug('preview loader data: ', loader_data)
        logger.debug(loader_data)
        return loader_data

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def read_pdf_file(documents) -> GoogleTranslator:
    try:
        logger.info('reading data from PDF files')
        page_1 = [doc for doc in documents if doc.metadata.get('page') == 0]
        page_2 = [doc for doc in documents if doc.metadata.get('page') == 1]
        logger.success('successfully reading data from PDF files')
        for doc in page_1:
            find_start_text = 'פתח תקווה'
            find_end_text = 'לתשלום לאחר המועד שנקבע'
            text_doc = page_1[0].page_content

            start_index = text_doc.find(find_start_text)
            if start_index == -1:
                logger.warning('Start text not found')

            start_index += len(find_start_text)
            end_index = text_doc.find(find_end_text, start_index)
            if end_index == -1:
                logger.warning('End text not found')

            new_text = text_doc[start_index:end_index]

            logger.info('translating relevant text in page 1')
            translated_page_1 = GoogleTranslator(
                source='hebrew', target='english').translate(new_text)
            logger.debug('preview translated page 1: ')
            logger.debug(translated_page_1)
        for doc in page_2:
            find_start_text = 'גישה1020638271'
            find_end_text = '** בשל עיגול סכימת החיובים תיתכ'
            text_doc = page_2[0].page_content
            logger.debug('preview text document: ')
            logger.debug(text_doc)

            start_index = text_doc.find(find_start_text)
            if start_index == -1:
                logger.warning('Start text not found')

            start_index += len(find_start_text)
            end_index = text_doc.find(find_end_text, start_index)
            if end_index == -1:
                logger.warning('End text not found')

            new_text = text_doc[start_index:end_index]

            logger.info('translating relevant text in page 2')
            translated_page_2 = GoogleTranslator(
                source='hebrew', target='english').translate(new_text)
            logger.debug('preview translated page 2: ')
            logger.debug(translated_page_2)
        logger.success('successfully translating relevant text in documents')
        translated_pages = translated_page_1 + translated_page_2
        logger.debug('preview translated text: ' + translated_pages)
        return translated_pages

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def build_document(document_data) -> Document:
    try:
        logger.info('building data structure in document')
        # logger.debug('building data structure in document')
        rebuild_document = [Document(metadata={
                                     'source': 'Invoice_200141400.pdf', 'page': '0'}, page_content=document_data)]
        logger.success('successfully build data structure in document')
        return rebuild_document

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def embed_document(document_data, chromadb_directory, chroma_collection_name) -> HuggingFaceEmbeddings:
    try:
        logger.info('starting embeddings document data process')
        # logger.debug('embeddings document data')
        # embeddings_data_output = OllamaEmbeddings(model="llama3.2:3b")

        embedding_text = Chroma.from_documents(
            documents=document_data,
            # embedding=embeddings_data_output,
            collection_name=chroma_collection_name,
            # embedding_function=embeddings_data_output,
            embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2'),
            persist_directory=chromadb_directory,
        )
        logger.success('successfully embeddings document data')
        embeddings_number = str(len(embedding_text))
        logger.debug('number of embeddings: ' + embeddings_number)
        return embedding_text

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def add_data_to_vector_store(chroma_collection_name, data_to_query):
    try:
        logger.info('adding data to chroma db')
        logger.debug('using chroma collection name: ' + chroma_collection_name)
        chroma_client = vector_store.chroma_db_setup()
        connection_string = vector_store.chroma_db_get_collection(
            chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=True, )
        vector_store.chroma_db_get_data_from_collection(connection_string)
        logger.success('successfully adding data to vector store')
        queried_data = query_data_from_vector_store(
            chroma_collection_name=chroma_collection_name, query_data=data_to_query)
        logger.debug('query data from vector store: ')
        logger.debug(queried_data)
        logger.success('successfully query data from vector store')
        return queried_data

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def query_data_from_vector_store(chroma_collection_name, query_data):
    try:
        logger.info('querying data from vector store')
        chroma_client = vector_store.chroma_db_setup()
        connection_string = vector_store.chroma_db_get_collection(
            chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=True, )
        query_embedding = vector_store.chroma_db_query_data_from_collection(
            connection_string, query_data=query_data)
        logger.success('successfully query data from vector store')
        return query_embedding

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def main():
    try:
        loader_data = load_files(dataset_directory=env_var[0])
        document_data = read_pdf_file(documents=loader_data)
        rebuild_document_data = build_document(document_data=document_data)
        embed_document(rebuild_document_data,
                       chromadb_directory=env_var[1], chroma_collection_name=env_var[2])
        add_data_to_vector_store(
            chroma_collection_name=env_var[2], data_to_query=env_var[3])

        # Query data from vector store ##
        query_embedding = query_data_from_vector_store(
            chroma_collection_name=env_var[2], query_data=env_var[3])
        logger.debug('preview query data from chroma db: ')
        logger.debug(query_embedding)

        # Get data from vector store ##
        # chroma_client = vector_store.chroma_db_setup()
        # connection_string = vector_store.chroma_db_get_collection(chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=True, )
        # get_embedding = vector_store.chroma_db_get_data_from_collection(connection_string)
        # logger.debug("preview get data from chroma db: ")
        # logger.debug(get_embedding)

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
    logger.info('Starting rag process PDF for bezetint invoices.')
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
