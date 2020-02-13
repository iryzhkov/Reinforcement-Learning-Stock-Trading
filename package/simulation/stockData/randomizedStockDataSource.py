"""Randomized Stock Data Source
"""

from package.simulation.stockData.baseStockDataSource import StockDataSource

import logging
import pandas as pd
import random

from datetime import datetime


# Class for adding randomization element on top of a regular data source 
class RandomizedStockDataSource(StockDataSource):
    def __init__(self, data_source: StockDataSource, variance=0.05):
        """Initializes Randomized Stock Data Source.

        Args:
            data_source (StockDataSource): data source to randomize.
            variance (float): variance to use for the randomization.
        """
        super(RandomizedStockDataSource, self).__init__()
        self.data_source = data_source
        self.variance = variance

    def prepareDataForDates(self, start_date: datetime, end_date: datetime, stocks):
        """Generates random data from the data source used for the initialization.

        Expects the child data source data to be already prepared.

        Args:
            start_date (datetime): Start of the date range
            end_date (datetime): End of the date range
            stocks (list or dict): list of stocks use.
        """
        for stock in stocks:
            d = {}

            for date in self.data_source.getAvailableDates():
                high_value, low_value = self.data_source.stock_data[stock].loc[date,['High', 'Low']]

                high_value = high_value * (1 + random.uniform(-self.variance, self.variance))
                low_value = low_value * (1 + random.uniform(-self.variance, self.variance))

                d[date] = [max(high_value, low_value), min(high_value, low_value)]

            self.stock_data[stock] = pd.DataFrame.from_dict(data=d, orient='index', columns=['High', 'Low'])


if __name__ == "__main__":
    pass
