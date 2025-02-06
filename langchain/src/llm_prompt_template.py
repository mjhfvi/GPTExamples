# from src.llm_tools import TODAY
from __future__ import annotations

from icecream import ic
from loguru import logger

from langchain.globals import set_llm_cache
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.docstore.document import Document


prompt_json_invoice = """
    You are an expert in processing invoice data.
    Please analyze the following invoice text, extract information and convert it into a structured dataset in a JSON format.

    Include the following fields if present:
    - Main customer number
    - Source tax invoice number
    - Date
    - Vendor Name
    - Customer Name
    - Paying customer number
    - Items (list of items with amount, quantity, price, and description)
    - credited items (list of items with amount, quantity, price, and description), set the amount and price in subtraction
    - Subtotal
    - Tax Amount
    - Total Amount

    Invoice Text:
    {input_text}


    notes: dates should only be in DD/MM/YYYY, keep the metadata of the Document, Billing Period should be MM/YYYY, provide the output in valid JSON format only.
    i am the customer and my name is Tzahi Cohen, so if you see any word 'Tsachi' change it to 'Tzahi',
    """

llm_prompt_validation = """
    You are an expert in data validation for building datasets, please analyze the following text and validate it.
    notes all the correction you did to the dataset, only show the differences in the text not all the text.

    make sure the included fields are present in the dataset with relevant values:
    - Invoice Number (int)
    - Date (str)
    - Vendor Name (str)
    - Customer Name (str)
    - paying customer number (int)
    - Items (list of items with quantity, price, and description) (list of str)
    - Subtotal (float)
    - Tax Amount (float)
    - Total Amount (float)
    - Payment charged via credit card ending (str)

    the instruction for the first llm was: the dates should only be in DD/MM/YYYY, keep the metadata of the Document, provide the output in valid JSON format only.
    i am the customer and my name is Tzahi Cohen, so if you see any word 'Tsachi' change it to 'Tzahi',

    """

# , the date today is {TODAY}
# def llm_prompt_template():
#     logger.info('starting chat with llm model, using wikipedia query')

#     set_llm_cache(InMemoryCache())
#     prompt = ChatPromptTemplate.from_messages([('system', prompt_json_invoice_hebrew)])
#     llm_chain = prompt | OLLAMA_MODEL_CONFIG
#     llm_human_question = 'explain what is langchain?'
#     llm_message = llm_chain.invoke(
#         {
#             'question': llm_human_question,
#             'tavily_results': 'use this data to answer the question: ',
#         }
#     )
#     ic('Ai Answer:')
#     ic(llm_message)
