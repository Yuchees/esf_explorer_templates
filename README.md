# ESF Map Template
[![DOI](https://zenodo.org/badge/306344480.svg)](https://zenodo.org/badge/latestdoi/306344480)

This web application is a mini example of the deployed [online ESF map](https://www.interactive-esf-maps.app/).
It uses Dash to achieve interactive HTML functions and Plotly to build scatter chart.
The web app is deployed to Heroku server.

Due to the data size limitation, only th4 chart and structures whose relative lattice energy are lower than 30 were present in this template.

## Run application locally
Create a new virtual environment by ```conda```:

```
conda create -n esf_app python=3.7
conda activate esf_app
```

Install dependence packages:

```pip install -r requirements.txt```

After installation, you can run the web application through terminal:

```python app.py```

The default local web page is http://127.0.0.1:8050/

## Citation

Please cite our paper if you use this template:
* Zhao, C., Chen, L., Che, Y. et al. Digital navigation of energy–structure–function maps 
  for hydrogen-bonded porous molecular crystals. Nat Commun 12, 817 (2021).
* DOI: https://doi.org/10.1038/s41467-021-21091-w

## Note to users
Data including tables and chemical structures are stored in `./data`

The HTML formatting information is placed in `./assets/esf_map.css`

`Procfile` is a declaring command file on Heroku platform.

The chemical structure file used in this app are formatted json files.
If you would like to use own structure, it must be converted from PDB file to json file.

Parse the structure file:
```
from structure_parser import pdb_to_json
pdb_to_json(pdb_path=<Your PDB file>, json_path=<Parsed json file>)
```
There are some limitations of the molecule 3D viewer
since the ```dash_bio``` is primitively designed for visualizing bioinformatics data,
such as no crystal periodic information and editing the colour of elements.

## More information
Tutorial for Dash:
https://dash.plotly.com/

Tutorial for plotly:
https://plotly.com/python/
