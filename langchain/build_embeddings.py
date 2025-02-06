from __future__ import annotations

import json
import os
import sys
from collections.abc import Sequence
from typing import Optional

import chromadb
from chromadb.api.types import CollectionMetadata
from chromadb.api.types import DataLoader
from chromadb.api.types import Documents
from chromadb.api.types import Embeddable
from chromadb.api.types import EmbeddingFunction
from chromadb.api.types import Embeddings
from chromadb.api.types import GetResult
from chromadb.api.types import IDs
from chromadb.api.types import Include
from chromadb.api.types import IncludeMetadataDocumentsEmbeddings
from chromadb.api.types import IncludeMetadataDocumentsEmbeddingsDistances
from chromadb.api.types import Loadable
from chromadb.api.types import Metadatas
from chromadb.api.types import QueryResult
from chromadb.api.types import URIs
from chromadb.api.types import Where
from chromadb.api.types import WhereDocument
from chromadb.config import DEFAULT_DATABASE
from chromadb.config import DEFAULT_TENANT
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions import create_langchain_embedding
from dotenv import load_dotenv
from icecream import ic
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger
from prettyformatter import pprint
from rich import inspect
from rich import print_json
from src import chromdb_tools
from src import documents_embedding
from src import documents_loader
from src import llm_tools
from src import vector_store
from src.config_tools import Error_Handler
# from langchain_ollama import OllamaEmbeddings

datasets_path = 'datasets/Bezeqint/raw/llm_datasets/'
embedding_folder_path = 'datasets/Bezeqint/raw/embedded_datasets/'


@Error_Handler
def main():
    logger.info('running main function')
    # load_documents_string = documents_loader.DocumentsLoaders(path=datasets_path)
    # file_data = load_documents_string.load_json_files()
    # json_data = json.loads(file_data)
    # inspect(json_data)

    file_data = '''invoice_details"
main_customer_number: 102063827
source_tax_invoice_number: 2024200141400
date_of_invoice_preparation: 31/01/2024
billing_period: 01/2024"
vendor_name: Bezeq International Ltd.
customer_name: Tzahi Cohen
paying_customer_number: 991865405
subtotal: 55.82
tax_amount: 10.49
total_amount: 65.31'''

    metadata = {'source': 'Invoice_200141400.pdf'}

    # document_data = Document(
    #     page_content=file_data,
    #     metadata={"source": "Invoice_200141400.pdf"}
    # )
    # print(document_data)

    # create_tenant_database = vector_store.create_tenant_database(
    #     chroma_host=os.environ['CHROMA_HOST'],
    #     chroma_port=os.environ['CHROMA_PORT'],
    #     tenant_name=os.environ['CHROMA_TENANT_NAME'],
    #     database_name=os.environ['CHROMA_DATABASE_NAME'],
    # )
    # ic(inspect(create_tenant_database))

    # create_collection = vector_store_connection.get_or_create_collection(
    #     name=os.environ['CHROMA_COLLECTION_NAME'],
    #     # embedding_function=EmbeddingFunction(embedding_function),
    #     # data_loader=Optional[DataLoader[document_data]]
    # )
    # print("create collection successfully: ", create_collection)

    # vector_store_connection.create_collection(
    #     name=os.environ['CHROMA_COLLECTION_NAME'],
    #     metadata={"service": "bezeqint"},
    #     # embedding_function=embedding_function,
    #     # get_or_create=True,
    # )
    # print('running create collection')

    working_collections = chromdb_tools.vector_store_connection.get_collection(
        name=2024)

    # count_of_collections = vector_store_connection.count_collections()
    # print("number of collections: ", count_of_collections)
    # list_of_collections = vector_store_connection.list_collections()
    # print("list of collections: ", list_of_collections)

    working_collections.add(
        # ids="bb20b604-151b-43b2-92f8-4adf32d288aa",
        ids='01-2024',
        documents=file_data,
        metadatas=metadata,
        # embeddings=embedding_function,
    )
    print('adding documents to chromadb collection:', working_collections.name)

    # get_collection_settings = vector_store_connection.get_settings()
    # for line in get_collection_settings:
    #     print(line)

    # peek_of_collections = working_collections.peek()
    # print(peek_of_collections)

    # query_of_collections = working_collections.query(query_texts='invoice', include=['metadatas', 'documents'])
    # print(query_of_collections, "\n\n")
    # inspect(working_collections, all=True)

    get_collection_data = working_collections.get(
        # ids='01-2024',
        where_document={'$contains': '991865405'},
        limit=5,
        # include=['embeddings', 'metadatas', 'documents'],
        include=['metadatas', 'documents'],
    )
    print('get_collection_data', get_collection_data)

    # working_collections.delete(
    #     ids='01-2024'
    #     ids="bb20b604-151b-43b2-92f8-4adf32d288aa",
    # )
    # print('successfully deleted collection from db')

    # vector_store_connection.delete_collection(os.environ['CHROMA_COLLECTION_NAME'])
    # print("collection '" + os.environ['CHROMA_COLLECTION_NAME'] + "' deleted from chromadb")
    # vector_store_connection.reset()
    # print('chromadb reset successfully')


if __name__ == '__main__':
    main()
