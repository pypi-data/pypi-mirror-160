import sys, os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chembee_config.benchmark.svc import SVClassifier
from chembee_config.benchmark.svc_poly import SVCPolyClassifier
from chembee_config.benchmark.spectral_clustering import SpectralClusteringClassifier
from chembee_config.benchmark.random_forest import RandomForestClassifier
from chembee_config.benchmark.naive_bayes import NaiveBayesClassifier
from chembee_config.benchmark.logistic_regression import LogisticRegressionClassifier
from chembee_config.benchmark.linear_regression import LinearRegressionClassifier
from chembee_config.benchmark.kmeans import KMeansClassifier
from chembee_config.benchmark.knn import KNNClassifier
from chembee_config.benchmark.mlp_classifier import NeuralNetworkClassifier
from chembee_config.benchmark.restricted_bm import RBMClassifier

from chembee_plotting.graphics import plotting_map_comparison
from file_utils import save_json_to_file, make_full_filename

import logging


logging.basicConfig(
    format="%(levelname)s:%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
    filename="chembee.log",
)

algorithms = [
    SVClassifier,
    SVCPolyClassifier,
    SpectralClusteringClassifier,
    RandomForestClassifier,
    NaiveBayesClassifier,
    LogisticRegressionClassifier,
    LinearRegressionClassifier,
    KMeansClassifier,
    KNNClassifier,
    NeuralNetworkClassifier,
    RBMClassifier,
]


def benchmark_standard(
    X,
    y,
    feature_names=["Feature 1", "Feature 2"],
    file_name="benchmark",
    prefix="plots/benchmarks",
    algorithms=algorithms,
    to_fit=True,
):

    metrics = {}
    for alg in algorithms:
        if alg is None:
            response_method = alg._response_method
        else:
            response_method = None
        try:
            metric = benchmark_algorithm_standard(
                alg,
                X,
                y,
                plot_function=plotting_map_comparison[len(alg.algorithms)],
                file_name="benchmark_" + alg.name,
                prefix=prefix,
                feature_names=feature_names,
                response_method=None,
                to_fit=to_fit,
            )
        except Exception as e:
            assert 1 == 2, str(e)
            logging.info("Could not fit classifier " + str(alg.name))
            logging.info(str(e))
            metric = None
        finally:
            continue
    file_name = make_full_filename(file_name=file_name, prefix=prefix)
    save_json_to_file(metrics, file_name=file_name)
    return metrics


def benchmark_cv_algorithms(
    algorithms: list,
    names: list,
    X: np.ndarray,
    y: np.ndarray,
    plot_function=plotting_map_comparison[1],
    file_name: str = "after_cv_benchmark",
    prefix: str = "plots/benchmarks/",
    feature_names: list = ["Feature 1", "Feature 2"],
    response_method: str = "predict",
    to_fit=True,
):
    """
    The benchmark_cv_algorithms function takes a list of algorithms and fits them to the data.
    It then plots the results using plot_cv_algorithms function.

    :param algorithms:list: Used to specify which algorithms to use in the benchmark.
    :param names:list: Used to specify the names of the algorithms.
    :param X:np.ndarray: Used to pass the data to be used for training and testing.
    :param y:np.ndarray: Used to pass the target variable.
    :param file_name:str="benchmark": Used to name the output file.
    :param prefix:str="benchmarks/": Used to specify the path to the directory where all benchmark plots are saved.
    :param feature_names:list=["Feature1": Used to label the x-axis of the plots.
    :param "Feature2"]: Used to Specify the name of the feature that is used for plotting.
    :param response_method:str="predict": Used to determine which method is used to generate the response.
    :param to_fit=True: Used to determine whether the model should be fitted before predicting or transforming.
    :param : Used to determine the method used to obtain the response from the model.
    :return: A list of metrics for each model.

    :doc-author: Julian M. Kleber
    """

    metrics_class = []
    models = []

    for i in range(len(algorithms)):

        clf = algorithms[i]
        name = names[i]
        file_name = name + file_name
        if to_fit:
            try:
                clf.fit(X, y)
            except:
                logging.info("Could not fit clf " + str(name))
        models.append(clf)
        if response_method == "predict":
            try:
                y_pred = clf.predict(X)
            except:
                logging.info("Could not predict results for" + str(name))
        elif response_method == "fit_predict":
            try:
                y_pred = clf.fit_predict(X, y)
            except:
                logging.info("Could not fit_predict results for" + str(name))
        elif response_method == "transform":
            try:
                y_pred = clf.transform(X)
            except:
                logging.info("Could not transform results for" + str(name))
        logging.info("Fitted model: " + str(name))

        try:
            plot_function(
                clf=clf,
                X=X,
                y=y,
                file_name=file_name,
                prefix=prefix,
                feature_names=feature_names,
                response_method=response_method,
            )
        except:
            logging.info("Could not plot name " + str(name))

    metrics = {k: v for k, v in zip(names, metrics_class)}
    return metrics


