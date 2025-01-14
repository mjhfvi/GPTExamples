from __future__ import annotations

import os
import sys

import chromadb
from loguru import logger


def chroma_db_setup(chroma_db_path='chroma_db'):
    """
    Set up a Chroma database.

    Set up a Chroma database by connecting to the given path and returning the
    client object.

    Parameters
    ----------
    chroma_db_path : str
        The path to the Chroma database to connect to.

    Returns
    -------
    chroma_client : chromadb.PersistentClient
        The client object for the connected Chroma database.

    Raises
    ------
    Exception
        If an error occurs while connecting to the Chroma database, an exception
        is raised. The exception is printed to the console and the program exits.
    """
    try:
        # build Chroma DB client connection string
        chroma_client = chromadb.PersistentClient(
            path=chroma_db_path
        )
        logger.debug('build Chroma DB client successfully')
        return chroma_client

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_get_collection(chroma_client, chroma_collection_name, list_collection_names=False,):
    """
    Retrieve a collection of documents from the Chroma database.

    Parameters
    ----------
    chroma_client : chromadb.Client
        The client object used to interact with the Chroma database.
    chroma_collection_name : str
        The name of the collection to retrieve.

    Returns
    -------
    ChromaCollection
        The ChromaCollection object containing the documents in the specified collection.

    Raises
    ------
    Exception
        If an error occurs while retrieving the collection, an exception is raised. The exception is printed to the console.
    """
    try:
        logger.debug('retrieving collection data for: ' +
                     chroma_collection_name)
        # Retrieve all collections from the Chroma database
        list_of_collections = chroma_db_list_collections(chroma_client)

        # Check if the specified collection exists in the database
        if chroma_collection_name not in list_of_collections:
            logger.warning(
                f"no collection named '{chroma_collection_name}' found in db, please create a collection")
            if list_collection_names is True:
                logger.info('list all the collections in db: ')
                logger.debug('\n'.join(list_of_collections))
                # print('\n'.join(list_of_collections))
            return None

        # Retrieve the collection if it exists
        else:
            connection_string = chroma_client.get_collection(
                chroma_collection_name)
            logger.debug('successfully retrieved Chroma DB collection name')
            return connection_string

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_list_collections(chroma_client, list_collection_names=False):
    """
    List collections in the Chroma database.

    Parameters
    ----------
    chroma_client : chromadb.Client
        The client object used to interact with the Chroma database.
    list_collection_names : bool, optional
        If True, print the names of all collections in the database. Defaults to False.

    Returns
    -------
    list
        A list of collection objects if list_collection_names is True.

    Raises
    ------
    Exception
        If an error occurs while listing the collections, an exception is raised. The exception is printed to the console.
    """
    try:
        # Retrieve all collections from the Chroma database
        list_all_collections = chroma_client.list_collections()
        logger.debug('number of total collections in db: ' +
                     str(len(list_all_collections)))

        list_of_collections = []
        for collection in list_all_collections:
            list_of_collections.append(collection.name)
        collection_list = sorted(list_of_collections, reverse=True)

        # Print and return collection names if requested
        if list_collection_names is True:
            logger.info('list all the collections in db: ')
            logger.info('\n'.join(collection_list))
        return collection_list

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_create_collection(chroma_client, chroma_collection_name, list_collection_names=False):
    """
    Create a Chroma collection by name.

    If the collection already exists, an error is raised.

    Parameters
    ----------
    chroma_client : chromadb.PersistentClient
        The Chroma client object to create the collection for.
    chroma_collection_name : str
        The name of the collection to create.

    Returns
    -------
    collection : chromadb.Collection
        The newly created collection object.

    Raises
    ------
    Exception
        If an error occurs while connecting to the Chroma database, an exception
        is raised. The exception is printed to the console and the program exits.
    """
    try:
        # Get the list of existing collections
        list_of_collections = chroma_db_list_collections(chroma_client)

        # Check if the collection already exists
        if chroma_collection_name in list_of_collections:
            logger.warning(
                f"collection named '{chroma_collection_name}' already exists in db, exiting")
            # print(print_color.WARNING + f"collection named '{chroma_collection_name}' already exists in db, exiting", print_color.END)
            if list_collection_names is True:
                logger.info('list all the collections in db: ')
                # print(print_color.INFORMATION + 'list all the collections in db: ', print_color.END)
                logger.info('\n'.join(list_of_collections))
            sys.exit(1)

        else:
            # Create the collection if it doesn't exist
            collection = chroma_client.create_collection(
                name=chroma_collection_name,
                get_or_create=True,
            )
            logger.info(
                f"collection '{chroma_collection_name}' created successfully in db")
            # print(print_color.INFORMATION + f"collection '{chroma_collection_name}' created successfully in db", print_color.END)
            return collection

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_delete_collection(chroma_client, chroma_collection_name, list_collection_names=False):
    """
    Delete a specific collection from the Chroma database.

    Parameters
    ----------
    chroma_client : chromadb.Client
        The client object used to interact with the Chroma database.
    chroma_collection_name : str
        The name of the collection to be deleted.
    list_collection_names : bool, optional
        If True, print the names of all collections in the database after deletion. Defaults to False.

    Raises
    ------
    Exception
        If an error occurs while deleting the collection, an exception is raised. The exception is printed to the console.
    """
    try:
        # Retrieve the list of all collections in the Chroma database
        list_of_collections = chroma_db_list_collections(chroma_client)

        # Check if the database contains any collections
        if not list_of_collections:
            logger.debug('chroma db empty, no collections found, exiting')
            exit(0)

        # Check if the specified collection exists in the database
        if chroma_collection_name in list_of_collections:
            logger.debug(f"found collection '{chroma_collection_name}' in db")

            # Delete the collection
            chroma_client.delete_collection(chroma_collection_name)
            logger.debug('collection deleted successfully')

            # Print and return collection names if requested
            if list_collection_names is True:
                logger.debug('list all the collections in db: ')
                logger.debug('\n'.join(list_of_collections))
            exit(0)
        else:
            # If the specified collection is not found, print an error and list all collections
            logger.debug(
                f"no collection named '{chroma_collection_name}' found in db, exiting")
            logger.debug('view all the collections in db: ')
            logger.debug('\n'.join(list_of_collections))
            exit(0)

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_get_data_from_collection(connection_string):
    """
    get data from a Chroma DB collection.

    This function retrieves data from a specified Chroma DB collection. It can optionally list collection IDs.

    .get also supports the where and where document filters. If no ids are supplied, it will return all items in the collection that match the where and where document filters.

    Parameters
    ----------
    connection_string : chromadb.Collection
        The collection object to query data from.
    list_collection_ids : bool, optional
        If True, queries and prints specific collection data. Defaults to False.

    Raises
    ------
    Exception
        If an error occurs while querying the collection, an exception is raised. The exception is printed to the console.
    """
    try:
        # Check if the collection is empty by examining the IDs
        if not connection_string.get()['ids']:
            logger.warning(f"collection '{connection_string.name}' is empty")
            # print(print_color.WARNING + f"collection '{connection_string.name}' is empty", print_color.END)

            # collection_data = connection_string.get(
            #     ids=['id1'],  # Specify which IDs to retrieve
            #     # Include embeddings and documents in the query
            #     include=['embeddings', 'documents', 'metadatas'],
            #     limit=5  # Limit the number of results
            # )
            # logger.debug('collection data results for: ')
            # print(print_color.INFORMATION + 'collection data results for: ', print_color.END, f'{connection_string.name}')
            # logger.debug(collection_data)
            # pprint(collection_data)
        else:
            # If list_collection_ids is False, query and print all collection data
            collection_data = connection_string.get(
                # Include embeddings and documents in the query
                include=['embeddings', 'documents', 'metadatas'],
                limit=5  # Limit the number of results
            )
            logger.debug('collection data results: ')
            logger.debug(collection_data)
            # print(print_color.INFORMATION + 'collection data results for: ', print_color.END, f'{connection_string.name}')
            # inspect(collection_data)
            # logger.debug(collection_data)
            # pprint(collection_data)

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_add_data_to_collection(connection_string, metadatas, documents, embeddings, print_collection_data=False):
    """
    Add data to a Chroma collection.

    Add data to a Chroma collection by specifying the documents and their
    corresponding ids.

    Parameters
    ----------
    connection_string : chromadb.Collection
        The Chroma collection object to add data to.

    Returns
    -------
    connection_string : chromadb.Collection
        The Chroma collection object with the newly added data.

    Raises
    ------
    Exception
        If an error occurs while adding the data, an exception is raised. The
        exception is printed to the console and the program exits.
    """
    try:
        logger.debug('documents: ', [documents[:100]], '\nmetadatas: ',
                     metadatas, '\nembeddings: ', [embeddings[0][:5]])
        # Add data to the collection
        connection_string.add(
            documents=[documents],
            ids=['id1'],
            metadatas=metadatas,
            embeddings=embeddings,
        )
        logger.info('successfully added data to collection ',
                    f'{connection_string.name}')
        if print_collection_data is True:
            chroma_db_get_data_from_collection(connection_string)
        return connection_string

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_query_data_from_collection(connection_string, query_data=None, number_results=5):
    """
    https://docs.trychroma.com/docs/querying-collections/query-and-get
    The query will return the n results closest matches to each query embedding, in order. An optional where filter dictionary can be supplied to filter by the metadata associated with each document. Additionally, an optional where document filter dictionary can be supplied to filter by contents of the document.
    """
    try:
        logger.debug('querying collection: ' + f'{connection_string.name}')
        # print(print_color.INFORMATION + 'data to query: ', print_color.END, query_data)

        query_results = connection_string.query(
            query_texts=['documents'],
            n_results=number_results,
            # where={"metadata_field": query_data},
            where_document={'$contains': query_data}
        )
        # logger.info('collection data results: ')
        # print(print_color.INFORMATION + 'collection data results: ', print_color.END)
        # pprint(query_results)
        return query_results

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def add_data_to_vector_store(chroma_collection_name, data_to_query):
    try:
        logger.info('adding data to chroma db')
        logger.debug('using chroma collection name: ' + chroma_collection_name)
        chroma_client = chroma_db_setup()
        connection_string = chroma_db_get_collection(
            chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=True)
        chroma_db_get_data_from_collection(connection_string)
        logger.success('successfully adding data to vector store')
        queried_data = query_data_from_vector_store(
            chroma_collection_name=chroma_collection_name, query_data=data_to_query)
        logger.debug('query data from vector store: ')
        logger.debug(queried_data)
        logger.success('successfully query data from vector store')
        return queried_data

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def query_data_from_vector_store(chroma_collection_name, query_data):
    try:
        logger.info('querying data from vector store')
        chroma_client = chroma_db_setup()
        connection_string = chroma_db_get_collection(
            chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=True)
        query_embedding = chroma_db_query_data_from_collection(
            connection_string, query_data=query_data)
        logger.success('successfully query data from vector store')
        logger.debug(query_embedding)
        return query_embedding

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_update_collection_name(connection_string, new_collection_name):
    try:
        # pprint(vars(connection_string))
        connection_string.modify(
            name=new_collection_name,
        )
        logger.info('successfully modified collection name to: ',
                    f'{connection_string.name}')
        # print(print_color.INFORMATION + f"successfully modified collection name to: '{connection_string.name}'" + print_color.END)

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_update_collection_data(connection_string, print_collection_data=False):
    try:
        connection_string.update(
            ids=['id1'],
            documents=['This is a document about strawberry'],
            metadatas=[{'document': '1', 'fruit': 'strawberry'}],
        )
        print('successfully updated collection data')
        if print_collection_data is True:
            chroma_db_get_data_from_collection(connection_string)

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_remove_data_from_collection(connection_string, ids=None, print_collection_data=False):
    try:
        if ids is not None:
            connection_string.delete(ids=ids)
            if print_collection_data is True:
                chroma_db_get_data_from_collection(connection_string)

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_reset_data_in_collection(chroma_db_path='../chroma_db/'):
    try:
        # chroma_client = chromadb.PersistentClient(path=chroma_db_path)
        logger.debug(vars(chromadb))
        # chroma_client = chromadb.PersistentClient(path=chroma_db_path, settings= Settings(allow_reset=True))
        # chroma_client.heartbeat()
        # chroma_client.reset()

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def chroma_db_from_documents_from_collection(chroma_collection_name, embedding_function, chroma_db_path='chroma_db'):
    try:
        from langchain_chroma import Chroma

        vector_store = Chroma(
            collection_name=chroma_collection_name,
            embedding_function=embedding_function,
            # Where to save data locally, remove if not necessary
            persist_directory=chroma_db_path,
            create_collection_if_not_exists=True
        )
        # chroma_db = chroma_client.from_documents(
        #     documents=documents,
        #     embedding=embeddings,
        #     persist_directory=chroma_db_path,
        #     collection_name=chroma_collection_name
        # )

        return vector_store

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


