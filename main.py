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
    
sim = Simulator()
strategies = [All_in(assumptions)]
years = 30
df = sim.simulate(years, strategies)

gr = Grapher()
chart = gr.graph(df)
st.altair_chart(chart)