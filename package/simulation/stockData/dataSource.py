from package.simulation.stockData.realDataSource import RealStockDataSource
from package.simulation.stockData.randomizedDataSource import RandomizedStockDataSource
from package.simulation.stockData.sinusoidDataSource import SinusoidStockDataSource

from datetime import datetime


_real_data_source = None


def getRandomizedDataSource(config):
    child_data_source = getDataSourceFromConfig(config['child_source'])
    variance = config['variance']
    return RandomizedStockDataSource(child_data_source, variance)


def getSinusoidDataSource():
    return SinusoidStockDataSource()


def getRealDataSource():
    global _real_data_source
    if _real_data_source is not None:
        return _real_data_source
    else:
        _real_data_source = RealStockDataSource()
        return _real_data_source


def getDataSourceFromConfig(data_source_config):
    if (data_source_config['source_type'] == 'real'): return getRealDataSource();
    elif (data_source_config['source_type'] == 'sinusoid'): return getSinusoidDataSource();
    elif (data_source_config['source_type'] == 'randomized'): return getRandomizedDataSource(data_source_config);


if __name__ == '__main__':
    stocks = ['GOOG', 'AMZN']
    config_1 = {'period': 60, 'anchor_date': datetime(2015, 1, 1), 'delta': 200, 'magnitude': 30}
    config_2 = {'period': 60, 'anchor_date': datetime(2015, 1, 15), 'delta': 200, 'magnitude': 30}
    stocks_config = {stocks[0]: config_1, stocks[1]: config_2}

    start_date = datetime(2016, 1, 1)
    end_date = datetime(2017, 1, 1)

    data_source_config = {'source_type': 'randomized', 'variance': 0.02, 'child_source': {'source_type': 'real'}}

    data_source = getDataSourceFromConfig(data_source_config)
    data_source.prepareDataForDates(start_date, end_date, stocks_config)
    data_source.drawPlotsForDates(start_date, end_date, stocks_config)
