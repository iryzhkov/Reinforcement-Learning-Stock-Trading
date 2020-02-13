"""Simulation class used to run a single session with nice graphs outputs.
"""

from package.simulation.stockData.baseStockDataSource import StockDataSource
from package.simulation.agent.baseAgent import BaseAgent
from package.simulation.stockData.stockDataSourceFactory import getDataSourceFromConfig
from package.simulation.session import Session

import logging
import matplotlib.pyplot as plt
from datetime import datetime


class Simulation:
    def __init__(self, agent: BaseAgent, simulation_config: dict):
        """Initializer for the Simulation class.

        Args:
            stock_data_source (StockDataSource): Stock data source used for this simulation.
            agent (BaseAgent): Agent used for this session.
            simulation_config (dict): Configuration for the session. Example:
        """

        self.stocks = agent.stocks
        self.stock_data_source = getDataSourceFromConfig(agent.data_source_config)
        self.start_date = simulation_config['start_date']
        self.end_date = simulation_config['end_date']
        self.stock_data_source.prepareDataForDates(self.start_date, self.end_date, self.stocks)

        def dateInRange(date):
            return self.start_date <= date <= self.end_date
        self.available_dates = list(filter(dateInRange, self.stock_data_source.getAvailableDates()))
        self.start_date = self.available_dates[agent.input_num_days]

        session_config = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'starting_balance': simulation_config['starting_balance']
        }
        self.session = Session(self.stock_data_source, agent, session_config)

    def runSimulation(self):
        """Initiates and runs a session
        """
        self.session.runSession()

    def drawPerformancePlot(self):
        """Draws performance plots for the session
        """
        num_figures = len(self.stocks) + 1
        fig, axis = plt.subplots(num_figures, sharex='col', gridspec_kw={'hspace': 0.03})

        # Drawing plots with stock data
        for index, stock in enumerate(self.stocks):
            data_to_plot = self.stock_data_source.stock_data[stock].loc[self.start_date:self.end_date]
            axis[index].set_ylabel(stock)
            axis[index].plot(data_to_plot.index, data_to_plot['High'], 'c-')
            axis[index].plot(data_to_plot.index, data_to_plot['Low'], 'r-')
            axis[index].grid(which='both', color='k', linestyle='--')
            axis[index].set_ylim(bottom=min(data_to_plot['Low']) - 5, top=max(data_to_plot['High']) + 5)

        # Adding marks for when stock was bought and sold.
        for date in self.session.action_history.index:
            actions = self.session.action_history.loc[date]
            for index, stock in enumerate(self.stocks):
                action = actions[stock]
                if action < 0:
                    sell_price = self.stock_data_source.getStockDataForDate(date, stock)['Low']
                    axis[index].plot([date, date], [0, sell_price], 'm:o')
                if action > 0:
                    buy_price = self.stock_data_source.getStockDataForDate(date, stock)['High']
                    axis[index].plot([date, date], [0, buy_price], 'b:o')

        # Adding net worth plot
        index = len(self.stocks)
        data_to_plot = self.session.records
        axis[index].plot(data_to_plot.index, data_to_plot['Net Worth'], 'm-')
        axis[index].set_ylabel('Net Worth')
        axis[index].grid(which='both', color='k', linestyle='--')

        plt.show()


if __name__ == '__main__':
    pass
