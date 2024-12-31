from __future__ import annotations

from datetime import datetime

# header_template = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',}


def hacker_news_retriever(url):
    """Define the metadata extraction function in the JSON file.\n
    Source https://api.python.langchain.com/en/latest/document_loaders/langchain_community.document_loaders.hn.HNLoader.html"""
    from langchain_community.document_loaders import HNLoader
    start_time = datetime.now()
    try:

        LOADER = HNLoader(url, show_progress=True,
                          header_template=header_template)
        DATA = LOADER.load()
        DATA[0].page_content[:300]
        print(DATA[0].metadata)
        # print(DATA[0].page_content[:300])
    except Exception as error:
        print('Something went wrong when Retrieving Documents: ',
              error, '\nError in Definition: ', __name__)
    finally:
        end_time = datetime.now()
        print('\nFinished retrieve hacker news topic: ',
              'Duration: {}'.format(end_time - start_time))


def Wikipedia_retriever(topic):
    """Define the Wikipedia topic to extract."""
    from langchain_community.retrievers import WikipediaRetriever
    start_time = datetime.now()
    try:
        RETRIEVER = WikipediaRetriever()
        DOCUMENTS = RETRIEVER.invoke(topic)
        print(DOCUMENTS[0].page_content[:400])

    except Exception as error:
        print('Something went wrong when Retrieving Documents: ',
              error, '\nError in Definition: ', __name__)
    finally:
        end_time = datetime.now()
        print('\nFinished retrieve wikipedia topic: ',
              'Duration: {}'.format(end_time - start_time))
