# run local chromadb: chroma run --host localhost --port 8000 --path ./chroma_data
from __future__ import annotations

import chromadb

# Chroma DB Server Variables
CHROMA_HOST = '172.22.54.208'
CHROMA_PORT = 8000

# Connect to Chroma DB with HttpClient Library
chroma_client = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT,
    ssl=False
)

# Connect to Chroma DB with Client Library
COLLECTION = chroma_client.list_collections()

while True:
    if not COLLECTION:
        print('No collection found, Exiting')
        break
    print(COLLECTION, '\ndo you want to delete all collections? (yes/no/exit)')
    user_input = input()
    if user_input != 'yes' and user_input != 'no' and user_input != 'exit':
        print('Invalid input, please enter yes/no/exit')
        continue
    if user_input == 'yes':
        chroma_client.reset()
        print('all collections deleted')
        break
    if user_input == 'no':
        print('do you want to delete a specific collection? (yes/no/exit)')
        user_input = input()
        if user_input != 'yes' and user_input != 'no' and user_input != 'exit':
            print('Invalid input, please enter yes/no/exit')
            continue
        if user_input == 'yes':
            print('Enter the collection name you want to delete')
            COLLECTION_NAME = input()
            chroma_client.delete_collection(name=COLLECTION_NAME)
            print(f"collection {COLLECTION_NAME} deleted")
            break
        if user_input == 'no':
            print('Exiting, No collection deleted')
            break
    if user_input == 'exit':
        print('Exiting, No collection deleted')
        break
