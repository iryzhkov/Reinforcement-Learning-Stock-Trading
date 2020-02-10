"""Base class for stock data sources. Implements basic getters.
"""

from package.simulation.stockData.baseStockDataSource import StockDataSource
import package.simulation.stockData.realStockDataSourceUtil as Util

import pandas as pd
from datetime import datetime


class RealStockDataSource(StockDataSource):
    def __init__(self):
        """Initializer for Real Stock Data Source.

        Tries to retrieve offline stock data.
        """
        super(RealStockDataSource, self).__init__()
        self.manifest = Util.getOfflineStockDataManifest()

    def prepareDataForDates(self, start_date: datetime, end_date: datetime, stocks: list):
        """Stock data preparation for Real Stock Data Source.

        Checks if the data can be retrieved from offline storage.
        Only downloads missing data, if some already present.

        Args:
            start_date (datetime): The start date for the date range.
            end_date (datetime): The end date for the date range.
            stocks (list of str): List of stocks for which to download data.
        """
        for stock in stocks:
            if stock not in self.manifest:
                # Case when the stock is completely new
                self.stock_data[stock] = Util.tryRequestStockDataForDates(start_date, end_date, stock)
                self.manifest[stock] = {'first_available_date': start_date, 'last_available_date': end_date}

                Util.updateOfflineStockDataManifest(self.manifest)
                Util.updateOfflineStockDataFor(self.stock_data[stock], stock)
            else:
                if stock not in self.stock_data:
                    # If stock data is stored offline but has not been loaded yet, load it
                    self.stock_data[stock] = Util.getOfflineStockDataFor(stock)

                # Check if we need to download any additional data for this preparation.
                have_updated = False

                if start_date < self.manifest[stock]['first_available_date']:
                    temp = Util.tryRequestStockDataForDates(start_date,
                                                            self.manifest[stock]['first_available_date'],
                                                            stock)
                    self.stock_data[stock] = pd.concat([temp, self.stock_data[stock]])
                    self.manifest[stock]['first_available_date'] = start_date
                    have_updated = True

                if end_date > self.manifest[stock]['last_available_date']:
                    temp = Util.tryRequestStockDataForDates(self.manifest[stock]['last_available_date'],
                                                            end_date,
                                                            stock)
                    self.stock_data[stock] = pd.concat([self.stock_data[stock], temp])
                    self.manifest[stock]['last_available_date'] = end_date
                    have_updated = True

                if have_updated:
                    Util.updateOfflineStockDataManifest(self.manifest)
                    Util.updateOfflineStockDataFor(self.stock_data[stock], stock)

                self.stock_data[stock] = Util.tryRequestStockDataForDates(start_date, end_date, stock)


if __name__ == "__main__":
    start = datetime(2015, 12, 1)
    end = datetime(2016, 3, 1)
    stocks = ['GOOG', 'AMZN']

    data_source = RealStockDataSource()
    data_source.prepareDataForDates(start, end, stocks)
    print(data_source.stock_data['GOOG'])
