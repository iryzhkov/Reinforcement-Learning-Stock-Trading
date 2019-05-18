import data_source

import pandas as pd
import quandl
import json
import os
from datetime import datetime



class RealStockDataSource(data_source.StockDataSource):
    def __init__(self):
        pass
    
# Keeps track stock data for each individual company
# Also updates the values in the data file.
class CompanyStockData:
    def __init__(self, stock_symbol, stock_data_manager):
        this.stock_symbol = stock_symbol;
        this.stock_data_manageer = stock_data_manager;

    def loadDataFromFile(self):
        pass

    # Update the file with the information
    def updateFile(self):
        pass
