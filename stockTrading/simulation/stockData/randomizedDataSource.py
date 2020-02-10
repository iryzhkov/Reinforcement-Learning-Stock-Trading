from stockTrading.simulation.stockData.dataSourceInterface import StockDataSource
from stockTrading.simulation.stockData.sinusoidDataSource import SinusoidStockDataSource

from datetime import datetime
import pandas as pd
import random


# Class for adding randomization element on top of a regular data source 
class RandomizedStockDataSource(StockDataSource):
    def __init__(self, data_source, variance=0.05):
        super(RandomizedStockDataSource, self).__init__()
        self.data_source = data_source
        self.variance = variance

    def prepareDataForDates(self, start_date, end_date, stocks):
        self.data_source.prepareDataForDates(start_date, end_date, stocks)
        day_count = (end_date - start_date).days + 1

        for stock in stocks:
            d = {}

            for date in self.data_source.getAvailableDates():
                high_value, low_value = self.data_source.stock_data[stock].loc[date,['High', 'Low']]

                high_value = high_value * (1 + random.uniform(-self.variance, self.variance))
                low_value = low_value * (1 + random.uniform(-self.variance, self.variance))

                d[date] = [max(high_value, low_value), min(high_value, low_value)]

            self.stock_data[stock] = pd.DataFrame.from_dict(data=d, orient='index', columns=['High', 'Low'])


if __name__ == "__main__":
    stocks = ['STOCK_1', 'STOCK_2']
    config_1 = {'period': 60, 'anchor_date': datetime(2015, 1, 1), 'delta': 100, 'magnitude': 20}
    config_2 = {'period': 60, 'anchor_date': datetime(2015, 1, 15), 'delta': 100, 'magnitude': 20}
    stocks_config = {stocks[0]: config_1, stocks[1]: config_2}

    start_date = datetime(2016, 1, 1)
    end_date = datetime(2016, 6, 1)

    data_source = RandomizedStockDataSource(SinusoidStockDataSource())

    data_source.prepareDataForDates(start_date, end_date, stocks_config)
    data_source.drawPlotsForDates(start_date, end_date, stocks_config)
