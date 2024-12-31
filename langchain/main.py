'''this is the main file of the langchain project'''
from __future__ import annotations

from langchain_community.vectorstores import Chroma
from src.llm_project import embeddings
from src.llm_project import loaders
from src.llm_project import splitters
from src.llm_project import vector_store

DATASET_DIRECTORY = 'datasets'
DATASET_FILE = 'dataset'
CHROMA_HOST = '172.22.54.208'
CHROMA_PORT = 8000
CHROMA_COLLECTION_NAME = 'mjhfvi'


if __name__ == '__main__':
    LOADER_CONFIG = loaders.FileLoaders(
        path=DATASET_DIRECTORY, loader_cls='txt', glob_pattern='txt')
    TEXT_DOCUMENTS = LOADER_CONFIG.load_files()
    splitters.splitting_documents(LOADER=TEXT_DOCUMENTS)
    EMBEDDINGS = embeddings.embeddings_string()
    VECTORSTORE = vector_store.connect_local_chromadb(
        CHROMA_COLLECTION_NAME=CHROMA_COLLECTION_NAME, EMBEDDINGS=EMBEDDINGS)

    # CHROMA_CLIENT = vector_store.connect_chromadb(CHROMA_HOST)
    # vectorstore.add_chromadb(CHROMA_CLIENT, CHROMA_COLLECTION_NAME=CHROMA_COLLECTION_NAME, DATA=LOAD_DATA)
    # vectorstore.query_chromadb(CHROMA_CLIENT, CHROMA_COLLECTION_NAME=CHROMA_COLLECTION_NAME, DATA=LOAD_DATA)

    # print("Starting Conversation with LLM ...")
    # question = "What are the approaches to Task Decomposition?"
    # docs = VECTORSTORE.similarity_search(question)
    # len(docs)

    # retrievers.Wikipedia_retriever('TOKYO GHOUL')
    # retrievers.hacker_news_retriever('https://news.ycombinator.com/item?id=34817881')
    # loaders.url_youtube_loader("https://www.youtube.com/watch?v=9bZkp7q19f0")
    # loaders.url_loader("https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023")
    # loaders.json_loader(path=DATASET_DIRECTORY + "/" + DATASET_FILE + ".json")
    # loaders.pdf_loader(path=DATASET_DIRECTORY + "/" + DATASET_FILE + ".pdf")
    # loaders.csv_loader(path=DATASET_DIRECTORY + "/" + DATASET_FILE + ".csv")
    # loaders.txt_loader(path=DATASET_DIRECTORY + "/")
    # loaders.md_loader(path=DATASET_DIRECTORY + "/")
    # print("\n" + 5*"#" + " Done ... " + 5*"#")
