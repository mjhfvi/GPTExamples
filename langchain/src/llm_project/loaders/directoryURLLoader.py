# Source: https://python.langchain.com/docs/integrations/document_loaders/url/
from __future__ import annotations

from langchain_community.document_loaders import UnstructuredURLLoader

urls = [
    'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023',
    'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-9-2023',
]

loader = UnstructuredURLLoader(urls=urls)
data = loader.load()
print(data)
data[0]
