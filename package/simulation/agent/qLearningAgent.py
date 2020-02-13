""" Reinforcement Learning based Agent (based on Q-Learning).
"""

import package.simulation.agent.baseAgent as BaseAgent
import package.simulation.agent.agentDataUtil as DataUtil
import package.simulation.agent.model.modelFactory as ModelFactory

import logging
import pandas as pd
import random

logger = logging.getLogger('simulation').getChild('agent').getChild('q-learning')


class QLearningAgent(BaseAgent.BaseAgent):
    def __init__(self, agent_config: dict):
        """Initializer for Q Learning Agent.

        Args:
            agent_config (dict): Agent configuration.
        """
        super(QLearningAgent, self).__init__(agent_config)
        self.model_trained = False

        self.model = ModelFactory.getModelFromConfig(agent_config['model_config'])
        self.learning_rate = agent_config['learning_rate']
        self.discount_rate = agent_config['discount_rate']
        logger.info('Q-Learning agent initialized.')

    def pickBestAction(self, state_dict: dict, possible_actions: list):
        """Picks an action based on the learned policy.

        Args:
            state_dict (dict): Dict with state data used to make a decision.
            possible_actions (list of list of int): List of possible actions to make.

        Returns:
            An action from the possible_actions
        """
        if not self.model_trained:
            return random.choice(possible_actions), 0

        state_action_dataframe = DataUtil.generateStateActionInputs(state_dict, possible_actions, self.stocks)

        expected_rewards = self.model.expectedReward(state_action_dataframe)
        maximum_reward = max(expected_rewards)
        best_action_index = expected_rewards.index(maximum_reward)
        if maximum_reward == 0:
            return random.choice(possible_actions), 0
        else:
            return possible_actions[best_action_index], maximum_reward

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

    def expectedModelValue(self, state_dict, action, next_state_dict, next_action, possible_next_actions, reward):
        """Returns value that Agent expects from the model for given State-Action and Next State-Action
        """
        next_state_best_action, next_state_action_q_value = self.pickBestAction(next_state_dict, possible_next_actions)
        current_state_action, current_state_action_q_value = self.pickBestAction(state_dict, [action.values.tolist()])

        new_expected_model_value = current_state_action_q_value + self.learning_rate * (
                reward + self.discount_rate * next_state_action_q_value - current_state_action_q_value)

        return new_expected_model_value


if __name__ == '__main__':
    pass
