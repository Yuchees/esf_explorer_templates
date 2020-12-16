#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
These functions is designed for crystal structure formation and
the 3D molecular viewer application
"""
import json
import pandas as pd

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
    fig = go.Figure()
    # The rest figure have a continues color bar.
    fig.add_trace(go.Scatter(
        x=df[x_axis_column_name],
        y=df[y_axis_column_name],
        text=df.index,
        marker=dict(
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
    # Set the format of points
    fig.update_traces(
        mode='markers',
        marker=dict(
            symbol='circle',
            opacity=0.7,
            line=dict(color='rgb(40, 40, 40)', width=0.2),
            size=8
        )
    )
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
    The molecular viewer

    Parameters
    ----------
    df: Dataframe
    interactive_data: dict

    Returns
    -------
    list
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
            index = int(interactive_data['points'][i]['pointIndex'])
            structure_name = int(df.iloc[index].Name)
            origin_idx = index
            json_path = './data/th4/{}.json'.format(structure_name)
            viewer = single_3d_viewer(json_path, origin_idx)
            mol_div.append(viewer)
    # Default structure
    except TypeError:
        json_path = './data/th4/100020031487063.json'
        mol_div.append(single_3d_viewer(json_path, 'TH4 global minimum'))
    return mol_div
