import data_source_interface.StockDataSource
import real_data_source_util as util

import pandas as pd
import quandl
import json
import os
from datetime import datetime


class RealStockDataSource(StockDataSource):
    def __init__(self):
        pass
    
# Keeps track stock data for each individual company
# Also updates the values in the data file.
class CompanyStockData:
    def __init__(self, stock_symbol):
        this.stock_symbol = stock_symbol;

    def loadDataFromFile(self):
        pass

    # Update the file with the information
    def updateFile(self):
        pass