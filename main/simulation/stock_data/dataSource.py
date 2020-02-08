import realDataSource
import randomizedDataSource
import sinusoidDataSource

_real_data_source = None;

def randomizeDataSource(data_source, randomization_config):
    return data_source;

def getSinusiodDataSource(sinusoid_data_source_config):
    pass;

def getRealDataSource():
    global __real_data_source;
    if __real_data_source is not None:
        return __real_data_source;
    else:
        __real_data_source = realDataSource.RealDataSource();
        return _real_data_source;

def getDataSourceFromConfig(data_source_config):
    pass;
