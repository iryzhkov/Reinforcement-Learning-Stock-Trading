import pandas as pd
import quandl
import json
import os
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'
QUANDL_MAX_REQUESTS_PER_DAY = 50

STORED_DATA_DIRECTORY = 'data'
STORED_DATA_INFO_FILE = 'data_info'

def getFilePath(file_name, file_format):
    return os.path.join(STORED_DATA_DIRECTORY, 
                        file_name + '.' + file_format);

# Global object that keeps track of 
class StockDataManager:
    def __init__(self):
        data_file = open(getFilePath(STORED_DATA_INFO_FILE, 'json'), 'r');
        self.data = json.load(data_file);

    def checkRequestCountAndDate(self):
        # Start counter from zero if the last request was not today
        today_date_str = datetime.now().strftime(DATE_FORMAT);
        if self.data['quandl_latest_request_date'] != today_date_str:
            self.data['quandl_latest_request_date'] = today_date_str;
            self.data['quandl_requests_today'] = 0;

    def updateFile(self):
        self.checkRequestCountAndDate()
        data_file = open(getFilePath(STORED_DATA_INFO_FILE, 'json'), 'w');
        json.dump(self.data, data_file, indent=2); 

    def hasStockDownloadedFor(self, stock_symbol):
        return stock_symbol in self.data['stored_stocks']

    def getStockDataInformation(self, stock_symbol):
        if self.hasStockDownloadedFor(stock_symbol):
            return self.data['stored_stocks'][stock_symbol];
        else:
            return None;

    def updateStockDataInformation(self, stock_symbol, new_information):
        self.data['stored_stocks'][stock_symbol] = new_information;
        self.updateFile();

    def canPerformRequest(self):
        self.checkRequestCountAndDate()
        return self.data['quandl_requests_today'] <= QUANDL_MAX_REQUESTS_PER_DAY 

    def tryRequestStockDataFor(self, stock_symbol, start_date, end_date):
        if not self.canPerformRequest():
            return None;

        self.checkRequestCountAndDate();
        self.data['quandl_requests_today'] += 1;
        self.updateFile();

        result = quandl.get('WIKI/' + stock_symbol, 
                            start_date=start_date, 
                            end_date=end_date);
        return result;

stock_data_manager = StockDataManager();
start_date = datetime(2016,1,1)
end_date = datetime(2017,1,1)
apple_data = stock_data_manager.tryRequestStockDataFor("AAPL", start_date, end_date) 
print(type(apple_data))
print(apple_data.head())