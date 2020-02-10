"""Base Agent Class.
"""

import random


def pickRandomAction(possible_actions):
    """Picks a random action from the list of possible_actions.

    Args:
        possible_actions (list of list of int): List of possible actions to make.

    Returns:
        An action from the possible_actions
    """
    return random.choice(possible_actions)


class BaseAgent:
    def __init__(self, data_source_config: dict, input_num_days: int, stocks: list):
        """Initializer for Base Agent.

        Args:
            data_source_config (dict): config that was used to create data source used for this agent.
            input_num_days (int): number of days of stock data that the agent looks into.
            stocks (list of str): stocks that the agent can buy/sell
        """
        self.data_source_config = data_source_config
        self.input_num_days = input_num_days
        self.stocks = stocks

    @staticmethod
    def pickAction(input_data: dict, possible_actions: list):
        """Picks an action from the list of possible_actions.

        Args:
            input_data (dict): The data used to make a decision on the action choice.
            possible_actions (list of list of int): List of possible actions to make.

        Returns:
            An action from the possible_actions
        """
        return pickRandomAction(possible_actions)
