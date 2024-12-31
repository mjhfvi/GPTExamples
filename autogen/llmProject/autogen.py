from __future__ import annotations

import json
import os
from typing import Any

import autogen.runtime_logging
from autogen import AssistantAgent
from autogen import Cache
from autogen import ConversableAgent
from autogen import GroupChat
from autogen import GroupChatManager
from autogen import UserProxyAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.coding import CodeBlock
from autogen.coding import DockerCommandLineCodeExecutor
from autogen.coding import LocalCommandLineCodeExecutor


# LLM Models
llm_mini = 'qwen2.5-coder:1.5b'
llm_small = 'codegemma:2b'
llm_mid = 'qwen2.5-coder:3b'
llm_high = 'llama3.2:3b'

# filename
work_dir = 'documents'

# Ollama Server URL
OLLAMA_SERVER = 'http://172.22.54.208:11434/v1'


# read file Guidelines for the bot
Project_Guidelines_Technical_Writer_Team = open(
    'Project_Guidelines_Technical_Writer_Team.txt', 'r').read()
Project_Guidelines_Security_Team = open(
    'Project_Guidelines_Security_Team.txt', 'r').read()
Project_Guidelines_Coding_Team = open(
    'Project_Guidelines_Coding_Team.txt', 'r').read()
Project_Guidelines_Devops_Team = open(
    'Project_Guidelines_Devops_Team.txt', 'r').read()
Project_Guidelines_QA_Team = open('Project_Guidelines_QA_Team.txt', 'r').read()

# read file System_Message for the bot
System_Message_Project_Manager = open(
    'System_Message_Project_Manager.txt', 'r').read()
System_Message_Devops = open('System_Message_Devops.txt', 'r').read()
System_Message_Devops_Senior = open(
    'System_Message_Devops_Senior.txt', 'r').read()
System_Message_QA = open('System_Message_QA.txt', 'r').read()
System_Message_QA_Senior = open('System_Message_QA_Senior.txt', 'r').read()
System_Message_Security = open('System_Message_Security.txt', 'r').read()
System_Message_Security_Senior = open(
    'System_Message_Security_Senior.txt', 'r').read()
System_Message_Technical_Writer = open(
    'System_Message_Technical_Writer.txt', 'r').read()

# read file Description for the bot
Description_UserProxyAgent = open('Description_UserProxyAgent.txt', 'r').read()
Description_Project_Manager = open(
    'Description_Project_Manager.txt', 'r').read()
Description_Devops = open('Description_Devops.txt', 'r').read()
Description_Devops_Senior = open('Description_Devops_Senior.txt', 'r').read()
Description_QA = open('Description_QA.txt', 'r').read()
Description_QA_Senior = open('Description_QA_Senior.txt', 'r').read()
Description_Security = open('Description_Security.txt', 'r').read()
Description_Security_Senior = open(
    'Description_Security_Senior.txt', 'r').read()
Description_Technical_Writer = open(
    'Description_Technical_Writer.txt', 'r').read()

# create a code executor instance named "code_executor_agent" with code execution.
code_executor_agent = LocalCommandLineCodeExecutor(
    timeout=320,
    work_dir=work_dir
    # virtual_env_context= None,
    # functions: List[Union[FunctionWithRequirements[Any, A], Callable[..., Any], FunctionWithRequirementsStr]] = [],
    # functions_module= "functions",
    # execution_policies= False,
)

# create a code executor instance named "code_executor_agent_docker" with code execution on docker.
# code_executor_agent_docker = DockerCommandLineCodeExecutor(
#     timeout=320,
#     # work_dir= work_dir,
#     image='python:3-slim',
#     # container_name= Optional[str] = None,
#     # bind_dir = None,
#     auto_remove=True,
#     stop_container=True,
#     # execution_policies= Optional[Dict[str, bool]] = None,
# )

config_list = [{'model': llm_high,
                'base_url': OLLAMA_SERVER,
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0], }]
assert len(config_list) > 0
print('models to use: ', [config_list[i]['model']
      for i in range(len(config_list))])

