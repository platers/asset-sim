import numpy as np

class Assumptions:
    MAX_LEVERAGE = 3 # maximum leverage at any time
    INTEREST_RATE = 0.015 # cost of borrowing money
    STARTING_AMOUNT = 10_000 # avoids divide by 0 errors
    EQUITY_RETURN_MEAN = 0.11
    EQUITY_RETURN_STD = 0.20
    RRA = 2 # relative risk aversion, 1 is log utility
    ANNUAL_SAVINGS = 50_000
    YEARS = 40
    SAVINGS_YEARS = np.inf

    def annual_savings(self, year): # this is a function for future extensibility
        if year < self.SAVINGS_YEARS:
            return self.ANNUAL_SAVINGS
        return 0

    def annual_returns(self, year):
        # https://towardsdatascience.com/are-stock-returns-normally-distributed-e0388d71267e
        return np.random.normal(self.EQUITY_RETURN_MEAN, self.EQUITY_RETURN_STD)