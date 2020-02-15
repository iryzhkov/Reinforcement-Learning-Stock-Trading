"""Linear Model for Q learning.
"""

from package.simulation.agent.model.baseModel import BaseModel

from sklearn import linear_model


class LinearModel(BaseModel):
    def __init__(self, config):
        """Initializer for the models.

        Args:
            config (dict): Model config
        """
        super(LinearModel, self).__init__(config)
        self.model = linear_model.SGDRegressor()


if __name__ == '__main__':
    pass
