from __future__ import annotations

import sys

from langchain_community.document_loaders import HNLoader
from langchain_community.retrievers import WikipediaRetriever
from loguru import logger

HEADER_TEMPLATE = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', }


def hacker_news_retriever(url) -> HNLoader:
    """Define the metadata extraction function in the JSON file.\n
    Source https://api.python.langchain.com/en/latest/document_loaders/langchain_community.document_loaders.hn.HNLoader.html"""
    try:
        loader = HNLoader(url, show_progress=True,
                          header_template=HEADER_TEMPLATE)
        DATA = loader.load()
        DATA[0].page_content[:300]
        logger.debug(DATA[0].metadata)
        # print(DATA[0].page_content[:300])

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


def Wikipedia_retriever(topic) -> WikipediaRetriever:
    """Define the Wikipedia topic to extract."""
    try:
        RETRIEVER = WikipediaRetriever()
        documents = RETRIEVER.invoke(topic)
        logger.debug(documents[0].page_content[:400])

    except Exception:
        logger.exception(
            'An error occurred while running the program, please check the logs for more information. ')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


if __name__ == '__main__':
    logger.error('this is not the main script, exiting ...')
    sys.exit()
