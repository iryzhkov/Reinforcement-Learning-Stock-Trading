from dataSourceInterface import StockDataSource
import realDataSourceUtil as util

import pandas as pd
import quandl
import json
import os
from datetime import datetime


class RealStockDataSource(StockDataSource):
    def prepareDataForDates(self, start_date, end_date, symbols):
        self._addSymbols(symbols);
        for symbol in self.symbols:
            if symbol in self.stock_data:
                print("Need to optimize by reducing number of downloaded items");
                self.stock_data[symbol] = util.tryRequestStockDataForDates(symbol, start_date, end_date);
            else:
                self.stock_data[symbol] = util.tryRequestStockDataForDates(symbol, start_date, end_date);
        
    def drawPlotsForDates(self, start_date, end_date, symbols):
        pass;

if __name__ == "__main__":
    start_date = datetime(2017, 2, 1)
    end_date = datetime(2017, 2, 7)
    stocks = ['GOOG', 'AMZN']

    real_data_source = RealStockDataSource();
    real_data_source.prepareDataForDates(start_date, end_date, stocks);
    available_dates = real_data_source.getAvailableDates();

    real_data_source.drawPlotsForDates(start_date, end_date, ['GOOG']);
