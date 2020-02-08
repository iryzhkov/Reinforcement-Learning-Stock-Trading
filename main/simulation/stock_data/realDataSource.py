from dataSourceInterface import StockDataSource
import realDataSourceUtil as util

import pandas as pd
import json
import os
from datetime import datetime


class RealStockDataSource(StockDataSource):
    def prepareDataForDates(self, start_date, end_date, stocks_config):
        self._addSymbols(symbols);
        for stock in self.stocks_config:
            if symbol in self.stock_data:
                print("Need to optimize by reducing number of downloaded items");
                self.stock_data[symbol] = util.tryRequestStockDataForDates(stock, start_date, end_date);
            else:
                self.stock_data[symbol] = util.tryRequestStockDataForDates(stock, start_date, end_date);


if __name__ == "__main__":
    start_date = datetime(2016, 1, 1)
    end_date = datetime(2018, 1, 1)
    stocks = ['GOOG', 'AMZN', 'AAPL', 'FB']

    real_data_source = RealStockDataSource();
    real_data_source.prepareDataForDates(start_date, end_date, stocks);
    available_dates = real_data_source.getAvailableDates();

    real_data_source.drawPlotsForDates(start_date, end_date, stocks);
