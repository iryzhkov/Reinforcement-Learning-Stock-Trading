from datetime import datetime


class Session:
    def __init__(self, stock_data_source, agent, session_config):
        self.stock_data_source = stock_data_source
        self.agent = agent

        self.start_date = session_config['start_date']
        self.end_date = session_config['end_date']

        self.balance = session_config['balance']
        self.stocks = session_config['stocks']
        self.stocks_owned = {}
        for stock in self.stocks:
            self.stocks_owned[stock] = 0

    def startSession(self):
        pass

    def _runForDate(self, date):
        pass

    def _generatePossibleActions(self):
        pass

    def _generateAgentInputForDate(self, date):
        pass

    def getActionHistory(self):
        pass

    def getBuyHistory(self):
        pass

    def getSellHistory(self):
        pass

    def getNetWorthHistory(self):
        pass

    def getStockHistory(self):
        pass

    def getPerformance(self):
        pass


if __name__ == '__main__':
    stocks = ['STOCK_1', 'STOCK_2']
    config_1 = {'period': 60, 'anchor_date': datetime(2015, 1, 1), 'delta': 100, 'magnitude': 20}
    config_2 = {'period': 60, 'anchor_date': datetime(2015, 1, 15), 'delta': 100, 'magnitude': 20}
    stocks_config = {stocks[0]: config_1, stocks[1]: config_2}

    data_source = None
    agent = None
    session_config = {'start_date': 0,
                      'end_date': 0,
                      'starting_balance': 1000,
                      'stocks': stocks,
                      }

    session = Session(data_source, agent, session_config)
