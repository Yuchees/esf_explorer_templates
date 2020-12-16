# -*- coding: utf-8 -*-
import parmed as pmd
import warnings
import json
import re
import pathlib
from dash_bio_utils import styles_parser


def create_data(pdb_path):
    """
    Parse the protein data bank (PDB) file to generate
    input modelData

    Parameters
    ------
    pdb_path: str
        Name of the biomolecular structure file in PDB format

    """
    # Use parmed to read the bond information from temp file
    top = pmd.load_file(str(pdb_path))

    # Read PDB file to create atom/bond information
    with open(pdb_path, 'r') as infile:
        # store only non-empty lines
        lines = [l.strip() for l in infile if l.strip()]

    # Initialize all variables
    var_nchains = []
    serial = []
    atm_name = []
    res_name = []
    chain = []
    res_id = []
    positions = []
    occupancy = []
    temp_factor = []
    atom_type = []
    ct = 0

    datb = {
        'atoms': [],
        'bonds': []
    }

    # Variables that store the character positions of different
    # parameters from the molecule PDB file
    serialpos = [6, 11]
    atm_namepos = [12, 16]
    r_namepos = [17, 20]
    chainpos = [21, 22]
    r_idpos = [22, 26]
    xpos = [30, 38]
    ypos = [38, 46]
    zpos = [46, 54]
    occupos = [54, 60]
    bfacpos = [60, 66]
    atm_typepos = [77, 79]

    for l in lines:
        line = l.split()
        if "ATOM" in line[0] or "HETATM" in line[0]:
            serial.append(int(l[serialpos[0]:serialpos[1]]))
            atm_name.append(l[atm_namepos[0]:atm_namepos[1]].strip())
            val_r_name = l[r_namepos[0]:r_namepos[1]].strip()
            res_name.append(val_r_name)
            chain_val = l[chainpos[0]:chainpos[1]].strip()
            chain.append(chain_val)
            if chain_val not in var_nchains:
                var_nchains.append(chain_val)
            val_r_id = int(l[r_idpos[0]:r_idpos[1]])
            res_id.append(val_r_id)
            x = float(l[xpos[0]:xpos[1]])
            y = float(l[ypos[0]:ypos[1]])
            z = float(l[zpos[0]:zpos[1]])
            positions.append([x, y, z])
            occupancy.append(l[occupos[0]:occupos[1]].strip())
            temp_factor.append(l[bfacpos[0]:bfacpos[1]].strip())
            atom_type.append(l[atm_typepos[0]:atm_typepos[1]].strip())
            ct += 1

    # Create list of atoms
    tmp_res = res_id[0]
    resct = 1
    for i in range(len(chain)):  # pylint: disable=consider-using-enumerate
        if tmp_res != res_id[i]:
            tmp_res = res_id[i]
            resct += 1
        datb['atoms'].append({
            "name": atm_name[i],
            "chain": chain[i],
            "positions": positions[i],
            "residue_index": resct,
            "element": atom_type[i],
            "residue_name": res_name[i] + str(res_id[i]),
            "serial": i,
        })

    # Create list of bonds using the parmed module
    for i in range(len(top.bonds)):
        bondpair = top.bonds[i].__dict__
        atom1 = re.findall(r"\[(\d+)\]", str(bondpair['atom1']))
        atom2 = re.findall(r"\[(\d+)\]", str(bondpair['atom2']))
        datb['bonds'].append({
            'atom2_index': int(atom1[0]),
            'atom1_index': int(atom2[0])
        })

    return json.dumps(datb)


def pdb_to_json(pdb_path, json_path, style='stick', mol_color='atom'):
    """
    Converge a PDB file to a parsed json file including molecule data and
    style data.

    Parameters
    ----------
    pdb_path: str
        PDB path string.
    json_path: str
        Output json file path.
    style: str
        Molecule style parameter.
    mol_color: str

    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    # OOP path detection and operation
    _pdb_path = pathlib.Path(pdb_path)
    _json_path = pathlib.Path(json_path)
    assert _pdb_path.suffix == '.pdb', \
        'Given file is not a pdb file, got {}'.format(pdb_path)
    if _json_path.is_dir():
        json_file_path = _json_path / _pdb_path.with_suffix('.json').name
    elif _json_path.suffix == '.json':
        json_file_path = _json_path
    else:
        raise ValueError('')
    molecule_data = json.loads(
        create_data(pdb_path=_pdb_path)
    )
    style_data = json.loads(
        styles_parser.create_style(
            pdb_path=_pdb_path, style=style, mol_color=mol_color
        )
    )
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump([molecule_data, style_data], json_file, ensure_ascii=False)
