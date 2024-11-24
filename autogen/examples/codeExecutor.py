from __future__ import annotations

import tempfile

from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

config_list = [
    {
        'model': 'llama3.2:latest',   # codellama:latest, llama3.2:latest, llama3.1:latest
        'base_url': 'http://192.168.50.50:11434/v1',
        'api_key': 'ollama',        # pragma: allowlist secret
        'price': [0, 0],
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

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()

# Create a local command line code executor.
executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    # work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
)

# Create an agent with code executor configuration.
code_executor_agent = ConversableAgent(
    'code_executor_agent',
    llm_config=False,  # Turn off LLM for this agent.
    # Use the local command line code executor.
    code_execution_config={'executor': executor},
    human_input_mode='NEVER',  # Asking for Human Input. "ALWAYS", "NEVER", "TERMINATE"
)

message_with_code_block = """This is a message with code block.
The code block is below:
```python
import numpy as np
import matplotlib.pyplot as plt
x = np.random.randint(0, 100, 100)
y = np.random.randint(0, 100, 100)
plt.scatter(x, y)
plt.savefig('scatter.png')
print('Scatter plot saved to scatter.png')
```
This is the end of the message.
"""

# Generate a reply for the given code.
reply = code_executor_agent.generate_reply(
    messages=[{'role': 'user', 'content': message_with_code_block}])

print(reply)
