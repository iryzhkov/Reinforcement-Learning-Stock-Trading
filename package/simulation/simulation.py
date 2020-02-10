"""Simulation class used to run a single session with nice graphs outputs.
"""

from package.simulation.stockData.baseStockDataSource import StockDataSource
from package.simulation.agent.baseAgent import BaseAgent
from package.simulation.stockData.stockDataSource import getDataSourceFromConfig
from package.simulation.session import Session

import matplotlib.pyplot as plt
from datetime import datetime


class Simulation:
    def __init__(self, stock_data_source: StockDataSource, agent: BaseAgent, session_config: dict):
        """Initializer for the Simulation class.

        Args:
            stock_data_source (StockDataSource): Stock data source used for this simulation.
            agent (BaseAgent): Agent used for this session.
            session_config (dict): Configuration for the session. Example:
        """
        self.session = Session(stock_data_source, agent, session_config)
        self.stock_data_source = stock_data_source
        self.stocks = session_config['stocks']
        self.start_date = session_config['start_date']
        self.end_date = session_config['end_date']

    def runSimulation(self):
        """Initiates and runs a session
        """
        self.session.runSession()

    def drawPerformancePlot(self):
        """Draws performance plots for the session
        """
        num_figures = len(self.stocks) + 1
        fig, axis = plt.subplots(num_figures, sharex='col')
        fig.suptitle("Simulation Performance")
        for index, stock in enumerate(stocks):
            data_to_plot = self.stock_data_source.stock_data[stock].loc[self.start_date:self.end_date]
            axis[index].set_ylabel(stock)
            axis[index].plot(data_to_plot.index, data_to_plot['High'], color='green')
            axis[index].plot(data_to_plot.index, data_to_plot['Low'], color='red')

        for date in self.session.action_history.index:
            actions = self.session.action_history.loc[date]
            for index, stock in enumerate(self.stocks):
                action = actions[stock]
                if action < 0:
                    sell_price = self.stock_data_source.getStockDataForDate(date, stock)['Low']
                    axis[index].plot([date, date], [0, sell_price], 'r--')
                if action > 0:
                    buy_price = self.stock_data_source.getStockDataForDate(date, stock)['High']
                    axis[index].plot([date, date], [0, buy_price], 'g--')

        index = len(self.stocks)
        data_to_plot = self.session.records
        axis[index].plot(data_to_plot.index, data_to_plot['Net Worth'])
        axis[index].set_ylabel('Net Worth')

        plt.show()


if __name__ == '__main__':
    prepare_start_date = datetime(2014, 1, 1)
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2015, 3, 1)

    stocks = ['STOCK_1', 'STOCK_2']
    config_1 = {'period': 10, 'anchor_date': datetime(2015, 1, 1), 'delta': 100, 'magnitude': 40}
    config_2 = {'period': 10, 'anchor_date': datetime(2015, 1, 15), 'delta': 100, 'magnitude': 40}
    stocks_config = {stocks[0]: config_1, stocks[1]: config_2}

    data_source_config = {'source_type': 'sinusoid'}
    data_source = getDataSourceFromConfig(data_source_config)
    data_source.prepareDataForDates(prepare_start_date, end_date, stocks_config)

    agent = BaseAgent(data_source_config, 0, stocks)

    session_config = {'start_date': start_date,
                      'end_date': end_date,
                      'starting_balance': 1000,
                      'stocks': stocks}

    simulation = Simulation(data_source, agent, session_config)
    simulation.runSimulation()
    simulation.drawPerformancePlot()

