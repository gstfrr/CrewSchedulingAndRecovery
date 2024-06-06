# -*- coding: utf-8 -*-
"""Gantt Chart visualiser

This is a visualiser for the scheduling. It is a Gantt Chart made with Pandas and Plotly.
This visualizer plots the results of the scheduling in a browser window and it saves the image to the output directory.
"""

import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

if not os.path.exists('output/images'):
    os.mkdir('output/images')

pio.renderers.default = 'browser'


def visualize(output_file: str) -> None:
    df = pd.read_excel(output_file)
    df = df.infer_objects()
    # Convert Start and End to datetime
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])

    # Create the Gantt chart
    fig = px.timeline(df, x_start="Start", x_end="End", y="Pilot", color="Pilot",
                      title='Gantt Chart for Flight Assignments', text="Flight")

    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Pilots',
        xaxis=dict(
            tickformat='%Y-%m-%d %H:%M',
            tickangle=45
        ),
        yaxis=dict(
            title='Pilots',
            categoryorder='total ascending'
        )
    )

    fig.update_yaxes(title_text='Pilots')
    fig.update_xaxes(title_text='Time')

    fig.write_image('output/images/chart.png', width=1920, height=1080, scale=2)
    # fig.show()
