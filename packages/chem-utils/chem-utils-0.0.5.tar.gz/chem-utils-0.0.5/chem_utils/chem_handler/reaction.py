#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 14:29
# @Author  : zhangbc0315@outlook.com
# @File    : reaction.py
# @Software: PyCharm

from rdkit.Chem.AllChem import ChemicalReaction as RDReaction

from chem_utils.chem.molecule import Molecule


class Reaction:

    def __init__(self):
        self._reactants: [Molecule] = []
        self._products: [Molecule] = []
        self._catalysts: [Molecule] = []
        self._solvents: [Molecule] = []


if __name__ == "__main__":
    pass
