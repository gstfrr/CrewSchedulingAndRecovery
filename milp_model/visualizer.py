# -*- coding: utf-8 -*-
"""Gantt Chart visualiser

This is a visualiser for the scheduling. It is a Gantt Chart made with Pandas and Plotly.
This visualizer plots the results of the scheduling in a browser window and it saves the image to the output directory.
"""

import plotly.graph_objects as go
import pandas as pd

from Domain import Pairing


def plot_flights(pairing: Pairing):
    """

    :param pairing: Pairing: Pairing to be plotted.

    """
    # Extract flight data for plotting
    flight_data = []
    flights = pairing.flights
    for flight in flights:
        flight_data.append({
            "Flight": flight.name,
            "Departure Airport": flight.origin,
            "Arrival Airport": flight.destination,
            "Departure": flight.start,
            "Arrival": flight.end
        })

    # Convert to DataFrame
    df_flights = pd.DataFrame(flight_data)

    # Create the figure
    fig = go.Figure()

    # Define colors for different flights
    colors = ['red', 'blue', 'green', 'purple']

    # Add each flight as a scatter trace with arrows
    for i, row in df_flights.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Departure'], row['Arrival']],
            y=[row['Departure Airport'], row['Arrival Airport']],
            mode='lines+markers+text',
            name=f"Flight {row['Flight']}",
            text=[row['Departure'].strftime('%H:%M'), row['Arrival'].strftime('%H:%M')],
            textposition="top center",
            line=dict(
                color=colors[i % len(colors)],
                width=2,
                shape='linear'
            ),
            marker=dict(
                size=10,
                symbol='arrow-bar-right'
            )
        ))

    # Update layout
    fig.update_layout(
        title=pairing.__repr__(),
        xaxis_title='Time',
        yaxis_title='Airport',
        xaxis=dict(
            tickformat='%H:%M',
            dtick=3600000,  # one hour in milliseconds
            title='Time'
        ),
        yaxis=dict(
            title='Airport',
            tickmode='array',
            tickvals=list(
                set([flight.origin for flight in flights] + [flight.destination for flight in flights]))
        ),
        hovermode='closest'
    )

    # Show the figure
    fig.write_image(width=1920, height=1080, scale=2,
                    file=f'output/images/chart_{pairing.pilot.name}-{pairing.name}-{len(pairing.flights)}-flights.png')
    # fig.show()
