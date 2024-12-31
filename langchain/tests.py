from __future__ import annotations

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

dataset_path = 'datasets'
dataset_file = 'dataset'

with open(dataset_path + '/' + dataset_file + '.txt') as dataset:
    dataset_info = dataset.read()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

texts = text_splitter.create_documents([dataset_info])

print(texts[0])
print(texts[1])
print(text_splitter.split_text(dataset_info)[:2])


embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# text = "This is a test document."
query_result = embeddings.embed_query(dataset_info)

# show only the first 100 characters of the stringified vector
print(str(query_result)[:100] + '...')
