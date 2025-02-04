from __future__ import annotations

import os
import sys

from loguru import logger
from prettyformatter import pprint
from rich import inspect
from rich import print_json
from src import config_vars
from src import documents_loader
from src.config_vars import Error_Handler


@logger.catch
def main():
    logger.info('running main function.')
    load_documents_string = documents_loader.DocumentsLoaders()
    load_documents_string.build_dataset()


@logger.catch
@Error_Handler
def build_invoice_bezeqint():
    logger.info('running build_invoice_bezeqint function.')
    load_documents_string = documents_loader.DocumentsLoaders()
    load_documents_string.build_dataset()


if __name__ == '__main__':
    # main()
    # inspect(build_invoice_bezeqint(), all=True)
    build_invoice_bezeqint()
