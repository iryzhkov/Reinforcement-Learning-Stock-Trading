"""Util for opening configuration files.
"""

import package.util.json as JSON

from os.path import dirname, join, exists

projectRoot = dirname(dirname(dirname(__file__)))
configPath = join(projectRoot, 'config_library')


def _configFilepath(config_name: str):
    """Returns config filepath based on the name.
    """
    return join(configPath, '{}.json'.format(config_name))


def getConfiguration(config_name: str):
    """Returns configuration.

    Args:
        config_name (str): Configuration name

    Returns:
        Dict with the configuration
    """
    config_filepath = _configFilepath(config_name)
    if exists(config_filepath):
        with open(config_filepath) as config_file:
            return JSON.openJson(config_file)
    else:
        raise FileNotFoundError('Configuration {} does not exist.'.format(config_name))


def updateConfiguration(config_name: str, new_config: dict):
    """Updates the configuration.

    Args:
        config_name (str): The name of configuration to update.
        new_config (dict): The configuration dict.
    """
    with open(_configFilepath(config_name), 'w+') as config_file:
        JSON.writeJson(config_file, new_config)
