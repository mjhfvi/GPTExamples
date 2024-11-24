from __future__ import annotations

from autogen import ConversableAgent

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

cathy = ConversableAgent(
    'cathy',
    system_message='Your name is Cathy and you are a part of a duo of comedians.',
    llm_config={
        'functions': function_list,
        'config_list': config_list,
        'timeout': 280,
        'temperature': 0.8,
        'cache_seed': None,
    },
    human_input_mode='NEVER',  # Human Input. "ALWAYS", "NEVER","TERMINATE"
)

joe = ConversableAgent(
    'joe',
    system_message='Your name is Joe and you are a part of a duo of comedians.',
    llm_config={
        'functions': function_list,
        'config_list': config_list,
        'timeout': 280,
        'temperature': 0.8,
        'cache_seed': None,
    },
    human_input_mode='NEVER',  # Human Input. "ALWAYS", "NEVER","TERMINATE"
)

result = joe.initiate_chat(
    cathy, message='Cathy, tell me a joke.', max_turns=2)
