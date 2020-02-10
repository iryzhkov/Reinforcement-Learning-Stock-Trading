from package.simulation.stockData.dataSourceInterface import StockDataSource

import unittest
from datetime import datetime


class StockDataSourceTest(unittest.TestCase):
    def setUp(self):
        stocks = ['STOCK_1', 'STOCK_2']
        config_1 = {'period': 20, 'anchor_date': datetime(2015, 1, 1), 'delta': 100, 'magnitude': 50}
        config_2 = {'period': 20, 'anchor_date': datetime(2015, 1, 10), 'delta': 100, 'magnitude': 50}
        configs = {stocks[0]: config_1, stocks[1]: config_2}

        start_date = datetime(2016, 1, 1)
        end_date = datetime(2016, 1, 30)

        self.data_source = StockDataSource()

    def testGetStockDataForDate(self):
        pass

    def testGetStockDataForNDaysBefore(self):
        pass

    def testGetAvailableDates(self):
        pass


if __name__ == '__main__':
    unittest.main()
