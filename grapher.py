import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import pandas as pd
import numpy as np
import altair as alt

class Grapher:

    def graph(self, df):
        chart = alt.Chart(df).mark_line().encode(
            x='Year',
            y='median(Assets)',
            color='Strategy',
        ).properties(
            width=1000,
            height=500
        )

        band = alt.Chart(df).mark_area(opacity=0.3).encode(
            x='Year',
            y='q1(Assets)',
            y2='q3(Assets)',
            color='Strategy',
        )
        return chart + band