if __name__ == '__main__':
    print('this is not the main script, exiting ...')
    sys.exit()

    # chroma_collection_name = 'document_06'
    # # chroma_collection_name = "Invoice_2024-01-01"
    # new_collection_name = 'document_21'
    # data_to_query = 'Invoice'
    # modify_data = 'strawberry'

    # # ids = ["id2"]
    # # # ids = ["id1", "id2"]
    # # metadatas = [{"document": "1", "fruit": "pineapple"}, {"document": "2", "fruit": "oranges"}]
    # # documents = [
    # #     "This is a document about pineapple",
    # #     "This is a document about oranges"]

    # # data_to_query = ["This is a query document about hawaii"]

    # chroma_client = chroma_db_setup()
    # chroma_db_list_collections(chroma_client, list_collection_names=True)
    # connection_string = chroma_db_get_collection(chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=False)
    # # pprint(vars(connection_string))
    # # if connection_string is None:
    # #     print("building a new collection", chroma_collection_name)
    # #     chroma_db_create_collection(chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=False)

    # # chroma_db_create_collection(chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=False)
    # # chroma_db_delete_collection(chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=False)
    # chroma_db_reset_data_in_collection(chroma_client)
    # # chroma_db_add_data_to_collection(connection_string=connection_string, ids=ids, metadatas=metadatas, documents=documents, print_collection_data=True)
    # # chroma_db_get_data_from_collection(connection_string)
    # # chroma_db_query_data_from_collection(connection_string, query_data=data_to_query)
    # # chroma_db_update_collection_name(connection_string, new_collection_name)
    # # chroma_db_update_collection_data(connection_string, print_collection_data=True)
    # # chroma_db_remove_data_from_collection(connection_string, ids=ids, print_collection_data=True)
    # # print("this is not the main script, exiting ...")
    # # sys.exit()
