"""Sinusoid Stock Data Source.
"""

from package.simulation.stockData.baseStockDataSource import StockDataSource

from datetime import datetime, timedelta
import pandas as pd
import math


# Class for generating sinusoid-like data
class SinusoidStockDataSource(StockDataSource):
    def prepareDataForDates(self, start_date, end_date, stocks_config):
        """Generates sinusoid data from stock_config.

        Args:
            start_date (datetime): Date range start for the preparation.
            end_date (datetime): Date range end for the preparation.
            stocks_config (dict): Stock configuration. For example:
                {'STOCK_1': {'anchor_date': datetime(2016, 1, 1), 'magnitude': 20, 'period': 10, 'delta': 10}}
        """
        day_count = (end_date - start_date).days + 1

        for stock in stocks_config:
            d = {}

            for date in (start_date + timedelta(i) for i in range(day_count)):
                phase = (date - stocks_config[stock]['anchor_date']).days * math.pi * 2 / stocks_config[stock]['period']
                value = math.sin(phase) * stocks_config[stock]['magnitude'] + stocks_config[stock]['delta']
                d[date] = [value, value]

            self.stock_data[stock] = pd.DataFrame.from_dict(data=d, orient='index', columns=['High', 'Low'])


if __name__ == "__main__":
    pass
