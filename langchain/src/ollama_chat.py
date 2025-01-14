from __future__ import annotations

import os
import sys

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from loguru import logger


def start_ollama_chat(response_message, data):
    try:
        # model = ChatOllama(
        #     model="llama3.2:1b",
        #     base_url="http://localhost:11434/",
        #     temperature=0.2,
        #     verbose=True,
        #     streaming=True,
        #     max_tokens=1000,
        #     max_retries=3,
        #     # cache=True,
        # )

        # response_message = model.invoke(response_message)
        # print(response_message.content)
        # retriever = vectorstore.as_retriever()
        # qa_chain = ({"context": data, "question": RunnablePassthrough()} | response_message | StrOutputParser())

        model = ChatOllama(model='llama3.2:1b')

        # RAG_TEMPLATE = """
        # You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
        # <context>
        # {context}
        # </context>
        # Answer the following question:
        # {question}"""

        # rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)

        # qa_chain = (
        #     {"context": data, "question": RunnablePassthrough()}
        #     | rag_prompt
        #     | model
        #     | StrOutputParser()
        # )

        # question = response_message
        # qa_chain.invoke(question)

        prompt = ChatPromptTemplate.from_template(
            'how much is the total amount of the invoice? {data}'
        )

        # Convert loaded documents into strings by concatenating their content
        # and ignoring metadata
        # def format_docs(docs):
        #     return "\n\n".join(doc.page_content for doc in docs)

        chain = data | prompt | model | StrOutputParser()
        question = 'What are the approaches to Task Decomposition?'
        vectorstore = data
        docs = vectorstore.similarity_search(question)

        chain.invoke(docs)
    except Exception as error:
        logger.exception(
            'An Error Occurred while loading files from disk', error)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error('program terminated by user.')


# def prompt_llm():
#     print('\nConnecting to LLM ...')
#     try:
#         QUERY_PROMPT = PromptTemplate(
#             input_variables=['question'],
#             template="""You are an AI language model assistant. Your task is to generate five
#             different versions of the given user question to retrieve relevant documents from
#             a vector database. By generating multiple perspectives on the user question, your
#             goal is to help the user overcome some of the limitations of the distance-based
#             similarity search. Provide these alternative questions separated by newlines.
#             Original question: {question}""",
#         )

#         template = """Answer the question based ONLY on the following context:
#         {context}
#         Question: {question}
#         """

#         prompt = ChatPromptTemplate.from_template(template)

#         return QUERY_PROMPT, prompt
#     except Exception as error:
#         print('\nSomething went wrong when connect to chroma db: ', error, '\nError in Definition: ', __name__, '\nExiting ...')
#         exit(1)
#     # finally:
#         # end_time = datetime.now()
#         # print("\nFinished Connect to Chroma DB: ", 'Duration: {}'.format(end_time - start_time))


# def query_llm(input):
#     if input:
#         # Initialize the language model with the specified model name
#         llm = ChatOllama(model=LLM_MODEL)
#         # Get the vector database instance
#         db = get_vector_db()
#         # Get the prompt templates
#         QUERY_PROMPT, prompt = get_prompt()

#         # Set up the retriever to generate multiple queries using the language model and the query prompt
#         retriever = MultiQueryRetriever.from_llm(
#             db.as_retriever(),
#             llm,
#             prompt=QUERY_PROMPT
#         )

#         # Define the processing chain to retrieve context, generate the answer, and parse the output
#         chain = (
#             {'context': retriever, 'question': RunnablePassthrough()}
#             | prompt
#             | llm
#             | StrOutputParser()
#         )

#         response = chain.invoke(input)

#         return response

#     return None


if __name__ == '__main__':
    start_ollama_chat(response_message, data)


# chain = {"docs": format_docs} | prompt | model | StrOutputParser()
# question = "What are the approaches to Task Decomposition?"
# docs = vectorstore.similarity_search(question)

# chain.invoke(docs)
# retriever = vectorstore.as_retriever()
# qa_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | rag_prompt
#     | model
#     | StrOutputParser()
# )
# question = "What are the approaches to Task Decomposition?"
# qa_chain.invoke(question)
