from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

from autogen import ConversableAgent
from autogen.coding import CodeBlock
from autogen.coding import LocalCommandLineCodeExecutor

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

config_list = [
    {'model': 'llama3.2-vision', 'base_url': 'http://localhost:11434/v1', 'api_key': 'ollama',      # pragma: allowlist secret
        'price': [0, 0], 'tags': ['llama3.2-vision', 'local']},                  # pragma: allowlist secret
    {'model': 'qwen2.5-coder:3b', 'base_url': 'http://localhost:11434/v1', 'api_key': 'ollama',     # pragma: allowlist secret
        'price': [0, 0], 'tags': ['qwen2.5-coder:3b', 'local']},      # pragma: allowlist secret
    {'model': 'llama3.2', 'base_url': 'http://localhost:11434/v1', 'api_key': 'ollama',     # pragma: allowlist secret
        'price': [0, 0], 'tags': ['ollama', 'local']},                  # pragma: allowlist secret
    {'model': 'qwen2.5-coder', 'base_url': 'http://localhost:11434/v1', 'api_key': 'ollama',        # pragma: allowlist secret
        'price': [0, 0], 'tags': ['qwen2.5-coder', 'local']},      # pragma: allowlist secret

]


class GuidelinesManager:
    """Handles loading and processing of guidelines from markdown files."""

    def __init__(self):
        self.guidelines: Dict[str, str] = {}

    def load_guidelines(self, filename: str) -> Optional[str]:
        """Load guidelines from a markdown file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                # Store guidelines by section
                sections = content.split('#')[1:]  # Split by headers
                for section in sections:
                    if section.strip():
                        lines = section.strip().split('\n')
                        title = lines[0].strip()
                        content = '\n'.join(lines[1:]).strip()
                        self.guidelines[title] = content
                return content
        except FileNotFoundError:
            logger.error(f"Guidelines file not found: {filename}")
            return None
        except Exception as e:
            logger.error(f"Error reading guidelines file {filename}: {e}")
            return None

    def get_section(self, section_name: str) -> Optional[str]:
        """Get specific section from guidelines."""
        return self.guidelines.get(section_name)

    def get_all_sections(self) -> List[str]:
        """Get list of all available sections."""
        return list(self.guidelines.keys())


def load_input_file(filename: str) -> Optional[str]:
    """Load user input from a file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Input file not found: {filename}")
        return None
    except Exception as e:
        logger.error(f"Error reading input file {filename}: {e}")
        return None


def create_executor() -> LocalCommandLineCodeExecutor:
    """Create and configure the command line executor."""
    return LocalCommandLineCodeExecutor(
        timeout=240,
        work_dir='./work'
    )


def create_assistant(executor: LocalCommandLineCodeExecutor, guidelines: str) -> ConversableAgent:
    """Create and configure the conversable agent with guidelines."""
    system_message = f"""You are a code executor responsible for implementing code with following specific guidelines. Here are your guidelines:
    {guidelines}
    Follow these guidelines strictly when generating code and configurations."""

    return ConversableAgent(
        name='assistantAgent',
        system_message=system_message,
        llm_config={
            'config_list': config_list,
            'temperature': 0.6,
            # 'max_tokens': 4096,
            # 'cache_seed': None,
        },
        code_execution_config={'executor': executor},
        # max_consecutive_auto_reply=2,
        # timeout=480,
        human_input_mode='NEVER',
    )


def main():
    """Main function to run the build application."""
    try:
        # Initialize guidelines manager
        guidelines_mgr = GuidelinesManager()

        # Load guidelines and input
        guidelines = guidelines_mgr.load_guidelines('agent_guidelines_code.md')
        build_input = load_input_file('agent_input.txt')

        if not all([guidelines, build_input]):
            logger.error('Failed to load required files')
            return

        # Log available guideline sections
        sections = guidelines_mgr.get_all_sections()
        logger.info(f"Loaded guideline sections: {sections}")

        # Create executor and assistant
        executor = create_executor()
        assistant = create_assistant(executor, guidelines)

        # Process the message
        logger.info('Starting message processing')
        reply = assistant.generate_reply(
            messages=[{
                'role': 'user',
                'content': f"Using the provided guidelines, please help with: {build_input}"
            }]
        )
        logger.info('Message processing completed')
        print(reply)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == '__main__':
    main()
