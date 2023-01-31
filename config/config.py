"""
Config package for the application
"""

import yaml


def read_config() -> dict:
    """Read config file config.yml and return a dictionary"""
    with open("config.yml", "r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)
