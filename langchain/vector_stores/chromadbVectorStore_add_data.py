# run local chromadb: chroma run --host localhost --port 8000 --path ./chroma_data
from __future__ import annotations

import chromadb

# Chrome Server DB Variables
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
COLLECTION = CHROMA_CLIENT.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME)

COLLECTION.add(
    documents=[
        'This is a document about pineapple',
        'This is a document about oranges'
    ],
    ids=['id1', 'id2']
)

results = COLLECTION.query(
    # Chroma will embed this for you
    query_texts=['This is a query document about hawaii'],
    n_results=2     # how many results to return
)

print(results)
