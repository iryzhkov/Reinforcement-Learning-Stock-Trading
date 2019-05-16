# Interface for stock data sources.
class StockDataSource:
  def getStockDataForDate(symbols, date):
    pass

  def getStockDataForDateRange(symbols, date_range):
    pass
