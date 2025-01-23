from __future__ import annotations

import os
import sys

from chromadb.utils.embedding_functions import create_langchain_embedding
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from loguru import logger
from prettyformatter import pprint
from rich import inspect
from rich import print_json
from src import documents_loader
# from chromadb.config import DEFAULT_DATABASE, DEFAULT_TENANT, Settings
# from chromadb.utils import embedding_functions
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_core.documents import Document
# from langchain_community.embeddings import SentenceTransformerEmbeddings, HuggingFaceEmbeddings

datasets_path = 'datasets/file_loader/datasets/'


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
        logger.info('running main function')
        load_documents_string = documents_loader.DocumentsLoaders(
            path=datasets_path)
        file_data = load_documents_string.load_json_files()

        ollama_model_name = 'llama3.2:1b'   # llama3.2:3b, llama3.2:1b
        # hf_model_name = "sentence-transformers/all-mpnet-base-v2"      # sentence-transformers/all-mpnet-base-v2 sentence-transformers/mxbai-embed-2d-large-v1

        embedding_function = OllamaEmbeddings(model=ollama_model_name)
        # embeddings_model = HuggingFaceEmbeddings(model_name=hf_model_name)

        # test_document = Document(
        #     page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
        #     metadata={"source": "tweet"},
        # )

        embedding_documents = embedding_function.embed_documents(
            file_data[0].page_content)
        print('list of embeddings:', len(embedding_documents),
              len(embedding_documents[0]))

        # embedded_query = embedding_function.embed_query("What was the name mentioned in the conversation?")
        # print(embedded_query[:10])

        vector_store_string = Chroma(
            collection_name=env_var[3],
            embedding_function=embedding_function,
            persist_directory=env_var[2],
            create_collection_if_not_exists=True
        )
        print('build vector store connection string')

        # build_embedding_documents = vector_store_string.from_documents(
        #     documents=file_data,
        #     embedding=embedding_documents,
        #     collection_name=env_var[3]
        # )
        # print("build embeddings documents")
        # inspect(build_embedding_documents)

        vector_store_string.add_documents(
            documents=file_data,
        )
        print('add embeddings documents to chroma db')

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
