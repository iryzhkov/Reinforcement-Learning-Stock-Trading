"""Factories for Stock Data Sources.
"""

from package.simulation.stockData.realStockDataSource import RealStockDataSource
from package.simulation.stockData.randomizedStockDataSource import RandomizedStockDataSource
from package.simulation.stockData.sinusoidStockDataSource import SinusoidStockDataSource


_real_data_source = None


def getRandomizedDataSourceFromConfig(config: dict):
    """Creates randomized data source.

    Args:
        config (dict): configuration for the data source.

    Returns:
        Randomized Stock Data Source
    """
    child_data_source = getDataSourceFromConfig(config['child_source'])
    variance = config['variance']
    return RandomizedStockDataSource(child_data_source, variance)


def getSinusoidDataSource():
    """Creates sinusoid data source.

    Returns:
        Sinusoid Stock Data Source
    """
    return SinusoidStockDataSource()


def getRealDataSource():
    """Returns Real Stock Data Source if it already exists. Otherwise, creates a new one.

    Returns:
        Real Stock Data Source
    """
    global _real_data_source
    if _real_data_source is not None:
        return _real_data_source
    else:
        _real_data_source = RealStockDataSource()
        return _real_data_source


def getDataSourceFromConfig(data_source_config: dict):
    """Creates a Stock Data Source based on the data_source_config

    Args:
        data_source_config (dict): Data Source Config used to build Stock Data Source

    Returns:
        A Data Source Config build based on the input config.
    """
    if data_source_config['source_type'] == 'real': return getRealDataSource();
    elif data_source_config['source_type'] == 'sinusoid': return getSinusoidDataSource();
    elif data_source_config['source_type'] == 'randomized': return getRandomizedDataSourceFromConfig(data_source_config);


if __name__ == '__main__':
    pass
