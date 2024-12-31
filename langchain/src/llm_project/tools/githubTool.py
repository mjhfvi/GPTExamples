# Source: https://python.langchain.com/docs/integrations/tools/github/
# GITHUB_APP_ID="" - A six digit number found in your app's general settings
# GITHUB_APP_PRIVATE_KEY="" - The location of your app's private key .pem file, or the full text of that file as a string.
# GITHUB_REPOSITORY="" - The name of the Github repository you want your bot to act upon. Must follow the format {username}/{repo-name}. Make sure the app has been added to this repository first!
# Optional: GITHUB_BRANCH- The branch where the bot will make its commits. Defaults to repo.default_branch.
# Optional: GITHUB_BASE_BRANCH- The base branch of your repo upon which PRs will based from. Defaults to repo.default_branch.
from __future__ import annotations

import getpass
import os

from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper

for env_var in [
    'GITHUB_APP_ID',
    'GITHUB_APP_PRIVATE_KEY',
    'GITHUB_REPOSITORY',
]:
    if not os.getenv(env_var):
        os.environ[env_var] = getpass.getpass()

github = GitHubAPIWrapper()
toolkit = GitHubToolkit.from_github_api_wrapper(github)

tools = toolkit.get_tools()

for tool in tools:
    print(tool.name)
