from __future__ import annotations

import base64
from io import BytesIO
from typing import List

from IPython.display import display
from IPython.display import HTML
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from PIL import Image

# llm = OpenAI(temperature=0.5, max_tokens=100)

llm = ChatOllama(
    model='qwen2.5-coder:1.5b',
    temperature=0.1,
    max_tokens=100
)

retriever = WikipediaRetriever()

docs = retriever.invoke('TOKYO GHOUL')

print(docs[0].page_content[:400])

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based only on the context provided.
    Context: {context}
    Question: {question}
    """
)


def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)


chain = (
    {'context': retriever | format_docs, 'question': RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print_status = chain.invoke(
    'Who is the main character in `Tokyo Ghoul` and does he transform into a ghoul?'
)

print(print_status)
