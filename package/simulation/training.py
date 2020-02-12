"""Training class used to run multiple sessions with a single agent.
"""

from package.simulation.agent.qLearningAgent import QLearningAgent
from package.simulation.session import Session
from package.simulation.stockData.randomizedStockDataSource import RandomizedStockDataSource
from package.simulation.stockData.stockDataSourceFactory import getDataSourceFromConfig

import logging
import pandas as pd
import random

from datetime import datetime

logger = logging.getLogger('training')
dateFmt = '%d %b %Y'

class Training:
    def __init__(self, stock_data_source, agent, start_date, end_date, stocks):
        self.agent = agent
        self.stock_data_source = stock_data_source
        self.minimum_start_date = start_date
        self.maximum_end_date = end_date
        self.stocks = stocks

        self.stock_data_source.prepareDataForDates(self.minimum_start_date, self.maximum_end_date, self.stocks)

        def dateInRange(date):
            return self.minimum_start_date <= date <= self.maximum_end_date

        self.available_dates = list(filter(dateInRange, self.stock_data_source.getAvailableDates()))

        self.minimum_session_duration = 20
        self.exploration_parameter = 0
        self.batch_size = 2
        self.epoch_number = 2

        self.minimum_start_balance = 500
        self.maximum_start_balance = 2000

        self.agent.exploration_parameter = 1

    def startTraining(self):
        """Starts training of the agent.
        """
        for epoch_iteration in range(self.epoch_number):
            sessions_data = {'records': [], 'data_sources': [], 'actions': [], 'stocks_owned': [], 'rewards': []}
            for batch_iteration in range(self.batch_size):
                session_config, data_source_start_date, data_source_end_date = self._generateSessionConfiguration()
                data_source = RandomizedStockDataSource(self.stock_data_source, variance=0.025)
                data_source.prepareDataForDates(data_source_start_date, data_source_end_date, self.stocks)

                session = Session(data_source, self.agent, session_config)
                session.runSession()

                sessions_data['records'].append(session.records)
                sessions_data['data_sources'].append(data_source)
                sessions_data['actions'].append(session.action_history)
                sessions_data['stocks_owned'].append(session.stock_history)

            sessions_data['rewards'] = self._generateRewards(sessions_data['records'])
            self.agent.train(sessions_data)

    @staticmethod
    def _generateRewards(records_list: list):
        """Generates rewards based on the agent performance

        Args:
            records_list (list of pd.DataFrame): list of sessions' records

        Returns:
            List of pd.DataFrame containing rewards
        """
        rewards_list = []
        for records in records_list:
            rewards = []
            for index in range(1, len(records)):
                reward = records.iloc[index]['Net Worth'] / records.iloc[index - 1]['Net Worth'] - 1
                rewards.append(reward)
            rewards_list.append(pd.DataFrame(rewards, columns=['Reward'], index=records.index[1:]))
        return rewards_list

    def _generateSessionConfiguration(self):
        """Generates random session configuration within given parameters.
        """
        session_days_duration = random.randrange(self.minimum_session_duration, len(self.available_dates) -
                                                 self.agent.input_num_days)
        start_date_index = random.randrange(self.agent.input_num_days, len(self.available_dates) -
                                            session_days_duration)
        end_date_index = start_date_index + session_days_duration

        session_start_date = self.available_dates[start_date_index]
        session_end_date = self.available_dates[end_date_index]
        data_source_start_date = self.available_dates[start_date_index - self.agent.input_num_days]
        data_source_end_date = session_end_date

        session_config = {
            'start_date': session_start_date,
            'end_date': session_end_date,
            'starting_balance': random.randrange(self.minimum_start_balance, self.maximum_start_balance),
            'stocks': self.stocks
        }

        return session_config, data_source_start_date, data_source_end_date


if __name__ == '__main__':
    prepare_start_date = datetime(2014, 1, 1)
    start_date = datetime(2016, 1, 1)
    end_date = datetime(2016, 4, 1)

    stocks = ['GOOG']
    data_source_config = {'source_type': 'real'}
    test_data_source = getDataSourceFromConfig(data_source_config)

    print("Preparing data source ...")
    test_data_source.prepareDataForDates(prepare_start_date, end_date, stocks)
    print("Done!")

    agent = QLearningAgent(data_source_config, 2, stocks)
    training = Training(test_data_source, agent, start_date, end_date, stocks)

    print("Running training ...")
    training.startTraining()
