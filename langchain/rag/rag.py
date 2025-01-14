'''this is the main file of the langchain project'''
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from GPTExamples.langchain.src.llm_project import documents_embedding
from GPTExamples.langchain.src.llm_project import file_loaders
from GPTExamples.langchain.src.llm_project import text_splitters
from src.llm_project import llm_model
from src.llm_project import vector_store

load_dotenv(dotenv_path='.env')
DATASET_DIRECTORY = os.getenv('DATASET_DIRECTORY')
DATASET_FILE = os.getenv('DATASET_FILE')
CHROMA_HOST = os.getenv('CHROMA_HOST')
CHROMA_PORT = os.getenv('CHROMA_PORT')
CHROMA_DB_PATH = os.getenv('CHROMA_PATH')
CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME')


student_info = """
Alexandra Thompson, a 19-year-old computer science sophomore with a 3.7 GPA,
is a member of the programming and chess clubs who enjoys pizza, swimming, and hiking
in her free time in hopes of working at a tech company after graduating from the University of Washington.
"""

club_info = """
The university chess club provides an outlet for students to come together and enjoy playing
the classic strategy game of chess. Members of all skill levels are welcome, from beginners learning
the rules to experienced tournament players. The club typically meets a few times per week to play casual games,
participate in tournaments, analyze famous chess matches, and improve members' skills.
"""

university_info = """
The University of Washington, founded in 1861 in Seattle, is a public research university
with over 45,000 students across three campuses in Seattle, Tacoma, and Bothell.
As the flagship institution of the six public universities in Washington state,
UW encompasses over 500 buildings and 20 million square feet of space,
including one of the largest library systems in the world.
"""

if __name__ == '__main__':
    loader_config = file_loaders.FileLoaders(
        path=DATASET_DIRECTORY, loader_cls='pdf', glob_pattern='pdf')
    # print("Print some values of 'loader_config': ", loader_config.load_files()[0].page_content[:30], "...")

    # split_config = splitters.splitting_documents(loader=loader_config.load_files())
    # print("Print value of 'split_config': ", split_config)

    # embeddings_string = embeddings.embeddings_string()
    # embedded_documents = embeddings.embeddings_string(model_name="all-MiniLM-L6-v2")
    # embedded_documents = embeddings.embeddings_string(model_name="llama3")

    # embeddings_text = embeddings.embeddings_text(embeddings=split_config, embeddings_model=embeddings_string)
    # print(len(embeddings_text), "Number of Embeddings Items.\n")

    # embedded_query = embeddings.embedded_query(embeddings=embeddings_text, query="What was the name mentioned in the conversation?", embeddings_model=embeddings_string)
    # print("Print some values of 'embedded_query': ", embedded_query[:10], "...\n")

    # vector_store_init_config = vector_store.local_chromadb_Initialize(chroma_collection_name=CHROMA_COLLECTION_NAME, persist_directory=CHROMA_DB_PATH)

    # vector_store.local_chromadb_save_to_collection(documents=embeddings_text, chroma_collection_name=CHROMA_COLLECTION_NAME, chroma_path=DATASET_DIRECTORY)

    # testing = vector_store.local_chromadb_read_collection(vector_store_db._collection_name, vector_store_db._persist_directory)

    # testing = vector_store.local_chromadb_save_to_collection(
    #     documents=[student_info, club_info, university_info],
    #     metadatas=[{"source": "student info"}, {"source": "club info"}, {'source': 'university info'}],
    #     ids=["id1", "id2", "id3"],
    #     chroma_collection_name=CHROMA_COLLECTION_NAME,
    #     )

    # print("Starting Conversation with LLM ...")
    # question = "What are the approaches to Task Decomposition?"
    # docs = VECTORSTORE.similarity_search(question)
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
    exit(0)
