# Source: https://microsoft.github.io/autogen/0.2/docs/topics/llm-caching/
from __future__ import annotations

from autogen import Cache

# Use Redis as cache
with Cache.redis(redis_url='redis://localhost:6379/0') as cache:
    user.initiate_chat(assistant, message=coding_task, cache=cache)

# Use DiskCache as cache
with Cache.disk() as cache:
    user.initiate_chat(assistant, message=coding_task, cache=cache)
