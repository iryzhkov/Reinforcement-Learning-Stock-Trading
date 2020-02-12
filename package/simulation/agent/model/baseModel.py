"""Base class for the q-learning models.
"""


class BaseModel:
    def __init__(self):
        pass

    def expectedReward(self, state, action):
        """Returns expected outcome based on the model.

        Returns the modeled action-state expected value.

        Args:
            state (list of float): a list of numbers, representing current state.
            action (list of int): a list of integers, representing possible action.

        Returns:
            A float, representing expected reward for the action.
        """
        raise NotImplementedError("BaseModel class does not support any operations with model.")

    def train(self, state, action, reward, next_state, next_optimal_action):
        """Integrates the feedback into the model.

        Args:
            state (list of float): the state, during which, the action was taken.
            action (list of int): the action that was taken.
            reward (float): the reward for the action.
            next_state (list of float): the result state of the action
            next_optimal_action (list of int): the optimal action at the next_state
        """
        raise NotImplementedError("BaseModel class does not support any operations with model.")
