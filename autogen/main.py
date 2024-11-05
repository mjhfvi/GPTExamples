import asyncio
from autogen_ext.code_executor.docker_executor import DockerCommandLineCodeExecutor
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_agentchat.agents import CodeExecutorAgent, CodingAssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.task import TextMentionTermination

async def main() -> None:
    async with DockerCommandLineCodeExecutor(work_dir="coding") as code_executor:
        code_executor_agent = CodeExecutorAgent("code_executor", code_executor=code_executor)
        coding_assistant_agent = CodingAssistantAgent(
            "coding_assistant", model_client=OpenAIChatCompletionClient(model="gpt-4o", api_key="YOUR_API_KEY")
        )
        termination = TextMentionTermination("TERMINATE")
        group_chat = RoundRobinGroupChat([coding_assistant_agent, code_executor_agent], termination_condition=termination)
        stream = group_chat.run_stream(
            "Create a plot of NVDIA and TSLA stock returns YTD from 2024-01-01 and save it to 'nvidia_tesla_2024_ytd.png'."
        )
        async for message in stream:
            print(message)

asyncio.run(main())