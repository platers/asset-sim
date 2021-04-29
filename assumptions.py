import numpy as np

class Assumptions:
    MAX_LEVERAGE = 3 # maximum leverage at any time
    INTEREST_RATE = 0.015 # cost of borrowing money
    STARTING_AMOUNT = 10_000 # avoids divide by 0 errors
    EQUITY_RETURN_MEAN = 0.08
    EQUITY_RETURN_STD = 0.12
    RRA = 1.2 # relative risk aversion, 1 is log utility

    def annual_savings(self, year):
        return 50_000

    def annual_returns(self, year):
        # https://towardsdatascience.com/are-stock-returns-normally-distributed-e0388d71267e
        return np.random.normal(self.EQUITY_RETURN_MEAN, self.EQUITY_RETURN_STD)