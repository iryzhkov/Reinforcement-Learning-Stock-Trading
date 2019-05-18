import real_data_source
import randomized_data_source
import sinusoid_data_souce

__real_data_source = None;

def getRandomizedDataSource(randomized_data_source_config):
    pass;

def getSinusiodDataSource(sinusoid_data_source_config):
    pass;

def getRealDataSource():
    global __real_data_source;
    if __real_data_source:
        return __real_data_source;

def getDataSourceFromConfig(data_source_config):
    pass;

class InvalidDataSourceConfig(ValueError):
    pass;