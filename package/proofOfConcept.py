"""Proof of concept workflow. Uses sinusoid data source and q-learning agent to show that the program can actually work.
"""
import package.util.config as Configuration
import package.simulation.agent.agentFactory as AgentFactory

from package.simulation.simulation import Simulation
from package.simulation.training import Training

import logging


def proofOfConcept():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    ch.setFormatter(fmt)
    simulation_logger = logging.getLogger('simulation')
    simulation_logger.setLevel(logging.DEBUG)
    simulation_logger.addHandler(ch)

    configuration = Configuration.getConfiguration('proof_of_concept')
    agent = AgentFactory.getAgentFromConfig(configuration['agent_config'])

    for training_config in configuration['training_configs']:
        training = Training(agent, training_config)
        training.startTraining()

    simulation = Simulation(agent, configuration['simulation_config'])
    simulation.runSimulation()
    simulation.drawPerformancePlot()

if __name__ == '__main__':
    proofOfConcept()
