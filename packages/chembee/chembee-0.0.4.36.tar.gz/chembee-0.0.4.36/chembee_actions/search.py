import numpy as np


def get_top_n_similar_compounds(similarities: list, n: int = 10, labels=None):
    """
    The get_top_n_similar_compounds function takes in a list of similarities and returns the top n similar compounds.
    The function takes in a list of similarities, sorts it, and then returns the top n most similar compounds.

    :param similarities:list: Used to pass in the list of similarities for each compound.
    :param n:int=10: Used to Specify the number of similar compounds to return.
    :return: The top n similar compounds for a given compound, for each similarity list

    :doc-author: Julian M. Kleber
    """
    if labels != None:
        assert len(labels) == len(similarities)
    similar_compounds_screen = {}
    for i, sims in enumerate(similarities):
        similar_compounds = np.argpartition(similarities, -n)[-n:].tolist()
        if labels != None:
            similar_compounds_screen[labels[i]] = labels
    return similar_compounds_screen


def get_similar_compounds(
    compounds_of_interest: np.ndarray,
    compounds: np.ndarray,
    distance="tanimoto",
    return_sim_matrix=True,
) -> dict:
    """
    The get_similar_compounds function takes a list of compounds and returns the n most similar compounds.
    The similarity is calculated by calculating a user defined distance metric between two compound vectors.
    The function works on arbitrary data and features. It could also take in vectorized fingerprints. The function
    is written as such that it could return the most similar compounds that are the same as the search compounds. You
    would have to exclude them manually. Still, the function is experimental and if you feel handling the exlusion of
    of identical compounds inside of this function is neccessary, please file an issue, or feature request.

    :param compounds_of_interest: Used to specify the compounds that we want to find similar compounds for.
    :param compounds: Used to store the similarity scores for each compound.
    :param n=10: Used to specify the number of similar compounds to return. Specify n='all' if you want to return all coumpounds
    :return: A dictionary containing the jsonified result, ready to use in web tech like MongoDB, Flask, React, etc., and another dictionary cointaining the complete similarity matrix

    :doc-author: Julian M. Kleber
    """
    from pyADA import ApplicabilityDomain

    AD = ApplicabilityDomain(verbose=True)
    sims = AD.analyze_similarity(
        base_train=compounds,
        base_test=compounds_of_interest,
        similarity_metric=distance,
    )
    if return_sim_matrix:
        return sims.to_dict(), AD.similarities_table_.to_dict()
    else:
        return sims.to_dict()


def screen_fingerprints_against_data(to_screen, base) -> dict:
    """
    The screen_fingerprints_against_data function takes two arguments: a list of fingerprints to screen, and a list of
    fingerprints against which the first argument will be screened. The function returns a dictionary with keys that are
    the fingerprint names in the first argument, and values that are lists containing the similarity scores for each molecule
    in the second argument. For example:

        >>>screen_fingerprints_against_data([FP11, FP12], [FP21, FP22])

        {1: {similarityScores: [0.24, 0.6], fingerPrint: FP11}, 2: {similarityScores: [0.1, 0.42], fingerPrint: FP12}}

    :param to_screen: Used to specify the fingerprints to be screened against the base.
    :param base: Used to define the set of molecules to compare against.
    :return: A dictionary with the similarity scores of the fingerprints in to_screen against all of the fingerprints in base.

    :doc-author: Julian M. Kleber
    """
    from rdkit.DataStructs import FingerprintSimilarity

    result = {}
    for count, probe in enumerate(to_screen):
        result[count] = {}
        sim = []
        for mol in base:
            sim.append(FingerprintSimilarity(probe, mol))
        result[count]["simalarityScores"] = sim
        result[count]["fingerPrint"] = probe
    return result


def get_similar_compounds_structure(
    compounds_of_interest, compounds, n=10, distance="tanimoto"
) -> dict:
    """
    The get_similar_compounds_structure function takes a list of compounds and returns the most similar compounds based on structure.
    The function takes in four arguments:

        1) A list of compound names (compounds_of_interest),
        2) A dataframe containing all the other compounds (compounds), and
        3) An integer n that specifies how many similar compounds to return. The default is 10.
        4) A distnace

    The function returns a dictionary with three keys: "InChi", "number" and "similarity". Number corresponds to the index number for each compound, while similarity contains their similarity score.

    :param compounds_of_interest: Used to Specify the compounds for which similar compounds are to be found.
    :param compounds: Used to Get the structure of all compounds in the database.
    :param n=10: Used to Specify how many similar compounds we want to find.
    :param distance="Tanimoto": Used to Specify the similarity metric to be used.
    :return: A dictionary with the following keys:.

    :doc-author: Julian M. Kleber
    """
    raise NotImplementedError(
        "Either implement with RDKit or just convert a fingerprint to a dataframe"
    )
    for i in range(len(compounds_of_interest)):
        compound = compounds_of_interest[i]
        similarity = calculate_similarity(compound, compounds, n=10)
        compounds["number"] = i
        compounds["similarity"] = similarity
        compounds["InChI"] = inchi
    return compounds
