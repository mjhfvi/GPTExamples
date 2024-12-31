# from dotenv import load_dotenv
# from dotenv import dotenv_values
# import os
# from datetime import datetime
# start_time = datetime.now()
# print(5*"#" + " Starting " + 5*"#")
# Define a variable called version
# config = dotenv_values(".env")
# print(config)
# config = dotenv_values()
# print(config)
from __future__ import annotations
VERSION = '0.1'

# VERSION = os.getenv("VERSION")
# print(VERSION)

# Print a welcome message
print(f"LLM Langchain Project: v{VERSION}\n")
