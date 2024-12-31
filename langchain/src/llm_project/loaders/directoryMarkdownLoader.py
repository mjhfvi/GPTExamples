# Source: https://python.langchain.com/docs/how_to/document_loader_directory/
from __future__ import annotations

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredFileLoader

text_loader_kwargs = {'autodetect_encoding': True}

# Directory Loader for markdown files
loader = DirectoryLoader(
    '../datasets/',
    glob='**/*.md',
    loader_cls=UnstructuredFileLoader,
    show_progress=True,
    use_multithreading=True,
    loader_kwargs=text_loader_kwargs
)

docs = loader.load()
len(docs)

print(docs[0].page_content[:100])
