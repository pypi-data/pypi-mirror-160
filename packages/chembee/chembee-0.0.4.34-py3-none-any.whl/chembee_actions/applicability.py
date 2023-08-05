from pyADA import ApplicabilityDomain
import numpy as np


def get_applicability_domain(
    clf,
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    threshold_step=(0, 0.65, 0.05),
    similarity_metric="tanimoto",
    metric_evaluation="auc",
) -> dict:
    """
    The get_applicability_domain function takes as input a classifier, training and test data,
    and returns the applicability domain of the classifier. The function also takes in optional arguments
    for threshold_step (default is 0.05), similarity metric (default is tanimoto), and metric evaluation
    (default is AUC). The function outputs a dictionary with keys 'threshold', 'similarity', and 'metric'
    with corresponding values for each key. It depends on the pyADAqsar package and further documentation can be found there
    (https://github.com/jeffrichardchemistry/pyADA)

    :param clf: Used to Specify the classifier that will be used to evaluate the applicability domain.
    :param X_train: Used to Train the model.
    :param X_test: Used to Define the test set to be used for applicability domain construction.
    :param y_train: Used to Fit the model on.
    :param y_test: Used to Evaluate the performance of the classifier.
    :param threshold_step=(0: Used to Define the step size of the threshold.
    :param 0.65: Used to Define the threshold for the applicability domain.
    :param 0.05): Used to Define the step size of the threshold.
    :param similarity_metric="tanimoto": Used to Define the similarity metric that will be used to compute the applicability domain.
    :param metric_evaluation="auc": Used to Specify the metric used to evaluate the applicability domain.
    :param : Used to Define the threshold step.
    :return: A dictionary with the following keys:.

    :doc-author: Julian M. Kleber
    """

    ad = ApplicabilityDomain(verbose=True)
    result = ad.fit(
        model=clf,
        base_test=X_test,
        base_train=X_train,
        y_true=y_test,
        threshold_reference="max",
        threshold_step=threshold_step,
        similarity_metric="tanimoto",
        alpha=1,
        beta=1,
        metric_avaliation="auc",
    )
    return result
