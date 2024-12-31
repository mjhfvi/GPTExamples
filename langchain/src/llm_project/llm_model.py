from __future__ import annotations

from datetime import datetime

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever

LLM_MODEL = os.getenv('LLM_MODEL', 'mistral')


def prompt_llm():
    """connect to chroma   HttpClient Library\nuse 'CHROMA_HOST' for host address\nuse 'CHROMA_PORT' for port number"""
    start_time = datetime.now()
    print('\nConnecting to LLM ...')
    try:
        QUERY_PROMPT = PromptTemplate(
            input_variables=['question'],
            template="""You are an AI language model assistant. Your task is to generate five
            different versions of the given user question to retrieve relevant documents from
            a vector database. By generating multiple perspectives on the user question, your
            goal is to help the user overcome some of the limitations of the distance-based
            similarity search. Provide these alternative questions separated by newlines.
            Original question: {question}""",
        )

        template = """Answer the question based ONLY on the following context:
        {context}
        Question: {question}
        """

        prompt = ChatPromptTemplate.from_template(template)

        return QUERY_PROMPT, prompt
    except Exception as error:
        print('\nSomething went wrong when connect to chroma db: ',
              error, '\nError in Definition: ', __name__, '\nExiting ...')
        exit(1)
    # finally:
        # end_time = datetime.now()
        # print("\nFinished Connect to Chroma DB: ", 'Duration: {}'.format(end_time - start_time))


def query(input):
    if input:
        # Initialize the language model with the specified model name
        llm = ChatOllama(model=LLM_MODEL)
        # Get the vector database instance
        db = get_vector_db()
        # Get the prompt templates
        QUERY_PROMPT, prompt = get_prompt()

        # Set up the retriever to generate multiple queries using the language model and the query prompt
        retriever = MultiQueryRetriever.from_llm(
            db.as_retriever(),
            llm,
            prompt=QUERY_PROMPT
        )

        # Define the processing chain to retrieve context, generate the answer, and parse the output
        chain = (
            {'context': retriever, 'question': RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        response = chain.invoke(input)

        return response

    return None
