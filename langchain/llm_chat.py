from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.cache import InMemoryCache
from langchain_community.cache import SQLiteCache
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings
from loguru import logger
from prettyformatter import pprint
from rich import inspect
from rich import print_json
from src import local_tools
from src import ollama_chat
from src import vector_store

from langchain.chains import RetrievalQA
from langchain.globals import set_llm_cache
# from pydantic import BaseModel
# from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage, trim_messages
# from langchain_ollama import ChatOllama
# from langchain.chains.llm import LLMChain
# from langchain.chains.combine_documents.stuff import StuffDocumentsChain
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_ollama.llms import OllamaLLM

# , you respond using JSON only
llm_system_instruction = 'You are a helpful assistant'
# Total for invoice with taxes
llm_human_question = 'what is the date of the invoice?'
llm_ai_message = 'this is a code example for you: '
query_data = 'what is the number of invoices in the data?'
# llm_request = "build a Data Parsing and Transformation from text to a json file format"
# query_text = "What is the total number of invoices?"
# query_text = "how much did i pay in 2014?"
# query_text = "what is the best way to organize this date when building rag for llm"
# query_text = "show me a python code to query chromadb and get the data from the collection that matches the query text 'invoices'?"
# query_text = "what are the invoices for 2024"


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


def main() -> None:
    try:
        logger.info('starting chat with llm model')
        chromadb_query = query_chroma(query_data)
        # print(chromadb_query[0].page_content)
        # exit(0)

        set_llm_cache(InMemoryCache())
        # set_llm_cache(SQLiteCache(database_path=".cache.db"))

        # ollama_config = local_tools.chat_ollama_config(model='llama3.2:1b')

        model_config = local_tools.ollama_llm_config(model='llama3.2:1b')

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    llm_system_instruction,
                ),
                ('human', '{question}' + '{data}'),
            ]
        )

        chain = prompt | model_config
        llm_message = chain.invoke(
            {
                'question': llm_human_question,
                'data': 'use this data to answer the question: ' + chromadb_query[0].page_content,
            }
        )

        print('\nAi Answer:')
        print(llm_message)

        # messages = [
        #     SystemMessage(llm_system_instruction),
        #     HumanMessage(llm_human_question),
        #     AIMessage(llm_ai_message),
        #     # HumanMessage("get the data from the collection that matches the query text 'invoices'?"),
        #     # AIMessage("Hmmm let me think.\n\nWhy, he's probably chasing after the last cup of coffee in the office!"),
        #     # HumanMessage("what do you call a speechless parrot"),
        # ]

        # messages_prompt = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", llm_system_instruction),
        #         ("human", llm_human_question),
        #     ]
        # )

        # chain = messages_prompt | ollama_config

        # ai_msg = chain.invoke(
        #     {
        #         "query": chromadb_query[0].page_content,
        #         "data_input": llm_human_question,
        #     }
        # )
        # ai_msg = ollama_config.invoke(messages)

        # print(ai_msg, '\n')
        # print(ai_msg.content)

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def query_chroma(query_data):
    try:
        logger.info('query chroma db for data.')
        ollama_model_name = 'llama3.2:1b'   # llama3.2:3b, llama3.2:1b
        embedding_function = OllamaEmbeddings(model=ollama_model_name)

        vector_store_string = Chroma(
            collection_name=env_var[3],
            embedding_function=embedding_function,
            persist_directory=env_var[2],
            # create_collection_if_not_exists=True
        )

        chromadb_query_data = vector_store_string.similarity_search(query_data)
        logger.debug('collection data search in chromadb: ' +
                     str(chromadb_query_data))

        # collection_get_data = chroma_collection_connection_string_data.collection_search_data(ids=None, document=None)
        # print(collection_get_data)
        # chroma_collection_connection_string_data.collection_add_data()
        # persistent_client = chromadb.PersistentClient(
        #     path=env_var[2],
        #     settings=Settings(
        #         allow_reset=True,
        #         is_persistent=True,
        #         anonymized_telemetry=False
        #     )
        # )

        # query_embedding = chroma_collection_connection_string_data.embed_query(env_var[3])
        # query_text = "What is the total number of invoices?"
        # chroma_connection = collection.similarity_search(query_text)

        # collection_query_data = chroma_collection_connection_string_data.collection_query_data(query_data=env_var[3], number_results=12)
        # print(collection_query_data)

        return chromadb_query_data

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
    # query_chroma()
    main()

    # TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
    # logger.trace("This is a trace message.")
    # logger.debug("This is a debug message")
    # logger.info("This is an info message.")
    # logger.success("This is a success message.")
    # logger.warning("This is a warning message.")
    # logger.error("This is an error message.")
    # logger.critical("This is a critical message.")
