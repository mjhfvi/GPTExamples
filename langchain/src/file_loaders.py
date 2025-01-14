from __future__ import annotations

import os
import sys
from datetime import datetime

from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import PythonLoader
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain_unstructured import UnstructuredLoader


class FileLoaders:
    """A flexible loader for various file types in a directory."""
    # print('[DEBUG][loaders]Starting Load Documents Process ...')

    def __init__(self, path, loader_cls, glob_pattern, debug=True):
        self.path = path
        self.loader_cls = loader_cls
        self.glob_pattern = glob_pattern
        self.debug = debug

    def load_files(self) -> list:
        """
        Generalized method to load files based on type.

        Args:
            file_type (str): Type of files to load (e.g., 'Python', 'Text').
            loader_cls (object): Loader class to use.
            glob_pattern (str): Glob pattern to match files.
            loader_kwargs (dict, optional): Additional arguments for the loader class. Defaults to None.
            show_progress (bool): Whether to show progress while loading. Defaults to True.
            use_multithreading (bool): Whether to use multithreading for the loader. Defaults to False.

        Returns:
            list: Loaded documents or None in case of an error.
        """
        start_time = datetime.now()
        try:
            folder_check(self.path)
            if self.loader_cls.lower() == 'txt':
                # print("Loading Text Files ...")
                if 'txt' not in self.glob_pattern:
                    documents = txt_directory_loader(
                        path=self.path, glob_pattern='**/**', show_progress=False, use_multithreading=False)
                if 'txt' in self.glob_pattern:
                    # print("[DEBUG][loaders]Found 'txt' in glob_pattern, Loading Text Files ...")
                    glob_pattern = '**/*.txt'
                    documents = txt_directory_loader(
                        path=self.path, glob_pattern=glob_pattern, show_progress=False, use_multithreading=False)
            if self.loader_cls.lower() == 'json':
                print('Loading JSON Files ...')
                if self.glob_pattern is None:    # if glob_pattern is not provided, remove the 'glob_pattern' parameter and use a full path to file
                    documents = json_file_loader(
                        path=self.path, show_progress=False, use_multithreading=False)
                if 'json' in self.glob_pattern:   # if glob_pattern provided, use search files in the directory
                    glob_pattern = '**/*.json'
                    documents = json_file_loader(
                        path=self.path, show_progress=False, use_multithreading=False)
            if self.loader_cls.lower() == 'md':
                if glob_pattern is None:
                    documents = md_loader(
                        path=self.path, loader_kwargs=None, show_progress=True, use_multithreading=False)
                if glob_pattern.contains('md'):
                    glob_pattern = '**/*.md'
                    documents = md_loader(
                        path=self.path, glob_pattern=glob_pattern, show_progress=True, use_multithreading=False)
            if self.loader_cls.lower() == 'csv':
                if glob_pattern is None:
                    documents = csv_loader(
                        path=self.path, loader_kwargs=None, show_progress=True, use_multithreading=False)
                if glob_pattern.contains('csv'):
                    glob_pattern = '**/*.csv'
                    documents = csv_loader(path=self.path, glob_pattern=glob_pattern,
                                           loader_kwargs=None, show_progress=True, use_multithreading=False)
            if self.loader_cls.lower() == 'url' or 'web' or 'webpage':
                if glob_pattern is None:
                    url_loader(file_type, loader_kwargs=None,
                               show_progress=True, use_multithreading=False)
                if glob_pattern is None or '':
                    glob_pattern = 'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023'
                    url_loader(glob_pattern=glob_pattern, loader_kwargs=None,
                               show_progress=True, use_multithreading=False)
            if self.loader_cls.lower() == 'youtube' or 'video':
                if glob_pattern is None:
                    url_youtube_loader(
                        loader_kwargs=None, show_progress=True, use_multithreading=False)
                if glob_pattern is None or '':
                    glob_pattern = 'https://www.youtube.com/watch?v=9bZkp7q19f0'
                    url_youtube_loader(glob_pattern=glob_pattern, loader_kwargs=None,
                                       show_progress=True, use_multithreading=False)
            # print("Preview 'documents': ", documents[:1], '...')
            if self.debug is True:
                print("[DEBUG]review value 'documents': ",
                      documents[0].page_content[:50], '...')
            return documents
        except Exception as error:
            print(
                f"Something went wrong when loading {self.loader_cls} documents: ", error, '\nError in Definition: ', __name__)
        finally:
            end_time = datetime.now()
            print(
                f"Successfully Loading {self.loader_cls} Files: Duration: {end_time - start_time}\n")


def folder_check(path):
    folder_check = os.path.exists(path)
    # if folder_check is True:
    # print(f"Folder '{path}' Exists, Continue ...")
    if not folder_check:
        print(f"Folder '{path}' Does Not Exist, Exiting ...")
        exit(1)
    return None


