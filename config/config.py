"""
Config wrapper for the application
"""

import yaml

APP_CONFIG = {}


def read_config():
    """Read config file config.yml and return a dictionary"""
    global APP_CONFIG
    APP_CONFIG = read_config_inner()


def save_config():
    """Save config file config.yml"""
    with open("config.yml", "w") as file:
        yaml.dump(APP_CONFIG, file)


def read_config_inner() -> dict:
    """Read config file config.yml and return a dictionary"""
    with open("config.yml", "r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)
