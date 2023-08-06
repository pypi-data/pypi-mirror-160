#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 14:30
# @Author  : zhangbc0315@outlook.com
# @File    : molecule.py
# @Software: PyCharm

from rdkit.Chem.rdchem import Mol as RDMol
from rdkit.Chem import AllChem


class Molecule:

    def __init__(self, rdmol: RDMol = None, smiles: str = None):
        if rdmol is not None:
            self._rdmol = rdmol
        elif smiles is not None:
            self._rdmol = AllChem.MolFromSmiles(smiles)
        else:
            raise AttributeError("rdmol and smiles cannot both be None.")


if __name__ == "__main__":
    pass
