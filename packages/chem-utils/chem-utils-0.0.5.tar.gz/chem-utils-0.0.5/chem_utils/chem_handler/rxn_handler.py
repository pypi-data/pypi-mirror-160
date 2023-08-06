#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 14:36
# @Author  : zhangbc0315@outlook.com
# @File    : rxn_handler.py
# @Software: PyCharm

from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import ChemicalReaction


class RxnHandler:

    # region ===== rdrxn_from_indigo_smiles =====

    @classmethod
    def _parse_indigo_tag(cls, indigo_tags_str: str) -> [[int]]:
        indigo_tags_str = indigo_tags_str.strip('|')
        indigo_tags = [[int(tag) for tag in tags.split('.')] for tags in indigo_tags_str.split(',')]
        return indigo_tags

    @classmethod
    def _split_smiles_by_indigo_tags(cls, rxn_smiles: str, indigo_tags: [[int]]) -> ([str], [str]):
        rs_smiles, ps_smiles = rxn_smiles.split('>>')
        r_smileses = rs_smiles.split('.')
        p_smileses = ps_smiles.split('.')
        all_smileses = r_smileses.copy()
        all_smileses.extend(p_smileses)
        num_rs = len(r_smileses)
        rs = []
        ps = []
        all_tags = []
        for tags in indigo_tags:
            all_tags.extend(tags)
            mol_smileses = []

            for tag in tags:
                mol_smileses.append(all_smileses[tag])
            if tags[0] >= num_rs:
                ps.append('.'.join(mol_smileses))
            else:
                rs.append('.'.join(mol_smileses))
        for i, smiles in enumerate(all_smileses):
            if i in all_tags:
                continue
            if i >= num_rs:
                ps.append(smiles)
            else:
                rs.append(smiles)
        return rs, ps

    @classmethod
    def _rdrxn_from_smileses(cls, r_smileses: [str], p_smileses: [str]):
        rdrxn = ChemicalReaction()
        for r_smiles in r_smileses:
            rdrxn.AddReactantTemplate(AllChem.MolFromSmiles(r_smiles))
        for p_smiles in p_smileses:
            rdrxn.AddProductTemplate(AllChem.MolFromSmiles(p_smiles))
        return rdrxn

    @classmethod
    def rdrxn_from_indigo_smiles(cls, indigo_smiles: str):
        rxn_smiles, indigo_tags_str = indigo_smiles.split(' |f:')
        indigo_tags = cls._parse_indigo_tag(indigo_tags_str)
        r_smileses, p_smileses = cls._split_smiles_by_indigo_tags(rxn_smiles, indigo_tags)
        print(r_smileses)
        print(p_smileses)
        return cls._rdrxn_from_smileses(r_smileses, p_smileses)

    # endregion


if __name__ == "__main__":
    from rdkit.Chem import Draw
    res = RxnHandler.rdrxn_from_indigo_smiles("[Na+:1].[cH:2]1[cH:7][cH:6][cH:5][cH:4][cH:3]1.[ClH:8].[Na+].[Cl-]>>[Na+:1].[cH:2]1[cH:7][cH:6][cH:5][cH:4][cH:3]1.[ClH:8].[Na+:1].[Cl-:8] |f:1.2,3.4,6.7.8.9|")
