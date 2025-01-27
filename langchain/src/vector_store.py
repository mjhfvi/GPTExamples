from __future__ import annotations

import getpass
import os
import sys

import chromadb
from chromadb.config import DEFAULT_DATABASE
from chromadb.config import DEFAULT_TENANT
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from loguru import logger
from rich import inspect
from rich import print_json


def Error_Handler(func):
    def Inner_Function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            logger.exception(
                f'An error occurred while running function: {func.__name__}, please check the logs for more information. ')
            # inspect(func)   # for more information set all=True
        except KeyboardInterrupt:
            logger.error('program terminated by user.')
    return Inner_Function


@Error_Handler
class ChromaConnectionString:
    """
    A class representing a connection string to a Chroma database.

    Attributes:
        chromadb_path (str): The path to the Chroma database.

    Methods:
        get_client: Returns a PersistentClient instance connected to the Chroma database.
    """

    def __init__(self, chromadb_path='chroma_db'):
        self.chromadb_path = chromadb_path

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

    def connection_string(self, chromadb_path=None) -> chromadb.PersistentClient:
        logger.debug(
            'successfully build a connection string for Chroma DB collection')
        return self.get_client(chromadb_path=chromadb_path)

    def list_collections(self):
        # try:
        list_all_collections = self.connection_string(
            chromadb_path=self.chromadb_path).list_collections()
        number_of_collections = len(list_all_collections)

        if number_of_collections == 0:
            logger.debug('chroma db empty, no collections found')

        list_of_collections = []
        for collection in list_all_collections:
            list_of_collections.append(collection.name)
        return sorted(list_of_collections, reverse=True)

        # except Exception:
        #     logger.exception(
        #         'An error occurred while running the program, please check the logs for more information. ')
        #     sys.exit(1)
        # except KeyboardInterrupt:
        #     logger.error('program terminated by user.')

    def create_collection(self, chroma_collection_name=None):
        # try:
        # logger.debug(f"creating collection {chroma_collection_name} in db")
        list_of_collections = self.list_collections()
        if chroma_collection_name in list_of_collections:
            logger.warning(
                f"collection named '{chroma_collection_name}' already exists in db")
            # return None

        else:
            logger.debug(
                f"collection '{chroma_collection_name}' created successfully in db")
            return self.connection_string(chromadb_path=self.chromadb_path).create_collection(name=chroma_collection_name, get_or_create=True)

        # except Exception:
        #     logger.exception(
        #         'An error occurred while running the program, please check the logs for more information. ')
        #     sys.exit(1)
        # except KeyboardInterrupt:
        #     logger.error('program terminated by user.')

    def delete_collection(self, chroma_collection_name=None):
        # try:
        list_of_collections = self.list_collections()
        if not list_of_collections:
            logger.debug('chroma db empty, no collections found')
            return None

        if chroma_collection_name in list_of_collections:
            logger.debug(
                f"found collection '{chroma_collection_name}' in db")
            self.connection_string(chromadb_path=self.chromadb_path).delete_collection(
                chroma_collection_name)
            logger.debug('collection deleted successfully')
            # logger.debug('list all the collections in db: ')
            # logger.debug('\n'.join(list_of_collections))
            # return

        else:
            logger.debug(
                f"no collection named '{chroma_collection_name}' found in db")
            # logger.debug('view all the collections in db: ')
            # logger.debug('\n'.join(list_of_collections))
            return None

        # except Exception:
        #     logger.exception(
        #         'An error occurred while running the program, please check the logs for more information. ')
        #     sys.exit(1)
        # except KeyboardInterrupt:
        #     logger.error('program terminated by user.')

    def reset_chromadb(self):
        # try:
        # connection_string = self.connection_string(chromadb_path=self.chromadb_path)
        self.connection_string(chromadb_path=self.chromadb_path).reset()

        # except Exception:
        #     logger.exception(
        #         'An error occurred while running the program, please check the logs for more information. ')
        #     sys.exit(1)
        # except KeyboardInterrupt:
        #     logger.error('program terminated by user.')


class ChromaCollectionConnectionString:
    """
    A class representing a connection string to a Chroma database.

    Attributes:
        chromadb_path (str): The path to the Chroma database.

    Methods:
        get_client: Returns a PersistentClient instance connected to the Chroma database.
    """

    def __init__(self, chromadb_path='chroma_db', chroma_collection_name=None):
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
        # try:
        return self.collection_connection_string().get()

        # except Exception:
        #     logger.exception(
        #         'An error occurred while running the program, please check the logs for more information. ')
        #     sys.exit(1)
        # except KeyboardInterrupt:
        #     logger.error('program terminated by user.')

    def collection_search_data(self, ids=None, document=None):
        # try:
        collection_get_data = self.collection_connection_string().get(
            # where={"ids": ids},
            # where={"documents": document},
            where_document={'$contains': document},
            include=['embeddings', 'metadatas', 'documents']
        )
        return collection_get_data

        # except Exception:
        #     logger.exception(
        #         'An error occurred while running the program, please check the logs for more information. ')
        #     sys.exit(1)
        # except KeyboardInterrupt:
        #     logger.error('program terminated by user.')

    def collection_add_data(self, data=None, ids=None, documents=None, metadatas=None, embeddings=None):
        # try:
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

        # except Exception:
        #     logger.exception(
        #         'An error occurred while running the program, please check the logs for more information. ')
        #     sys.exit(1)
        # except KeyboardInterrupt:
        #     logger.error('program terminated by user.')

    def collection_query_data(self, query_data='example', number_results=1):
        # try:
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

        # except Exception:
        #     logger.exception(
        #         'An error occurred while running the program, please check the logs for more information. ')
        #     sys.exit(1)
        # except KeyboardInterrupt:
        #     logger.error('program terminated by user.')

    def collection_remove_data(self, ids=None):
        # try:
        connection_string = self.collection_connection_string()
        connection_string.delete(ids=ids)

        # except Exception:
        #     logger.exception(
        #         'An error occurred while running the program, please check the logs for more information. ')
        #     sys.exit(1)
        # except KeyboardInterrupt:
        #     logger.error('program terminated by user.')

    def collection_delete(self, query_data='example'):
        # try:
        logger.debug('deleting collection: ' +
                     f'{self.collection_connection_string().name}')
        self.collection_connection_string().delete(
            where={'metadata_field': query_data},
            where_document={'$contains': query_data},
        )

        # except Exception:
        #     logger.exception(
        #         'An error occurred while running the program, please check the logs for more information. ')
        #     sys.exit(1)
        # except KeyboardInterrupt:
        #     logger.error('program terminated by user.')


# @Error_Handler
def query_chromadb(query) -> list:
    try:
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

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')

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


if __name__ == '__main__':
    print('this is not the main script, exiting ...')
    sys.exit()
