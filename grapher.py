import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import pandas as pd
import numpy as np
import altair as alt

class Grapher:

    def graph(self, df):
        chart = alt.Chart(df).mark_line().encode(
            x='Year',
            y='Assets',
            color='Strategy',
        ).properties(
            width=1000,
            height=500
        )
        return chart
