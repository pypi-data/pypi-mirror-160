# want to do with ROC check: https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html#sphx-glr-auto-examples-model-selection-plot-roc-crossval-py
# making own scoring: https://scikit-learn.org/stable/modules/cross_validation.html
# Want to do Stratified k-fold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.metrics import accuracy_score

# algorithm

# cross validation parameters
import logging


logging.basicConfig(
    format="%(levelname)s:%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
    filename="chembee_actions.log",
)


def screen_cross_validation_grid_search(
    scores, clf_list, X_train, X_test, y_train, y_test, refit
) -> tuple:

    fitted_clf = {}
    result_clf = []
    for alg in clf_list:
        logging.info("Performing Grid search CV for" + str(alg.name))
        clf, report, best_parameters, best_index = cross_validation_grid_search(
            scores, alg, X_train, X_test, y_train, y_test, refit=refit
        )

        result = {
            "report": report,
            "best_parameters": best_parameters,
            "best_index": best_index,
        }
        fitted_clf[alg.name] = result
        result_clf.append(clf)
    return fitted_clf, result_clf


def cross_validation_grid_search(
    scores: list, clf, X_train, X_test, y_train, y_test, refit
) -> tuple:
    """
    The cross_validation_grid_search function takes in a list of scores, the classifier,
    the training data and labels, the test data and labels. It then performs a grid search
    on all hyperparameters for each score in scores using cross-validation on the training set.
    It returns a dictionary with keys as each score name and values as another dictionary with
    keys 'best_params' (a list of best parameters) 'best_score' (the best average cross-validation
    score), 'train_accuracy' (training accuracy on entire training set), 'test_accuracy'(testing accuracy
    on test set). The function also prints out all results.

    :param scores:list: Used to Specify the metrics that we want to use for evaluating our model.
    :param clf: Used to Pass the classifier that will be used in cross validation.
    :param X_train: Used to Train the algorithm.
    :param X_test: Used to Test the model on unseen data.
    :param y_train: Used to Fit the model.
    :param y_test: Used to Calculate the accuracy of the model.
    :param refit: Used to Choose the best model from the grid search.
    :return: The best parameters and the best estimator.

    :doc-author: Trelent
    """

    clf = GridSearchCV(clf, clf.hyperparameters, scoring=scores, n_jobs=-1, refit=refit)
    clf.fit(X_train, y_train)

    return clf, clf.cv_results_, clf.best_params_, clf.best_index_


def stratified_n_fold(clf, X_data, y_data, n=5, cut_off_filter=None) -> dict:
    """
    The stratified_n_fold function takes a classifier, training data and labels, and returns the average accuracy of the classifier on each fold.
    The function also takes an optional cut_off_filter parameter that allows you to filter out features with low variance.

    :param clf: Used to pass in the classifier that will be used.
    :param X_data: Used to pass the data to be used for training and testing.
    :param y_data: Used to specify the labels of the data.
    :param n=5: Used to specify the number of folds.
    :param cut_off_filter=None: Used to filter the data.
    :return: A dictionary with two lists: accuracies_train and accuracies_test.

    :doc-author: Julian M. Kleber
    """
    # Run classifier with cross-validation and plot ROC curves
    cv = StratifiedKFold(n_splits=n)
    accuracies_test = []
    accuracies_train = []
    for i, (train, test) in enumerate(cv.split(X_data, y_data.astype(np.int32))):

        clf.fit(X_data[train], y_data.astype(np.int32)[train])
        y_pred = clf.predict(X_data[test])
        score = accuracy_score(y_pred, y_data.astype(np.int32)[test])
        accuracies_test.append(float(score))
        y_pred = clf.predict(X_data[train])
        score = accuracy_score(y_pred, y_data.astype(np.int32)[train])
        accuracies_train.append(float(score))

    result = {"accuracies_train": accuracies_train, "accuracies_test": accuracies_test}

    return result


def stratified_n_fold_filter(clf, X_data, y_data, n=5, cut_off_filter=None) -> dict:
    """
    The stratified_n_fold_filter function takes in a classifier, training data and labels, and returns the average accuracy of the classifier on each fold. Additionally it also returns a list of indices that were filtered out due to having an accuracy below some cut_off_filter value.
    Note: To be SOLID and avoid weird code as well as performance issues the function, stratified_n_fold is basically implemented twice. One with and one time without a filter.
    :param clf: Used to pass the classifier that should be used.
    :param X_data: Used to pass the data to be used for training and testing.
    :param y_data: Used to determine the number of classes.
    :param n=5: Used to specify the number of folds in the stratifiedkfold function.
    :param cut_off_filter=None: Used to filter out the indices of the test set that have a lower accuracy than cut_off_filter.
    :return: A dictionary with the following keys:.

    :doc-author: Julian M. Kleber
    """

    cv = StratifiedKFold(n_splits=n)
    accuracies_test = []
    accuracies_train = []
    filtered_indices = []
    for i, (train, test) in enumerate(cv.split(X_data, y_data.astype(np.int32))):
        clf.fit(X_data[train], y_data.astype(np.int32)[train])
        y_pred = clf.predict(X_data[test])
        score = accuracy_score(y_pred, y_data.astype(np.int32)[test])
        accuracies_test.append(float(score))
        y_pred = clf.predict(X_data[train])
        score = accuracy_score(y_pred, y_data.astype(np.int32)[train])
        accuracies_train.append(float(score))
        if cut_off_filter != None:
            if score < cut_off_filter:
                filtered_indices.append(test)
    if len(filtered_indices) < 1:
        filtered_indices = None
    result = {
        "accuracies_train": accuracies_train,
        "accuracies_test": accuracies_test,
        "filtered_indices": filtered_indices,
    }

    return result
