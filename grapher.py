import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import pandas as pd
import numpy as np
import altair as alt

class Grapher:

    def graph(self, df):
        line = alt.Chart(df).mark_line().encode(
            x='Year',
            y='median(Assets)',
            color='Strategy',
        ).properties(
            width=1000,
            height=500
        )

        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['Year'], empty='none')
        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(df).mark_point().encode(
            x='Year',
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )
        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=5).encode(
            text=alt.condition(nearest, 'median(Assets)', alt.value(' '), format=',.2r')
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(df).mark_rule(color='gray').encode(
            x='Year',
        ).transform_filter(
            nearest
        )

        band = alt.Chart(df).mark_area(opacity=0.3).encode(
            x='Year',
            y='q1(Assets)',
            y2='q3(Assets)',
            color='Strategy',
        )
        # Put the five layers into a chart and bind the data
        chart = alt.layer(
            line, band, selectors, points, rules, text
        )
        return chart
