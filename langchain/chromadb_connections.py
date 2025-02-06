from __future__ import annotations

import os
import sys

from icecream import ic
from loguru import logger
from prettyformatter import pprint
from pydantic import BaseModel
from pydantic import conint
from pydantic import Field
from pydantic import ValidationError
from rich import inspect
from src import documents_loader
from src import vector_store
from src.config_tools import Error_Handler
from src.llm_tools import TODAY


@Error_Handler
def main():
    logger.info('starting main function')
    # vector store data ##
    # chroma_connection_string_data = vector_store.chroma_connection_string(chromadb_path=env_var[2])
    # chroma_collection_connection_string_data = vector_store.ChromaConnectionString(chromadb_path=env_var[2], chroma_collection_name=env_var[3])
    chroma_collection_connection_string_data = vector_store.ChromaConnectionString(
        connection_method='http',
        chroma_host=os.environ['CHROMA_HOST'],
        chroma_port=os.environ['CHROMA_PORT'],
        chroma_collection_name=os.environ['CHROMA_COLLECTION_NAME'],
        tenant_name=os.environ['CHROMA_TENANT_NAME'],
        database_name=os.environ['CHROMA_DATABASE_NAME']
    )
    # inspect(chroma_collection_connection_string_data)
    # chroma_collection_connection_string_data.reset_chromadb()

    # list_of_collections = chroma_collection_connection_string_data.list_collections()
    # ic(inspect(list_of_collections))

    # create_tenant_database = vector_store.create_tenant_database(chroma_host='localhost', chroma_port=32312, tenant_name='invoice', database_name='bezeqint')
    # ic(inspect(create_tenant_database))

    # create_collection = chroma_collection_connection_string_data.create_collection()
    # ic(inspect(create_collection))

    # chroma_collection_connection_string_data.delete_collection()

    # collection_get_data = chroma_collection_connection_string_data.collection_get_data()
    # print(collection_get_data)
    # collection_get_data = chroma_collection_connection_string_data.collection_search_data(
    #     document='invoice_information')
    # print(collection_get_data)
    # chroma_collection_connection_string_data.collection_add_data()
    # collection_query_data = chroma_collection_connection_string_data.collection_query_data(query_data=env_var[4], number_results=1)
    # print(collection_query_data)
    # collection_query_data = chroma_collection_connection_string_data.collection_remove_data(ids=['id1'])
    # print(collection_query_data)
    # chroma_collection_connection_string_data.collection_delete()

    # list_of_collections = chroma_collection_connection_string_data.list_collections()
    # inspect(list_of_collections)
if __name__ == '__main__':
    main()
