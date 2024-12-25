# Source: https://python.langchain.com/docs/integrations/document_loaders/bshtml/
from __future__ import annotations

import chromadb
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PythonLoader
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.text_splitter import Language
from langchain.text_splitter import RecursiveCharacterTextSplitter

LOADER = DirectoryLoader(
    './',
    glob='**/*.py',
    loader_cls=PythonLoader,
    show_progress=True
)

DOCUMENTS = LOADER.load()
# print(len(DOCUMENTS))

print(f"{len(DOCUMENTS)} documents loaded.")
print('Creating vectorstore.')

TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=20,
    length_function=len,
)

DOCUMENTS_TEXT = TEXT_SPLITTER.split_documents(DOCUMENTS)

print(len(DOCUMENTS_TEXT))
print(DOCUMENTS_TEXT[0])

EMBEDDINGS = HuggingFaceEmbeddings(
    model_name='all-MiniLM-L6-v2',
    multi_process=True,
    show_progress=True,
)

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
COLLECTION = CHROMA_CLIENT.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME)

COLLECTION.add(DOCUMENTS_TEXT)

results = COLLECTION.query(
    # Chroma will embed this for you
    query_texts=['This is a query document'],
    n_results=2     # how many results to return
)

print(results)
