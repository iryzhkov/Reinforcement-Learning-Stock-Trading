""" Reinforcement Learning based Agent (based on Q-Learning).
"""

import package.simulation.agent.baseAgent as BaseAgent
import package.simulation.agent.agentDataUtil as DataUtil

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

    def expectedModelValues(self, state_action_values, actions, rewards, data_source):
        """Returns value that Agent expects from the model for given State-Action and Next State-Action
        """
        current_model_values = self.model.expectedReward(state_action_values)

        next_state_action_q_value = current_model_values[-1]

        expected_model_values = {}
        for index, date in enumerate(reversed(state_action_values.index[:-1])):
            current_state_action_q_value = current_model_values[index]
            # TODO(igor.o.ryzhkov@gmail.com): change next state if the action was random
            expected_model_values[date] = current_state_action_q_value + self.learning_rate * (
                    rewards.loc[date] + self.discount_rate * next_state_action_q_value - current_state_action_q_value)
            next_state_action_q_value = expected_model_values[date]

        expected_model_values = pd.DataFrame.from_dict(expected_model_values, orient='index')
        expected_model_values = expected_model_values.rename(columns={'Reward': 'Expected Value'})
        return expected_model_values

if __name__ == '__main__':
    pass
