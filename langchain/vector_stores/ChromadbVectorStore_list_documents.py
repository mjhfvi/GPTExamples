from __future__ import annotations

import chromadb
from chromadbx import UUIDGenerator

# Chroma DB Server Variables
CHROMA_HOST = '172.22.54.208'
CHROMA_PORT = 8000
CHROMA_COLLECTION_NAME = 'mjhfvi'

# Connect to Chroma DB with HttpClient Library
chroma_client = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT,
    ssl=False
)

COLLECTION_LIST = chroma_client.list_collections()
print('Collection List: ' + COLLECTION_LIST)

COLLECTION = chroma_client.get_collection(name=CHROMA_COLLECTION_NAME)
print(COLLECTION.get())
