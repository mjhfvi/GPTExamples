from __future__ import annotations

from datetime import datetime

from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import PythonLoader
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import UnstructuredURLLoader


class FileLoader:
    """A flexible loader for various file types in a directory."""

    def __init__(self, file_path):
        self.file_path = file_path

    def load_files(self, file_type, loader_cls, glob_pattern, loader_kwargs=None, show_progress=True, use_multithreading=False):
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
            loader_kwargs = loader_kwargs or {}
            loader = DirectoryLoader(
                self.file_path,
                glob=glob_pattern,
                loader_cls=loader_cls,
                show_progress=show_progress,
                use_multithreading=use_multithreading,
                loader_kwargs=loader_kwargs
            )

            documents = loader.load()
            print(f"{len(documents)} {file_type} Documents Loaded.")

            if file_type.lower() == 'text' and documents:
                # Preview the content for text files.
                print(documents[0].page_content[:100])

            return documents
        except Exception as error:
            print(
                f"Something went wrong when loading {file_type} documents: ", error, '\nError in Definition: ', __name__)
        finally:
            end_time = datetime.now()
            print(
                f"\nFinished loading {file_type} files: Duration: {end_time - start_time}")


##########################
# Initialize the loader
file_loader = FileLoader('/path/to/your/directory')

# Load Python files
python_documents = file_loader.load_files(
    file_type='Python',
    loader_cls=PythonLoader,
    glob_pattern='**/*.py'
)

# Load Text files
text_documents = file_loader.load_files(
    file_type='Text',
    loader_cls=TextLoader,
    glob_pattern='**/*.txt',
    loader_kwargs={'autodetect_encoding': True},
    use_multithreading=True
)
