import pandas as pd
import numpy as np
import streamlit as st

class Simulator:
    def simulate(self, assumptions, strategies, runs=200):
        columns = ['Year', 'Strategy', 'Assets', 'Run']
        data = []
        for strategy in strategies:
            for run in range(runs):
                assets = strategy.assumptions.STARTING_AMOUNT
                run_data = []
                for year in range(assumptions.YEARS + 1):
                    data.append([year, strategy.name, assets, run])
                    assets = strategy.annual_returns(year, assets)
                    assets += strategy.assumptions.annual_savings(year)
                    if assumptions.BANKRUPTCY:
                        assets = max(assets, 10)
                    run_data.append(assets)
        
        df = pd.DataFrame(data, columns=columns)
        return df