import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
from assumptions import Assumptions
from strategy import *
from simulator import Simulator
from grapher import Grapher

st.title('Asset Sim')

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
     Lifecycle(assumptions, years)),
    format_func=lambda s : s.name,
    default=[default_strategy]
)
if not strategies:
    strategies = [All_in(assumptions)]

assumptions.ANNUAL_SAVINGS = st.sidebar.number_input('Annual savings', value=50_000, step=10_000)
assumptions.STARTING_AMOUNT = st.sidebar.number_input('Starting amount', value=10_000, step=10_000)
assumptions.EQUITY_RETURN_MEAN = st.sidebar.number_input('Annual return mean', value=.08, step=.01)
assumptions.EQUITY_RETURN_STD = st.sidebar.number_input('Annual return standard deviation', value=.12, step=.01)

years = st.sidebar.number_input('Years', value=40, step=10, min_value=1)



sim = Simulator()
df = sim.simulate(years, strategies, runs=200)

gr = Grapher()
chart = gr.graph(df)
st.altair_chart(chart)