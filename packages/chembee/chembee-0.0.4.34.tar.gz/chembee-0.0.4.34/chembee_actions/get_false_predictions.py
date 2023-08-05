import numpy as np


def get_false_predictions(clf, X_data, y_true) -> list:
    """
    The get_false_predictions function returns a tuple of two lists. The first list contains the indices of false positive predictions, and the second list contains the indices of false negative predictions.

    Parameters: clf (sklearn classifier object) - A trained sklearn classifier object
                X_data (numpy array) - A numpy array containing feature data for each example in dataset
                y_data (numpy array) - A numpy array containing labels for each example in dataset

                Returns: tuple(list): Two lists, one with all indices where a false positive occured, and one with all indicies where a false negative occured

    :param clf: Used to store the classifier that is being used.
    :param X_data: Used to store the data that is used to make predictions with the classifier.
    :param y_data: Used to get the true values of the data.
    :return: A tuple containing two lists: false_pos and false_neg.

    :doc-author: Julian M. Kleber
    """

    y_pred = clf.predict(X_data)
    mask_1 = y_true == 0
    mask_2 = y_pred == 1
    false_pos = np.where(mask_1 * mask_2)[0]
    mask_1 = y_true == 1
    mask_2 = y_pred == 0
    false_neg = np.where(mask_1 * mask_2)[0]

    return false_pos.tolist(), false_neg.tolist()
