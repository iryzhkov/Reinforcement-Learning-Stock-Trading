from package.simulation.stockData.baseStockDataSource import StockDataSource

import unittest
from datetime import datetime


class StockDataSourceTest(unittest.TestCase):
    def setUp(self):
        self.stocks = ['STOCK_1', 'STOCK_2']
        self.data_source = StockDataSource()

    def testGetStockDataForDate(self):
        pass

    def testGetStockDataForNDaysBefore(self):
        pass

    def testGetAvailableDates(self):
        pass


if __name__ == '__main__':
    unittest.main()
