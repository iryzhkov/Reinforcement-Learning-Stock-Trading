"""Utils used by Real Stock Data Source.
"""

import json
import quandl
import pandas as pd

from datetime import datetime
from os.path import dirname, join, exists

quandl.ApiConfig.api_key = '5wzrzhdhdqLsG2r6uC_3'

projectRoot = dirname(dirname(dirname(dirname(__file__))))
offlineStockDataPath = join(projectRoot, 'offline_stock_data')
offlineStockDataManifestPath = join(offlineStockDataPath, 'manifest.json')

dropColumns = ['Open', 'Close', 'Volume', 'Ex-Dividend', 'Split Ratio',
               'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']

dateFormat = '%d %b %Y'


def _dateToStr(date):
    """Converts datetime to str.

    Args:
        date (datetime): Date to convert.

    Returns:
        A string representation of the date.
    """
    return date.strftime(dateFormat)


def _dateHook(json_dict):
    """Converts str to datetime during json load.

    Args:
        json_dict (dict): Manifest dict.

    Returns:
        A dict with dates in the datetime class.
    """
    for key, value in json_dict.items():
        if key.endswith('date'):
            json_dict[key] = datetime.strptime(value, dateFormat)
        else:
            pass
    return json_dict


def getOfflineStockDataManifest():
    """Returns manifest for the available offline data.

    If manifest is not found, creates an empty one.

    Returns:
        A dict with the manifest. For example:
        {'STOCK_1':
            {'first_available_date': datetime(2016, 1, 1),
             'last_available_date': datetime(2017, 2, 28)},
         'STOCK_2':
            {'first_available_date': datetime(2014, 2, 4),
             'last_available_date': datetime(2016, 6, 15)}}
    """
    if exists(offlineStockDataManifestPath):
        with open(offlineStockDataManifestPath) as manifest_file:
            return json.load(manifest_file, object_hook=_dateHook)
    else:
        manifest = {}
        updateOfflineStockDataManifest(manifest)
        return manifest


def updateOfflineStockDataManifest(newManifest: dict):
    """Updates the offline stock data manifest using newManifest.

    Args:
        newManifest (dict): New offline stock data manifest. For example:
            {'STOCK_1':
                {'first_available_date': datetime(2016, 1, 1),
                 'last_available_date': datetime(2017, 2, 28)},
             'STOCK_2':
                {'first_available_date': datetime(2014, 2, 4),
                 'last_available_date': datetime(2016, 6, 15)}}
    """
    with open(offlineStockDataManifestPath, 'w+') as manifestFile:
        json.dump(newManifest, manifestFile, indent=4, sort_keys=True, default=_dateToStr)


def _stockDataFilePath(stock: str):
    """Returns file path to the offline stock data for given stock.

    Args:
        stock (str): Stock name
    """
    return join(offlineStockDataPath, stock + '.csv')


def getOfflineStockDataFor(stock: str):
    """Retrieves offline stock data for a given stock

    Args:
        stock (str): Stock for which to retrieve the data.
    """
    return pd.read_csv(_stockDataFilePath(stock), index_col=0)


def updateOfflineStockDataFor(new_stock_data: pd.DataFrame, stock: str):
    """Updates the offline stock data using new_stock_data

    Args:
        new_stock_data (pd.DataFrame): New stock data to store
        stock (str): Stock name
    """
    new_stock_data.to_csv(_stockDataFilePath(stock), date_format='%Y-%m-%d')


def tryRequestStockDataForDates(start_date, end_date, stock):
    """Tries to request stock data using quandl

    Args:
         start_date (datetime): Start date for the requested data range.
         end_date (datetime): End date for the requested data range.
         stock (str): Stock name for the request.
    """
    result = quandl.get('WIKI/' + stock,
                        start_date=start_date,
                        end_date=end_date)

    result.drop(dropColumns, axis=1)
    return result


if __name__ == "__main__":
    print(offlineStockDataPath)
