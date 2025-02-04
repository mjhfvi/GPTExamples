from __future__ import annotations

import os
import sys

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from loguru import logger

from langchain.embeddings import CacheBackedEmbeddings

# store = LocalFileStore("./cache/")


class DocumentsEmbeddings:
    def __init__(self, model_name='llama3.2:3b'):
        self.model_name = model_name

    def model_embeddings(self) -> None:
        embeddings_string = OllamaEmbeddings(
            model=self.model_name,
            base_url='http://localhost:11434'
        )

        # embeddings_string = HuggingFaceEmbeddings(
        #     model_name='sentence-transformers/all-mpnet-base-v2',
        #     model_kwargs={'device': 'cpu'},
        #     encode_kwargs={'normalize_embeddings': False},
        # )

        # if model_name not in ['sentence-transformers/all-mpnet-base-v2', 'all-MiniLM-L6-v2']:
        #   raise Exception("Embeddings model not supported")
        # if model_name in 'sentence-transformers/all-mpnet-base-v2':
        #     logger.debug('using default embeddings model: sentence-transformers/all-mpnet-base-v2')
        #     embeddings_model = embeddings_default(model_name=model_name)
        # if model_name not in ['sentence-transformers/all-mpnet-base-v2']:
        #     print(
        #         "not using default embeddings model 'all-mpnet-base-v2', new embeddings model is: ", model_name)
        #     if model_name == 'all-MiniLM-L6-v2':
        #         print('using default embeddings model: all-MiniLM-L6-v2')
        #         embeddings_model = embeddings_default(model_name=model_name)
        #     if model_name == 'llama3':
        #         embeddings_model = OllamaEmbeddings(model="llama3")

        return embeddings_string

    # def embeddings_documents(self):
        # load_documents_string = documents_loader.DocumentsLoaders(path=datasets_path)
        # files_list = load_documents_string.load_json_files()

        # embeddings_documents = embedding_string.embed_query(str(document_data))
        # print(str(embeddings_documents)[:100])  # Show the first 100 characters of the vector

        # print(embeddings_documents)
        # return embeddings_documents

    # def embeddings_text(embeddings_model, embeddings_data, folder_path='data', write_to_disk=False) -> list:
    #         embeddings_config = embeddings.embed_query(embeddings_data)
    #         # for index, embed in enumerate(embeddings_data):

    #         #     # embeddings_config = embeddings_model.embed_documents(embed)
    #         #     if not os.path.exists(folder_path):
    #         #         logger.debug(f"folder {folder_path} was not found, building new folder")
    #         #         os.makedirs(folder_path)

    #         #     if write_to_disk is True:
    #         # logger.debug('print embeddings text to disk')
    #         # with open('data/embeddings.txt', 'w') as output:
    #         #     logger.debug("review value of 'embed': ", embeddings_config[:5], '...')
    #         #     output.write(str(embeddings_config))
    #         #     logger.debug('successfully print embeddings text to disk')

    #         return embeddings_config

    def embeddings_text_single_file(embeddings_string, data_to_embeddings, folder_path='data'):
        logger.debug(data_to_embeddings)
        embeddings_data_output = embeddings_string.embed_documents(
            data_to_embeddings)
        if not os.path.exists(folder_path):
            logger.debug(
                f"folder {folder_path} did not found, building new folder")
            os.makedirs(folder_path)

        with open('data/embeddings.txt', 'w') as output:
            logger.debug("review values of 'embeddings_config': ")
            logger.debug(embeddings_data_output[0][:7])
            logger.debug(len(embeddings_data_output),
                         'Number of Embeddings Items.')
            output.write(str(embeddings_data_output))
        return embeddings_data_output[0]

    def embedded_query(embeddings, query, embeddings_model):
        embedded_query = embeddings_model.embed_query(query)
        logger.debug("Preview 'embedded_query': ", embedded_query[:5])
        # print("embeddings model: ", embeddings.model_name)
        return embedded_query


if __name__ == '__main__':
    logger.error('this is not the main script, exiting ...')
    sys.exit()
