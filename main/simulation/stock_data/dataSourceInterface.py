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
            return pd.to_datetime(self.stock_data[symbol].index);

    def prepareDataForDates(self, start_date, end_date, symbols):
        raise NotImplementedError();

    def drawPlotsForDates(self, start_date, end_date, symbols):
        fig, axis = plt.subplots(len(symbols), sharex=True);
        fig.suptitle("Stock Prices");
        for index, symbol in enumerate(symbols):
            plottable_data = self.stock_data[symbol].loc[start_date:end_date];
            axis[index].set_title(symbol);
            axis[index].plot(plottable_data.index, plottable_data['High'], color='green');
            axis[index].plot(plottable_data.index, plottable_data['Low'], color='red');
        plt.show();

    def _addSymbols(self, symbols):
        symbols = set(symbols);
        self.symbols = self.symbols.union(symbols);
