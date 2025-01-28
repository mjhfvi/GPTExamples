from __future__ import annotations

import os
import sys
from typing import Optional

from icecream import ic
from langchain_chroma import Chroma
from langchain_community.cache import InMemoryCache
from langchain_community.cache import SQLiteCache
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import chain
from langchain_core.runnables import RunnableConfig
from langchain_ollama import OllamaEmbeddings
from loguru import logger
from prettyformatter import pprint
from pydantic import BaseModel
from pydantic import Field
from rich import inspect
from rich import print_json
from src import llm_tools
from src import local_tools
from src import ollama_chat
from src import vector_store
from src.config_vars import Error_Handler
from src.config_vars import OLLAMA_CHAT_CONFIG
from src.config_vars import OLLAMA_MODEL_CONFIG
from src.config_vars import TODAY

from langchain.globals import set_llm_cache


# llm instruction
llm_system_instruction = 'You are a helpful assistant'

# Total for invoice with taxes
# llm_human_question = 'what is the date of the invoice from bezeqint?'

# data query for chromadb
chromdb_query = 'what is the number of invoices in the data?'
# chromdb_query = "build a Data Parsing and Transformation from text to a json file format"
# chromdb_query = "What is the total number of invoices?"
# chromdb_query = "how much did i pay in 2014?"
# chromdb_query = "what is the best way to organize this date when building rag for llm"
# chromdb_query = "show me a python code to query chromadb and get the data from the collection that matches the query text 'invoices'?"
# chromdb_query = "what are the invoices for 2024"


@Error_Handler
def llm_chromadb_query():
    logger.info('starting chat with llm model, using chroma db query')
    # set cache ##
    set_llm_cache(InMemoryCache())
    # set_llm_cache(SQLiteCache(database_path=".cache.db"))

    # chroma db data query ##
    chromadb_query = vector_store.query_chromadb(
        query=os.environ['DATA_TO_QUERY'])
    # logger.debug(chromadb_query)

    # llm model call with chroma db query ##
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', llm_system_instruction),
            ('human', '{question}' + '{data}')
        ]
    )
    llm_chain = prompt | OLLAMA_MODEL_CONFIG
    llm_human_question = 'what is the date of the invoice from bezeqint?'
    llm_message = llm_chain.invoke(
        {
            'question': llm_human_question,
            'data': 'use this data to answer the question: ' + chromadb_query[0].page_content,
        }
    )
    print('\nAi Answer:')
    print(llm_message)


@Error_Handler
def llm_wikipedia_query():
    logger.info('starting chat with llm model, using wikipedia query')
    # set cache ##
    set_llm_cache(InMemoryCache())
    # set_llm_cache(SQLiteCache(database_path=".cache.db"))

    # wikipedia web search ##
    api_wrapper = WikipediaAPIWrapper(
        top_k_results=1, doc_content_chars_max=4000, lang='en')
    wikipedia_query = WikipediaQueryRun(api_wrapper=api_wrapper)
    wikipedia_results = wikipedia_query.invoke({'query': 'langchain'})

    logger.debug('results from wikipedia: ' + str(wikipedia_results))

    # llm model call with chroma db query ##
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', llm_system_instruction + f"The date today is {TODAY}."),
            ('human', '{question}' + '{tavily_results}')
        ]
    )
    llm_chain = prompt | OLLAMA_MODEL_CONFIG
    llm_human_question = 'explain what is langchain?'
    llm_message = llm_chain.invoke(
        {
            'question': llm_human_question,
            'tavily_results': 'use this data to answer the question: ' + wikipedia_results,
        }
    )
    ic('Ai Answer:')
    ic(llm_message)


