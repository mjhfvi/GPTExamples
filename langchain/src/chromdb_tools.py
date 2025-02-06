from __future__ import annotations

import os
import sys

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger
from rich import inspect
from rich import print_json
# from langchain_community.vectorstores import Chroma
# from langchain_ollama import ChatOllama
# from langchain_ollama.llms import OllamaLLM
# from langchain.docstore.document import Document


# embedding_function = OllamaEmbeddings(model=os.getenv('LLM_MODEL', 'llama3.2:1b'),base_url=os.getenv('OLLAMA_URL', 'http://localhost:11434'))
# embedding_function = HuggingFaceEmbeddings(model_name=os.environ['EMBEDDINGS_MODEL_NAME'])
# embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(os.environ['EMBEDDINGS_MODEL_NAME'])
# embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=os.environ['EMBEDDINGS_MODEL_NAME'])
embedding_function = HuggingFaceEmbeddings(model_name=os.environ['EMBEDDINGS_MODEL_NAME'], model_kwargs={
                                           'trust_remote_code': True}, show_progress=True)

vector_store_connection = chromadb.HttpClient(
    host=os.environ['CHROMA_HOST'],
    port=os.environ['CHROMA_PORT'],
    # ssl = False,
    # headers = None,
    settings=Settings(
        allow_reset=True,
        anonymized_telemetry=False,
        is_persistent=True,
    ),
    tenant=os.environ['CHROMA_TENANT_NAME'],
    database=os.environ['CHROMA_DATABASE_NAME'],
    # tenant=DEFAULT_TENANT,
    # database=DEFAULT_DATABASE,
    # collection_name=os.environ['CHROMA_COLLECTION_NAME']
)

vector_store_string = Chroma(
    collection_name=os.environ['CHROMA_COLLECTION_NAME'],
    embedding_function=embedding_function,
    client_settings=Settings(
        chroma_server_host=os.environ['CHROMA_HOST'],
        chroma_server_http_port=os.environ['CHROMA_PORT'],
    ),
    create_collection_if_not_exists=True
)


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
