from __future__ import annotations

import re
import sys
from unicodedata import normalize

from chromadb.config import Settings
from deep_translator import GoogleTranslator
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_ollama.llms import OllamaLLM
from loguru import logger
from rich import inspect
from rich import print_json

from langchain.docstore.document import Document


def chat_ollama_config(model: str = 'llama3.2:1b', temperature: int = 0.2):
    # logger.info('starting ollama config')
    ollama_config = ChatOllama(
        model=model,   # llama3.2:3b, llama3.2:1b, mistral:7b
        temperature=temperature,
        num_predict=256,
        cache=False,
        base_url='http://localhost:11434',
        # format="json",
    )
    return ollama_config


def ollama_llm_config(model: str = 'llama3.2:1b', temperature: int = 0.2):
    # logger.info('starting ollama config')
    # model = OllamaLLM(model="llama3.2:1b")
    ollama_config = OllamaLLM(
        model=model,   # llama3.2:3b, llama3.2:1b, mistral:7b
        temperature=temperature,
        num_predict=256,
        cache=None,
        base_url='http://localhost:11434',
        format='',
    )
    return ollama_config


# def build_document(document_data, date_of_document="01-01-2000", file_name="example.txt", service_provider=None):
#         logger.info('building data structure in document')
#         # print(document_data)
#         # logger.debug('building data structure in document')
#         rebuild_document = [Document(metadata={'file_name': file_name, 'service_provider': service_provider, 'invoice_date': date_of_document}, page_content=str(document_data))]
#         logger.success('successfully build data structure in document')
#         return rebuild_document


# def embed_document(document_data, chromadb_directory, chroma_collection_name, EMBEDDINGS_MODEL_NAME) -> HuggingFaceEmbeddings:
#         logger.info('starting embeddings document data process')
#         embedding_text = Chroma.from_documents(
#             documents=document_data,
#             # embedding=embeddings_data_output,
#             collection_name=chroma_collection_name,
#             # embedding_function=embeddings_data_output,
#             embedding=HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME),
#             path=chromadb_directory,
#             client_settings=Settings(is_persistent=True)
#         )
#         logger.success('successfully embeddings document data')
#         embeddings_number = str(len(embedding_text))
#         logger.debug('number of embeddings: ' + embeddings_number)
#         return embedding_text


if __name__ == '__main__':
    logger.error('this is not the main function, exiting ...')
    sys.exit()
