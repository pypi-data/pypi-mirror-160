import pandas as pd
from mordred import Calculator, descriptors
import numpy as np

from rdkit import Chem
from rdkit.Chem import (
    Descriptors,
    Descriptors3D,
    rdMolDescriptors,
    PandasTools,
    RDKFingerprint,
)
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect

# Utilities
import os
from tqdm import tqdm


def calculate_mordred_descriptors(mols: list) -> pd.DataFrame:
    """
    The calculate_mordred_descriptors function calculates Mordred descriptors for a set of molecules.
    The function takes as input a list of RDKit molecule objects and returns the calculated descriptors in
    a pandas dataframe.

    :param mols: Used to specify the molecules for which descriptors are to be calculated.
    :param : Used to specify the calculation of 3d descriptors.
    :return: A pandas dataframe containing the calculated descriptors.

    :doc-author: Julian M. Kleber
    """

    calc = Calculator(descriptors, ignore_3D=False)
    data = calc.pandas(mols)
    return data


def calculate_lipinski_desc(data_set: pd.DataFrame, mols: pd.Series) -> pd.DataFrame:
    """
    The calculate_lipinski_desc function calculates the molecular descriptors for each molecule in a data set.
    The function takes two arguments:
        1) data_set - A pandas DataFrame containing the SMILES strings of each molecule in a data set.
        2) mols - A pandas Series containing the RDKit Mol object of each molecule in a data set.

    The function returns one value:
        1) The original DataFrame with additional columns for each descriptor, which contain floats.

    :param data_set:pd.DataFrame: Used to Store the calculated descriptors.
    :param mols:pd.Series: Used to Pass a series of molecules to the function.
    :return: A dataframe with the descriptors for each molecule in the mols series.

    :doc-author: Trelent
    """

    for i, mol in tqdm(enumerate(mols)):
        Chem.SanitizeMol(mol)
        data_set.loc[i, "Molecule"] = mol
        data_set.loc[i, "MolWt"] = Descriptors.MolWt(mol)
        data_set.loc[i, "LogP"] = Descriptors.MolLogP(mol)
        data_set.loc[i, "NumHAcceptors"] = Descriptors.NumHAcceptors(mol)
        data_set.loc[i, "NumHDonors"] = Descriptors.NumHDonors(mol)
        data_set.loc[i, "NumHeteroatoms"] = Descriptors.NumHeteroatoms(mol)
        data_set.loc[i, "NumRotatableBonds"] = Descriptors.NumRotatableBonds(mol)
        data_set.loc[i, "NumHeavyAtoms"] = Descriptors.HeavyAtomCount(mol)
        data_set.loc[
            i, "NumAliphaticCarbocycles"
        ] = Descriptors.NumAliphaticCarbocycles(mol)
        data_set.loc[
            i, "NumAliphaticHeterocycles"
        ] = Descriptors.NumAliphaticHeterocycles(mol)
        data_set.loc[i, "NumAliphaticRings"] = Descriptors.NumAliphaticRings(mol)
        data_set.loc[i, "NumAromaticCarbocycles"] = Descriptors.NumAromaticCarbocycles(
            mol
        )
        data_set.loc[
            i, "NumAromaticHeterocycles"
        ] = Descriptors.NumAromaticHeterocycles(mol)
        data_set.loc[i, "NumAromaticRings"] = Descriptors.NumAromaticRings(mol)
        data_set.loc[i, "RingCount"] = Descriptors.RingCount(mol)
        data_set.loc[i, "FractionCSP3"] = Descriptors.FractionCSP3(mol)

        data_set.loc[i, "TPSA"] = Descriptors.TPSA(mol)
        data_set.loc[i, "NPR1"] = rdMolDescriptors.CalcNPR1(mol)
        data_set.loc[i, "NPR2"] = rdMolDescriptors.CalcNPR2(mol)
        data_set.loc[i, "InertialShapeFactor"] = Descriptors3D.InertialShapeFactor(mol)
        data_set.loc[i, "RadiusOfGyration"] = Descriptors3D.RadiusOfGyration(mol)
    return data_set


def convert_mols_to_rdk_fp(mols, return_bit=False):
    """
    The convert_mols_to_rdkfingerprint function converts a list of RDKit molecules into a list of RDKit fingerprints.

    :param mols: Used to pass the molecules that are to be converted into fingerprints.
    :return: A list of rdkit fingerprints.

    :doc-author: Julian M. Kleber
    """
    if return_bit:
        fps = [np.array(RDKFingerprint(x)).tolist() for x in mols]
    else:
        fps = [RDKFingerprint(x) for x in mols]
    return fps


def convert_mols_to_morgan_fp(mols, radius=3, n_bits=2048, return_bit=False):
    """
    The convert_mols_to_morgan_fp function converts a list of molecules to their Morgan fingerprints.

    :param mols: Used to specify the molecules that are to be converted into Morgan fingerprints.
    :param radius=3: Used to determine the number of bits that will be used to represent each molecule.
    :param n_bits=2048: Used to determine the number of bits in the Morgan fingerprint.
    :return: A list of fingerprints.

    :doc-author: Julian M. Kleber
    """
    if return_bit:
        fps = [
            GetMorganFingerprintAsBitVect(
                np.array(x).tolist(),
                useChirality=True,
                useFeatures=True,
                radius=radius,
                nBits=n_bits,
            )
            for x in mols
        ]
    else:
        fps = [
            GetMorganFingerprintAsBitVect(
                x, useChirality=True, useFeatures=True, radius=radius, nBits=n_bits
            )
            for x in mols
        ]
    return fps


def convert_mol_to_inchi(mols):
    """
    The convert_mol_to_inchi function converts a molecule into an InChI string.

    :param mol: Used to pass the molecule to the function.
    :return: A tuple of the inchi and inchikey.

    :doc-author: Julian M. Kleber
    """

    from rdkit import Chem

    inchis = []
    inchikeys = []
    for mol in mols:
        inchis.append(str(Chem.MolToInchi(mol)))
        inchikeys.append(str(Chem.MolToInchiKey(mol)))

    return inchis, inchikeys


def get_mols_from_supplier(indices, supplier):
    """
    The get_mols_from_supplier function takes a list of indices and a supplier object,
    and returns the molecules corresponding to those indices.

    :param indices: Used to specify which molecules to retrieve from the supplier.
    :param supplier: Used to specify the supplier of the molecules.
    :return: A list of molecules.

    :doc-author: Julian M. Kleber
    """

    mols = []
    for indx in indices:
        mol = supplier[indx]
        mols.append(mol)
    return mols


def load_data(file_path: str):
    """
    The load_data function loads the data from a file and returns it as a Pandas DataFrame.

    :param file_path:str: Used to specify the location of the.
    :return: A dataframe with the columns specified by the sdf data entries

    :doc-author: Julian M. Kleber
    """

    sdfFile = os.path.join(file_path)
    mols = Chem.SDMolSupplier(sdfFile)
    frame = PandasTools.LoadSDF(
        sdfFile,
        smilesName="SMILES",
        molColName="Molecule",
        includeFingerprints=True,
        removeHs=False,
        strictParsing=True,
    )
    frame = calculate_lipinski_desc(data_set=frame, mols=mols)
    return frame


if __name__ == "__main__":
    from utils import save_csv

    data = load_data("tests/data/Biodeg.sdf")
    save_csv(data, "converted_data.csv")
