"""Simulation class used to run a single session with nice graphs outputs.
"""

from package.simulation.stockData.baseStockDataSource import StockDataSource
from package.simulation.agent.baseAgent import BaseAgent
from package.simulation.stockData.stockDataSourceFactory import getDataSourceFromConfig
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
        num_figures = len(self.stocks) + 2
        fig, axis = plt.subplots(num_figures, sharex='col', gridspec_kw={'hspace': 0.03})

        # Drawing plots with stock data
        for index, stock in enumerate(stocks):
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

        # Adding Day2Day Growth plot
        index += 1
        data_to_plot = self.session.records
        axis[index].plot(data_to_plot.index, data_to_plot['Day to Day Growth'], 'b-')
        axis[index].set_ylabel('Day to Day Growth')
        axis[index].axhline(y=0, alpha=0.3, linestyle='--', color='k')
        axis[index].axhline(y=min(data_to_plot['Day to Day Growth']), linestyle='--', color='m')
        axis[index].grid(which='both', color='k', linestyle='--')

        plt.show()


if __name__ == '__main__':
    prepare_start_date = datetime(2014, 1, 1)
    start_date = datetime(2016, 1, 1)
    end_date = datetime(2017, 1, 1)

    stocks = ['GOOG', 'AMZN']
    data_source_config = {'source_type': 'randomized',
                          'child_source': {'source_type': 'real'},
                          'variance': 0.025}
    data_source = getDataSourceFromConfig(data_source_config)

    print("Preparing data source ...")
    data_source.prepareDataForDates(prepare_start_date, end_date, stocks)
    print("Done!")

    agent = BaseAgent(data_source_config, 0, stocks)

    session_config = {'start_date': start_date,
                      'end_date': end_date,
                      'starting_balance': 10000,
                      'stocks': stocks}

    simulation = Simulation(data_source, agent, session_config)

    print("Running simulation ...")
    simulation.runSimulation()
    print("Done! Plotting results ...")
    simulation.drawPerformancePlot()

