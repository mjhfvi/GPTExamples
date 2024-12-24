# Source: https://python.langchain.com/docs/integrations/tools/ddg/
from __future__ import annotations

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
search_result = search.invoke("Obama's first name?")

# search = DuckDuckGoSearchResults()
# search_result = search.invoke("Obama")

print(search_result)
