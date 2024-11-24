from __future__ import annotations

from autogen import ConversableAgent
# from autogen import Cache

prompt_price_per_1k = (0)
completion_token_price_per_1k = (0)

config_list = {
    'model': 'llama3.2:latest',   # codellama:latest, llama3.2:latest, llama3.1:latest
    'base_url': 'http://192.168.50.50:11434/v1',
    'api_key': 'ollama',        # pragma: allowlist secret
    'timeout': 120,
    # value between 0 and 1 that controls the randomness of the generated text.
    # A higher temperature will result in more random and diverse text,
    # while a lower temperature will result in more
    'temperature': 0.9,
    # "top_p": 0.2,     # Note: It is recommended to set temperature or top_p but not both.
    # the maximum number of tokens (words or word pieces) to generate in the output.
    'max_tokens': 2048,
    'stream': False,     # stream text output, True or False
    'price': [prompt_price_per_1k, completion_token_price_per_1k],
    'cache_seed': None,
    # To disable caching completely, set cache_seed to "None"
    # This is a random seed value. A seed is used in random number generation to ensure reproducibility.
    # By setting a seed, you can ensure that the random processes in the model produce the same results
    # every time it’s run with that seed. The value '42' is just an example;
    # you can change this seed value for different trials to get varied results.
    'tags': ['llama', 'local'],
}

agent = ConversableAgent(
    'chatbot',
    llm_config=config_list,
    # system_message="system message 01",
    # Turn off code execution, by default it is off.
    code_execution_config=False,
    function_map=None,  # No registered functions, by default it is None.
    human_input_mode='NEVER',  # Human Input. "ALWAYS", "NEVER","TERMINATE"
    is_termination_msg=lambda msg: 'good bye' in msg['content'].lower(),
    # Limit the number of consecutive auto-replies.
    max_consecutive_auto_reply=2,
)

reply = agent.generate_reply(
    messages=[{'content': 'Tell me a joke.', 'role': 'user'}])
print(reply)
