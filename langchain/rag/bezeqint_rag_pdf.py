from __future__ import annotations

import chromadb
from deep_translator import GoogleTranslator
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from prettyformatter import pprint
from src import documents_embedding
from src import file_loaders
from src import llm_model
from src import text_splitters
from src import vector_store

import ollama
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma

file_path = './datasets/BezeqintInvoice/'
# directory_path = (file_path)

loader = PyPDFDirectoryLoader(file_path)

documents = loader.load()
# print("\n[DEBUG]", documents)

page_1 = [doc for doc in documents if doc.metadata.get('page') == 0]
page_2 = [doc for doc in documents if doc.metadata.get('page') == 1]

for doc in page_1:
    find_start_text = 'פתח תקווה'
    find_end_text = 'לתשלום לאחר המועד שנקבע'
    text_doc = page_1[0].page_content

    start_index = text_doc.find(find_start_text)
    if start_index == -1:
        print('Start text not found')

    start_index += len(find_start_text)
    end_index = text_doc.find(find_end_text, start_index)
    if end_index == -1:
        print('End text not found')

    new_text = text_doc[start_index:end_index]

    translated_page_1 = GoogleTranslator(
        source='hebrew', target='english').translate(new_text)
    # print(translated_page_1, "\n")

for doc in page_2:
    find_start_text = 'גישה1020638271'
    find_end_text = '** בשל עיגול סכימת החיובים תיתכ'
    text_doc = page_2[0].page_content
    # print(text_doc)

    start_index = text_doc.find(find_start_text)
    if start_index == -1:
        print('Start text not found')

    start_index += len(find_start_text)
    end_index = text_doc.find(find_end_text, start_index)
    if end_index == -1:
        print('End text not found')

    new_text = text_doc[start_index:end_index]

    translated_page_2 = GoogleTranslator(
        source='hebrew', target='english').translate(new_text)
    # print(translated_page_2, "\n")

translated_pages = translated_page_1 + translated_page_2

printing_text = [Document(metadata={
                          'source': 'Invoice_200141400.pdf', 'page': '0'}, page_content=translated_pages)]
chroma_collection_name = 'Invoice_2024-01-01'

# page_number = str(page_1[0].metadata.get('page'))

# print(document.metadata.get('date'))
# chroma_collection_name = ("Invoice_" + document.metadata.get('date'))
# print(chroma_collection_name)

embeddings_data_output = OllamaEmbeddings(model='llama3.2:3b')

embedding_text = Chroma.from_documents(
    collection_name=chroma_collection_name,
    # embedding_function=embeddings_data_output,
    embedding=embeddings_data_output,
    documents=printing_text,
    # Where to save data locally, remove if not necessary
    persist_directory='./chroma_db',
)

print(embedding_text)

chroma_client = vector_store.chroma_db_setup(print_debug=False)
# vector_store.chroma_db_create_collection(chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=False)
connection_string = vector_store.chroma_db_get_collection(
    chroma_client, chroma_collection_name=chroma_collection_name, list_collection_names=True, print_debug=True)
# test_data = vector_store.chroma_db_add_data_to_collection(connection_string=connection_string, chroma_collection_name, metadatas=metadatas, documents=translated_page_1, embeddings=embeddings_text, print_collection_data=True)
test_data = vector_store.chroma_db_get_data_from_collection(connection_string)
print(test_data)
# vector_store.chroma_db_from_documents_from_collection(chroma_client=chroma_client, chroma_collection_name=chroma_collection_name, documents=translated_page_1, embeddings=embeddings_text)

# query_embedding = vector_store.chroma_db_get_data_from_collection(connection_string=connection_string)
# data_to_query = "Invoice"
# query_embedding = vector_store.chroma_db_query_data_from_collection(connection_string, query_data=data_to_query)
# print(query_embedding)

# results = collection.query(
#     query_embeddings=[query_embedding],
#     n_results=5
# )

# for doc in results['documents']:
#     print(doc)

# llm_prompt = "how much is the total amount of the invoice?"

# generate a response combining the prompt and data we retrieved in step 2
# output = ollama.generate(
#     model="llama3.2:3b",
#     prompt=f"Using this data: {data_to_query}. Respond to this prompt: {llm_prompt}"
# )

# print(output['response'])

# print(dir(embeddings_data_output))
# print(vars(embeddings_data_output))
# print(type(embeddings_data_output))
# print(type(page_1))
# print(type(loader))
