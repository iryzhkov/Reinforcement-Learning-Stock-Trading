"""Linear Model for Q learning.
"""

from package.simulation.agent.model.baseModel import BaseModel

import pandas as pd
import logging

from sklearn import neural_network


class NeuralNetworkModel(BaseModel):
    def __init__(self, config):
        """Initializer for the models.

        Args:
            config (dict): Model config
        """
        super(NeuralNetworkModel, self).__init__(config)
        self.hidden_layer_sizes = tuple(config['nn_configuration'])
        self.model = neural_network.MLPRegressor(hidden_layer_sizes=self.hidden_layer_sizes)

    def initializeModel(self, model_config=None):
        """Initializes model.

        Args:
            model_config
        """


if __name__ == '__main__':
    pass
