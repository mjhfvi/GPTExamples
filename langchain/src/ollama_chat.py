from __future__ import annotations

import os
import sys

from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from loguru import logger

from langchain.prompts import ChatPromptTemplate

# from dotenv import load_dotenv
# import vector_store
# dotenv_path = '/home/mjhfvi/repository/GPTExamples/langchain/.env'

# def load_local_env_var():
#     try:
#         logger.info('loading environment variables from .env file')
#         load_dotenv(dotenv_path=dotenv_path, verbose=True)
#         if not os.getenv('DATASET_DIRECTORY') and not os.getenv('CHROMA_PATH') and not os.getenv('CHROMA_COLLECTION_NAME'):
#             logger.error('env values are empty')
#             exit(1)
#         else:
#             logger.success('successfully loading environment variables from .env file.')
#             DATASET_DIRECTORY = os.getenv('DATASET_DIRECTORY')
#             CHROMA_DB_PATH = os.getenv('CHROMA_PATH', 'chroma_db')
#             CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME')
#             DATA_TO_QUERY = os.getenv('DATA_TO_QUERY')
#             logger.debug('preview environment variables data: ' + "\n" + DATASET_DIRECTORY + "\n" + CHROMA_DB_PATH + "\n" + CHROMA_COLLECTION_NAME + "\n" + DATA_TO_QUERY)
#             return DATASET_DIRECTORY, CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, DATA_TO_QUERY

#     except Exception:
#         logger.exception('An error occurred while running the program, please check the logs for more information. ')
#         sys.exit(1)
#     except KeyboardInterrupt:
#         logger.error('program terminated by user.')


# def query_data_from_vector_store(chroma_collection_name, query_data):
#     try:
#         logger.info('querying data from vector store')
#         chroma_client = vector_store.chroma_db_setup()
#         connection_string = vector_store.chroma_db_get_collection(chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=True)
#         query_embedding = vector_store.chroma_db_query_data_from_collection(connection_string, query_data=query_data)
#         logger.success('successfully query data from vector store')
#         return query_embedding

#     except Exception:
#         logger.exception('An error occurred while running the program, please check the logs for more information. ')
#         sys.exit(1)
#     except KeyboardInterrupt:
#         logger.error('program terminated by user.')


def start_ollama_chat(query_question, chroma_collection_name, query_data, retriever, temperature=0, EMBEDDINGS_MODEL_NAME='all-MiniLM-L6-v2'):
    try:
        # retriever = query_data_from_vector_store(chroma_collection_name=chroma_collection_name, query_data=query_data)
        logger.debug('preview query data from chroma db: ')
        logger.debug(retriever)
        model = ChatOllama(model='llama3.2:1b', temperature=temperature)
        embedding_function = HuggingFaceEmbeddings(
            model_name=EMBEDDINGS_MODEL_NAME),
        # query_question = "what is the total amount of the invoice? and what is the VAT amount to pay? and list the extra service i received"
        prompt_template = ChatPromptTemplate.from_messages(
            [('system', query_question), ('user', '{text}')]
        )
        prompt = prompt_template.invoke(
            {'language': 'Italian', 'text': retriever})
        prompt.to_messages()
        response = model.invoke(prompt)
        print(response.content)

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


if __name__ == '__main__':
    logger.error('this is not the main script, exiting ...')
    sys.exit()
