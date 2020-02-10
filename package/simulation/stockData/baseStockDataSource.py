"""Base class for stock data sources. Implements basic getters.
"""

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


class StockDataSource:
    def __init__(self):
        """Initializer for DataSource. Sets up dict for stock_data and set for stocks.
        """
        self.stock_data = {}

    def getStockDataForDate(self, date: datetime, stock: list):
        """Returns stock data at provided date for provided stock.

        Args:
            date (datetime): The date, for which to get the stock data.
            stock (str): Stock, for which to get the stock data.

        Returns:
            A dict with prices for stock at that specific date. For example:
            {'High': 1001, 'Low': 1000}
        """
        return self.stock_data[stock].loc[date]

    def getStockDataForNDaysBefore(self, date: datetime, number_of_days: int, stocks: list):
        """Returns stock data for number_of_days prior to the given date for provided stocks.

        Args:
            date (datetime): The end date (result does not have data for this date).
            number_of_days (int): Number of days, for which to get the stock data.
            stocks (list of str): List of stock names, for which to get the stock data.

        Returns:
            A dict mapping stock names to their prices at that specific date range. For example:
            {'STOCK_123': [{'High': 1001, 'Low': 1000}, {'High': 1002, 'Low': 1001}]}

        Raises:
            LookUpError: Days requested are outside of the prepared data.
        """
        result = {}
        for stock in stocks:
            end_date_index = self.stock_data[stock].index.get_loc(date)
            start_date_index = end_date_index - number_of_days
            if start_date_index < 0:
                raise LookupError('Trying to access data outside of the prepared dates.')
            result[stock] = self.stock_data[stock].iloc[start_date_index:end_date_index]
        return result

    def getAvailableDates(self):
        """Returns available dates for this DataSource

        Returns:
            List of datetime dates, that are available for querying.
        """
        for stock in self.stock_data:
            return pd.to_datetime(self.stock_data[stock].index)

    def prepareDataForDates(self, start_date: datetime, end_date: datetime, stocks_config: list):
        """Loads/Generates stock data for given date range.

        This is the main function that must be implemented by each new stock data source.

        Args:
            start_date (datetime): Date range start.
            end_date (datetime): Date range end.
            stocks_config (dict/list): List of stocks to get the data for.

        Raises:
            NotImplementedError: base class does not support this method.
        """
        raise NotImplementedError()

    def drawPlotsForDates(self, start_date: datetime, end_date: datetime, stocks: list):
        """Draws plots for the stock data generated in the given date range.

        Uses matplotlib to plot relevant stock data.

        Args:
            start_date (datetime): Date range start.
            end_date (datetime): Date range end.
            stocks (list of str): Which stocks plot
        """
        fig, axis = plt.subplots(len(stocks), sharex='col')
        fig.suptitle("Stock Prices")
        for index, stock in enumerate(stocks):
            data_to_plot = self.stock_data[stock].loc[start_date:end_date]
            axis[index].set_title(stock)
            axis[index].plot(data_to_plot.index, data_to_plot['High'], color='green')
            axis[index].plot(data_to_plot.index, data_to_plot['Low'], color='red')
        plt.show()
