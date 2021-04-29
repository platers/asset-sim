import pandas as pd
import numpy as np

class Simulator:
    def simulate(self, years, strategies):
        S = []

        for strategy in strategies:
            assets = strategy.assumptions.STARTING_AMOUNT
            asset_data = []
            for year in range(years):
                assets = strategy.annual_returns(year, assets)
                assets += strategy.assumptions.annual_savings(year)
                assets = max(assets, 1000) # bankruptcy
                asset_data.append(assets)
            S.append(pd.Series(asset_data, index=range(years), name=strategy.name))
        
        df = pd.concat(S, axis=1)
        df.index.name = "Year"
        df = df.reset_index().melt('Year')
        df = df.rename({'variable': 'Strategy', 'value': 'Assets'}, axis='columns')
        return df