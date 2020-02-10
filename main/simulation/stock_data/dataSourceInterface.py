import pandas as pd
import matplotlib.pyplot as plt

# Base Class for StockDataSource type classes 
class StockDataSource:
    def __init__(self):
        self.stock_data = {}
        self.stocks = set()

    def getStockDataForDate(self, date, stocks):
        result = {}
        for stock in stocks:
            result[stock] = self.stock_data[stock].loc[date]
        return result

    def getStockDataForNDaysBefore(self, date, number_of_days, stocks):
        result = {}
        for stock in stocks:
            end_date_index = self.stock_data[stock].index.get_loc(date)
            start_date_index = end_date_index - number_of_days
            result[stock] = self.stock_data[stock].iloc[start_date_index:end_date_index]
        return result

    def getAvailableDates(self):
        for stock in self.stocks:
            return pd.to_datetime(self.stock_data[stock].index)

    def prepareDataForDates(self, start_date, end_date, stocks_config):
        raise NotImplementedError()

    def drawPlotsForDates(self, start_date, end_date, stocks):
        fig, axis = plt.subplots(len(stocks), sharex=True)
        fig.suptitle("Stock Prices")
        for index, stock in enumerate(stocks):
            plottable_data = self.stock_data[stock].loc[start_date:end_date]
            axis[index].set_title(stock)
            axis[index].plot(plottable_data.index, plottable_data['High'], color='green')
            axis[index].plot(plottable_data.index, plottable_data['Low'], color='red')
        plt.show()

    def _addStocks(self, stocks):
        stocks = set(stocks)
        self.stocks = self.stocks.union(stocks)
