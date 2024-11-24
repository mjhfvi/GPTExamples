from __future__ import annotations

import logging
import os
from typing import Optional

from autogen import config_list_from_json
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# LLM Configuration
config_list = [{
    'model': 'llama3.2',
    'base_url': 'http://192.168.50.50:11434/v1',
    'api_key': 'ollama',        # pragma: allowlist secret
    'price': [0, 0],
}]


def load_message_file(filename: str) -> Optional[str]:
    """Load message content from a file with error handling."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Message file not found: {filename}")
        return None
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        return None


def create_executor() -> LocalCommandLineCodeExecutor:
    """Create and configure the command line executor."""
    return LocalCommandLineCodeExecutor(
        timeout=60,
    )


def create_assistant(executor: LocalCommandLineCodeExecutor, system_message: str) -> ConversableAgent:
    """Create and configure the conversable agent."""
    return ConversableAgent(
        name='assistantAgent',
        system_message=system_message,
        llm_config={
            'config_list': config_list,
            'temperature': 0.6,
            # "request_timeout": 280,
        },
        code_execution_config={'executor': executor},
        human_input_mode='NEVER'
    )


def main():
    """Main function to run the build application."""
    try:
        # Load message files
        build_input = load_message_file('agent_input.txt')
        assistant_message = load_message_file('agent_guidelines_code.md')

        if not all([assistant_message, build_input]):
            logger.error('Failed to load required message files')
            return

        # Create executor and assistant
        executor = create_executor()
        assistant = create_assistant(executor, assistant_message)

        # Process the message
        # logger.info("Starting message processing")
        reply = assistant.generate_reply(
            messages=[{'role': 'user', 'content': build_input}]
        )
        # logger.info("Message processing completed")
        print(reply)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise  # Adding raise to see the full error stack


if __name__ == '__main__':
    main()
