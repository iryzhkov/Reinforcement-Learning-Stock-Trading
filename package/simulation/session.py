"""Session class used to run a single simulation of agent's actions.
"""

from package.simulation.stockData.baseStockDataSource import StockDataSource
from package.simulation.agent.baseAgent import BaseAgent
from package.simulation.stockData.stockDataSource import getDataSourceFromConfig

import pandas as pd
from datetime import datetime, timedelta


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
        self.stocks = session_config['stocks']
        self.stocks_owned = {}
        for stock in self.stocks:
            self.stocks_owned[stock] = 0

        self.records = None
        day_zero_date = self.start_date - timedelta(days=1)

        self.records_indices = [day_zero_date]
        self.balance_history = [self.balance]
        self.net_worth_history = [self._getNetWorthForDate(day_zero_date)]
        self.action_history = []
        self.stock_history = [[self.stocks_owned[stock] for stock in self.stocks]]

    def runSession(self):
        """Starts the session run.
        """
        def dateInRange(date):
            return self.start_date <= date <= self.end_date
        available_dates = filter(dateInRange, self.stock_data_source.getAvailableDates())

        for date in available_dates:
            possible_actions = self._generatePossibleActions(date)
            agent_input = self._generateAgentInputForDate(date)
            agent_action = self.agent.pickAction(agent_input, possible_actions)
            self._executeAction(date, agent_action)
            self._addRecordsForDate(date, agent_action)

        self.records = pd.DataFrame(list(zip(self.balance_history, self.net_worth_history)),
                                    index=self.records_indices, columns=['Balance', 'Net Worth'])
        self.action_history = pd.DataFrame(self.action_history,
                                           index=self.records_indices[1:], columns=self.stocks)
        self.stock_history = pd.DataFrame(self.stock_history, index=self.records_indices, columns=self.stocks)

    def _generatePossibleActions(self, date: datetime):
        """Generates a list of possible actions for agent for given date.

        Args:
            date (datetime): The date for which to generate list of actions.

        Returns
            A list of possible actions.
        """
        possible_actions = [[0] * len(self.stocks)]

        for index, stock in enumerate(self.stocks):
            if self.stocks_owned[stock] > 0:
                sell_action = [0] * len(self.stocks)
                sell_action[index] = -1
                possible_actions += [sell_action]

            if self.stock_data_source.getStockDataForDate(date, stock)['High'] < self.balance:
                buy_action = [0] * len(self.stocks)
                buy_action[index] = 1
                possible_actions += [buy_action]

        return possible_actions

    def _executeAction(self, date: datetime, agent_action: list):
        """Executes action during the date

        Args:
            date (datetime): Date for which to execute action.
            agent_action (list of int): Action that the agent selected.
        """
        self.action_history += [[0] * len(self.stocks)]
        for index, action in enumerate(agent_action):
            stock = self.stocks[index]
            low_price = self.stock_data_source.getStockDataForDate(date, stock)['Low']
            high_price = self.stock_data_source.getStockDataForDate(date, stock)['High']

            if action == -1:
                self.action_history[-1][index] = -self.stocks_owned[stock]
                self.balance += self.stocks_owned[stock] * low_price
                self.stocks_owned[stock] = 0

            elif action == 1:
                num_stocks_purchased = self.balance // high_price
                self.action_history[-1][index] = num_stocks_purchased
                self.stocks_owned[stock] += num_stocks_purchased
                self.balance -= num_stocks_purchased * high_price

    def _generateAgentInputForDate(self, date):
        """Generates input to use for the agent.

        Args:
            date (datetime): The date for which to generate the input.

        Returns:
            A dict with data used for agent input.
        """
        return {}

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

    def getPerformance(self):
        pass


if __name__ == '__main__':
    prepare_start_date = datetime(2014, 1, 1)
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2016, 1, 7)

    stocks = ['STOCK_1', 'STOCK_2']
    config_1 = {'period': 60, 'anchor_date': datetime(2015, 1, 1), 'delta': 100, 'magnitude': 20}
    config_2 = {'period': 60, 'anchor_date': datetime(2015, 1, 15), 'delta': 100, 'magnitude': 20}
    stocks_config = {stocks[0]: config_1, stocks[1]: config_2}

    data_source_config = {'source_type': 'sinusoid'}
    data_source = getDataSourceFromConfig(data_source_config)
    data_source.prepareDataForDates(prepare_start_date, end_date, stocks_config)

    agent = BaseAgent(data_source_config, 0, stocks)

    session_config = {'start_date': start_date,
                      'end_date': end_date,
                      'starting_balance': 1000,
                      'stocks': stocks}

    session = Session(data_source, agent, session_config)
    session.runSession()
