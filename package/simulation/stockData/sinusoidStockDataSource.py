"""Sinusoid Stock Data Source.
"""

from package.simulation.stockData.baseStockDataSource import StockDataSource

import logging
import pandas as pd
import math

from datetime import datetime, timedelta


# Class for generating sinusoid-like data
class SinusoidStockDataSource(StockDataSource):
    def __init__(self, stocks_config: dict):
        """Initializer for Sinusoid Stock Data Source

        Args:
            stocks_config (dict): Configuration for the stocks
        """
        super(SinusoidStockDataSource, self).__init__();
        self.stocks_config = stocks_config

    def prepareDataForDates(self, start_date, end_date, stocks):
        """Generates sinusoid data from stock_config.

        Args:
            start_date (datetime): Date range start for the preparation.
            end_date (datetime): Date range end for the preparation.
            stocks (list): List of stocks

        Raises:

        """
        day_count = (end_date - start_date).days + 1

        for stock in stocks:
            d = {}

            for date in (start_date + timedelta(i) for i in range(day_count)):
                phase = (date - self.stocks_config[stock]['anchor_date']).days * \
                        math.pi * 2 / self.stocks_config[stock]['period']
                value = math.sin(phase) * self.stocks_config[stock]['magnitude'] + self.stocks_config[stock]['delta']
                d[date] = [value, value]

            self.stock_data[stock] = pd.DataFrame.from_dict(data=d, orient='index', columns=['High', 'Low'])


if __name__ == "__main__":
    pass
