class StockMarketSimulator:
    def __init__(self):
        self.budget = 0;
        self.stocks = {};
        self.stock_codes = set();

    def setBudget(self, new_budget):
        if (additional_budget > 0):
            self.budget = new_budget 

    def addBudget(self, additional_budget):
        if (additional_budget > 0):
            self.budget += additional_budget

    def buyStocks(self, date, stock_symbol, number_to_buy):
        self.stocks[stock_code] += number_to_buy
            
    def getNetWorth(self):
        # TODO(iryzhkov): get net worth of the stocks
        return self.budget

