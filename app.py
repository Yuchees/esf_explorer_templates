#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Template of the interactive ESF map within 3D molecular viewer
Author: Yu Che
"""

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc

from utils import th4_plot, structure_viewer
from config import CONFIG

# Set up web server
app = dash.Dash(__name__)
server = app.server
# Load dataframe
df = pd.read_csv('./data/th4.csv')
columns_dict = [{'label': i, 'value': i} for i in df.columns[1:-1]]

# Application object and HTML components
app.layout = html.Div(
    id='main',
    className='app_main',
    children=[
        # Dash title and icon
        html.Div(
            id='mol3d-title',
            children=[
                html.Img(
                    id='dash-logo',
                    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/"
                        "logo/new-branding/dash-logo-by-plotly-stripe.png"
                ),
                html.H1(id='chart-title', children='ESF maps')
            ]
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
                    options=[
                        {'label': 'ESF Map: TH4', 'value': 'th4'}
                    ],
                    value='th4'
                ),
                html.Div(
                    id='color-bar-control',
                    className='dropdown-control',
                    children=[
                        html.H3('Colour bar:'),
                        dcc.Dropdown(
                            id='colour_column',
                            options=columns_dict,
                            value='No. of hydrogen bonds'
                        )
                    ]
                ),
                html.Div(
                    id='x-axis',
                    className='dropdown-control',
                    children=[
                        html.H3('X-axis:'),
                        dcc.Dropdown(
                            id='x_axis_column',
                            className='axis_controller',
                            options=columns_dict,
                            value='Density (g/cm^3)'
                        )
                    ]
                ),
                html.Div(
                    id='y-axis',
                    className='dropdown-control',
                    children=[
                        html.H3('Y-axis:'),
                        dcc.Dropdown(
                            id='y_axis_column',
                            className='axis_controller',
                            options=columns_dict,
                            value='Relative lattice energy (kJ/mol)'
                        )
                    ]
                ),
                html.P('The X and Y axis dropdown are disabled '
                       'when choose landmarks chart.'),
                html.Div(
                    id='range-slider-control',
                    className='dropdown-control',
                    children=[
                        html.H3('Range slider:'),
                        dcc.Dropdown(
                            id='range_column',
                            options=columns_dict,
                            value='Relative lattice energy (kJ/mol)'
                        )
                    ]
                ),
                # Dash range slider and texts
                dcc.RangeSlider(id='range-slider'),
                html.P(id='selected_data'),
                # User instructions
            ]
        ),
        html.Div(
            id='selected_structure',
            children=[
                html.H3(className='viewer-title',
                        children='Selected structure:'),
                dcc.Loading(id='loading_selected', className='loading')
            ]
        )
    ]
)


# Setting range slider properties
@app.callback(
    dash.dependencies.Output('range-slider', 'min'),
    [dash.dependencies.Input('range_column', 'value')])
def select_bar1(range_column_value):
    return df[range_column_value].min()


@app.callback(
    dash.dependencies.Output('range-slider', 'max'),
    [dash.dependencies.Input('range_column', 'value')])
def select_bar2(range_column_value):
    return df[range_column_value].max()


@app.callback(
    dash.dependencies.Output('range-slider', 'value'),
    [dash.dependencies.Input('range_column', 'value')])
def select_bar3(range_column_value):
    return [df[range_column_value].min(), df[range_column_value].max()]


@app.callback(
    dash.dependencies.Output('range-slider', 'step'),
    [dash.dependencies.Input('range_column', 'value')]
)
def range_step(range_column_value):
    step = (df[range_column_value].max() - df[range_column_value].min())/100
    return step


# Print the selected range
@app.callback(
    dash.dependencies.Output('selected_data', 'children'),
    [dash.dependencies.Input('range-slider', 'value'),
     dash.dependencies.Input('range_column', 'value')])
def callback(range_slider_value, range_column_value):
    return 'Structure {} between {:>.1f} and {:>.1f} are selected.'.format(
        range_column_value, range_slider_value[0], range_slider_value[1]
    )


# Chemical structure 3D viewer
@app.callback(
    dash.dependencies.Output('loading_selected', 'children'),
    [dash.dependencies.Input('indicator-graphic', 'selectedData')])
def display_selected_structure(selectedData):
    return structure_viewer(df, selectedData)


# Figure updated by different dash components
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('x_axis_column', 'value'),
     dash.dependencies.Input('y_axis_column', 'value'),
     dash.dependencies.Input('colour_column', 'value'),
     dash.dependencies.Input('range_column', 'value'),
     dash.dependencies.Input('range-slider', 'value')])
def update_graph(x_axis_column_name, y_axis_column_name, colour_column_value,
                 range_column_value, range_slider_value):
    filtered_df = pd.DataFrame(
        data=df[
            (df[range_column_value] >= range_slider_value[0]) &
            (df[range_column_value] <= range_slider_value[1])]
    )
    # General ESF map
    fig = th4_plot(filtered_df, x_axis_column_name, y_axis_column_name,
                   colour_column_value)
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
