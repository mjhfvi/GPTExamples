# Source: https://python.langchain.com/docs/integrations/vectorstores/chroma/
from __future__ import annotations

import chromadb
from chromadb.config import Settings

# Server DB
CHROMA_HOST = '172.22.54.208'
CHROMA_PORT = 8000
CHROMA_COLLECTION_NAME = 'mjhfvi'

# Get Collections by Name
chroma_client = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT,
    ssl=False
)
# collections = chroma_client.get_collection(
#     name=CHROMA_COLLECTION_NAME
#     )
# print(collections)

# Get or Create Collections by Name
collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME
)

collection.add(
    embeddings=students_embeddings,
    documents=[student_info, club_info, university_info],
    metadatas=[{'source': 'student info'}, {
        'source': 'club info'}, {'source': 'university info'}],
    ids=['id1', 'id2', 'id3']
)
