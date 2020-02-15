"""Base Agent Class.
"""

import package.simulation.agent.agentDataUtil as DataUtil
import package.simulation.agent.model.modelFactory as ModelFactory

import logging
import pandas as pd
import random

logger = logging.getLogger('simulation').getChild('agent').getChild('base')


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
        self.model = ModelFactory.getModelFromConfig(agent_config['model_config'])
        self.model_trained = False

    def train(self, sessions_data: dict):
        """Train model based on the sessions_data

        sessions_data (dict): Data gathered during training sessions. Includes data sources, stock ownership history,
            balance history, rewards history, action history.
        """
        data_sources = sessions_data['data_sources']
        stocks_owned = sessions_data['stocks_owned']
        actions_list = sessions_data['actions']
        records_list = sessions_data['records']
        rewards_list = sessions_data['rewards']

        logger.info('Transforming sessions data into training data')
        training_data_list = []
        for i in range(len(rewards_list)):
            training_data = DataUtil.generateTrainingDataFromSession(data_sources[i], stocks_owned[i], actions_list[i],
                                                                     rewards_list[i], records_list[i], self)
            training_data_list.append(training_data)

        state_action_values = pd.concat(training_data_list)
        expected_values_data_frame = state_action_values.pop('Expected Value')
        logger.info('Training data ({} rows) is ready'.format(len(state_action_values)))

        logger.info('Starting model training.')
        self.model.train(state_action_values, expected_values_data_frame)
        self.model_trained = True
        logger.info('Model training finished.')

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
        """Picks random action from the possible actions list.

        Args:
            state_dict (dict): Dict with state data used to make a decision.
            possible_actions (list of list of int): List of possible actions to make.

        Returns:
            An action and expected score for this action
        """
        return random.choice(possible_actions), 0
