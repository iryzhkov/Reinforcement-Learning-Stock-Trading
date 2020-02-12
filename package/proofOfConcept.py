from package.simulation.agent.qLearningAgent import QLearningAgent
from package.simulation.simulation import Simulation
from package.simulation.training import Training
from package.simulation.stockData.stockDataSourceFactory import getDataSourceFromConfig

from datetime import datetime


def proofOfConcept():
    training_period_start = datetime(2014, 1, 1)
    training_period_end = datetime(2015, 1, 1)

    simulation_data_period_start = datetime(2013, 12, 1)
    simulation_period_start = datetime(2014, 1, 1)
    simulation_period_end = datetime(2014, 3, 1)

    stocks = ['STOCK_1', 'STOCK_2']
    data_source_config = {'source_type': 'sinusoid'}
    config_1 = {'period': 60, 'anchor_date': datetime(2015, 1, 1), 'delta': 100, 'magnitude': 20}
    config_2 = {'period': 60, 'anchor_date': datetime(2015, 1, 15), 'delta': 100, 'magnitude': 20}
    stocks_config = {stocks[0]: config_1, stocks[1]: config_2}

    session_config = {'start_date': simulation_period_start,
                      'end_date': simulation_period_end,
                      'starting_balance': 1000,
                      'stocks': stocks}

    test_data_source = getDataSourceFromConfig(data_source_config)
    test_data_source.stocks_config = stocks_config

    agent = QLearningAgent(data_source_config, 2, stocks)

    print("Preparing data")
    test_data_source.prepareDataForDates(simulation_data_period_start, simulation_period_end, stocks)

    print("Data prepared, running simulation")
    agent.exploration_parameter = 0
    simulation = Simulation(test_data_source, agent, session_config)
    simulation.runSimulation()
    simulation.drawPerformancePlot()

    print("Starting training")
    training = Training(test_data_source, agent, training_period_start, training_period_end, stocks)
    training.startTraining()
    print("Training complete")

    print("Starting final simulation")
    agent.exploration_parameter = 0
    test_data_source.prepareDataForDates(simulation_data_period_start, simulation_period_end, stocks)
    simulation = Simulation(test_data_source, agent, session_config)
    simulation.runSimulation()
    simulation.drawPerformancePlot()


if __name__ == '__main__':
    proofOfConcept()
