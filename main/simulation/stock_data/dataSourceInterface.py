from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Base Class for StockDataSource type classes 
class StockDataSource:
    def __init__(self):
        self.stock_data = {};
        self.symbols = set();

    def getStockDataForDate(self, date, symbols):
        result = {}
        for symbol in symbols:
            result[symbol] = self.stock_data[symbol].loc[date];
        return result

    def getStockDataForNDaysBefore(self, date, number_of_days, symbols):
        result = {}
        for symbol in symbols:
            end_date_index = self.stock_data[symbol].index.get_loc(date); 
            start_date_index = end_date_index - number_of_days; 
            result[symbol] = self.stock_data[symbol].iloc[start_date_index:end_date_index];
        return result

    def getAvailableDates(self):
        for symbol in self.symbols:
            return [t.date() for t in self.stock_data[symbol].index];

    def prepareDataForDates(self, start_date, end_date, symbols):
        raise NotImplementedError();

    def drawPlotsForDates(self, start_date, end_date, symbols):
        for symbol in symbols:
            plottable_data = self.stock_data[symbol].loc[start_date:end_date];
            plottable_data.plot(y=['High', 'Low']);


    def _addSymbols(self, symbols):
        symbols = set(symbols);
        self.symbols = self.symbols.union(symbols);
