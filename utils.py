# -*- coding: utf-8 -*-
"""
These functions is designed for crystal structure formation and
the 3D molecular viewer application
"""
import json

import plotly.graph_objects as go
import dash_html_components as html
import dash_bio as bio


def load_json(file_path):
    """
    Loading the structure json file

    Parameters
    ----------
    file_path: str

    Returns
    -------

    """
    with open(file_path, 'r', encoding='utf-8') as json_file:
        mol_data, style_data = json.load(json_file)
    return mol_data, style_data


def th4_plot(df, x_axis_column_name, y_axis_column_name, colour_column_value):
    """
    Plotly Figure object for th4 data

    Parameters
    ----------
    df: DataFrame
        Data table
    x_axis_column_name: str
    y_axis_column_name: str
    colour_column_value: str

    Returns
    -------
    Figure
        Plotly figure object
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        # X and Y coordinates from data table
        x=df[x_axis_column_name],
        y=df[y_axis_column_name],
        text=df.index,
        mode='markers',
        # Set the format of scatter
        marker=dict(
            symbol='circle',
            opacity=0.7,
            line=dict(color='rgb(40, 40, 40)', width=0.2),
            size=8,
            # Colour bar
            color=df[colour_column_value],
            colorscale='RdBu',
            colorbar=dict(
                thicknessmode='pixels',
                thickness=20,
                title=dict(text=colour_column_value, side='right')
            ),
            reversescale=True,
            showscale=True
        )
    ))
    # Set the format of axes
    axis_template = dict(linecolor='#444', tickcolor='#444',
                         ticks='outside', showline=True, zeroline=False,
                         gridcolor='lightgray')
    fig.update_layout(
        xaxis=dict(axis_template, **dict(title=x_axis_column_name)),
        yaxis=dict(axis_template, **dict(title=y_axis_column_name)),
        clickmode='event+select',
        hovermode='closest',
        plot_bgcolor='white'
    )
    return fig


def structure_viewer(df, interactive_data):
    """
    The molecular 3D viewer

    Parameters
    ----------
    df: Dataframe
        Data table
    interactive_data: dict
        Plotly callback information
    Returns
    -------
    list
        A list of viewer object
    """

    def single_3d_viewer(json_file, structure_index):
        mol_data, style_data = load_json(json_file)
        mol_3d = html.Div(
            id='viewer',
            children=[
                html.P('Structure ID: {}'.format(structure_index)),
                bio.Molecule3dViewer(
                    id='mol-3d-viewer',
                    selectionType='atom',
                    styles=style_data,
                    modelData=mol_data
                )
            ]
        )
        return mol_3d

    mol_div = []
    # Loading multiple 3D viewer
    try:
        for i in range(len(interactive_data['points'])):
            # Find index from plotly callback information
            index = int(interactive_data['points'][i]['pointIndex'])
            origin_idx = index
            # Get structure name
            structure_name = int(df.iloc[index].Name)
            # Path of parsed structure file
            json_path = './data/th4/{}.json'.format(structure_name)
            mol_div.append(single_3d_viewer(json_path, origin_idx))
    # Default structure
    except TypeError:
        json_path = './data/th4/100020031487063.json'
        mol_div.append(single_3d_viewer(json_path, 'TH4 global minimum'))
    return mol_div
