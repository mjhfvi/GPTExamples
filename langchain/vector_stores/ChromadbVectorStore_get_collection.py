# Source: https://python.langchain.com/docs/integrations/vectorstores/chroma/
from __future__ import annotations

import chromadb
# from chromadb.config import Settings

# Server DB
CHROMA_HOST = '172.22.54.208'
CHROMA_PORT = 8000
CHROMA_COLLECTION_NAME = 'mjhfvi'

# Connect to Chroma DB with HttpClient Library
chroma_client = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT,
    ssl=False
)

# Connect to Chroma DB with Client Library
CHROMA_CLIENT = chromadb.Client()
COLLECTION = CHROMA_CLIENT.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME)
print(COLLECTION)
