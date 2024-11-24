from __future__ import annotations

import autogen
from autogen import AssistantAgent
from autogen import UserProxyAgent

prompt_price_per_1k = (0)
completion_token_price_per_1k = (0)

config_list = {
    'model': 'llama3.2:latest',   # codellama:latest, llama3.2:latest, llama3.1:latest
    'base_url': 'http://192.168.50.50:11434/v1',
    'api_key': 'ollama',        # pragma: allowlist secret
    'price': [prompt_price_per_1k, completion_token_price_per_1k],
}

assistant = AssistantAgent('assistant', llm_config=config_list)

user_proxy = UserProxyAgent(
    'user_proxy',
    code_execution_config={
        'executor': autogen.coding.LocalCommandLineCodeExecutor(work_dir='coding')},
    human_input_mode='NEVER',  # Asking for Human Input. "ALWAYS", "NEVER", "TERMINATE"
)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message='Plot a chart of NVDA and TESLA stock price change YTD.',

)
