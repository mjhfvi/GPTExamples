# Source: https://python.langchain.com/docs/integrations/document_loaders/url/
from __future__ import annotations

from langchain_community.document_loaders import SeleniumURLLoader

urls = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    # "https://goo.gl/maps/NDSHwePEyaHMFGwh8",
]

loader = SeleniumURLLoader(urls=urls)
data = loader.load()
data[0]

print(data[0])
