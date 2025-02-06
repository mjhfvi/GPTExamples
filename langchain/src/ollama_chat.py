from __future__ import annotations

import os
import sys

from langchain_community.cache import InMemoryCache
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from loguru import logger

from langchain.prompts import ChatPromptTemplate
# from langchain_core.prompts import ChatPromptTemplate


def start_ollama_chat(query_question, chroma_collection_name, query_data, retriever, max_output_tokens='-1', format=None, temperature=0, EMBEDDINGS_MODEL_NAME='all-MiniLM-L6-v2'):
    # retriever = query_data_from_vector_store(chroma_collection_name=chroma_collection_name, query_data=query_data)
    logger.debug('preview query data from chroma db: ')
    logger.debug(retriever)
    model = ChatOllama(
        model=os.getenv('LLM_MODEL', 'llama3.2:1b'),
        temperature=temperature,
        format=format,
        num_predict=max_output_tokens,
        verbose=True
    )
    logger.debug('using cache in memory')
    set_llm_cache(InMemoryCache())
    # logger.debug('using SQLite cache on disk')
    # set_llm_cache(SQLiteCache(database_path=".cache.db"))
    HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)
    prompt_template = ChatPromptTemplate.from_messages(
        [('system', query_question), ('user', '{text}')]
    )
    prompt = prompt_template.invoke({'system': 'query', 'text': retriever})
    prompt.to_messages()
    response = model.invoke(prompt)
    print(response.content)


if __name__ == '__main__':
    logger.error('this is not the main function, exiting ...')
    sys.exit()
