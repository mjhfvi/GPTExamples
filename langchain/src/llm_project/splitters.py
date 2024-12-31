from __future__ import annotations

from datetime import datetime

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter


def splitting_documents(LOADER):
    """Define the metadata extraction function in the JSON file."""
    start_time = datetime.now()
    print('\nStarting Split Documents Process ...')
    # print(loader)
    # print(len(loader))
    try:
        if LOADER is None:
            print('Data in Loader is Empty, No Data to Split, Exiting ...')
            exit(1)
        if LOADER is not None:
            print('Found Data in Document Loader, Continue Splitting Documents ...')
            DOCUMENTS = LOADER.load()
            print(f"{len(DOCUMENTS)} Documents Loaded ...")
            print("Print Splitter Preview 'DOCUMENTS': ",
                  DOCUMENTS[0].page_content[:20], '......')

        TEXT_SPLITTER = CharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=10,
            # separator="\n\n",
            # length_function=len,
        )

        DOCUMENTS = TEXT_SPLITTER.create_documents(
            DOCUMENTS[0].page_content[0])
        # print(docs[0].page_content[:100])
        # print("\nPrinting Preview 'DOCUMENTS': ", DOCUMENTS)

        end_time = datetime.now()
        print('Successfully Split Documents: ',
              'Duration: {}'.format(end_time - start_time), '\n')
        # return DOCUMENTS_TEXT
    except Exception as error:
        print('\nSomething Went Wrong When Split Documents: ', error,
              '\nError in Definition: ', __name__, '\nExiting ...')
        # exit(1)
    # finally:
    #     end_time = datetime.now()
    #     print("\nFinished split documents: ", 'Duration: {}'.format(end_time - start_time))
