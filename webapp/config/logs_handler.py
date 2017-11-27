"""
This module prints logs.
"""

import logging
from logging import FileHandler, StreamHandler, Formatter
from os import getcwd
from os.path import join, exists


class LogsHandler:
    def __init__(self):
        # Default format
        # 2017-08-08 18:54:19,618 - logHandler - INFO - Hello World!
        formatter = Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        # Handler for console.
        self.console_handler = StreamHandler()
        self.console_handler.setLevel(logging.NOTSET)
        self.console_handler.setFormatter(formatter)

        # Handler to write file.
        # path = join(getcwd(), "static" , "app.logs")
        # self.file_handler = FileHandler(path)
        # self.file_handler.setLevel(logging.NOTSET)
        # self.file_handler.setFormatter(formatter)

    # Get logger.
    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.console_handler)
        # if self.file_handler:
        #     logger.addHandler(self.file_handler)
        return logger
