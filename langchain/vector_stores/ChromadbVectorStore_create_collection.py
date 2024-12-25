# Source: https://python.langchain.com/docs/integrations/vectorstores/chroma/
from __future__ import annotations

import chromadb

# Chroma DB Server Variables
CHROMA_HOST = '172.22.54.208'
CHROMA_PORT = 8000
CHROMA_COLLECTION_NAME = 'mjhfvi'

# Connect to Chroma DB with HttpClient Library
CHROMA_CLIENT = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT,
    ssl=False
)

# Connect to Chroma DB with Client Library
# chroma_client = chromadb.Client()

# Create Collections by Name
CHROMA_CLIENT.create_collection(name=CHROMA_COLLECTION_NAME)

# Get Collections by Name
collections = CHROMA_CLIENT.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME)
print(collections)
