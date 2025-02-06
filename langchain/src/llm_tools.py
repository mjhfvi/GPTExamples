from __future__ import annotations

import datetime
import getpass
import os
import sys

from dotenv import find_dotenv
from dotenv import load_dotenv
from langchain_community.cache import InMemoryCache
from langchain_community.tools import TavilySearchResults
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_ollama.llms import OllamaLLM
from loguru import logger
from prettyformatter import pprint
from rich import inspect
from rich import print_json
from src.llm_prompt_template import llm_prompt_validation
from src.llm_prompt_template import prompt_json_invoice

from langchain.globals import set_llm_cache
from langchain.prompts import PromptTemplate


def chat_ollama_config(model: str = os.getenv('LLM_MODEL', 'llama3.2:1b'), temperature: int = 0.1):
    ollama_config = ChatOllama(
        model=model,
        temperature=temperature,
        # num_predict=256,
        cache=True,
        base_url=os.getenv('OLLAMA_URL', 'http://localhost:11434'),
        verbose=True,
        format='json',
    )
    return ollama_config


def ollama_llm_config(model: str = os.getenv('LLM_MODEL', 'llama3.2:1b'), temperature: int = 0.1):
    ollama_config = OllamaLLM(
        model=model,
        temperature=temperature,
        # num_predict=256,
        cache=True,
        base_url=os.getenv('OLLAMA_URL', 'http://localhost:11434'),
        verbose=True,
        format='json',
    )
    return ollama_config


def build_dataset_llm(dataset_document):
    set_llm_cache(InMemoryCache())

    llm_prompt = PromptTemplate(
        # input_variables=[dataset_document],
        template=prompt_json_invoice
    )

    llm_chain = llm_prompt | ollama_llm_config(
        temperature=0.1) | StrOutputParser()
    llm_response = llm_chain.invoke({'input_text': dataset_document})
    logger.debug('successfully built llm response to json')
    # pprint(llm_response)
    return llm_response


def tavily_search_results(query) -> TavilySearchResults:
    tavily_tool = TavilySearchResults(
        name='tavily_search_results_json',
        description='A web search engine that provides search results in JSON format.',
        max_results=3,
        search_depth='advanced',
        include_answer=True,
        include_raw_content=True,
        include_images=True,
        handle_validation_error=False,
        # include_domains=[...],
        # exclude_domains=[...],
        # name="...",            # overwrite default tool name
        # description="...",     # overwrite default tool description
        # args_schema=...,       # overwrite default args_schema: BaseModel
    )
    tavily_results = tavily_tool.invoke(query)
    # logger.debug(tavily_results)
    return tavily_results


# set llm model config ##
# OLLAMA_MODEL_CONFIG = ollama_llm_config(model='llama3.2:1b', temperature=0.0)
# OLLAMA_CHAT_CONFIG = chat_ollama_config(model='llama3.2:1b', temperature=0.0)
TODAY = datetime.datetime.now().strftime('%Y-%m-%d')

if __name__ == '__main__':
    logger.error('this is not the main function, exiting ...')
    sys.exit()
