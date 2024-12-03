from __future__ import annotations

import os

import autogen
from autogen import AssistantAgent
from autogen import ConversableAgent
from autogen import GroupChat
from autogen import GroupChatManager
from autogen import UserProxyAgent
from autogen.coding import CodeBlock
from autogen.coding import DockerCommandLineCodeExecutor
from autogen.coding import LocalCommandLineCodeExecutor
# from flaml import autogen


config_list = [
    {'model': 'qwen2.5-coder:latest', 'base_url': 'http://localhost:11434/v1',
        'api_key': 'ollama', 'price': [0, 0], },                    # pragma: allowlist secret
    {'model': 'llama3.2-vision:latest', 'base_url': 'http://localhost:11434/v1',
        'api_key': 'ollama', 'price': [0, 0], },                    # pragma: allowlist secret
    {'model': 'qwen2.5-coder:3b', 'base_url': 'http://localhost:11434/v1',
        'api_key': 'ollama', 'price': [0, 0], },                    # pragma: allowlist secret
    {'model': 'llama3.2:latest', 'base_url': 'http://localhost:11434/v1',
        'api_key': 'ollama', 'price': [0, 0], },                    # pragma: allowlist secret
]

# filename
work_dir = 'documents'
# read file guidelines for the bot
code_guidelines = open('code_guidelines.md', 'r').read()
devops_input = open('devops_input.txt', 'r').read()
qa_input = open('qa_input.txt', 'r').read()
security_input = open('security_input.txt', 'r').read()
technical_writer_input = open('technical_writer_input.txt', 'r').read()

# create a code executor instance named "code_executor_agent" with code execution.
code_executor_agent = LocalCommandLineCodeExecutor(
    timeout=3600,
    work_dir=work_dir
    # virtual_env_context= None,
    # functions: List[Union[FunctionWithRequirements[Any, A], Callable[..., Any], FunctionWithRequirementsStr]] = [],
    # functions_module= "functions",
    # execution_policies= None,
)

# create a code executor instance named "code_executor_agent_docker" with code execution on docker.
code_executor_agent_docker = DockerCommandLineCodeExecutor(
    timeout=3600,
    work_dir=work_dir,
    image='python:3-slim',
    # container_name= Optional[str] = None,
    bind_dir=None,
    auto_remove=True,
    stop_container=True,
    # execution_policies= Optional[Dict[str, bool]] = None,
    # code_execution_config= False,
    # code_execution_config={
    #     # "executor": code_executor,
    #     "work_dir": work_dir,
    #     "use_docker": True,
    # }
)

