from __future__ import annotations

from langchain_community.document_loaders import HNLoader

LOADER = HNLoader('https://news.ycombinator.com/item?id=34817881')
DATA = LOADER.load()
DATA[0].page_content[:300]

print(DATA[0].metadata)
# print(DATA[0].page_content[:300])
