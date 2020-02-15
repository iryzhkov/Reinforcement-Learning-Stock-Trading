"""Simulation class used to run a single session with nice graphs outputs.
"""

from package.simulation.agent.baseAgent import BaseAgent
from package.simulation.stockData.stockDataSourceFactory import getDataSourceFromConfig
from package.simulation.session import Session
from package.util.plotter import Plotter


class Simulation:
    def __init__(self, agent: BaseAgent, simulation_config: dict, plotter=None):
        """Initializer for the Simulation class.

        Args:
            agent (BaseAgent): Agent used for this session.
            simulation_config (dict): Configuration for the session.
            plotter (Plotter): Plotter to use for the data plot.
        """

        self.stocks = agent.stocks
        self.simulation_name = simulation_config['simulation_name']
        self.plotter = plotter

        self.stock_data_source = getDataSourceFromConfig(agent.data_source_config)
        self.start_date = simulation_config['start_date']
        self.end_date = simulation_config['end_date']
        agent.exploration_parameter = 0

        self.stock_data_source.prepareDataForDates(self.start_date, self.end_date, self.stocks)

        def dateInRange(date):
            return self.start_date <= date <= self.end_date
        self.available_dates = list(filter(dateInRange, self.stock_data_source.getAvailableDates()))
        self.start_date = self.available_dates[agent.input_num_days]

        session_config = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'starting_balance': simulation_config['starting_balance']
        }
        self.session = Session(self.stock_data_source, agent, session_config)

    def runSimulation(self):
        """Initiates and runs a session
        """
        self.session.runSession()
        if self.plotter:
            self.plotter.plotSession(self.session, self.simulation_name)
