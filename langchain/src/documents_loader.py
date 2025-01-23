from __future__ import annotations

import glob
import json
import os
import pathlib
import re
import sys
from pathlib import Path
from unicodedata import normalize

import markdown
from deep_translator import GoogleTranslator
from jsonschema import validate
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PythonLoader
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_core.documents import Document
from langchain_unstructured import UnstructuredLoader
from loguru import logger
from prettyformatter import pprint
from pypdf import PdfReader
from rich import inspect
from rich import print_json
# from pydantic import BaseModel


class DocumentsLoaders():
    def __init__(self, path):
        self.path = path
        # self.loader_cls = loader_cls
        # self.glob_pattern = glob_pattern

    def build_dataset(self) -> list:
        try:
            self.folder_check(self.path)
            logger.debug('loading all files in path: ' + str(self.path))

            files_found_list = glob.glob(pathname=os.path.join(
                self.path, '*.*'), include_hidden=False)
            logger.debug('found files in path: ' + str(len(files_found_list)))
            logger.debug(files_found_list)

            for file in files_found_list:
                if file.endswith('.txt'):
                    logger.debug('Working on file: ' + str(file))
                    file_data = self.txt_loader(file)
                    # documents_list.append(file_data)
                if file.endswith('.json'):
                    logger.debug('Working on file: ' + str(file))
                    file_data = self.json_loader(file)
                    rebuild_file = self.change_to_single_quotes(file_data)

                    file_name = Path(file).stem
                    # print(file_name)
                    folder_path = os.path.dirname(os.path.abspath(file))
                    dataset_folder = folder_path + '/datasets'
                    logger.debug(
                        'creating a dataset folder to save files in: ' + str(dataset_folder))
                    self.folder_check(dataset_folder, build_new_folder=True)

                    self.save_file_to_disk(dataset_folder, str(
                        '/dataset_' + file_name + '.json'), str(rebuild_file))
                if file.endswith('.py'):
                    logger.debug('Working on file: ' + str(file))
                    file_data = self.python_loader(file)
                    # documents_list.append(file_data)
                if file.endswith('.md'):
                    logger.debug('Working on file: ' + str(file))
                    file_data = self.md_loader(file)

                    file_name = Path(file).stem
                    folder_path = os.path.dirname(os.path.abspath(file))
                    dataset_folder = folder_path + '/datasets'
                    logger.debug(
                        'creating a dataset folder to save files in: ' + str(dataset_folder))
                    self.folder_check(dataset_folder, build_new_folder=True)

                    self.save_file_to_disk(dataset_folder, str(
                        '/dataset_' + file_name + '.json'), str(file_data))
                    # documents_list.append(file_data)
                if file.endswith('.csv'):
                    logger.debug('Working on file: ' + str(file))
                    file_data = self.csv_loader(file)
                    # documents_list.append(file_data)
                if file.endswith('.pdf'):
                    logger.debug('Working on file: ' + str(file))
                    documents_data = []

                    file_name = Path(file).stem
                    folder_path = os.path.dirname(os.path.abspath(file))
                    dataset_folder = folder_path + '/datasets'
                    logger.debug(
                        'creating a dataset folder to save files in: ' + str(dataset_folder))
                    self.folder_check(dataset_folder, build_new_folder=True)

                    page_data = self.extract_data_from_pdf(file)

                    for pages in page_data:
                        documents_data.append(pages)
                    list_of_data = ' '.join([str(data)
                                            for data in documents_data])
                    format_file = self.reformat_text(list_of_data)

                    find_date = self.find_dates(format_file)
                    if 'bezeqint' in format_file:
                        logger.debug("service found: 'bezeqint'")
                        found_service = 'bezeqint'
                    else:
                        logger.debug('service not found')
                        found_service = 'unknown'

                    formatted_file = str(format_file)

                    document_data = Document(
                        page_content=formatted_file,
                        metadata={
                            'source': file, 'date': find_date[0], 'type': 'pdf', 'service': found_service}
                    )
                    logger.debug(document_data)

                    self.save_file_to_disk(dataset_folder, str(
                        '/dataset_' + file_name + '.json'), str(document_data))

        except Exception:
            logger.exception(
                'An error occurred while running the program, please check the logs for more information. ')
            sys.exit(1)
        except KeyboardInterrupt:
            logger.error('program terminated by user.')

    def load_json_files(self):
        logger.debug('loading json file from folder: ' + self.path)
        files_found_list = glob.glob(pathname=os.path.join(
            self.path, '*.*'), include_hidden=False)
        logger.debug('found files in path: ' + str(len(files_found_list)))
        # json_file_list = []
        for file in files_found_list:
            if file.endswith('.json'):
                logger.debug('Working on file: ' + str(file))
                # json_file_list.append(file)
                file_data = self.json_loader(file)
                logger.debug(file_data)

        return file_data

    def txt_loader(self, path):
        try:
            # text_loader_kwargs = {'autodetect_encoding': True}
            loader = TextLoader(
                file_path=path,
                # glob=glob_pattern,
                # loader_cls=TextLoader,
                # show_progress=show_progress,
                # use_multithreading=use_multithreading,
                # loader_kwargs={'autodetect_encoding': True}
            )

            documents = loader.load()
            if len(documents) == 0:
                logger.warning('no txt documents found.')
                # exit(1)
            else:
                logger.debug('documents loaded from disk: ', len(documents))
            return documents

        except Exception:
            logger.exception(
                'An error occurred while running the program, please check the logs for more information. ')
            sys.exit(1)
        except KeyboardInterrupt:
            logger.error('program terminated by user.')

    def json_loader(self, path):
        def metadata_func(record: dict, metadata: dict) -> dict:
            metadata['question'] = record.get('question')
            metadata['answer'] = record.get('answer')
            return metadata

        loader = JSONLoader(
            file_path=path,
            jq_schema='.',
            # content_key='content',
            # metadata_func=metadata_func,
            text_content=False,
            # is_content_key_jq_parsable=False,
        )

        documents = loader.load()
        # logger.debug("document preview: " + str(documents))
        # logger.debug(documents[0].metadata)
        return documents

    def md_loader(self, path):
        try:
            logger.debug('md loader: ' + path)
            # text_loader_kwargs = {'autodetect_encoding': True}
            loader = UnstructuredMarkdownLoader(
                file_path=path,
                mode='single',
                # glob='**/[!.]*',
                # loader_cls=UnstructuredFileLoader,
                # show_progress=True,
                # use_multithreading=True,
                # loader_kwargs=text_loader_kwargs
            )

            documents = loader.load()
            len(documents)
            logger.debug(documents[0].page_content[:100])
            return documents

        except Exception:
            logger.exception(
                'An error occurred while running the program, please check the logs for more information. ')
            sys.exit(1)
        except KeyboardInterrupt:
            logger.error('program terminated by user.')

    def python_loader(self, file_path):
        """Directory Loader for python files\nOnly use 'file_path' value to set the folder path and search all md files"""
        try:
            loader = DirectoryLoader(
                file_path,
                glob='**/*.py',
                loader_cls=PythonLoader,
                show_progress=True
            )

            documents = loader.load()
            # print(len(documents))

            logger.debug(f"{len(documents)} Documents Loaded.")
            # print('Creating vectorstore.')
            return documents

        except Exception:
            logger.exception(
                'An error occurred while running the program, please check the logs for more information. ')
            sys.exit(1)
        except KeyboardInterrupt:
            logger.error('program terminated by user.')

    def csv_loader(self, file_path):
        """Directory Loader for csv files\nOnly use 'file_path' value to set the folder path and search all md files"""
        try:
            # text_loader_kwargs = {'autodetect_encoding': True}

            loader = CSVLoader(
                file_path=file_path,
                encoding='utf8'
                # csv_args={
                #     'delimiter': ',',
                #     'quotechar': '"',
                #     'fieldnames': ['Index', 'Height', 'Weight']
                # }
            )

            documents = loader.load()
            logger.debug(documents)
            return documents

        except Exception:
            logger.exception(
                'An error occurred while running the program, please check the logs for more information. ')
            sys.exit(1)
        except KeyboardInterrupt:
            logger.error('program terminated by user.')

    def folder_check(self, path, build_new_folder=False):
        # logger.debug('checking if folder exists ')
        folder_check = os.path.exists(path)
        if build_new_folder is True:
            if not os.path.exists(path):
                os.makedirs(path)
                logger.debug(f"folder '{path}' created.")
                return
        if folder_check is True:
            logger.debug(f"folder '{path}' exists.")
        if not folder_check:
            logger.warning(
                f"folder '{path}' Does Not Exist, please provide a valid path.")
            exit(1)

    def save_file_to_disk(self, folder_path, file_path, file_data):
        file = open(folder_path + file_path, 'w')
        file.write(file_data)
        file.close()

    def extract_data_from_pdf(self, file):
        logger.debug('extracting data from pdf')
        reader = PdfReader(file)
        # print(str(reader.metadata))
        logger.debug('number of pages in pdf file: ' + str(len(reader.pages)))
        page = reader.pages
        pages_data = []
        for page in reader.pages:
            page_data = page.extract_text()
            check_data = self.contains_hebrew(page_data)
            if check_data is True:
                translated_text = self.translated_to_english(page_data)
                pages_data.append(translated_text)
            if check_data is False:
                pages_data.append(page_data)
        logger.debug(pages_data)
        return pages_data

    def contains_hebrew(self, file):
        hebrew_range = range(0x0590, 0x05FF + 1)
        return any(ord(char) in hebrew_range for char in file)

    def translated_to_english(self, document):
        try:
            logger.debug('translating pages to english')
            translated_document = []
            if not self.contains_hebrew(document):
                translated_document.append(document)
            if self.contains_hebrew(document):
                logger.debug(
                    'found hebrew characters in file, translating to english')
                # fixed_text = document[::-1]
                # fixed_text = normalize('NFKD', fixed_text)
                translated_document.append(GoogleTranslator(
                    source='hebrew', target='english').translate(document))
            logger.debug(translated_document)
            return translated_document

        except Exception:
            logger.exception(
                'An error occurred while running the program, please check the logs for more information. ')
            sys.exit(1)
        except KeyboardInterrupt:
            logger.error('program terminated by user.')

    def reformat_text(self, document):
        cleaned = document.replace('[', '').replace(
            ']', '').replace("\"", '').replace("'", '')
        # fixed02 = self.change_to_single_quotes(fixed01)
        # cleaned = fixed02.replace("[", "").replace("]", "").replace("'", "").replace("\\n", "\n")
        return cleaned

    def change_to_single_quotes(self, file_data):
        logger.debug('changing all double_quotes to single_quotes')
        return str(file_data).replace('"', "'")

    def find_dates(self, file_data):
        logger.debug('finding dates in file')
        return re.findall(r'\d{2}/\d{4}', file_data)

    # def validate_json(self, file_path):
    #     schema = {
    #         "type": "object",
    #         "properties": {
    #             "name": {"type": "string"},
    #             "age": {"type": "integer"},
    #             "email": {"type": "string", "format": "email"},
    #             "address": {"type": "string"}
    #         },
    #         "required": ["name", "age"]
    #     }

    #     validate_json = validate(instance=file_path, schema=schema)
    #     print(validate_json)

    # def pdf_loader(self, file_path):
    #     try:
    #         loader = PyPDFLoader(file_path=file_path)
    #         loader = UnstructuredLoader(file_path)
    #         documents = loader.load()
    #         logger.debug('Documents parts Loaded: ' + str(len(documents)))
    #         # logger.debug('Documents metadata:' + str(documents[0].metadata))
    #         return documents

    #     except Exception:
    #         logger.exception(
    #             'An error occurred while running the program, please check the logs for more information. ')
    #         sys.exit(1)
    #     except KeyboardInterrupt:
    #         logger.error('program terminated by user.')


if __name__ == '__main__':
    logger.error('this is not the main script, exiting ...')
    sys.exit()
