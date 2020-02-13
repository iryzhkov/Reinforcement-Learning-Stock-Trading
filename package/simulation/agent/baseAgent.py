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
    def __init__(self, agent_config: dict):
        """Initializer for Base Agent.

        Args:
            agent_config (dict): Agent configuration
        """
        self.exploration_parameter = 0

        self.data_source_config = agent_config['data_source_config']
        self.input_num_days = agent_config['input_num_days']
        self.stocks = self.data_source_config['stocks']

    def pickAction(self, state_dict: dict, possible_actions: list):
        """Picks an action based on the agent policy.

        Args:
            state_dict (dict): Dict with state data used to make a decision.
            possible_actions (list of list of int): List of possible actions to make.

        Returns:
            An action from the possible_actions that agent selected to execute
        """
        if random.random() <= self.exploration_parameter:
            return pickRandomAction(possible_actions)
        else:
            best_action, expected_reward = self.pickBestAction(state_dict, possible_actions)
            return best_action

    def pickBestAction(self, state_dict: dict, possible_actions: list):
        """Picks random.

        Args:
            state_dict (dict): Dict with state data used to make a decision.
            possible_actions (list of list of int): List of possible actions to make.

        Returns:
            An action and expected score for this action
        """
        return random.choice(possible_actions), 0