def benchmark_algorithm_standard(
    algorithm: list,
    X: np.ndarray,
    y: np.ndarray,
    plot_function: object(),
    file_name: str = "benchmark",
    prefix: str = "benchmarks/",
    feature_names: list = ["Feature 1", "Feature 2"],
    response_method: str = "predict",
    to_fit=True,
) -> dict:
    """
    The benchmark_algorithm_standard function takes a list of algorithms,
    a list of names for the algorithms, and a dataset (X and y),
    and returns an array of metrics. The function is meant to be used for standard algorithms and not cross validation
    objects. For cross_validation objects, choose the benchmark_cv object. The function also plots the results.

    :param algorithm:list: Used to store the algorithms that will be used in the benchmark.
    :param names:list: Used to pass the names of the algorithms that will be used in the plot.
    :param X:np.ndarray: Used to pass the data to the benchmark_algorithm_standard function.
    :param y:np.ndarray: Used to pass the target variable to the plot_roc_curve function.
    :param plot_function:object(): Used to pass a function to the benchmark_algorithm_standard function.
    :param file_name:str="benchmark": Used to define the name of the file that will be saved.
    :param prefix:str="benchmarks/": Used to specify the path where the plots will be saved.
    :param feature_names:list=["Feature1": Used to label the x-axis of the plot.
    :param "Feature2"]: Used to Specify the name of the feature that is used in the plot.
    :param response_method:str="predict": Used to determine the method used to generate a response from the model.
    :param to_fit=True: Used to tell the algorithm to fit the model before predicting.
    :param : Used to define the type of plot to be created.
    :return: A dictionary of metrics.

    :doc-author: Julian M. Kleber"""

    name = algorithm.name
    algorithms = algorithm.algorithms
    file_name = "benchmark_" + name
    metrics_class = []
    models = []
    for i in range(len(algorithm.titles)):

        clf = algorithms[i]
        if to_fit:
            clf = clf.fit(X, y)
        models.append(clf)
        if response_method == "predict":
            y_pred = clf.predict(X)
        elif response_method == "fit_predict":
            y_pred = clf.fit_predict(X, y)
        if response_method == "transform":
            y_pred = clf.transform(X)
        logging.info("Fitted model: " + str(algorithm.titles[i]))

    plot_function(
        models=models,
        titles=algorithm.titles,
        X=X,
        y=y,
        file_name=file_name,
        prefix=prefix,
        feature_names=feature_names,
        response_method=response_method,
    )

    metrics = {k: v for k, v in zip(algorithm.titles, metrics_class)}
    return metrics


# should refactor the above functions
def benchmark_algorithm(
    algorithms: list,
    X: np.ndarray,
    y: np.ndarray,
    plot_function: object(),
    file_name: str = "benchmark",
    prefix: str = "benchmarks/",
    feature_names: list = ["Feature 1", "Feature 2"],
    response_method: str = "predict",
    to_fit=True,
) -> dict:
    """
    This function is not used in production at the moment and serves as a draft on how to abstract the functions above,
    to refactor the code and make it more maintainable.
    The benchmark_algorithm function is used to benchmark the performance of a given algorithm.
    It takes as input an algorithm, and returns a dictionary containing the metrics for that algorithm.
    The function is designed to be called within a loop, so that it can be used to compare multiple algorithms at once.

    :param algorithm: Used to specify the algorithm to use.
    :param X:np.ndarray: Used to pass the data to be used for training and testing.
    :param y:np.ndarray: Used to pass the target variable to the plot_roc_curve function.
    :param plot_function:object(): Used to pass a function that plots the results.
    :param file_name:str="benchmark": Used to name the plot file.
    :param prefix:str="benchmarks/": Used to specify the path to store the generated plots.
    :param feature_names:list=["Feature1": Used to name the columns of the dataframe.
    :param "Feature2"]: Used to Specify the names of the features in your dataset.
    :param response_method:str="predict": Used to determine whether the models should be used to predict the response or transform it.
    :param to_fit=True: Used to fit the model to the data.
    :param : Used to specify the name of the file to which we want to save our plots.
    :return: A dictionary with the following keys:.

    :doc-author: Julian M. Kleber
    """

    clf = algorithms[i]
    if to_fit:
        clf = clf.fit(X, y)
    if response_method == "predict":
        y_pred = clf.predict(X)
    elif response_method == "fit_predict":
        y_pred = clf.fit_predict(X, y)
    elif response_method == "transform":
        y_pred = clf.transform(X)
    else:
        logging.info("No valid response method")
    logging.info("Fitted model: " + str(algorithm.titles[i]))

    metrics = {k: v for k, v in zip(algorithm.titles, metrics_class)}
    return metrics
