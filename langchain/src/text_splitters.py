from __future__ import annotations

import os
import sys

import nltk
from langchain_text_splitters import CharacterTextSplitter
from loguru import logger


def splitting_documents(loader, chunk_size=1000, chunk_overlap=200, debug=True) -> CharacterTextSplitter:
    # print('[DEBUG][splitters]Starting Split Documents Process ...')
    # print(loader)
    # print(len(loader))
    if loader is None:
        print('Data in Loader is Empty, No Data to Split, Exiting ...')
        exit(1)
    if loader is not None:
        # print("Print Splitter Preview 'documents': ", documents[0].page_content[:40], '......')
        # print(f"{len(loader)} Documents Loaded ...")

        # text_splitter = TokenTextSplitter(
        #     chunk_size=chunk_size,    # 10
        #     chunk_overlap=chunk_overlap   # 0
        #     )

        # text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        #     chunk_size=chunk_size,      # 1000
        #     chunk_overlap=chunk_overlap,    # 200
        #     encoding_name="cl100k_base",
        # )

        # texts = loader[0].page_content
        # print(loader[0].page_content)
        # if debug is True:
        #     print("[DEBUG]review value 'texts': ", texts[:40])

        # nltk.download('punkt_tab')
        # print("Total tokens in document: ", len(nltk.word_tokenize(texts)))

        # print(text)
        # documents = text_splitter.create_documents([text])
        # for doc in documents:
        #     print(doc.page_content)

        # metadatas = [{"document": 1}]
        # documents = text_splitter.create_documents(
        #     [texts], metadatas=metadatas
        # )
        # metadatas = [{"document": 1}, {"document": 2}]
        # documents = text_splitter.create_documents(
        #     [texts, texts], metadatas=metadatas
        # )

        # print("\nPreview value 'documents': ", documents)

        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator='\n\n',
            length_function=len,
            is_separator_regex=False,
        )

        chunks = text_splitter.split_documents(loader)
        logger.debug(
            f"split {len(loader)} documents into {len(chunks)} chunks.")

        if debug is True:
            logger.debug("print value 'chunks': ",
                         chunks[0].page_content[:50], '...')
            logger.debug('Number of total chunks created', len(chunks))

            folder_path = 'data'
            if not os.path.exists(folder_path):
                logger.warning(
                    f"folder {folder_path} did not found, building new folder")
                os.makedirs(folder_path)

            for index, chunk in enumerate(chunks):
                with open('data/chunks{}.txt'.format(index), 'w') as output:
                    output.write(str(chunk.page_content))
                    logger.debug(len(chunk.page_content),
                                 'Tokens in chunk.')

                # for chunk in chunks:
                #     print(chunk.page_content)
                #     print(len(chunk.page_content), "Tokens in chunk.")

                # with open('data/chunks.txt', 'w') as file_handler:
                #     index = 1
                #     for chunk in chunks:
                #         file_handler.write("{}. {}\n\n".format(index, chunk))
                #         index += 1
                #         print(len(chunk.page_content), "Tokens in chunk.")
                    # write_file.write_file(file_name="data/chunks.txt", data=chunk)

            # print("Total number of tokens in document: ", len(nltk.word_tokenize(loader[0].page_content)))
            # print("Total number of tokens in split document: ", len(nltk.word_tokenize(chunks[0].page_content)))
            # print("Total number of tokens in split document: ", len(nltk.word_tokenize(chunks[1].page_content)))

        logger.debug('Successfully Split Documents into Chunks ...')
        return chunks


if __name__ == '__main__':
    print('this is not the main function, exiting ...')
    sys.exit()
