""" Reinforcement Learning based Agent (based on Q-Learning).
"""

import package.simulation.agent.baseAgent as BaseAgent
import package.simulation.agent.agentDataUtil as DataUtil
from package.simulation.agent.model.linearModel import LinearModel

import pandas as pd
import random


class QLearningAgent(BaseAgent.BaseAgent):
    def __init__(self, data_source_config: dict, input_num_days: int, stocks: list):
        """Initializer for Q Learning Agent.

        Args:
            data_source_config (dict): config that was used to create data source used for this agent.
            input_num_days (int): number of days of stock data that the agent looks into.
            stocks (list of str): stocks that the agent can buy/sell
        """
        super(QLearningAgent, self).__init__(data_source_config, input_num_days, stocks)

        self.model_initialized = False
        self.model = LinearModel()
        self.learning_rate = 0.1
        self.discount_rate = 0.9
        self.exploration_parameter = 0.01

    def initializeModel(self, sample_model_input: pd.DataFrame):
        """Initializes model with the provided sample output.
        """
        self.model.initializeModel(sample_model_input)
        self.model_initialized = True

    def pickAction(self, state_dict: dict, possible_actions: list):
        """Picks an action based on the agent policy.

        Args:
            state_dict (dict): Dict with state data used to make a decision.
            possible_actions (list of list of int): List of possible actions to make.

        Returns:
            An action from the possible_actions that agent selected to execute
        """
        if random.random() <= self.exploration_parameter:
            return BaseAgent.pickRandomAction(possible_actions)
        else:
            return self.pickBestAction(state_dict, possible_actions)

    def pickBestAction(self, state_dict: dict, possible_actions: list):
        """Picks an action based on the learned policy.

        Args:
            state_dict (dict): Dict with state data used to make a decision.
            possible_actions (list of list of int): List of possible actions to make.

        Returns:
            An action from the possible_actions
        """
        state_action_dataframe = DataUtil.generateStateActionInputs(state_dict, possible_actions, self.stocks)
        if not self.model_initialized:
            self.initializeModel(state_action_dataframe)

        expected_rewards = [output['predictions'][0] for output in self.model.expectedReward(state_action_dataframe)]
        best_action_index = expected_rewards.index(max(expected_rewards))
        if max(expected_rewards) == 0:
            return random.choice(possible_actions)
        else:
            return possible_actions[best_action_index]

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

        training_data_list = []
        for i in range(len(rewards_list)):
            training_data = DataUtil.generateTrainingDataFromSession(data_sources[i], stocks_owned[i], actions_list[i],
                                                                     rewards_list[i], records_list[i], self)
            training_data_list.append(training_data)

        state_action_values = pd.concat(training_data_list)
        expected_values_data_frame = state_action_values.pop('Expected Value')
        self.model.train(state_action_values, expected_values_data_frame)

    def expectedModelValue(self, state_dict, action, next_state_dict, next_action, possible_next_actions, reward):
        """Returns value that Agent expects from the model for given State-Action and Next State-Action
        """
        current_sate_action_data_frame = DataUtil.generateStateActionInputs(state_dict, [action.values.tolist()],
                                                                            self.stocks)
        next_state_action_data_frame = DataUtil.generateStateActionInputs(next_state_dict,
                                                                          [self.pickBestAction(next_state_dict,
                                                                                               possible_next_actions)],
                                                                          self.stocks)
        current_model_values = [output['predictions'][0] for output in self.model.expectedReward(
            pd.concat([current_sate_action_data_frame, next_state_action_data_frame]))]
        current_state_action_q_value, next_state_action_q_value = current_model_values

        new_expected_model_value = current_state_action_q_value + self.learning_rate * (
                reward + self.discount_rate * next_state_action_q_value - current_state_action_q_value)

        return new_expected_model_value


if __name__ == '__main__':
    pass
