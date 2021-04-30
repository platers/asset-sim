import pandas as pd
import numpy as np

class Simulator:
    def simulate(self, years, strategies, runs=200):
        columns = ['Year', 'Strategy', 'Assets', 'Run']
        data = []
        for strategy in strategies:
            for run in range(runs):
                assets = strategy.assumptions.STARTING_AMOUNT
                run_data = []
                for year in range(years + 1):
                    data.append([year, strategy.name, assets, run])
                    assets = strategy.annual_returns(year, assets)
                    assets += strategy.assumptions.annual_savings(year)
                    run_data.append(assets)
        
        df = pd.DataFrame(data, columns=columns)
        return df