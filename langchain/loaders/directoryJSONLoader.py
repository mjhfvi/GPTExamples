# Source: https://python.langchain.com/docs/integrations/document_loaders/json/
from __future__ import annotations

from langchain_community.document_loaders import JSONLoader


# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:
    metadata['sender_name'] = record.get('sender_name')
    metadata['timestamp_ms'] = record.get('timestamp_ms')
    return metadata


loader = JSONLoader(
    file_path='../datasets/dataset.json',
    jq_schema='.messages[]',
    content_key='content',
    metadata_func=metadata_func,
)

docs = loader.load()
print(docs[0].metadata)
