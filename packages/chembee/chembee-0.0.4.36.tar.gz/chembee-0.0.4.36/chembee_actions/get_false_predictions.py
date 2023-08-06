import numpy as np


def get_data_impurities(fitted_clf, X_data, y_true, n=6) -> list:
    """
    The get_data_impurities function takes a classifier, the data and true labels. It returns two lists of column names:
    the first list is the false positive columns, and the second list is the false negative columns. The function also takes an
    optional argument n which defaults to 6. This means that if there are more than 6 impurities in either category (false positives or negatives) then only
    the first six will be returned.

    :param clf: Used to store the classifier that is used to make predictions.
    :param X_data: Used to get the data that is used to train and test the model.
    :param y_true: Used to Get the true labels of the data.
    :param n=6: Used to Specify the number of false positive and negative values to be returned.
    :return: A list of two lists.

    :doc-author: Trelent
    """

    false_pos_col = []
    false_neg_col = []
    for i in range(n):
        false_neg, false_pos = get_false_predictions(
            fitted_clf=fitted_clf, X_data=X_data, y_true=y_true
        )
        false_pos_col.append(false_pos)
        false_neg_col.append(false_neg)
    false_pos = np.unique(false_pos_col).tolist()
    false_neg = np.unique(false_neg_col).tolist()
    return [false_pos, false_neg]


def get_false_predictions(fitted_clf, X_data, y_true) -> list:
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

    y_pred = fitted_clf.predict(X_data)
    mask_1 = y_true == 0
    mask_2 = y_pred == 1
    false_pos = np.where(mask_1 * mask_2)[0]
    mask_1 = y_true == 1
    mask_2 = y_pred == 0
    false_neg = np.where(mask_1 * mask_2)[0]

    return false_pos.tolist(), false_neg.tolist()
