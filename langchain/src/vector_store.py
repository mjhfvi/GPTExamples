'''vector store data from chromadb functions'''
from __future__ import annotations

import getpass
import os
import sys

import chromadb
from chromadb.config import DEFAULT_DATABASE
from chromadb.config import DEFAULT_TENANT
from chromadb.config import Settings
from langchain_chroma import Chroma
from loguru import logger
from pydantic import BaseModel
from pydantic import conint
from pydantic import Field
from pydantic import ValidationError
from rich import inspect
from rich import print_json


class ChromaConnectionString():
    """
    A class representing a connection string to a Chroma database.

    Attributes:
        chromadb_path (str): The path to the Chroma database.

    Methods:
        get_client: Returns a PersistentClient instance connected to the Chroma database.
    """

    def __init__(
        self,
        connection_method: str = None,
        chroma_host: str = 'localhost',
        chroma_port: int = None,
        chromadb_path: str = 'chroma_db',
        chroma_collection_name: str = None,
        tenant_name: str = DEFAULT_TENANT,
        database_name: str = DEFAULT_DATABASE
    ):

        self.chroma_host = chroma_host
        self.chroma_port = chroma_port
        self.chroma_collection_name = chroma_collection_name
        self.chromadb_path = chromadb_path
        self.tenant_name = tenant_name
        self.database_name = database_name
        self.connection_method = connection_method

    def connection_string(self):
        if self.connection_method == 'local':
            logger.debug('local connection method')
            return self.get_client(self.chromadb_path)
            # return 'local'
        elif self.connection_method == 'http':
            logger.debug('http connection method')
            return self.get_client_http(self.chroma_host, self.chroma_port, self.tenant_name, self.database_name)
            # return 'http'

    def list_collections(self):
        connection_of_string = self.connection_string()
        # inspect(connection_of_string)

        list_all_collections = connection_of_string.list_collections()
        # print(list_all_collections[0].name)

        number_of_collections = len(list_all_collections)

        if number_of_collections == 0:
            logger.debug('chroma db empty, no collections found')
            return None

        list_of_collections = []
        for collection in list_all_collections:
            list_of_collections.append(collection.name)
        # print(list_of_collections[0])
        # inspect(sorted(list_of_collections, reverse=True))
        # print(sorted(list_of_collections))
        return sorted(list_of_collections, reverse=True)

    def get_client(self, chromadb_path) -> chromadb.PersistentClient:
        return chromadb.PersistentClient(
            path=chromadb_path,
            settings=Settings(
                allow_reset=True,
                is_persistent=True,
                anonymized_telemetry=False
            )
        )

    def get_client_http(self, chroma_host, chroma_port, tenant_name, database_name) -> chromadb.HttpClient:
        return chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            # ssl = False,
            # headers = None,
            settings=Settings(
                allow_reset=True,
                anonymized_telemetry=False
            ),
            tenant=tenant_name,
            database=database_name,
        )

    def create_collection(self):
        logger.debug(
            f"creating collection {self.chroma_collection_name} in db")
        connection_of_string = self.connection_string()
        list_all_collections = connection_of_string.list_collections()
        # print(list_all_collections)
        # list_of_collections = self.list_collections()
        if self.chroma_collection_name in list_all_collections[0].name:
            logger.warning(
                f"collection named '{self.chroma_collection_name}' already exists in db")
            return None

        else:
            # connection_of_string = chromadb.AdminClient()
            # connection_of_string.create_tenant(name=self.tenant_name)
            # connection_of_string.create_database(name=self.database_name)
            # connection_of_string.create_tenant(Settings(name='invoice'))
            connection_of_string.create_collection(
                name=self.chroma_collection_name,
                get_or_create=True
            )
            logger.debug(
                f"collection '{self.chroma_collection_name}' created successfully in db")
            return self.chroma_collection_name

    def delete_collection(self):
        connection_of_string = self.connection_string()
        list_all_collections = connection_of_string.list_collections()
        # print(self.chroma_collection_name)
        # inspect(list_all_collections[0].name)

        if not list_all_collections:
            logger.debug('chroma db empty, no collections found')
            return None

        if self.chroma_collection_name in list_all_collections[0].name:
            logger.debug(
                f"found collection '{self.chroma_collection_name}' in db")
            # connection_of_string.delete_collection(self.chroma_collection_name)
            # logger.debug('collection deleted successfully')
            # logger.debug('list all the collections in db: ')
            # logger.debug('\n'.join(list_of_collections))
            # return

        else:
            logger.debug(
                f"no collection named '{self.chroma_collection_name}' found in db")
            # logger.debug('view all the collections in db: ')
            # logger.debug('\n'.join(list_of_collections))
            return None

    def reset_chromadb(self):
        # connection_string = self.connection_string(chromadb_path=self.chromadb_path)
        connection_of_string = self.connection_string()
        connection_of_string.reset()
        logger.debug('chromadb reset successfully')


