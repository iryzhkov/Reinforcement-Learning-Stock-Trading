"""Factories for Models.
"""

from package.simulation.agent.model.neuralNetworkModel import NeuralNetworkModel
from package.simulation.agent.model.linearModel import LinearModel


def getNeuralNetworkModel(config: dict):
    """Creates Neural Network Model

    Args:
        config (dict): configuration for the model.

    Returns:
        NeuralNetworkModel
    """
    return NeuralNetworkModel(config)


def getLinearModel(config: dict):
    """Creates Linear Model

    Args:
        config (dict): configuration for the model.

    Returns:
        NeuralNetworkModel
    """
    return LinearModel(config)


def getModelFromConfig(model_config: dict):
    """Creates Model from the config

    Args:
        model_config (dict): A config describing model.

    Returns:
        An agent created based on the config.
    """
    if model_config['model_type'] == 'nn':
        return getNeuralNetworkModel(model_config)
    elif model_config['model_type'] == 'linear':
        return getLinearModel(model_config)


if __name__ == '__main__':
    pass
