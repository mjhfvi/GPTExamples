from __future__ import annotations

from datetime import datetime

from langchain_chroma import Chroma


def connect_local_chromadb(CHROMA_COLLECTION_NAME, EMBEDDINGS) -> Chroma:
    """connect to chroma   HttpClient Library\nuse 'CHROMA_HOST' for host address\nuse 'CHROMA_PORT' for port number"""
    start_time = datetime.now()
    print('\nConnecting to Chroma DB ...')

    try:
        VECTOR_STORE = Chroma(
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_function=EMBEDDINGS,
            # Where to save data locally, remove if not necessary
            persist_directory='./chroma_langchain_db',
        )
        end_time = datetime.now()
        print('Successfully Connected to Chroma DB: ',
              'Duration: {}'.format(end_time - start_time))
        return VECTOR_STORE
    except Exception as error:
        print('\nSomething went wrong when connect to chroma db: ',
              error, '\nError in Definition: ', __name__, '\nExiting ...')
        exit(1)
    # finally:
        # end_time = datetime.now()
        # print("\nFinished Connect to Chroma DB: ", 'Duration: {}'.format(end_time - start_time))


# def connect_chromadb(CHROMA_HOST: str = "127.0.0.1", CHROMA_PORT: int = 8000, CHROMA_COLLECTION_NAME: str = "test") -> Chroma.HttpClient:
#     """connect to chroma   HttpClient Library\nuse 'CHROMA_HOST' for host address\nuse 'CHROMA_PORT' for port number"""
#     start_time = datetime.now()
#     try:
#         # CHROMA_CLIENT = Chroma.HttpClient(
#         #     host=CHROMA_HOST,
#         #     port=CHROMA_PORT,
#         #     ssl=False
#         # )
#         CHROMA_CLIENT = Chroma(
#             collection_name=CHROMA_COLLECTION_NAME,
#             # embedding_function=OpenAIEmbeddings(),
#             client=HttpClient(
#                 host="localhost",
#                 port=8000,
#                 ssl=False,
#                 # headers: Optional[Dict[str, str]] = None,
#                 # settings: Optional[Settings] = None,
#                 tenant=DEFAULT_TENANT,
#                 database=DEFAULT_DATABASE
#                 )
#             )

#         # CHROMA_CLIENT = Chroma(
#         #     collection_name=CHROMA_COLLECTION_NAME,
#         #     client = HttpClient(
#         #         host="localhost",
#         #         port=8000,
#         #         tenant=DEFAULT_TENANT,
#         #         database=DEFAULT_DATABASE,
#         #         ssl=False,
#         #         # headers: Optional[Dict[str, str]] = None,
#         #         # settings: Optional[Settings] = None,
#         #     )
#         # )
#         return CHROMA_CLIENT
#     except Exception as error:
#         print("Something went wrong when connect to chroma db: ", error, "\nError in Definition: ", __name__, "\nExiting ...")
#         exit(1)
#     finally:
#         end_time = datetime.now()
#         print("\nFinished connect to chroma db: ", 'Duration: {}'.format(end_time - start_time))


# def add_chromadb(CHROMA_CLIENT: str, CHROMA_COLLECTION_NAME: str = "test", DATA: any = list) -> chromadb.add:
#     """add data to chroma db"""
#     start_time = datetime.now()
#     try:
#         print("Adding Data to Chroma DB ...")
#         COLLECTION = CHROMA_CLIENT.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
#         print(f"Collection {CHROMA_COLLECTION_NAME} Created. Adding Documents.\n")
#         COLLECTION.add(
#             documents=[
#                 'This is a document about pineapple',
#                 'This is a document about oranges'
#             ],
#             ids=['id1', 'id2']
#             )

#         print("Querying Chroma DB ...\n")
#         # RESULTS = COLLECTION.query(
#         #     """Chroma will embed this in the DB and return the results.""",
#         #     query_texts=['This is a query document about hawaii'],
#         #     n_results=2     # how many results to return
#         # )
#         # print("print value 'RESULTS': ", RESULTS)
#     except Exception as error:
#         print("Something went wrong when Adding Data to Chroma DB: ", error, "\nError in Definition: ", __name__, "\nExiting ...")
#         exit(1)
#     finally:
#         end_time = datetime.now()
#         print("\nFinished connect to chroma db: ", 'Duration: {}'.format(end_time - start_time))


# def list_chromadb(CHROMA_CLIENT: str, CHROMA_COLLECTION_NAME) -> chromadb.list_collections:
#     """list collection from chroma db"""
#     start_time = datetime.now()
#     try:
#         COLLECTION_LIST = CHROMA_CLIENT.list_collections()
#         print('Collection List: ' + COLLECTION_LIST)

#         COLLECTION = CHROMA_CLIENT.get_collection(name=CHROMA_COLLECTION_NAME)
#         print(COLLECTION.get())

#     except Exception as error:
#         print("Something went wrong when list collection chroma db: ", error, "\nError in Definition: ", __name__, "\nExiting ...")
#         exit(1)
#     finally:
#         end_time = datetime.now()
#         print("\nFinished loading list collection: ", 'Duration: {}'.format(end_time - start_time))
