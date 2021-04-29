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


# Sidebar widgets

strategies = st.sidebar.multiselect(
    'Strategy',
    (All_in(assumptions), Leveraged(assumptions, 2)),
    format_func=lambda s : s.name
)
if not strategies:
    strategies = [All_in(assumptions)]

annual_savings = st.sidebar.number_input('Annual savings', value=50_000, step=10_000)
starting_amount = st.sidebar.number_input('Starting amount', value=10_000, step=10_000)
years = st.sidebar.number_input('Years', value=40, step=10)

assumptions.ANNUAL_SAVINGS = annual_savings
assumptions.STARTING_AMOUNT = starting_amount




sim = Simulator()
df = sim.simulate(years, strategies)

gr = Grapher()
chart = gr.graph(df)
st.altair_chart(chart)