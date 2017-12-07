"""
This module provides configuration for application.
"""

import yaml
from os import getcwd
from os.path import join


class ApplicationConfig:
    @staticmethod
    def get_config():
        path = join(getcwd(), "app_config.yaml")
        print type(path)
        with open(path, 'r') as file_config:
            cfg = yaml.load(file_config)
            return cfg
