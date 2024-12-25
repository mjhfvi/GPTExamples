# Source: https://python.langchain.com/docs/integrations/document_loaders/bshtml/
from __future__ import annotations

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
