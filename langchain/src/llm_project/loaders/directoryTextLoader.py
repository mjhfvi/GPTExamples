# Source: https://python.langchain.com/docs/integrations/document_loaders/bshtml/
from __future__ import annotations

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

text_loader_kwargs = {'autodetect_encoding': True}

# Directory Loader for text files
loader = DirectoryLoader(
    '../datasets/',
    glob='**/*.txt',
    loader_cls=TextLoader,
    show_progress=True,
    use_multithreading=True,
    loader_kwargs=text_loader_kwargs
)


docs = loader.load()
len(docs)

print(docs[0].page_content[:100])
