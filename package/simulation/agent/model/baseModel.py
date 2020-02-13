"""Base class for the q-learning models.
"""

import pandas as pd


class BaseModel:
    def __init__(self, config: dict):
        """Initializer for the models.

        Args:
            config (dict): Model config
        """
        self.model = None
        self.trained = False
        self.num_epochs = config['epoch_number']
        self.batch_size = config['batch_size']

    def expectedReward(self, state_action_dataframe: pd.DataFrame):
        """Returns expected outcome based on the model.

        Returns the modeled action-state expected value.

        Args:
            state_action_dataframe (dp.DataFrame): A state_action dataframe containing all state-action values.

        Returns:
            A float, representing expected reward for the action in the state.
        """
        if self.model is None or not self.trained:
            return [0] * len(state_action_dataframe)
        else:
            return list(self.model.predict(state_action_dataframe))

    def train(self, state_action_dataframe, expected_values_dataframe):
        """Integrates the feedback into the model.

        Args:
            state_action_dataframe (pd.DataFrame): dataframe with state-action values to train on
            expected_values_dataframe (pd.DataFrame): dataframe with expected reward values for the state-action values
        """
        if self.model is not None:
            for i in range(self.num_epochs):
                self.model.partial_fit(state_action_dataframe, expected_values_dataframe)
            self.trained = True