# create a UserProxyAgent instance named "user_proxy" with code execution.
user_proxy = UserProxyAgent(
    name='user_proxy',
    description=Description_UserProxyAgent,
    system_message=Project_Guidelines_Coding_Team,
    max_consecutive_auto_reply=4,
    is_termination_msg=lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    # code_execution_config= False,
    # code_execution_config={
    #     "name": "user_proxy",
    #     # "executor": code_executor_agent,
    # },
    code_execution_config={'executor': code_executor_agent},
    llm_config={
        'config_list': [
            {
                'model': llm_high,
                'base_url': OLLAMA_SERVER,
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.2,
        'cache_seed': 11,
    },
)

# create an AssistantAgent instance for devops_agents with the LLM configuration.
project_manager = ConversableAgent(
    name='project_manager',
    description=Description_Project_Manager,
    system_message=System_Message_Project_Manager,
    max_consecutive_auto_reply=2,
    # is_termination_msg= lambda msg: 'done' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,
    # code_execution_config={
    #     'executor': code_executor_agent,    # False,
    #     # "use_docker": False,
    #     },
    llm_config={
        'config_list': [
            {
                'model': llm_high,
                'base_url': OLLAMA_SERVER,
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0,
        'cache_seed': 11,
    },
)

devops_agent = AssistantAgent(
    name='devops_agent',
    description=Description_Devops,
    system_message=System_Message_Devops,
    max_consecutive_auto_reply=2,
    # is_termination_msg= lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    # code_execution_config= False,
    # code_execution_config={
    #     'executor': code_executor_agent,    # False,
    #     },

    code_execution_config={'executor': code_executor_agent},

    llm_config={
        'config_list': [
            {
                'model': llm_small,
                'base_url': OLLAMA_SERVER,
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.3,
        'cache_seed': 12,
    },
)

devops_senior_agent = AssistantAgent(
    name='devops_senior_agent',
    description=Description_Devops_Senior,
    system_message=System_Message_Devops_Senior,
    max_consecutive_auto_reply=2,
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
                'model': llm_mid,
                'base_url': OLLAMA_SERVER,
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.1,
        'cache_seed': 12,
    },
)

# create an AssistantAgent instance for qa_agents with the LLM configuration.
qa_agent = AssistantAgent(
    name='qa_agent',
    description=Description_QA,
    system_message=System_Message_QA,
    max_consecutive_auto_reply=2,
    is_termination_msg=lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,

    # code_execution_config={
    #     "work_dir": work_dir,
    #     "use_docker": False
    #     },

    llm_config={
        'config_list': [
            {
                'model': llm_small,
                'base_url': OLLAMA_SERVER,
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.3,
        'cache_seed': 13,
    },
)

qa_senior_agent = AssistantAgent(
    name='qa_senior_agent',
    description=Description_QA_Senior,
    system_message=System_Message_QA_Senior,
    max_consecutive_auto_reply=2,
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
                'model': llm_mid,
                'base_url': OLLAMA_SERVER,
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.1,
        'cache_seed': 13,
    },
)

# create an AssistantAgent instance for security_agents with the LLM configuration.
security_agent = AssistantAgent(
    name='security_agent',
    description=Description_Security,
    system_message=System_Message_Security,
    max_consecutive_auto_reply=2,
    is_termination_msg=lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,

    # code_execution_config={
    #     "work_dir": work_dir,
    #     "use_docker": False
    #     },

    llm_config={
        'config_list': [
            {
                'model': llm_small,
                'base_url': OLLAMA_SERVER,
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.3,
        'cache_seed': 14,
    },
)

security_senior_agent = AssistantAgent(
    name='security_senior_agent',
    description=Description_Security_Senior,
    system_message=System_Message_Security_Senior,
    max_consecutive_auto_reply=2,
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
                'model': llm_mid,
                'base_url': OLLAMA_SERVER,
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.1,
        'cache_seed': 14,
    },
)

# create an AssistantAgent instance for Technical Writer with the LLM configuration.
technical_writer_agent = AssistantAgent(
    name='technical_writer_agent',
    description=Description_Technical_Writer,
    system_message=System_Message_Technical_Writer,
    max_consecutive_auto_reply=2,
    # is_termination_msg= lambda msg: 'end' in msg['content'].lower(),
    human_input_mode='NEVER',  # ALWAYS, NEVER, TERMINATE
    code_execution_config=False,

    # code_execution_config={
    #     "work_dir": work_dir,
    #     "use_docker": False
    #     },

    llm_config={
        'config_list': [
            {
                'model': llm_mini,
                'base_url': OLLAMA_SERVER,
                'api_key': 'ollama',        # pragma: allowlist secret
                'price': [0, 0],
            }
        ],
        'temperature': 0.1,
        'cache_seed': 15,
    },
)

# 1. create an AssistantAgent instance named "assistant"
assistant = AssistantAgent(
    name='assistant',
    system_message='You are a helpful assistant.',
    llm_config={
        'timeout': 600,
        'cache_seed': 42,
        'config_list': config_list,
    },
)

# 2. create the RetrieveUserProxyAgent instance named "ragproxyagent"
# Refer to https://microsoft.github.io/autogen/docs/reference/agentchat/contrib/retrieve_user_proxy_agent
# and https://microsoft.github.io/autogen/docs/reference/agentchat/contrib/vectordb/couchbase
# for more information on the RetrieveUserProxyAgent and CouchbaseVectorDB
ragproxyagent = RetrieveUserProxyAgent(
    name='ragproxyagent',
    human_input_mode='NEVER',
    max_consecutive_auto_reply=3,
    retrieve_config={
        'task': 'code',
        'docs_path': [
            'https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Examples/Integrate%20-%20Spark.md',
            'https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Research.md',
        ],
        'chunk_token_size': 2000,
        'model': config_list[0]['model'],
        'vector_db': 'couchbase',  # Couchbase Capella VectorDB
        # Couchbase Capella collection name to be utilized/created
        'collection_name': '_default',
        'db_config': {
            # Couchbase Capella connection string os.environ["CB_CONN_STR"] 172.22.54.208
            'connection_string': 'couchbase://localhost',
            # Couchbase Capella username os.environ["CB_USERNAME"]
            'username': 'admin',
            # Couchbase Capella password os.environ["CB_PASSWORD"]
            'password': '',
            'bucket_name': 'beer-sample',  # Couchbase Capella bucket name
            'scope_name': '_default',  # Couchbase Capella scope name
            'index_name': 'vector_index',  # Couchbase Capella index name to be created
        },
        'get_or_create': True,  # set to False if you don't want to reuse an existing collection
        'overwrite': False,  # set to True if you want to overwrite an existing collection, each overwrite will force a index creation and reupload of documents
    },
    code_execution_config=False,  # set to False if you don't want to execute the code
)

# reset the assistant. Always reset the assistant before starting a new conversation.
assistant.reset()

# given a problem, we use the ragproxyagent to generate a prompt to be sent to the assistant as the initial message.
# the assistant receives the message and generates a response. The response will be sent back to the ragproxyagent for processing.
# The conversation continues until the termination condition is met, in RetrieveChat, the termination condition when no human-in-loop is no code block detected.
# With human-in-loop, the conversation will continue until the user says "exit".
code_problem = 'How can I use FLAML to perform a classification task and use spark to do parallel training. Train 30 seconds and force cancel jobs if time limit is reached.'
chat_result = ragproxyagent.initiate_chat(
    assistant, message=ragproxyagent.message_generator, problem=code_problem)

# Start a sequence of two-agent chats, Each element in the list is a dictionary that specifies the arguments for the initiate_chat method.
# user_proxy.initiate_chats(
#     [
#         {
#             'recipient': project_manager,
#             'message': 'define the project to the team',
#             'max_turns': 4,
#             'summary_method': 'reflection_with_llm',        # reflection_with_llm, last_msg
#             'summary_prompt': 'Summarize the conversation',
#         },
#         {
#             'recipient': devops_agent,
#             'message': 'build the code for the project',
#             'max_turns': 4,
#             'summary_method': 'last_msg',                   # reflection_with_llm, last_msg
#             'summary_prompt': 'Summarize the conversation',
#         },
#     ]
# )

# Use Redis as cache
# with Cache.redis(redis_url='redis://172.22.54.208:6379/0') as cache:
#     user_proxy.initiate_chats(
#         [
#             {
#                 'recipient': project_manager,
#                 'message': 'define the project to the team',
#                 'max_turns': 4,
#                 'summary_method': 'reflection_with_llm',        # reflection_with_llm, last_msg
#                 'summary_prompt': 'Summarize the conversation',
#                 'cache': cache,
#             },
#             {
#                 'recipient': devops_agent,
#                 'message': 'build the code for the project',
#                 'max_turns': 4,
#                 'summary_method': 'last_msg',                   # reflection_with_llm, last_msg
#                 'summary_prompt': 'Summarize the conversation',
#                 'cache': cache,
#             },
#             {
#                 'recipient': devops_senior_agent,
#                 'message': 'review the code from the devops team and suggest improvements',
#                 'max_turns': 2,
#                 'summary_method': 'reflection_with_llm',        # reflection_with_llm, last_msg
#                 'summary_prompt': 'Summarize the conversation',
#                 'cache': cache,
#             },
#             {
#                 'recipient': qa_agent,
#                 'message': 'test the code from the devops team',
#                 'max_turns': 4,
#                 'summary_method': 'last_msg',                   # reflection_with_llm, last_msg
#                 'summary_prompt': 'Summarize the conversation',
#                 'cache': cache,
#             },
#             {
#                 'recipient': qa_senior_agent,
#                 'message': 'review the work for the qa team and suggest improvements',
#                 'max_turns': 2,
#                 'summary_method': 'reflection_with_llm',        # reflection_with_llm, last_msg
#                 'summary_prompt': 'Summarize the work you did',
#                 'cache': cache,
#             },
#             {
#                 'recipient': security_agent,
#                 'message': 'build a security check for the code',
#                 'max_turns': 4,
#                 'summary_method': 'last_msg',                   # reflection_with_llm, last_msg
#                 'summary_prompt': 'Summarize the conversation',
#                 'cache': cache,
#             },
#             {
#                 'recipient': security_senior_agent,
#                 'message': 'review the work for the security team and suggest improvements',
#                 'max_turns': 2,
#                 'summary_method': 'reflection_with_llm',        # reflection_with_llm, last_msg
#                 'summary_prompt': 'Summarize the work you did',
#                 'cache': cache,
#             },
#             {
#                 'recipient': technical_writer_agent,
#                 'message': 'summarize the project workflow and write the technical documentation',
#                 'max_turns': 2,
#                 'summary_method': 'last_msg',        # reflection_with_llm, last_msg
#                 'summary_prompt': 'Summarize the project workflow',
#                 'cache': cache,
#             },
#         ]
#     )

# Stop logging
# autogen.runtime_logging.stop()
