import quandl
import json
import os
from datetime import datetime

quandl.ApiConfig.api_key = '5wzrzhdhdqLsG2r6uC_3'

DATE_FORMAT = '%Y-%m-%d'
QUANDL_MAX_REQUESTS_PER_DAY = 50

STORED_DATA_DIRECTORY = 'data'
STORED_DATA_INFO_FILE = 'data_info'

DROP_COLUMNS = ['Open', 'Close', 'Volume', 'Ex-Dividend', 'Split Ratio',
                'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']


def getFilePath(file_name, file_format):
    return os.path.join(STORED_DATA_DIRECTORY, 
                        file_name + '.' + file_format)


def updateRequestCountAndDate(data):
    # Start counter from zero if the last request was not today
    today_date_str = datetime.now().strftime(DATE_FORMAT)
    if data['quandl_latest_request_date'] != today_date_str:
        data['quandl_latest_request_date'] = today_date_str
        data['quandl_requests_today'] = 0


def getMetadata():
    with open(getFilePath(STORED_DATA_INFO_FILE, 'json'), 'r') as data_file:
        data = json.load(data_file)
        updateRequestCountAndDate(data)
        return data


def updateMetadataFile(data):
    with open(getFilePath(STORED_DATA_INFO_FILE, 'json'), 'w') as data_file:
        json.dump(data, data_file, indent=2)


def hasStockDownloadedFor(data, stock_symbol):
    return False
    # return stock_symbol in data['stored_stocks']


def tryRequestStockDataForDates(stock_symbol, start_date, end_date):
    result = quandl.get('WIKI/' + stock_symbol, 
                        start_date=start_date, 
                        end_date=end_date)

    result.drop(DROP_COLUMNS, axis=1)
    return result


if __name__ == "__main__":
    start_date = datetime(2016,1,1)
    end_date = datetime(2016,1,7)
    
    print("Requestion Data")
    apple_data = tryRequestStockDataForDates("AAPL", start_date, end_date)
    apple_data.drop(columns=DROP_COLUMNS)
    print(apple_data)
