from __future__ import annotations

import os
import sys
from datetime import datetime

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from prettyformatter import pprint
from src import text_splitters


def embeddings_string(model_name='sentence-transformers/all-mpnet-base-v2', debug=False) -> HuggingFaceEmbeddings:
    """build embeddings string"""
    # start_time = datetime.now()
    # print('Building Embeddings String ...')
    try:
        # if model_name not in ['sentence-transformers/all-mpnet-base-v2', 'all-MiniLM-L6-v2']:
        #   raise Exception("Embeddings model not supported")
        if model_name in 'sentence-transformers/all-mpnet-base-v2':
            if debug is True:
                print(
                    'using default embeddings model: sentence-transformers/all-mpnet-base-v2')
            embeddings_model = embeddings_default(model_name=model_name)
        if model_name not in ['sentence-transformers/all-mpnet-base-v2']:
            print(
                "not using default embeddings model 'all-mpnet-base-v2', new embeddings model is: ", model_name)
            if model_name == 'all-MiniLM-L6-v2':
                print('using default embeddings model: all-MiniLM-L6-v2')
                embeddings_model = embeddings_default(model_name=model_name)
            # if model_name == 'llama3':
            #     embeddings_model = OllamaEmbeddings(model="llama3")

        return embeddings_model
    except Exception as error:
        print('\nAn Error Occurred while building Embeddings string: ',
              error, '\nError in Definition: ', __name__, 'Exiting ...')
        sys.exit(1)
    # finally:
    #     end_time = datetime.now()
    #     print("Successfully Build Embeddings String: ", 'Duration: {}'.format(end_time - start_time), "\n")


def embeddings_default(model_name):
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,      # model_name='all-MiniLM-L6-v2'
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False},
    )
    return embeddings


def embeddings_text(embeddings_model, embeddings_data, debug=False):
    # start_time = datetime.now()
    try:
        # print(embeddings_data, "\n")
        # if len(embeddings) == len(embeddings):
        #     print("confirmation of chunks received as expected: ", len(embeddings), " = ", len(embeddings))
        # else:
        # print("chunks received not as expected, exiting ...")
        # sys.exit(1)

        for index, embed in enumerate(embeddings_data):
            embeddings_config = embeddings_model.embed_documents(embed)
            # building local text file for each chunk for debugging
            if debug is True:
                folder_path = 'data'
                if not os.path.exists(folder_path):
                    print(
                        f"folder {folder_path} did not found, building new folder")
                    os.makedirs(folder_path)

                with open('data/embeddings.txt', 'w') as output:
                    print("[DEBUG]review value of 'embed': ",
                          embeddings_config[:5], '...')
                    output.write(str(embeddings_config))
                    print('[DEBUG]print embeddings text to file')

                # for index, embed in enumerate(embeddings_config[0]):
                # with open('data/embeddings{}.txt'.format(index), 'w') as output:
                #     print("[DEBUG]review value of 'embed', index {}: ".format(index), embeddings_config[0][:5], '...')
                #     output.write(str(embeddings_config[0]))
                #     print("[DEBUG]print embeddings text to file")

        # if debug is True:
            # print("[DEBUG]number of chunks received from value of 'split_config': ", len(split_config))
            # print("[DEBUG]number of embeddings in value of 'embeddings': ", len(embeddings))
            # print("[DEBUG]review value 'embeddings_config': ", embeddings_config[0][:40], "...")
            # print("[DEBUG]review value of 'embeddings': ", embeddings[0].page_content[:50], "...")
            # print("[DEBUG]review value of 'embeddings_config', index {}:".format(index), embeddings_config[0][:5], '...')

        # return embeddings_config
    except Exception as error:
        print('\nAn Error Occurred while building Embeddings Text: ',
              error, '\nError in Definition: ', __name__, 'Exiting ...')
        sys.exit(1)
    except KeyboardInterrupt:
        print('\nProgram terminated by user.')
    # finally:
    #     end_time = datetime.now()
    #     print("Successfully Build Embeddings Text: ", 'Duration: {}'.format(end_time - start_time), "\n")


def embeddings_text_single_file(embeddings_string, data_to_embeddings):
    try:
        # print(data_to_embeddings, "\n")
        embeddings_data_output = embeddings_string.embed_documents(
            data_to_embeddings)

        folder_path = 'data'
        if not os.path.exists(folder_path):
            print(f"folder {folder_path} did not found, building new folder")
            os.makedirs(folder_path)

        with open('data/embeddings.txt', 'w') as output:
            # print("[DEBUG]review value of 'embeddings_config': ", embeddings_config)
            # print("[DEBUG]review value of 'embeddings_data_output': ", embeddings_data_output[0][:7], '...')
            print(len(embeddings_data_output), 'Number of Embeddings Items.\n')
            output.write(str(embeddings_data_output))
            # print("[DEBUG]print embeddings text to file")
            # print("[DEBUG]review value of 'embeddings_data_output': ", embeddings_data_output[0])

        return embeddings_data_output[0]
        # return embeddings_data_output['data'][0]['embedding']
    except Exception as error:
        print('\nAn Error Occurred while building Embeddings Text to single file: ',
              error, '\nError in Definition: ', __name__, 'Exiting ...')
        sys.exit(1)
    except KeyboardInterrupt:
        print('\nProgram terminated by user.')
    # finally:
    #     end_time = datetime.now()
    #     print("Successfully Build Embeddings Text: ", 'Duration: {}'.format(end_time - start_time), "\n")


def embedded_query(embeddings, query, embeddings_model):
    # start_time = datetime.now()
    try:
        embedded_query = embeddings_model.embed_query(query)
        print("Preview 'embedded_query': ", embedded_query[:5])
        # print("embeddings model: ", embeddings.model_name)
        return embedded_query

    except Exception as error:
        print('\nAn Error Occurred while Embeddings Query: ', error,
              '\nError in Definition: ', __name__, 'Exiting ...')
        sys.exit(1)
    # finally:
    #     end_time = datetime.now()
    #     print("Successfully Build Embeddings Query: ", 'Duration: {}'.format(end_time - start_time), "\n")


if __name__ == '__main__':
    print('this is not the main script, exiting ...')
    sys.exit()
