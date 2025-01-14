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
from src import vector_store

from langchain.docstore.document import Document


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


def load_files(dataset_directory):
    try:
        logger.debug('loading files from disk')
        loader = PyPDFDirectoryLoader(dataset_directory)
        logger.debug('using folder', dataset_directory)
        loader_data = loader.load()
        logger.success('successfully loading date from folder')
        # pprint("\n[DEBUG]", loader_data)
        return loader_data
    except Exception as error:
        logger.exception(
            'An Error Occurred while loading files from disk', error)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def read_pdf_file(documents):
    try:
        logger.debug('reading pdf file')
        page_1 = [doc for doc in documents if doc.metadata.get('page') == 0]
        page_2 = [doc for doc in documents if doc.metadata.get('page') == 1]
        logger.success('successfully read pages')
        for doc in page_1:
            find_start_text = 'פתח תקווה'
            find_end_text = 'לתשלום לאחר המועד שנקבע'
            text_doc = page_1[0].page_content

            start_index = text_doc.find(find_start_text)
            if start_index == -1:
                print('Start text not found')

            start_index += len(find_start_text)
            end_index = text_doc.find(find_end_text, start_index)
            if end_index == -1:
                print('End text not found')

            new_text = text_doc[start_index:end_index]

            translated_page_1 = GoogleTranslator(
                source='hebrew', target='english').translate(new_text)
            # print(translated_page_1, "\n")
        for doc in page_2:
            find_start_text = 'גישה1020638271'
            find_end_text = '** בשל עיגול סכימת החיובים תיתכ'
            text_doc = page_2[0].page_content
            # print(text_doc)

            start_index = text_doc.find(find_start_text)
            if start_index == -1:
                print('Start text not found')

            start_index += len(find_start_text)
            end_index = text_doc.find(find_end_text, start_index)
            if end_index == -1:
                print('End text not found')

            new_text = text_doc[start_index:end_index]

            translated_page_2 = GoogleTranslator(
                source='hebrew', target='english').translate(new_text)
            # print(translated_page_2, "\n")
        logger.debug('translate relevant text in document')
        translated_pages = translated_page_1 + translated_page_2
        # print('[DEBUG]', translated_pages)
        return translated_pages
    except Exception as error:
        logger.exception('An Error Occurred while reading files', error)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def build_document(document_data):
    try:
        logger.debug('building data in document')
        rebuild_document = [Document(metadata={
                                     'source': 'Invoice_200141400.pdf', 'page': '0'}, page_content=document_data)]
        logger.success('successfully build data in document')
        return rebuild_document
    except Exception as error:
        logger.exception(
            'An Error Occurred while loading files from disk', error)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def embed_document(document_data, chromadb_directory, chroma_collection_name):
    try:
        logger.debug('embeddings document data')
        # embeddings_data_output = OllamaEmbeddings(model="llama3.2:3b")
        logger.info('starting embeddings document data process')
        embedding_text = Chroma.from_documents(
            documents=document_data,
            # embedding=embeddings_data_output,
            collection_name=chroma_collection_name,
            # embedding_function=embeddings_data_output,
            embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2'),
            persist_directory=chromadb_directory,
        )
        logger.success('successfully embeddings document data')
        # print("number of embeddings: ", len(embedding_text))

        return embedding_text
    except Exception as error:
        logger.exception('An Error Occurred while embeddings data', error)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def add_data_to_vector_store(chroma_collection_name):
    try:
        logger.debug('adding data to vector store')
        chroma_client = vector_store.chroma_db_setup(print_debug=False)
        connection_string = vector_store.chroma_db_get_collection(
            chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=True, print_debug=True)
        test_data = vector_store.chroma_db_get_data_from_collection(
            connection_string)
        print(test_data)
        logger.success('successfully adding data to vector store')
        logger.debug('query data from vector store')
        query_data_from_vector_store(
            chroma_collection_name=chroma_collection_name, query_data=data_to_query)
        logger.success('successfully query data from vector store')
        return test_data
    except Exception as error:
        logger.exception('An Error Occurred while embeddings data', error)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def query_data_from_vector_store(chroma_collection_name, query_data):
    try:
        logger.debug('query data from vector store')
        chroma_client = vector_store.chroma_db_setup(print_debug=False)
        connection_string = vector_store.chroma_db_get_collection(
            chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=True, print_debug=True)
        query_embedding = vector_store.chroma_db_query_data_from_collection(
            connection_string, query_data=query_data)
        logger.success('successfully query data from vector store')
        return query_embedding
    except Exception as error:
        logger.exception('An Error Occurred while embeddings data', error)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


if __name__ == '__main__':
    logger.remove()
    # TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
    logger.add(sys.stdout, level='DEBUG')
    logger.info('Starting RAG process')
    env_var = load_local_env_var()
    chroma_collection_name = 'Invoice_2024-01-01'
    data_to_query = 'Invoice'

    # Add data to vector store ##
    loader_data = load_files(dataset_directory=env_var[0])
    document_data = read_pdf_file(documents=loader_data)
    rebuild_document_data = build_document(document_data=document_data)
    embed_document(rebuild_document_data,
                   chromadb_directory=env_var[1], chroma_collection_name=chroma_collection_name)
    add_data_to_vector_store(chroma_collection_name=chroma_collection_name)

    # Query data from vector store ##
    query_embedding = query_data_from_vector_store(
        chroma_collection_name=chroma_collection_name, query_data=data_to_query)
    pprint(query_embedding)

    # Get data from vector store ##
    # chroma_client = vector_store.chroma_db_setup(print_debug=False)
    # connection_string = vector_store.chroma_db_get_collection(chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=True, print_debug=True)
    # get_embedding = vector_store.chroma_db_get_data_from_collection(connection_string)
    # print(get_embedding)

    # logger.trace("This is a trace message.")
    # logger.debug("This is a debug message")
    # logger.info("This is an info message.")
    # logger.success("This is a success message.")
    # logger.warning("This is a warning message.")
    # logger.error("This is an error message.")
    # logger.critical("This is a critical message.")
