import pandas as pd
import numpy as np

class Simulator:
    def simulate(self, years, strategies, runs=200):
        means = []
        lower = []
        columns = ['Year', 'Strategy', 'Assets', 'Run']
        data = []
        for strategy in strategies:
            for run in range(runs):
                assets = strategy.assumptions.STARTING_AMOUNT
                run_data = []
                for year in range(years):
                    assets = strategy.annual_returns(year, assets)
                    assets += strategy.assumptions.annual_savings(year)
                    assets = max(assets, 1000) # bankruptcy
                    run_data.append(assets)
                    tmp = [year, strategy.name, assets, run]
                    data.append(tmp)
        
        df = pd.DataFrame(data, columns=columns)
        return df