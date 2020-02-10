from stockTrading.simulation.stockData.dataSourceInterface import StockDataSource

from datetime import datetime, timedelta
import pandas as pd
import math


# Class for generating sinusoid-like data
class SinusoidStockDataSource(StockDataSource):
    def prepareDataForDates(self, start_date, end_date, stocks_config):
        self._addStocks(stocks_config.keys())
        day_count = (end_date - start_date).days + 1

        for stock in stocks_config:
            d = {}

            for date in (start_date + timedelta(i) for i in range(day_count)):
                phase = (date - stocks_config[stock]['anchor_date']).days * math.pi * 2 / stocks_config[stock]['period']
                value = math.sin(phase) * stocks_config[stock]['magnitude'] + stocks_config[stock]['delta']
                d[date] = [value, value]

            self.stock_data[stock] = pd.DataFrame.from_dict(data=d, orient='index', columns=['High', 'Low'])


if __name__ == "__main__":
    stocks = ['STOCK_1', 'STOCK_2']
    config_1 = {'period': 60, 'anchor_date': datetime(2015, 1, 1), 'delta': 100, 'magnitude': 20}
    config_2 = {'period': 60, 'anchor_date': datetime(2015, 1, 15), 'delta': 100, 'magnitude': 20}
    configs = {stocks[0]: config_1, stocks[1]: config_2}

    start_date = datetime(2016, 1, 1)
    end_date = datetime(2017, 1, 1)

    data_source = SinusoidStockDataSource()
    data_source.prepareDataForDates(start_date, end_date, configs)
    data_source.drawPlotsForDates(start_date, end_date, stocks)
