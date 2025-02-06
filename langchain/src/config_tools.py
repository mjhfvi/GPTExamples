from __future__ import annotations

import datetime
import getpass
import os
import sys

from loguru import logger
from prettyformatter import pprint
from rich import inspect


def Error_Handler(func):
    def Get_Function_Error(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            logger.exception(
                f'An error occurred while running function: {func.__name__}, please check the logs for more information')
            # pprint("get code", func.__code__)
            # pprint("get globals", func.__globals__)
            # inspect(func.__code__, all=True)   # for more information set all=True
            # pprint("for more debug information, in config_vars.py add to inspect all=True")
        except KeyboardInterrupt:
            logger.error('program terminated by user.')
    return Get_Function_Error


if __name__ == '__main__':
    print('this is not the main script, exiting ...')
    sys.exit()
