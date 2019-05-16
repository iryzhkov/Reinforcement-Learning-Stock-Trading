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

    def addStockCodes(self, new_stock_codes):
        for code in new_stock_codes:
            if code not in self.stock_codes:
                self.stock_codes.add(code);
                self.stocks[code] = 0;
                # TODO(iryzhkov): load price data for the new code

    def buyStocks(self, date, stock_code, number_to_buy):
        if stock_code in self.stock_codes:
            # TODO(iryzhkov): get the price
            self.stocks[stock_code] += number_to_buy
            
    def getNetWorth(self):
        # TODO(iryzhkov): get net worth of the stocks
        return self.budget