class ChromaCollectionConnectionString(BaseModel):
    """
    A class representing a connection string to a Chroma database.

    Attributes:
        chromadb_path (str): The path to the Chroma database.

    Methods:
        get_client: Returns a PersistentClient instance connected to the Chroma database.
    """

    def __init__(self, chromadb_path: str = 'chroma_db', chroma_collection_name: str = None):
        self.chromadb_path = chromadb_path
        self.chroma_collection_name = chroma_collection_name

    def get_client(self, chromadb_path=None) -> chromadb.PersistentClient:
        path = chromadb_path or self.chromadb_path
        return chromadb.PersistentClient(
            path=path,
            settings=Settings(
                allow_reset=True,
                is_persistent=True,
                anonymized_telemetry=False
            )
        )

    def collection_connection_string(self, chromadb_path=None) -> chromadb.PersistentClient:
        # logger.debug(f"successfully build a connection string for Chroma DB collection {self.chroma_collection_name}")
        connection_string = self.get_client(chromadb_path=chromadb_path)
        # collection_connection_string = connection_string.get_collection(name=self.chroma_collection_name)
        return connection_string.get_or_create_collection(name=self.chroma_collection_name)

    def collection_get_data(self):
        return self.collection_connection_string().get()

    def collection_search_data(self, ids=None, document=None):
        collection_get_data = self.collection_connection_string().get(
            # where={"ids": ids},
            # where={"documents": document},
            where_document={'$contains': document},
            include=['embeddings', 'metadatas', 'documents']
        )
        return collection_get_data

    def collection_add_data(self, data=None, ids=None, documents=None, metadatas=None, embeddings=None):
        self.collection_connection_string().add(
            ids=ids,
            # tenant=tenant,
            # database=database,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents,
            # uris=uris,
            # data=data
        )

        logger.debug('successfully added data to collection: ' +
                     f'{self.collection_connection_string().name}')
        # get_data_from_collection(connection_string)
        # return connection_string

    def collection_query_data(self, query_data='example', number_results=1):
        logger.debug('querying collection: ' +
                     f'{self.collection_connection_string().name}' + '  with query string: ' + f'{query_data}')
        collection_query_data = self.collection_connection_string().query(
            query_texts=[query_data],
            n_results=number_results,
            # where={"metadata_field": query_data},
            # where_document={'$contains': query_data},
            # query_embeddings=[query_embeddings],
            # include=["embeddings", "metadatas", "documents"]
        )
        return collection_query_data

    def collection_remove_data(self, ids=None):
        connection_string = self.collection_connection_string()
        connection_string.delete(ids=ids)

    def collection_delete(self, query_data='example'):
        logger.debug('deleting collection: ' +
                     f'{self.collection_connection_string().name}')
        self.collection_connection_string().delete(
            where={'metadata_field': query_data},
            where_document={'$contains': query_data},
        )


def query_chromadb(query) -> list:
    # logger.debug('query chroma db for data.')
    ollama_model_name = 'llama3.2:1b'   # llama3.2:3b, llama3.2:1b
    embedding_function = OllamaEmbeddings(model=ollama_model_name)

    vector_store_string = Chroma(
        embedding_function=embedding_function,
        persist_directory=os.environ['CHROMA_DB_PATH'],
        collection_name=os.environ['CHROMA_COLLECTION_NAME'],
        # create_collection_if_not_exists=True
    )

    query_data = vector_store_string.similarity_search(query)

    if query_data:
        logger.debug('query chroma db for: ' + str(query))
        logger.debug('got data from chromadb: ' + str(query_data))
        return query_data
    else:
        return None
    # return query_data
    # else:
    #     logger.warning('no data found in chromadb.')

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


def create_tenant_database(chroma_host='localhost', chroma_port=None, tenant_name='default_tenant', database_name='default_database'):
    adminClient = chromadb.AdminClient(Settings(
        chroma_api_impl='chromadb.api.fastapi.FastAPI',
        chroma_server_host=chroma_host,
        chroma_server_http_port=chroma_port,
        chroma_server_ssl_enabled=False,
        allow_reset=True,
        is_persistent=True,
        anonymized_telemetry=False
    ))

    # list_of_tenant = adminClient.get_tenant(tenant_name)
    # inspect("Tenants: " + str(list_of_tenant))
    # if list_of_tenant:
    #     logger.debug(f"tenant '{tenant_name}' already exists")
    #     return None
    # else:
    # logger.debug(f"tenant '{tenant_name}' does not exist")
    try:
        list_of_tenant = adminClient.create_tenant(tenant_name)
        adminClient.create_database(database_name, tenant_name)
        logger.debug(
            f'successfully created tenant {tenant_name} and database {database_name}')
        # inspect(list_of_tenant)
        return list_of_tenant
    except Exception as error:
        logger.warning(f'error creating tenant: {error}')
        return None

    # get_tenants = adminClient.get_tenant(tenant_name)
    # inspect("Tenants: " + str(get_tenants))


if __name__ == '__main__':
    print('this is not the main function, exiting ...')
    sys.exit()
