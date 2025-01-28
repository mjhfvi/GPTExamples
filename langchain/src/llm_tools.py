from __future__ import annotations

import getpass
import os
import sys

from dotenv import find_dotenv
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from loguru import logger


# def load_local_env_var() -> os.getenv:
#     try:
#         logger.info('loading variables')
#         load_dotenv(find_dotenv('/../.env'), verbose=True)

#         logger.debug('loading TAVILY_API_KEY key')
#         if not os.environ.get("TAVILY_API_KEY"):
#             logger.warning('cant find TAVILY_API_KEY in environment variables')
#         if os.environ.get("TAVILY_API_KEY") is not None:
#             os.environ['TAVILY_API_KEY'] = os.environ.get('TAVILY_API_KEY')
#         if not os.getenv('TAVILY_API_KEY'):
#             logger.warning('cant find TAVILY_API_KEY in .env file')
#         if os.getenv('TAVILY_API_KEY') is not None:
#             os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
#         if not os.environ.get("TAVILY_API_KEY") and not os.getenv('TAVILY_API_KEY'):
#             logger.warning('cant find TAVILY_API_KEY in environment variables and .env file')
#             os.environ['TAVILY_API_KEY'] = getpass.getpass("please enter TAVILY_API_KEY:\n")
#             if os.environ['TAVILY_API_KEY'] is not None:
#                 logger.success('successfully loading TAVILY_API_KEY key.')
#         else:
#             logger.success('successfully loading TAVILY_API_KEY key.')

#         return

#     except Exception:
#         logger.exception(
#             'An error occurred while running the program, please check the logs for more information. ')
#         sys.exit(1)
#     except KeyboardInterrupt:
#         logger.error('program terminated by user.')

def tavily_search_results(query) -> TavilySearchResults:
    tavily_tool = TavilySearchResults(
        name='tavily_search_results_json',
        description='A web search engine that provides search results in JSON format.',
        max_results=3,
        search_depth='advanced',
        include_answer=True,
        include_raw_content=True,
        include_images=True,
        handle_validation_error=False,
        # include_domains=[...],
        # exclude_domains=[...],
        # name="...",            # overwrite default tool name
        # description="...",     # overwrite default tool description
        # args_schema=...,       # overwrite default args_schema: BaseModel
    )
    tavily_results = tavily_tool.invoke(query)
    # logger.debug(tavily_results)

    return tavily_results
