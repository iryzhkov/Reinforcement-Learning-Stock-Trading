"""Training class used to run multiple sessions with a single agent.
"""

from package.simulation.agent.baseAgent import BaseAgent
from package.simulation.session import Session
from package.simulation.stockData.randomizedStockDataSource import RandomizedStockDataSource
from package.simulation.stockData.stockDataSourceFactory import getDataSourceFromConfig
from package.util.plotter import Plotter

import logging
import math
import pandas as pd
import random

logger = logging.getLogger('simulation').getChild('training')


class Training:
    def __init__(self, agent: BaseAgent, training_config: dict, plotter=None):
        """Initializes training for the agent.

        Unpacks variables from the training_config.

        Args:
            agent (BaseAgent): The agent that will be trained.
            training_config (dict): Configuration for the training.
            plotter (Plotter): Plotter to use for performance recording
        """
        self.agent = agent
        self.training_name = training_config['training_name']
        self.plotter = plotter
        self.stock_data_source = getDataSourceFromConfig(self.agent.data_source_config)
        self.variance = training_config['variance']

        self.minimum_start_date = training_config['minimum_start_date']
        self.maximum_end_date = training_config['maximum_end_date']
        self.minimum_session_duration = training_config['minimum_session_duration']
        self.maximum_session_duration = training_config['maximum_session_duration']
        self.minimum_start_balance = training_config['minimum_start_balance']
        self.maximum_start_balance = training_config['maximum_start_balance']

        self.batch_size = training_config['batch_size']
        self.epoch_number = training_config['epoch_number']

        self.agent.exploration_parameter = training_config['exploration_parameter']
        self.stocks = agent.stocks

        self.stock_data_source.prepareDataForDates(self.minimum_start_date, self.maximum_end_date, self.stocks)

        def dateInRange(date):
            return self.minimum_start_date <= date <= self.maximum_end_date
        self.available_dates = list(filter(dateInRange, self.stock_data_source.getAvailableDates()))
        logger.info('Finished initializing training.')

    def startTraining(self):
        """Starts training of the agent.
        """
        logger.info('Starting training for the agent.')
        for epoch_iteration in range(self.epoch_number):
            logger.info('Starting training epoch {} out of {}.'.format(epoch_iteration + 1, self.epoch_number))
            sessions_data = {'records': [], 'data_sources': [], 'actions': [], 'stocks_owned': [], 'rewards': []}
            sessions = []
            for batch_iteration in range(self.batch_size):
                logger.info('Starting session {} out of {}.'.format(batch_iteration + 1, self.batch_size))
                session_config, data_source_start_date, data_source_end_date = self._generateSessionConfiguration()
                data_source = RandomizedStockDataSource(self.stock_data_source, variance=self.variance)
                data_source.prepareDataForDates(data_source_start_date, data_source_end_date, self.stocks)
                logger.info('Generated data source for the session')

                session = Session(data_source, self.agent, session_config)
                session.runSession()
                logger.info('Session ended. Saving session results')

                sessions_data['records'].append(session.records)
                sessions_data['data_sources'].append(data_source)
                sessions_data['actions'].append(session.action_history)
                sessions_data['stocks_owned'].append(session.stock_history)
                sessions += [session]

            if self.plotter:
                filename = '{}_epoch_{}'.format(self.training_name, epoch_iteration + 1)
                self.plotter.plotSession(random.choice(sessions), filename)

            logger.info('Training epoch ended. Generating rewards for the sessions.')
            sessions_data['rewards'] = self._generateRewards(sessions_data['records'])
            logger.info('Sending session results for agent training.')
            self.agent.train(sessions_data)

        if self.plotter:
            filename = '{}_epoch_{}'.format(self.training_name, epoch_iteration + 1)
            self.plotter.plotTraining(self, filename)

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
                growth = records.iloc[index]['Net Worth'] - records.iloc[index - 1]['Net Worth']
                growth_rate = growth / records.iloc[0]['Balance'] - 0.01
                reward = 2 / (2 + math.expm1(-growth_rate * 75)) - 1
                rewards.append(reward)
            rewards_list.append(pd.DataFrame(rewards, columns=['Reward'], index=records.index[:-1]))
        return rewards_list

    def _generateSessionConfiguration(self):
        """Generates random session configuration within given parameters.
        """
        session_days_duration = random.randrange(self.minimum_session_duration, min(self.maximum_session_duration, len(self.available_dates) -
                                                 self.agent.input_num_days))
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
    pass
