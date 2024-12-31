# from langchain_community.document_loaders import DirectoryLoader, PythonLoader, JSONLoader, TextLoader, CSVLoader, UnstructuredURLLoader, SeleniumURLLoader, UnstructuredFileLoader
# from langchain_unstructured import UnstructuredLoader
from __future__ import annotations

from datetime import datetime

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import TextLoader


class FileLoaders:
    """A flexible loader for various file types in a directory."""

    def __init__(self, path, loader_cls, glob_pattern):
        self.path = path
        self.loader_cls = loader_cls
        self.glob_pattern = glob_pattern

    def load_files(self):
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
            if self.loader_cls.lower() == 'txt':
                if self.glob_pattern is None:
                    DOCUMENTS = txt_directory_loader(
                        path=self.path, glob_pattern='**/**', show_progress=False, use_multithreading=False)
                if 'txt' in self.glob_pattern:
                    glob_pattern = '**/*.txt'
                    DOCUMENTS = txt_directory_loader(
                        path=self.path, glob_pattern=glob_pattern, show_progress=False, use_multithreading=False)
            if self.loader_cls.lower() == 'json':
                if self.glob_pattern is None:    # if glob_pattern is not provided, remove the 'glob_pattern' parameter and use a full path to file
                    DOCUMENTS = json_file_loader(
                        path=self.path, show_progress=False, use_multithreading=False)
                if 'json' in self.glob_pattern:   # if glob_pattern provided, use search files in the directory
                    glob_pattern = '**/*.json'
                    DOCUMENTS = json_file_loader(
                        path=self.path, show_progress=False, use_multithreading=False)
            # if self.loader_cls.lower() == 'md':
            #     if glob_pattern is None:
            #         DOCUMENTS = md_loader(path, self.loader_cls, loader_kwargs=None, show_progress=True, use_multithreading=False)
            #     if glob_pattern.contains("md"):
            #         glob_pattern = '**/*.md'
            #         DOCUMENTS = md_loader(path, loader_cls, glob_pattern, show_progress=True, use_multithreading=False)
            # if loader_cls.lower() == 'csv':
                # if glob_pattern is None:
                #     DOCUMENTS = csv_loader(path, loader_cls, loader_kwargs=None, show_progress=True, use_multithreading=False)
                # if glob_pattern.contains("csv"):
                #     glob_pattern = '**/*.csv'
                #     DOCUMENTS = csv_loader(path, loader_cls, glob_pattern, loader_kwargs=None, show_progress=True, use_multithreading=False)
            return DOCUMENTS
            # if loader_cls.lower() == 'url' or 'web' or 'webpage':
            #     if glob_pattern is None:
            #         url_loader(file_type, loader_cls, loader_kwargs=None, show_progress=True, use_multithreading=False)
            #     if glob_pattern is None or "":
            #         glob_pattern = 'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023'
            #         url_loader(file_type, loader_cls, glob_pattern, loader_kwargs=None, show_progress=True, use_multithreading=False)
            # if loader_cls.lower() == 'youtube' or 'video':
            #     if glob_pattern is None:
            #         url_youtube_loader(file_type, loader_cls, loader_kwargs=None, show_progress=True, use_multithreading=False)
            #     if glob_pattern is None or "":
            #         glob_pattern = 'https://www.youtube.com/watch?v=9bZkp7q19f0'
            #         url_youtube_loader(file_type, loader_cls, glob_pattern, loader_kwargs=None, show_progress=True, use_multithreading=False)
        except Exception as error:
            print(
                f"Something went wrong when loading {self.loader_cls} documents: ", error, '\nError in Definition: ', __name__)
        finally:
            end_time = datetime.now()
            print(
                f"Finished loading {self.loader_cls} files: Duration: {end_time - start_time}\n")


def txt_directory_loader(path, glob_pattern, show_progress=False, use_multithreading=False) -> None:
    """Directory Loader for text files\nOnly use 'path' value to set the folder path and search all md files"""
    # start_time = datetime.now()
    try:
        # text_loader_kwargs = {'autodetect_encoding': True}
        LOADER = DirectoryLoader(
            path,
            glob=glob_pattern,
            loader_cls=TextLoader,
            show_progress=show_progress,
            use_multithreading=use_multithreading,
            loader_kwargs={'autodetect_encoding': True}
        )

        DOCUMENTS = LOADER.load()
        len(DOCUMENTS)
        # print("\nDocument Loader Preview:", DOCUMENTS[0].page_content[:20], ".....\n", end=" ")
        return LOADER
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

        LOADER = JSONLoader(
            path=path,
            jq_schema='.messages[]',
            content_key='content',
            metadata_func=metadata_func,
        )

        DOCUMENTS = LOADER.load()
        print(DOCUMENTS[0].metadata)
        # print(DOCUMENTS)
        return DOCUMENTS
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
        LOADER = DirectoryLoader(
            file_path,
            glob='**/*.md',
            loader_cls=UnstructuredFileLoader,
            show_progress=True,
            use_multithreading=True,
            loader_kwargs=text_loader_kwargs
        )

        DOCUMENTS = LOADER.load()
        len(DOCUMENTS)
        print(DOCUMENTS[0].page_content[:100])
        return DOCUMENTS
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

        LOADER = UnstructuredLoader(file_paths)
        DOCUMENTS = LOADER.load()
        DOCUMENTS[0]
        print(DOCUMENTS[0].metadata)
        return DOCUMENTS
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
        LOADER = DirectoryLoader(
            file_path,
            glob='**/*.py',
            loader_cls=PythonLoader,
            show_progress=True
        )

        DOCUMENTS = LOADER.load()
        # print(len(DOCUMENTS))

        print(f"{len(DOCUMENTS)} Documents Loaded.")
        # print('Creating vectorstore.')
        return DOCUMENTS
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

        LOADER = CSVLoader(
            file_path=file_path,
            encoding='utf8'
            # csv_args={
            #     'delimiter': ',',
            #     'quotechar': '"',
            #     'fieldnames': ['Index', 'Height', 'Weight']
            # }
        )

        DOCUMENTS = LOADER.load()
        print(DOCUMENTS)
        return DOCUMENTS
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

        LOADER = UnstructuredURLLoader(urls=urls)
        DATA = LOADER.load()
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

        LOADER = SeleniumURLLoader(urls=urls)
        DATA = LOADER.load()
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
