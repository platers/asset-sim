import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
from assumptions import Assumptions
from strategy import *
from simulator import Simulator
from grapher import Grapher

st.title('Asset Sim (alpha release)')

assumptions = Assumptions()
years = 40 # redefined below


# Sidebar widgets

st.sidebar.title('Settings')
default_strategy = All_in(assumptions)
strategies = st.sidebar.multiselect(
    'Strategy',
    (default_strategy,
     Leveraged(assumptions, 2),
     Kelly(assumptions),
     Half_Kelly(assumptions),
     Half_in(assumptions),
     Lifecycle(assumptions)),
    format_func=lambda s : s.name,
    default=[default_strategy]
)
if not strategies:
    strategies = [All_in(assumptions)]

assumptions.ANNUAL_SAVINGS = st.sidebar.number_input('Annual savings', value=50_000, step=10_000)
assumptions.STARTING_AMOUNT = st.sidebar.number_input('Starting amount', value=10_000, step=10_000)
assumptions.EQUITY_RETURN_MEAN = st.sidebar.number_input('Annual return mean', value=.11, step=.01)
assumptions.EQUITY_RETURN_STD = st.sidebar.number_input('Annual return standard deviation', value=.20, step=.01, min_value=0.0)
assumptions.INTEREST_RATE = st.sidebar.number_input('Annual interest rate (only for leveraged strategies)', value=.02, step=.01)
assumptions.YEARS = st.sidebar.number_input('Years', value=40, step=10, min_value=1)

with st.sidebar.beta_expander('Lifecycle'):
    assumptions.MAX_LEVERAGE = st.number_input('Max leveraage', value=3.0, step=1.0, min_value=0.0)
    assumptions.RRA = st.number_input('RRA', value=2.0, step=1.0, min_value=0.1)

# re initialize strategies based on user defined parameters
for i in range(len(strategies)):
    s = strategies[i]
    if type(s) is Lifecycle:
        s = Lifecycle(assumptions)
    strategies[i] = s

sim = Simulator()
df = sim.simulate(years, strategies, runs=200)

gr = Grapher()
chart = gr.graph(df)
st.altair_chart(chart)

st.markdown('''
    ## FAQ
    ### How is the graph generated?
    This tool uses a monte carlo simulation. It simulates many runs and aggegates them together. 
    The lines are the median amounts of assets at a point in time. The error bands show first and third quartiles.

    ### Why median?
    Medians are less sensitive to outliers than means. A few lucky runs can blow up a mean.

    ### Where do the default values come from?
    They are best guesses based on historical data. The return values are based on the S&P 500.

    ### What do the strategies do?
    The strategies with a number after the name are leveraged by that amount. For example, 0.5x means you invest half of your current assets while 2x means you invest double your current assets.

    Kelly and half Kelly are leveraged strategies calculated according to the Kelly criterion.

    Lifecycle is described in "Lifecycle Investing" by Ian Ayres, Barry Nalebuff. It takes more leverage early and less later. 
    Relative risk aversion(RRA) is a measure of an investors risk tolerance. RRA of 1 is log utility, higher is more risk averse. 


    ### Why can't I change X?
    Asset sim prioritizes a simple interface with the minimum required parameters to be useful for financial planning. 
    If you believe there is an essential feature missing, you can raise an issue on [github](https://github.com/platers/asset-sim), or better yet, submit a pull request!

    ### Are there bugs?
    Possibly, this tool hasn't been well tested yet. If you find any, please submit an issue on [github](https://github.com/platers/asset-sim).
''')
