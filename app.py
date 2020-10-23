#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Template of the interactive ESF map within 3D molecular viewer
Author: Yu Che
"""

import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc

from utils import df_selection, structure_viewer
from config import CONFIG

app = dash.Dash(__name__)
server = app.server

# Load DataFrames
df = pd.read_csv()

app.layout = html.Div(
    id='main',
    className='app_main',
    children=[
        # Dash title and icon
        html.Div(
            id='mol3d-title',
            children=[]
        ),
        # Dash graph and 3D molecule viewer
        dcc.Graph(id='indicator-graphic', config=CONFIG),
        # Dash axis, colour bar and range selection controller
        html.Div(
            id='plot-controller',
            children=[
                html.H3('Chart types:'),
                dcc.RadioItems(
                    id='chart-type',
                    options=[]
                ),
                html.Div(
                    id='color-bar-control',
                    className='dropdown-control',
                    children=[]
                ),
                html.Div(
                    id='x-axis',
                    className='dropdown-control',
                    children=[]
                ),
                html.Div(
                    id='y-axis',
                    className='dropdown-control',
                    children=[]
                )
            ]
        ),
        html.Div(
            id='selected_structure',
            children=[
                html.H3(className='viewer-title', children='Selected structure:'),
                dcc.Loading(id='loading_selected', className='loading')
            ]
        )
    ]
)


# Chemical structure 3D viewer
@app.callback(
    dash.dependencies.Output('loading_selected', 'children'),
    [dash.dependencies.Input('indicator-graphic', 'selectedData'),
     dash.dependencies.Input('colour_column', 'value'),
     dash.dependencies.Input('chart-type', 'value')])
def display_selected_structure(selectedData, colour_column_value,
                               chart_type_value):
    return structure_viewer(selectedData, colour_column_value, chart_type_value)


# Figure updated by different dash components
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('chart-type', 'value'),
     dash.dependencies.Input('x_axis_column', 'value'),
     dash.dependencies.Input('y_axis_column', 'value'),
     dash.dependencies.Input('colour_column', 'value')])
def update_graph(chart_type_value, x_axis_column_name, y_axis_column_name,
                 colour_column_value):
    # General ESF map
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_axis_column_name],
        y=df[y_axis_column_name],
        text=df[''],
        mode='markers',
        marker={'size': 10,
                'color': df[colour_column_value],
                'colorbar': {'title': colour_column_value},
                'colorscale': 'RdBu',
                'showscale': True}
        ))
    fig.update_layout()
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