# create an AssistantAgent instance for project_manager with the LLM configuration.
project_manager = AssistantAgent(
    name='project_manager',
    description='You are a helpful AI Project Manager, Build and develop the project team to ensure maximum performance, by providing purpose and direction',
    system_message=code_guidelines,
    max_consecutive_auto_reply=8,
    is_termination_msg=lambda msg: 'done' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,
    # code_execution_config={
    #     'executor': code_executor_agent,    # False,
    #     # "use_docker": False,
    #     },
    llm_config={
        'config_list': [
            {
                'model': 'qwen2.5-coder:latest',
                'base_url': 'http://localhost:11434/v1',
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0,
        'cache_seed': 10,
    },
)

# create an AssistantAgent instance for devops_agents with the LLM configuration.
devops_agent_01 = AssistantAgent(
    name='devops_agent_01',
    description='You are a helpful AI Devops Assistant, Assisting with Writing Code for the Project',
    system_message=code_guidelines,
    max_consecutive_auto_reply=6,
    # is_termination_msg= lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,
    # code_execution_config={
    #     'executor': code_executor_agent,    # False,
    #     # "use_docker": False,
    #     },
    llm_config={
        'config_list': [
            {
                'model': 'qwen2.5-coder:3b',
                'base_url': 'http://localhost:11434/v1',
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.2,
        'cache_seed': 11,
    },
)

devops_agent_02 = AssistantAgent(
    name='developer_agent_02',
    description='You are a helpful AI Assistant Assisting with Writing Code for the Project',
    # system_message= code_guidelines,
    max_consecutive_auto_reply=6,
    # is_termination_msg= lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,
    # code_execution_config={
    #     'executor': code_executor_agent,    # False,
    #     # "use_docker": False,
    #     },
    llm_config={
        'config_list': [
            {
                'model': 'llama3.2:latest',
                'base_url': 'http://localhost:11434/v1',
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.2,
        'cache_seed': 11,
    },
)

# create an AssistantAgent instance for security_agents with the LLM configuration.
security_agent_01 = AssistantAgent(
    name='security_agent_01',
    description='You are a helpful AI Security Assistant, Assisting with Writing Security Tests for the Project',
    system_message=code_guidelines,
    max_consecutive_auto_reply=4,
    # is_termination_msg= lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,
    # code_execution_config={
    #     'executor': code_executor_agent,    # False,
    #     # "use_docker": False,
    #     },
    llm_config={
        'config_list': [
            {
                'model': 'qwen2.5-coder:3b',
                'base_url': 'http://localhost:11434/v1',
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.4,
        'cache_seed': 12,
    },
)

security_agent_02 = AssistantAgent(
    name='security_agent_02',
    description='You are a helpful AI Security Assistant Assisting with Writing Security Tests for the Project',
    # system_message= code_guidelines,
    max_consecutive_auto_reply=4,
    # is_termination_msg= lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,
    # code_execution_config={
    #     'executor': code_executor_agent,    # False,
    #     # "use_docker": False,
    #     },
    llm_config={
        'config_list': [
            {
                'model': 'llama3.2:latest',
                'base_url': 'http://localhost:11434/v1',
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.6,
        'cache_seed': 12,
    },
)

# create an AssistantAgent instance for qa_agents with the LLM configuration.
qa_agent_01 = AssistantAgent(
    name='qa_agent_01',
    description='You are a helpful AI QA Assistant, Assisting with Writing QA Tests for the Project',
    # system_message= code_guidelines,
    max_consecutive_auto_reply=4,
    # is_termination_msg= lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,
    # code_execution_config={
    #     'executor': code_executor_agent,    # False,
    #     # "use_docker": False,
    #     },
    llm_config={
        'config_list': [
            {
                'model': 'qwen2.5-coder:3b',
                'base_url': 'http://localhost:11434/v1',
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.2,
        'cache_seed': 13,
    },
)

qa_agent_02 = AssistantAgent(
    name='qa_agent_02',
    description='You are a helpful AI QA Assistant, Assisting with Writing QA Tests for the Project',
    # system_message= code_guidelines,
    max_consecutive_auto_reply=4,
    # is_termination_msg= lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,
    # code_execution_config={
    #     'executor': code_executor_agent,    # False,
    #     # "use_docker": False,
    #     },
    llm_config={
        'config_list': [
            {
                'model': 'qwen2.5-coder:latest',
                'base_url': 'http://localhost:11434/v1',
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.4,
        'cache_seed': 13,
    },
)

# create an AssistantAgent instance for Technical Writer with the LLM configuration.
technical_writer_agent_01 = AssistantAgent(
    name='technical_writer_agent_01',
    description='You are a helpful AI Technical Writer, Assisting with Writing the Technical Documents for the Project',
    system_message=code_guidelines,
    max_consecutive_auto_reply=4,
    # is_termination_msg= lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    # code_execution_config= False,
    code_execution_config={
        'executor': code_executor_agent,    # False,
        # "use_docker": False,
    },
    llm_config={
        'config_list': [
            {
                'model': 'llama3.2:latest',
                'base_url': 'http://localhost:11434/v1',
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0,
        'cache_seed': 14,
    },
)

# create a UserProxyAgent instance named "user_proxy" with code execution.
user_proxy = UserProxyAgent(
    name='user_proxy',
    description='You are a DevOps Engineer Asking your AI Assistant to Write Code for a Project',
    system_message='agent_input',
    # max_consecutive_auto_reply= 2,
    # is_termination_msg= lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,
)

# Initiate Group Chat Each with initiate_chat method.
# chat_results = project_manager.initiate_chats(
#     [
#         {
#             "recipient": devops_agent_01,
#             "message": devops_input,
#             "max_turns": 6,
#             "summary_method": "reflection_with_llm",        # reflection_with_llm, last_msg
#             # "summary_prompt": "Summarize the conversation",
#         },
#         # {
#         #     "recipient": devops_agent_02,
#         #     "message": "review the work and suggest improvements",
#         #     "max_turns": 4,
#         #     "summary_method": "reflection_with_llm",
#         #     "summary_prompt": "Summarize the conversation",
#         # },
#         {
#             "recipient": qa_agent_01,
#             "message": qa_input,
#             "max_turns": 6,
#             "summary_method": "last_msg",
#             "summary_prompt": "Summarize the work you did",
#         },
#         # {
#         #     "recipient": qa_agent_02,
#         #     "message": "review the qa tests and suggest more tests and improvements",
#         #     "max_turns": 4,
#         #     "summary_method": "last_msg",
#         #     "summary_prompt": "Summarize the conversation",
#         # },
#         {
#             "recipient": security_agent_01,
#             "message": security_input,
#             "max_turns": 4,
#             "summary_method": "last_msg",
#             "summary_prompt": "Summarize the work you did",
#         },
#         # {
#         #     "recipient": security_agent_02,
#         #     "message": "review the security and suggest more tests and improvements",
#         #     "max_turns": 4,
#         #     "summary_method": "last_msg",
#         #     "summary_prompt": "Summarize the conversation",
#         # },
#         {
#             "recipient": technical_writer_agent_01,
#             "message": technical_writer_input,
#             "max_turns": 4,
#             "summary_method": "reflection_with_llm",
#             "summary_prompt": "Summarize the project workflow",
#         },
#     ]
# )

group_chat = autogen.GroupChat(
    agents=[
        user_proxy,
        devops_agent_01,
        qa_agent_01,
        security_agent_01,
        technical_writer_agent_01
    ],
    messages=[],
    max_round=12
)

manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config={
        'config_list': [
            {
                'model': 'llama3.2:latest',
                'base_url': 'http://localhost:11434/v1',
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0,
        'cache_seed': 14,
    },
)

user_proxy.initiate_chat(
    manager,
    message=devops_input,
)
