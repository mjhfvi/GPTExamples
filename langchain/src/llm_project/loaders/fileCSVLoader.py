# Source: https://python.langchain.com/docs/integrations/document_loaders/csv/
from __future__ import annotations

from langchain_community.document_loaders import CSVLoader

text_loader_kwargs = {'autodetect_encoding': True}

loader = CSVLoader(
    file_path='../datasets/dataset.csv',
    encoding='utf8'
    # csv_args={
    #     'delimiter': ',',
    #     'quotechar': '"',
    #     'fieldnames': ['Index', 'Height', 'Weight']
    # }
)

data = loader.load()

print(data)
