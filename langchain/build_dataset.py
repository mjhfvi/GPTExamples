from __future__ import annotations

import os
import sys

from loguru import logger
from prettyformatter import pprint
from rich import inspect
from rich import print_json
from src import documents_embedding
from src import documents_loader
from src import llm_tools
from src.config_tools import Error_Handler
from src.llm_prompt_template import llm_prompt_validation
from src.llm_prompt_template import prompt_json_invoice
# from src.local_tools import ollama_llm_config

# from langchain_community.document_loaders import PyPDFLoader
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from langchain_core.output_parsers import StrOutputParser
# from langchain.globals import set_llm_cache
# from langchain_community.cache import InMemoryCache

file_path = os.environ['DATASET_DIRECTORY'] + os.environ['DATASET_FILE']
# print(file_path)


@logger.catch
def main():
    logger.info('running main function.')
    load_documents_string = documents_loader.DocumentsLoaders()
    load_documents_string.build_dataset()


@Error_Handler
def build_invoice_bezeqint():
    logger.info('running build_invoice_bezeqint function.')
    load_documents_string = documents_loader.DocumentsLoaders(
        path=os.environ['DATASET_DIRECTORY'])
    dataset_document = load_documents_string.build_dataset(use_llm=True)
    # pprint(dataset_document, '\n\n')

    # set_llm_cache(InMemoryCache())

    # llm_prompt = PromptTemplate(
    #     # input_variables=[dataset_document],
    #     template=prompt_json_invoice
    # )

    # llm_chain = llm_prompt | ollama_llm_config(temperature=0.1) | StrOutputParser()
    # llm_response = llm_chain.invoke({"input_text": dataset_document})
    # pprint(llm_response)

    # load_documents_string.save_file_to_disk(folder_path='datasets/Bezeqint/raw/', file_name='Invoice_200141400.json', file_data=llm_response)

    # llm_validation = PromptTemplate(
    #     template=llm_prompt_validation
    # )
    # chain_validation = llm_validation | ollama_llm_config() | StrOutputParser()
    # response = chain_validation.invoke({"input_text": llm_response})
    # print('\n\nrunning llm validation: \n' + response)

    # return llm_response


# def embedding_documents_bezeqint():
#     load_documents_string = documents_loader.DocumentsLoaders(path='datasets/Bezeqint/raw/llm_datasets/')
#     print(load_documents_string)
    # embedding_documents = documents_embedding.DocumentsEmbeddings()
    # embedding_documents.embeddings_text()


if __name__ == '__main__':
    # main()
    build_invoice_bezeqint()
    # embedding_documents_bezeqint()
