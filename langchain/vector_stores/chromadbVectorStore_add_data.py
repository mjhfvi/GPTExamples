# run local chromadb
# chroma run --host localhost --port 8000 --path ./chroma_data
from __future__ import annotations

import chromadb

CHROMA_COLLECTION_NAME = 'mjhfvi'

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name=CHROMA_COLLECTION_NAME)
collection.add(
    documents=[
        'This is a document about pineapple',
        'This is a document about oranges'
    ],
    ids=['id1', 'id2']
)
results = collection.query(
    # Chroma will embed this for you
    query_texts=['This is a query document about hawaii'],
    n_results=2     # how many results to return
)
print(results)
