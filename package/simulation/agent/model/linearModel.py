"""Linear Model for Q learning.
"""

from package.simulation.agent.model.baseModel import BaseModel
import package.simulation.agent.model.modelDataUtil as DataUtil

import tensorflow as tf
import pandas as pd
import logging

tf.get_logger().setLevel(logging.CRITICAL)


class LinearModel(BaseModel):
    def __init__(self):
        self.model = None
        self.learning_rate = 0.1
        self.discount_rate = 0
        self.bach_size = 100
        self.num_epochs = 1

    def initializeModel(self, sample_input: pd.DataFrame):
        """Initializes model.

        Args:
            sample_input (pd.DataFrame): Sample of input data.
        """
        feature_columns = [tf.feature_column.numeric_column(column, dtype=tf.float64) for column in
                           sample_input.columns]
        head = tf.estimator.RegressionHead()
        self.model = tf.estimator.LinearEstimator(head, feature_columns=feature_columns)

    def expectedReward(self, state_action_dataframe: pd.DataFrame):
        """Returns expected outcome based on the model.

        Returns the modeled action-state expected value.

        Args:
            state_action_dataframe (dp.DataFrame): A state_action dataframe containing all state-action values.

        Returns:
            A float, representing expected reward for the action in the state.
        """
        return self.model.predict(DataUtil.generateInputFunction(state_action_dataframe))

    def train(self, state_action_dataframe, expected_values_dataframe):
        """Integrates the feedback into the model.

        Args:
            state_action_dataframe (pd.DataFrame): dataframe with state-action values to train on
            expected_values_dataframe (pd.DataFrame): dataframe with expected reward values for the state-action values
        """
        self.model.train(DataUtil.generateInputFunction(state_action_dataframe, expected_values_dataframe))


if __name__ == '__main__':
    pass
