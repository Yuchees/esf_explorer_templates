#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
These functions is designed for crystal structure formation and the 3D molecular
viewer for the application
"""
import json
import pandas as pd
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


def df_selection(chart_name):
    """

    Parameters
    ----------
    chart_name

    Returns
    -------

    """
    # Load DataFrames
    df_trip = pd.read_csv('./data/df_trip.csv')
    energy_trip = pd.read_csv('./data/energy_trip.csv')
    th4 = pd.read_csv('./data/th4.csv')
    if chart_name == 'th4':
        return th4
    elif chart_name == 'df_trip':
        return df_trip
    elif chart_name == 'energy_trip':
        return energy_trip
    else:
        raise ValueError('Chart type error')


def structure_viewer(interactive_data, color_bar, chart_name):
    """
    The molecular viewer

    Parameters
    ----------
    interactive_data: dict
    color_bar: str
    chart_name: str

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
    cluster_dict = {'0': 'TH4', '1': 'TH2', '2': 'T2'}
    try:
        for i in range(len(interactive_data['points'])):
            df = df_selection(chart_name=chart_name)
            if chart_name == 'th4':
                if color_bar == 'Pore dimensionality':
                    index = int(interactive_data['points'][i]['pointIndex'])
                    cluster_idx = interactive_data['points'][i]['curveNumber']
                    selected_df = df[
                        df.loc[:, 'Pore dimensionality'] == int(cluster_idx)
                        ].iloc[index]
                    structure_name = selected_df.Name
                    origin_idx = selected_df.index[0]

                else:
                    index = int(interactive_data['points'][i]['pointIndex'])
                    structure_name = int(df.iloc[index].Name)
                    origin_idx = index
            else:
                # Finding the original index from the grouped data
                index = int(interactive_data['points'][i]['pointIndex'])
                cluster_idx = interactive_data['points'][i]['curveNumber']
                cluster_name = cluster_dict[str(cluster_idx)]
                selected_df = df[df.Molecule == cluster_name].iloc[index]
                structure_name = selected_df.Name
                origin_idx = selected_df.name
            json_path = './data/{}/{}.json'.format(chart_name, structure_name)
            viewer = single_3d_viewer(json_path, origin_idx)
            mol_div.append(viewer)
    # Default structure
    except TypeError:
        json_path = './data/th4/100020031487063.json'
        mol_div.append(single_3d_viewer(json_path, 'TH4 global minimum'))
    return mol_div