def llm_tavily_query():
    logger.info('starting chat with llm model, using tavily query')
    # set cache ##
    set_llm_cache(InMemoryCache())
    # set_llm_cache(SQLiteCache(database_path=".cache.db"))

    # tavily web search ##
    tavily_tool_call = {
        'args': {'query': 'bezeq international?'},
        'id': '1',
        'name': 'tavily',
        'type': 'tool_call',
    }
    tavily_results = llm_tools.tavily_search_results(tavily_tool_call)
    logger.debug('results from tavily: ' + str(tavily_results.content))

    # llm model call with chroma db query ##
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', llm_system_instruction),
            ('human', '{question}' + '{tavily_results}')
        ]
    )
    llm_chain = prompt | OLLAMA_MODEL_CONFIG
    llm_human_question = "explain what is \'bezeq international\'?"
    llm_message = llm_chain.invoke(
        {
            'question': llm_human_question,
            'tavily_results': 'use this data to answer the question: ' + tavily_results.content,
        }
    )
    ic('\nAi Answer:')
    ic(llm_message)


def llm_chromadb_tavily_query():
    logger.info('starting chat with llm model, using chromadb and tavily query')
    # set cache ##
    set_llm_cache(InMemoryCache())
    # set_llm_cache(SQLiteCache(database_path=".cache.db"))

    # chroma db data query ##
    chromadb_query = vector_store.query_chromadb(
        query=os.environ['DATA_TO_QUERY'])
    # logger.debug(chromadb_query)

    # tavily web search ##
    tavily_tool_call = {
        'args': {'query': 'bezeq international?'},
        'id': '1',
        'name': 'tavily',
        'type': 'tool_call',
    }
    tavily_results = llm_tools.tavily_search_results(tavily_tool_call)
    logger.debug('results from tavily: ' + str(tavily_results.content))

    llm_human_question = 'how much is my invoice to bezeq international in 01 2024?'

    # llm model call with tavily query ##
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', llm_system_instruction + f"The date today is {TODAY}."),
            ('human', '{question}'),
            ('assistant', '{chromadb_query}' + '{tavily_results}'),
            # ("placeholder", "{messages}"),
        ]
    )
    llm_chain = prompt | OLLAMA_MODEL_CONFIG
    llm_message = llm_chain.invoke(
        {
            'context': 'The date today is ' + TODAY,
            'question': llm_human_question,
            'tavily_results': 'use this tavily results data to answer the question: ' + tavily_results.content,
            'chromadb_query': 'use this chroma query data to answer the question: ' + chromadb_query[0].page_content,
        }
    )
    ic('Ai Answer:')
    ic(llm_message)


def llm_chromadb_query_structured_output():
    logger.info('starting chat with llm model, using structured output')
    # set cache ##
    set_llm_cache(InMemoryCache())
    # set_llm_cache(SQLiteCache(database_path=".cache.db"))

    class Joke(BaseModel):
        """Joke to tell user."""
        setup: str = Field(description='The setup of the joke')
        punchline: str = Field(description='The punchline to the joke')
        rating: Optional[int] = Field(
            default=None, description='How funny the joke is, from 1 to 10')

    structured_llm = OLLAMA_MODEL_CONFIG.with_structured_output(Joke)
    llm_message = structured_llm.invoke('Tell me a joke about cats')
    ic('Ai Answer:')
    ic(llm_message)


def llm_chromadb_query_json_structured_output():
    logger.info('starting chat with llm model, using json structured output')
    # set cache ##
    set_llm_cache(InMemoryCache())
    # set_llm_cache(SQLiteCache(database_path=".cache.db"))

    json_schema = {
        'title': 'joke',
        'description': 'Joke to tell user.',
        'type': 'object',
        'properties': {
            'setup': {
                'type': 'string',
                'description': 'The setup of the joke',
            },
            'punchline': {
                'type': 'string',
                'description': 'The punchline to the joke',
            },
            'rating': {
                'type': 'integer',
                'description': 'How funny the joke is, from 1 to 10',
                'default': None,
            },
        },
        'required': ['setup', 'punchline'],
    }
    structured_llm = OLLAMA_MODEL_CONFIG.with_structured_output(json_schema)
    llm_message = structured_llm.invoke('Tell me a joke about cats')

    ic('Ai Answer:')
    ic(llm_message)


if __name__ == '__main__':
    # load_local_env_var()
    # llm_chromadb_query()
    llm_wikipedia_query()
    # llm_chromadb_tavily_query()
    # llm_chromadb_query_structured_output()
    # llm_chromadb_query_json_structured_output()