def txt_directory_loader(path, glob_pattern, show_progress=False, use_multithreading=False) -> DirectoryLoader:
    """Directory Loader for text files\nOnly use 'path' value to set the folder path and search all md files"""
    # start_time = datetime.now()
    try:
        # text_loader_kwargs = {'autodetect_encoding': True}
        loader = DirectoryLoader(
            path,
            glob=glob_pattern,
            loader_cls=TextLoader,
            show_progress=show_progress,
            use_multithreading=use_multithreading,
            loader_kwargs={'autodetect_encoding': True}
        )

        documents = loader.load()
        if len(documents) == 0:
            print('No Documents Found. Exiting ...')
            exit(1)
        else:
            print('documents loaded from disk: ', len(documents))
        # print("[DEBUG][loaders]", path, glob_pattern)
        # print("[DEBUG][loaders]Documents Loaded: ", documents)
        # print("[DEBUG][loaders]Documents Loaded: ", documents[0].page_content)
        # print("[DEBUG][loaders]Documents Loaded: ", documents[0].page_content[:30], "...")
        # document_text = documents
        return documents
    except Exception as error:
        print('Something Went Wrong When Loading Documents: ',
              error, '\nError in Definition: ', __name__)
        exit(1)
    # finally:
    #     end_time = datetime.now()
    #     print("\nFinished loading text files: ", 'Duration: {}'.format(end_time - start_time))


def json_file_loader(path) -> JSONLoader:
    """Define the metadata extraction function in the JSON file."""
    start_time = datetime.now()
    try:
        def metadata_func(record: dict, metadata: dict) -> dict:
            metadata['sender_name'] = record.get('sender_name')
            metadata['timestamp_ms'] = record.get('timestamp_ms')
            return metadata

        loader = JSONLoader(
            path=path,
            jq_schema='.messages[]',
            content_key='content',
            metadata_func=metadata_func,
        )

        documents = loader.load()
        print(documents[0].metadata)
        # print(documents)
        return documents
    except Exception as error:
        print('Something went wrong when loading documents: ',
              error, '\nError in Definition: ', __name__)
    finally:
        end_time = datetime.now()
        print('\nFinished loading json files: ',
              'Duration: {}'.format(end_time - start_time))


def md_loader(file_path: int = 'datasets/') -> None:
    """Directory Loader for markdown files\nOnly use 'file_path' value to set the folder path and search all md files"""
    start_time = datetime.now()
    try:
        text_loader_kwargs = {'autodetect_encoding': True}
        loader = DirectoryLoader(
            file_path,
            glob='**/*.md',
            loader_cls=UnstructuredFileLoader,
            show_progress=True,
            use_multithreading=True,
            loader_kwargs=text_loader_kwargs
        )

        documents = loader.load()
        len(documents)
        print(documents[0].page_content[:100])
        return documents
    except Exception as error:
        print('Something went wrong when loading documents: ',
              error, '\nError in Definition: ', __name__)
    finally:
        end_time = datetime.now()
        print('\nFinished loading markdown files: ',
              'Duration: {}'.format(end_time - start_time))


def pdf_loader(file_path: int = 'datasets/') -> None:
    """Directory Loader for pdf files\nuse 'file_path' value to set the folder path and file name"""
    start_time = datetime.now()
    try:
        file_paths = [file_path]

        loader = UnstructuredLoader(file_paths)
        documents = loader.load()
        documents[0]
        print(documents[0].metadata)
        return documents
    except Exception as error:
        print('Something went wrong when loading documents: ',
              error, '\nError in Definition: ', __name__)
    finally:
        end_time = datetime.now()
        print('\nFinished loading pdf files: ',
              'Duration: {}'.format(end_time - start_time))


def python_loader(file_path: int = 'datasets/') -> None:
    """Directory Loader for python files\nOnly use 'file_path' value to set the folder path and search all md files"""
    start_time = datetime.now()
    try:
        loader = DirectoryLoader(
            file_path,
            glob='**/*.py',
            loader_cls=PythonLoader,
            show_progress=True
        )

        documents = loader.load()
        # print(len(documents))

        print(f"{len(documents)} Documents Loaded.")
        # print('Creating vectorstore.')
        return documents
    except Exception as error:
        print('Something went wrong when Loading Documents: ',
              error, '\nError in Definition: ', __name__)
    finally:
        end_time = datetime.now()
        print('\nFinished Loading Python Files: ',
              'Duration: {}'.format(end_time - start_time))


def csv_loader(file_path: int = 'datasets/') -> None:
    """Directory Loader for csv files\nOnly use 'file_path' value to set the folder path and search all md files"""
    start_time = datetime.now()
    try:
        text_loader_kwargs = {'autodetect_encoding': True}

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
        print(documents)
        return documents
    except Exception as error:
        print('Something went wrong when loading documents: ',
              error, '\nError in Definition: ', __name__)
    finally:
        end_time = datetime.now()
        print('\nFinished loading csv files: ',
              'Duration: {}'.format(end_time - start_time))


def url_loader(url) -> None:
    start_time = datetime.now()
    try:
        urls = [url]
        # 'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023',

        loader = UnstructuredURLLoader(urls=urls)
        DATA = loader.load()
        print(DATA)
        DATA[0]
        return DATA
    except Exception as error:
        print('Something went wrong when loading documents: ',
              error, '\nError in Definition: ', __name__)
    finally:
        end_time = datetime.now()
        print('\nFinished loading url: ',
              'Duration: {}'.format(end_time - start_time))


def url_youtube_loader(url) -> None:
    start_time = datetime.now()
    try:
        urls = [url]
        # 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        # "https://goo.gl/maps/NDSHwePEyaHMFGwh8",
        # ]

        loader = SeleniumURLLoader(urls=urls)
        DATA = loader.load()
        DATA[0]

        print(DATA[0])
        return DATA
    except Exception as error:
        print('Something went wrong when loading documents: ',
              error, '\nError in Definition: ', __name__)
    finally:
        end_time = datetime.now()
        print('\nFinished loading youtube url: ',
              'Duration: {}'.format(end_time - start_time))


if __name__ == '__main__':
    print('this is not the main script, exiting ...')
    sys.exit()
