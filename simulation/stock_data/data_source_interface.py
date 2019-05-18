# Interface for stock data sources.
class StockDataSource:
    def getStockDataForDate(self, date, symbols):
        raise NotImplementedError();

    def getStockDataForDateRange(self, date_range, symbols):
        raise NotImplementedError();