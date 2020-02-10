import quandl
from datetime import datetime

quandl.ApiConfig.api_key = '5wzrzhdhdqLsG2r6uC_3'

DROP_COLUMNS = ['Open', 'Close', 'Volume', 'Ex-Dividend', 'Split Ratio',
                'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']


def tryRequestStockDataForDates(stock_symbol, start_date, end_date):
    result = quandl.get('WIKI/' + stock_symbol,
                        start_date=start_date,
                        end_date=end_date)

    result.drop(DROP_COLUMNS, axis=1)
    return result


if __name__ == "__main__":
    start_date = datetime(2016, 1, 1)
    end_date = datetime(2016, 1, 7)

    print("Requestion Data")
    apple_data = tryRequestStockDataForDates("AAPL", start_date, end_date)
    apple_data.drop(columns=DROP_COLUMNS)
    print(apple_data)
