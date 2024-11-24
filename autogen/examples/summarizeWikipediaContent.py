from __future__ import annotations

import json
import tempfile

import mwparserfromhell
import requests

from autogen.agentchat import AssistantAgent
from autogen.agentchat import register_function
from autogen.agentchat import UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

prompt_price_per_1k = (0)
completion_token_price_per_1k = (0)

config_list = [
    {
        'model': 'llama3.2:latest',   # codellama:latest, llama3.2:latest, llama3.1:latest
        'base_url': 'http://192.168.50.50:11434/v1',
        'api_key': 'ollama',        # pragma: allowlist secret
        'price': [prompt_price_per_1k, completion_token_price_per_1k],
    }
]

function_list = [
    {
        'name': 'wikipedia_search',
        'description': 'Perform a search on Wikipedia',
        'parameters': {
            'type': 'object',
            'properties': {
                'title': {
                    'type': 'string',
                    'description': 'Name of the article to search for',
                }
            },
            'required': ['title'],
        },
    }
]

SYSTEM_PROMPT = """
You are a knowledgeable librarian that answers questions from your supervisor.

For research tasks, only use the functions provided to you. Check the functions output and make your answer.

Constraints:
- Think step by step.
- Be accurate and precise.
- Answer briefly, in few words.
- Reflect on your answer, and if you think you are hallucinating, reformulate the answer.
- When you receive the result of a tool call, use it to respond to the supervisor, and then add the word "TERMINATE"
- Do not repeat yourself
"""

system_message = {'role': 'system', 'content': SYSTEM_PROMPT}

temp_dir = tempfile.TemporaryDirectory()

code_executor_config = LocalCommandLineCodeExecutor(
    timeout=30,
    work_dir=temp_dir.name,
)

agent = AssistantAgent(
    name='librarian',
    system_message=SYSTEM_PROMPT,
    human_input_mode='NEVER',   # Asking for Human Input. "ALWAYS", "NEVER", "TERMINATE"
    llm_config={
        'functions': function_list,
        'config_list': config_list,
        'timeout': 280,
        'temperature': 0.2,
    },
)

user = UserProxyAgent(
    name='supervisor',
    human_input_mode='ALWAYS',  # Asking for Human Input. "ALWAYS", "NEVER", "TERMINATE"
    max_consecutive_auto_reply=1,
    code_execution_config={'excutor': code_executor_config},
)


# Tools #
def wikipedia_search(title: str) -> str:
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'revisions',
            'rvprop': 'content',
        },
    ).json()
    page = next(iter(response['query']['pages'].values()))
    wikicode = page['revisions'][0]['*']
    parsed_wikicode = mwparserfromhell.parse(wikicode)
    content = parsed_wikicode.strip_code()
    return json.dumps({'name': 'wikipedia_search', 'content': content})


register_function(
    wikipedia_search,
    caller=agent,
    executor=user,
    name='wikipedia_search',
    description='Perform a search on Wikipedia',
)

chat_result = user.initiate_chat(
    agent,
    message="Get the content of the Wikipedia page for 'EA_Sports'. Then, summarize the page content.",
)

print(chat_result)
