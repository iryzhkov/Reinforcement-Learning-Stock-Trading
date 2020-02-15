"""Util for plotting sessions / trainings.
"""
import matplotlib
import matplotlib.pyplot as plt

from os.path import dirname, join
from pathlib import Path
from datetime import datetime

matplotlib.use('Agg')
projectRoot = dirname(dirname(dirname(__file__)))
plottingPath = join(projectRoot, 'plots')
dateFormat = '%Y_%b_%d_%H_%M_%S'


class Plotter:
    def __init__(self, config):
        """
        """
        self.path = join(plottingPath, config['path'])
        self.path = join(self.path, datetime.now().strftime(dateFormat))
        Path(self.path).mkdir(parents=True, exist_ok=True)

    def _getFilepath(self, filename):
        """Returns filepath for the file with filename

        Args:
            filename (str): Filename
        """
        if not filename.endswith(('.png', '.jpg', '.jpeg')):
            filename = filename + '.png'
        return join(self.path, filename)

    def plotSession(self, session, output_file: str):
        """Plots session.

        Args:
            session (Session): Session which to plot.
            output_file (str): Name of the output file for the plot.
        """
        num_figures = len(session.stocks) + 1
        fig, axis = plt.subplots(num_figures, sharex='col', gridspec_kw={'hspace': 0.03}, figsize=(15, 10))

        # Drawing plots with stock data
        for index, stock in enumerate(session.stocks):
            data_to_plot = session.stock_data_source.stock_data[stock].loc[session.start_date:session.end_date]
            axis[index].set_ylabel(stock)
            axis[index].plot(data_to_plot.index, data_to_plot['High'], 'c-')
            axis[index].plot(data_to_plot.index, data_to_plot['Low'], 'r-')
            axis[index].grid(which='both', color='k', linestyle='--')
            axis[index].set_ylim(bottom=min(data_to_plot['Low']) - 5, top=max(data_to_plot['High']) + 5)

        # Adding marks for when stock was bought and sold.
        for date in session.action_history.index:
            actions = session.action_history.loc[date]
            for index, stock in enumerate(session.stocks):
                action = actions[stock]
                if action < 0:
                    sell_price = session.stock_data_source.getStockDataForDate(date, stock)['Low']
                    axis[index].plot([date, date], [0, sell_price], 'm:o')
                if action > 0:
                    buy_price = session.stock_data_source.getStockDataForDate(date, stock)['High']
                    axis[index].plot([date, date], [0, buy_price], 'b:o')

        # Adding net worth plot
        index = len(session.stocks)
        data_to_plot = session.records
        axis[index].plot(data_to_plot.index, data_to_plot['Net Worth'], 'm-')
        axis[index].set_ylabel('Net Worth')
        axis[index].grid(which='both', color='k', linestyle='--')

        fig.savefig(self._getFilepath(output_file))
        plt.close(fig)

    def plotTraining(self, training, output_file: str):
        """Plots training results.

        Args:
            training (Training): Training which to plot.
            output_file (str): Name of the output file for the plot.
        """
        pass
