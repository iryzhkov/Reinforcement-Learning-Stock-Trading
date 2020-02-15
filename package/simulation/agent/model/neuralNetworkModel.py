"""Linear Model for Q learning.
"""

from package.simulation.agent.model.baseModel import BaseModel

from sklearn import neural_network


class NeuralNetworkModel(BaseModel):
    def __init__(self, config):
        """Initializer for the models.

        Args:
            config (dict): Model config
        """
        super(NeuralNetworkModel, self).__init__(config)
        self.hidden_layer_sizes = tuple(config['nn_configuration'])
        self.learning_rate = config['learning_rate'] if 'learning_rate' in config else 'constant'
        self.model = neural_network.MLPRegressor(hidden_layer_sizes=self.hidden_layer_sizes, batch_size=self.batch_size,
                                                 learning_rate=self.learning_rate)


if __name__ == '__main__':
    pass
