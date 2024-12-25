# Source: https://python.langchain.com/docs/integrations/document_loaders/unstructured_file/
from __future__ import annotations

from langchain_unstructured import UnstructuredLoader
# from unstructured.cleaners.core import clean_extra_whitespace

file_paths = [
    '../datasets/dataset.pdf',
]


loader = UnstructuredLoader(file_paths)
docs = loader.load()
docs[0]
print(docs[0].metadata)


# loader = UnstructuredLoader(
#     "../data/dataset.pdf",
#     post_processors=[clean_extra_whitespace],
# )

# docs = loader.load()
# docs[5:10]
