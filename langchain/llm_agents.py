from __future__ import annotations

import datetime
import os
import sys
from tempfile import TemporaryDirectory

from icecream import ic
from langchain_anthropic import ChatAnthropic
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools import ShellTool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from loguru import logger
from prettyformatter import pprint
from rich import inspect
from rich import print_json
from src import llm_tools
from src import local_tools
from src import ollama_chat
from src import vector_store
from src.config_vars import Error_Handler
from src.config_vars import OLLAMA_CHAT_CONFIG
from src.config_vars import OLLAMA_MODEL_CONFIG
from src.config_vars import TODAY

from langchain.agents import AgentType
from langchain.agents import initialize_agent


def llm_agent():
    memory = MemorySaver()
    search = TavilySearchResults(max_results=2)
    tools = [search]
    agent_executor = create_react_agent(
        OLLAMA_CHAT_CONFIG, tools, checkpointer=memory)

    # Use the agent ##
    config = {'configurable': {'thread_id': 'abc123'}}
    for chunk in agent_executor.stream({'messages': [HumanMessage(content='hi im bob! and i live in sf')]}, config):
        pprint(chunk)
        pprint('----')

    for chunk in agent_executor.stream({'messages': [HumanMessage(content='whats the weather where I live?')]}, config):
        pprint(chunk)
        pprint('----')


def llm_agent_file_system():        # Source: https://python.langchain.com/docs/integrations/tools/filesystem/
    # We'll make a temporary directory to avoid clutter
    working_directory = TemporaryDirectory(delete=False)
    # If you don't provide a root_dir, operations will default to the current working directory
    toolkit = FileManagementToolkit(root_dir=str(working_directory.name))
    toolkit.get_tools()
    tools = FileManagementToolkit(root_dir=str(working_directory.name), selected_tools=[
                                  'read_file', 'write_file', 'list_directory']).get_tools()
    pprint(tools)
    read_tool, write_tool, list_tool = tools
    write_tool.invoke({'file_path': 'example.txt', 'text': 'Hello World!'})
    # List files in the working directory
    list_tool.invoke({})


def llm_bash():
    shell_tool = ShellTool(
        name='terminal',
        description='Run shell commands on this machine.',
        ask_human_input=False,
    )
    ic(shell_tool.run(
        {'commands': ['echo Hello', 'whoami']}, start_color='yellow', color='green'))

    shell_tool.description = shell_tool.description + \
        f"args {shell_tool.args}".replace('{', '{{').replace('}', '}}')
    self_ask_with_search = initialize_agent(
        [shell_tool], OLLAMA_CHAT_CONFIG, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    self_ask_with_search.run(
        'Download the langchain.com webpage and grep for all urls. Return only a sorted list of them. Be sure to use double quotes.')


def llm_human_as_a_tool():
    # set llm model config ##
    # llm = local_tools.chat_ollama_config(model='llama3.2:1b', temperature=0.0)
    # math_llm = local_tools.ollama_llm_config(model='llama3.2:1b', temperature=0.0)
    tools = load_tools(
        ['human', 'llm-math'],
        llm=OLLAMA_CHAT_CONFIG,
        allow_dangerous_tools=True,
    )

    agent_chain = initialize_agent(
        tools,
        OLLAMA_CHAT_CONFIG,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    agent_chain.run("What's my friend Eric's surname?")


def llm_python_repl():
    python_repl = PythonREPL()
    # python_repl.run("print(1+1)")
    # You can create the tool to pass to an agent
    repl_tool = Tool(
        name='python_repl',
        description='A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.',
        func=python_repl.run,
    )
    llm_agent_run = repl_tool.run('print(1+1)')
    ic(llm_agent_run)


if __name__ == '__main__':
    # load_local_env_var()
    # llm_agent()
    # llm_agent_file_system()
    # llm_bash()
    # llm_human_as_a_tool()
    llm_python_repl()
