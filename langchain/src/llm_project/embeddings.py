from __future__ import annotations

from datetime import datetime

from langchain_huggingface import HuggingFaceEmbeddings


def embeddings_string() -> HuggingFaceEmbeddings:
    """build embeddings string"""
    start_time = datetime.now()
    print('Starting Embeddings Process ...')
    try:
        # model_name='all-MiniLM-L6-v2'
        EMBEDDINGS = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-mpnet-base-v2')

        end_time = datetime.now()
        print('Successfully Embeddings Data: ',
              'Duration: {}'.format(end_time - start_time))
        return EMBEDDINGS
    except Exception as error:
        print('\nSomething went wrong when Embeddings Data: ', error,
              '\nError in Definition: ', __name__, '\nExiting ...')
        exit(1)
    # finally:
    #     end_time = datetime.now()
    #     print("\nFinished connect to chroma db: ", 'Duration: {}'.format(end_time - start_time))
