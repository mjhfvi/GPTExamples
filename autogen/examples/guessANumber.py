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

agent_with_number = ConversableAgent(
    'agent_with_number',
    system_message='You are playing a game of guess-my-number. You have the '
    'number 4 in your mind, and I will try to guess it. '
    "If I guess too high, say 'too high', if I guess too low, say 'too low'. ",
    llm_config={
        'config_list': config_list,
        'timeout': 280,
        'temperature': 0.2,
    },
    # terminate if the number is guessed by the other agent
    # Human Input. "ALWAYS", "NEVER","TERMINATE"
    is_termination_msg=lambda msg: '4' in msg['content'], human_input_mode='NEVER',
)

agent_guess_number = ConversableAgent(
    'agent_guess_number',
    system_message='I have a number in my mind, and you will try to guess it. '
    "If I say 'too high', you should guess a lower number. If I say 'too low', "
    'you should guess a higher number. ',
    llm_config={
        'config_list': config_list,
        'timeout': 280,
        'temperature': 0.2,
    },
    human_input_mode='NEVER',  # Human Input. "ALWAYS", "NEVER","TERMINATE"
)

result = agent_with_number.initiate_chat(
    agent_guess_number,
    message='I have a number between 1 and 10. Guess it!',
)
