"""Session class used to run a single simulation of agent's actions.
"""

import package.simulation.agent.agentDataUtil as AgentDataUtil

from package.simulation.agent.baseAgent import BaseAgent
from package.simulation.stockData.baseStockDataSource import StockDataSource

import logging
import pandas as pd
from datetime import datetime, timedelta

logger = logging.getLogger('simulation').getChild('session')


class Session:
    def __init__(self, stock_data_source: StockDataSource, agent: BaseAgent, session_config: dict):
        """Initializer for the Session class.

        Args:
            stock_data_source (StockDataSource): Stock data source used for this session.
            agent (BaseAgent): Agent used for this session.
            session_config (dict): Configuration for this session. Example:
        """
        self.stock_data_source = stock_data_source
        self.agent = agent

        self.start_date = session_config['start_date']
        self.end_date = session_config['end_date']

        self.balance = session_config['starting_balance']
        self.stocks = self.agent.stocks
        self.stocks_owned = {}
        for stock in self.stocks:
            self.stocks_owned[stock] = 0

        self.records = None
        day_zero_date = self.start_date - timedelta(days=1)

        self.records_indices = [day_zero_date]
        self.balance_history = [self.balance]
        self.net_worth_history = []
        self.action_history = []
        self.stock_history = [[self.stocks_owned[stock] for stock in self.stocks]]

        self.performance = {}
        logger.info('The session is initialized.')

    def runSession(self):
        """Starts the session run.
        """
        def dateInRange(date):
            return self.start_date <= date <= self.end_date
        available_dates = list(filter(dateInRange, self.stock_data_source.getAvailableDates()))
        self.net_worth_history = [self._getNetWorthForDate(available_dates[0])]

        logger.info('Starting session with duration {}.'.format(len(available_dates)))
        for date in available_dates:
            possible_actions = AgentDataUtil.generatePossibleActions(self.stock_data_source, self.stocks,
                                                                     date, self.balance, self.stocks_owned)
            state_data = AgentDataUtil.generateStateInputForAgent(self.stock_data_source, self.agent,
                                                                  date, self.balance, self.stocks_owned)
            agent_action = self.agent.pickAction(state_data, possible_actions)
            self._addRecordsForDate(date, agent_action)
            self._executeAction(date, agent_action)

        self.records = pd.DataFrame(list(zip(self.balance_history, self.net_worth_history)),
                                    index=self.records_indices, columns=['Balance', 'Net Worth'])
        self.action_history = pd.DataFrame(self.action_history,
                                           index=self.records_indices[1:], columns=self.stocks)
        self.stock_history = pd.DataFrame(self.stock_history, index=self.records_indices, columns=self.stocks)
        self._recordPerformance()
        logger.info('Session ended with average daily growth: {}, average daily transactions: {}'.format(
            self.performance['average_daily_growth_rate'], self.performance['average_daily_transactions']))

    def _executeAction(self, date: datetime, agent_action: list):
        """Executes action during the date

        Args:
            date (datetime): Date for which to execute action.
            agent_action (list of int): Action that the agent selected.
        """
        for index, action in enumerate(agent_action):
            stock = self.stocks[index]
            low_price = self.stock_data_source.getStockDataForDate(date, stock)['Low']
            high_price = self.stock_data_source.getStockDataForDate(date, stock)['High']

            if action == -1:
                self.balance += self.stocks_owned[stock] * low_price
                self.stocks_owned[stock] = 0

            elif action == 1:
                num_stocks_purchased = self.balance // high_price
                self.stocks_owned[stock] += num_stocks_purchased
                self.balance -= num_stocks_purchased * high_price

    def _addRecordsForDate(self, date: datetime, action_taken: list):
        """Adds records of the date to the session records.

        Args:
            date (datetime): date for which to record data.
            action_taken (list of int): action taken by the agent during that date.
        """
        self.records_indices.append(date)
        self.balance_history.append(self.balance)
        self.net_worth_history.append(self._getNetWorthForDate(date))
        self.stock_history += [[self.stocks_owned[stock] for stock in self.stocks]]
        self.action_history += [action_taken]

    def _getNetWorthForDate(self, date: datetime):
        """Calculates Net Worth for the given date.

        Args:
            date (datetime): The date for which to calculate net worth.

        Returns:
            A float representing net worth.
        """
        result = self.balance

        for stock in self.stocks:
            result += self.stocks_owned[stock] * self.stock_data_source.getStockDataForDate(date, stock)['Low']

        return result

    def _recordPerformance(self):
        """Calculates and records the overall session performance.
        """
        self.performance = {
            'average_daily_growth_rate': 0,
            'average_daily_transactions': 0,
        }


if __name__ == '__main__':
    pass
