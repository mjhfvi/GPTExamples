from __future__ import annotations

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode

dataset_path = 'datasets'
dataset_file = 'dataset'

text_loader_kwargs = {'autodetect_encoding': True}

loader = DirectoryLoader(
    '../datasets/',
    glob='**/*.txt',
    loader_cls=TextLoader,
    show_progress=True,
    use_multithreading=True,
    loader_kwargs=text_loader_kwargs
)

documents = loader.load(file_path=dataset_path + '/' + dataset_file + '.txt')

text_parser = SentenceSplitter(
    chunk_size=1024,
    # separator=" ",
)

text_chunks = []
# maintain relationship with source doc index, to help inject doc metadata in (3)
doc_idxs = []
for doc_idx, doc in enumerate(documents):
    cur_text_chunks = text_parser.split_text(doc.text)
    text_chunks.extend(cur_text_chunks)
    doc_idxs.extend([doc_idx] * len(cur_text_chunks))


nodes = []
for idx, text_chunk in enumerate(text_chunks):
    node = TextNode(
        text=text_chunk,
    )
    src_doc = documents[doc_idxs[idx]]
    node.metadata = src_doc.metadata
    nodes.append(node)
