import matplotlib.pyplot as plt
import pandas as pd

from sklearn.inspection import DecisionBoundaryDisplay
from file_utils import prepare_file_name_saving

# set the standard parameters

plt.rcParams["font.size"] = "20"
plt.tight_layout()


def plot_comparison_4(
    models,
    titles,
    X,
    y,
    prefix=None,
    file_name="SVC_benchmark",
    feature_names=["Feature 1", "Feature 2"],
    response_method="predict",
):
    """
    The plot_comparision_4 function plots the decision boundaries for a set of models.
    It takes as input:
    - models: A list of scikit learn model objects.  Each model object must have a .predict method that takes in an array of features and returns predictions based on those features.  The plot_comparision_4 function uses these predictions to create the decision boundary for each model, and then plots them together in a single figure.
    - titles: A list with one element for each element in 'models'.  Each string is used to label the corresponding plot's legend, so make sure that they are unique!
    - X: An array containing feature values used to train/evaluate the models passed via 'models'.   These feature values should be scaled between 0 and 1 (if not already done).   The first two columns should correspond to x coordinates while the second two columns should correspond to y coordinates (i.e., this is an Nx4 matrix).  This argument corresponds directly with what you would pass into plt.scatter(...), so if you have already scaled your data, then just pass it here without re-scaling it!
    - y: An array containing labels corresponding with observations contained within X (i.e., this

    :param models: Used to Pass a list of models that should be compared.
    :param titles: Used to Give a name to each model in the plot.
    :param X: Used to Define the data that will be used for training and testing.
    :param y: Used to Define the target variable.
    :param prefix=None: Used to Define a string that will be added to the name of the file when it is saved.
    :param file_name="SVC_benchmark": Used to Save the plot as an image.
    :param feature_names=["Feature1": Used to Specify the labels for the x and y axis.
    :param "Feature2"]: Used to Specify which feature is used for the x-axis.
    :return: The subplot of the models.

    :doc-author: Trelent
    """

    fig, sub = plt.subplots(2, 2, figsize=(20, 13))
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    make_comparison_plot(
        fig=fig,
        sub=sub,
        models=models,
        titles=titles,
        X=X,
        y=y,
        file_name=file_name,
        feature_names=feature_names,
        prefix=prefix,
        response_method=response_method,
    )


def plot_comparison_3(
    models,
    titles,
    X,
    y,
    prefix=None,
    file_name="SVC_benchmark",
    feature_names=["Feature 1", "Feature 2"],
    response_method="predict",
):
    """
    The plot_comparison_3 function creates a 3x3 grid of plots, each comparing the performance of a different model.
    The models are passed in as an array and their titles as another array. The X and y data is also required to generate
    the plots. The function will automatically save the plot to file_name + .png in your current working directory unless
    otherwise specified using prefix = "". If you would like to save multiple comparisons, simply call this function once with
    different sets of parameters.

    :param models: Used to pass the models that are to be compared.
    :param titles: Used to set the title of each plot.
    :param X: Used to pass the data.
    :param y: Used to specify the target variable.
    :param prefix=None: Used to pass a string to the plot_comparison_3 function.
    :param file_name="SVC_benchmark": Used to name the file that will be saved in your directory.
    :param feature_names=["Feature1": Used to specify the names of the features in x.
    :param "Feature2"]: Used to Specify the name of the feature that will be plotted on the y-axis.
    :param response_method="predict": Used to specify the method used to generate the response.
    :param : Used to specify the type of response.
    :return: A dictionary with the trained models.

    :doc-author: Julian M. Kleber
    """

    fig, sub = plt.subplots(1, 3, figsize=(20, 13))
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    make_comparison_plot(
        fig=fig,
        sub=sub,
        models=models,
        titles=titles,
        X=X,
        y=y,
        file_name=file_name,
        feature_names=feature_names,
        prefix=prefix,
        response_method=response_method,
    )


def plot_comparison_2():
    raise NotImplementedError()


def plot_comparison_1(
    clf,
    X,
    y,
    prefix=None,
    file_name="SVC_benchmark",
    feature_names=["Feature 1", "Feature 2"],
    response_method="predict",
):
    """
    The plot_comparison_1 function creates a plot of the decision boundary for a given classifier.
    It takes as input:
    - clf, which is an instance of sklearn's SVC class with default parameters (except for C and gamma)
    - X, which is the feature matrix containing all training samples in rows and their features in columns.
    The number of columns must be equal to two because this function plots each sample as a point on the xy-plane.
    This function assumes that there are only two features in X (i.e., it can only plot 2D decision boundaries).
    If you want to use more than two features, then you need to reduce your data set so that it contains only 2D points!

        - y, which is the vector containing all labels corresponding to each training sample from X

        - prefix=None: A string indicating what should be printed before file_name when saving files; if None or empty string then no prefix will be added

        - file_name="SVC_benchmark": The name used when saving files; if None or empty string then no file will be saved but instead everything will simply get plotted on screen using plt.show()

        - feature_names=

    :param clf: Used to pass the classifier to be used.
    :param X: Used to specify the features that are used to train the model.
    :param y: Used to specify the class labels.
    :param prefix=None: Used to specify a prefix for the file name.
    :param file_name="SVC_benchmark": Used to save the plot as a png file.
    :param feature_names=["Feature1": Used to set the labels on the x and y axis.
    :param "Feature2"]: Used to set the name of the second feature.
    :param response_method="predict": Used to specify that the.
    :param : Used to set the title of the plot.
    :return: The decision boundary plot of the svc model.

    :doc-author: Julian M. Kleber
    """
    plt.rcParams["font.size"] = "35"
    X0, X1 = X[:, 0], X[:, 1]
    fig, ax = plt.subplots(1, 1, figsize=(20, 13))
    disp = DecisionBoundaryDisplay.from_estimator(
        clf,
        X,
        response_method=response_method,
        cmap=plt.cm.coolwarm,
        alpha=0.7,
        ax=ax,
        xlabel=feature_names[0],
        ylabel=feature_names[1],
    )
    plt.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, edgecolors="k")
    ax.set_xticklabels(())
    ax.set_yticklabels(())

    file_name = prepare_file_name_saving(
        prefix=prefix, file_name=file_name, ending=".png"
    )
    fig.savefig(file_name)
    plt.cla()
    plt.clf()
    plt.close()


def make_comparison_plot(
    fig,
    sub,
    models,
    titles,
    X,
    y,
    prefix=None,
    file_name="SVC_benchmark",
    feature_names=["Feature 1", "Feature 2"],
    response_method="predict",
):
    """
    The make_comparison_plot function creates a plot comparing the decision boundaries of several models.
    It takes as input:
        - fig, a matplotlib figure object to be saved to file (figsize=(12,8))
        - sub, an array of axes objects on which plotting will occur (nrows=2, ncols=3)
        - models: an array of sklearn classifiers for which decision boundaries will be plotted.
            Note that these must have been fitted already with fit()!

        The function then creates plots comparing the decision boundary and prediction values for each model in turn.

        It returns nothing.

    :param fig: Used to pass the figure object to which we want to plot.
    :param sub: Used to create a subplot grid.
    :param models: Used to pass the classifiers that will be used in the plot.
    :param titles: Used to set the title of each subplot.
    :param X: Used to pass the data to be plotted.
    :param y: Used to specify the response variable.
    :param prefix=None: Used to make sure that the file_name is saved in the current working directory.
    :param file_name="SVC_benchmark": Used to create a file_name for the plot.
    :param feature_names=["Feature1": Used to label the axes of the plot.
    :param "Feature2"]: Used to specify the name of the x and y axis.
    :return: A plot of the decision boundaries for a set of classifiers.

    :doc-author: Julian M. Kleber
    """

    X0, X1 = X[:, 0], X[:, 1]

    for clf, title, ax in zip(models, titles, sub.flatten()):
        disp = DecisionBoundaryDisplay.from_estimator(
            clf,
            X,
            response_method=response_method,
            cmap=plt.cm.coolwarm,
            alpha=0.7,
            ax=ax,
            xlabel=feature_names[0],
            ylabel=feature_names[1],
        )
        ax.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, edgecolors="k")
        ax.set_xticks(())
        ax.set_yticks(())
        ax.set_title(title)

    file_name = prepare_file_name_saving(
        prefix=prefix, file_name=file_name, ending=".png"
    )
    fig.savefig(file_name)
    plt.cla()
    plt.clf()
    plt.close()


def save_fig(ax, name: str, save_path=None, dpi=300):
    """Frequently used snippet to save a plot

    Args:
        ax ([type]): Seaborn axis
        name (str): Name of the plot
        save_path ([type], optional): Where to save the plot. Defaults to None:str.
        dpi (int, optional): Resolution of the plot. Defaults to 300.

    Returns:
        (None)
    """
    if save_path is None:
        save_path = name
    else:
        save_path.joinpath(name)
    fig = ax.get_figure()
    fig.savefig(save_path, dpi=dpi)
    plt.cla()
    plt.clf()
    plt.close()
    return None


plotting_map_comparison = {
    1: plot_comparison_1,
    2: plot_comparison_2,
    3: plot_comparison_3,
    4: plot_comparison_4,
}
if __name__ == "__main__":

    data = pd.read_csv("converted_data.csv")
    biodeg = data[data["ReadyBiodegradability"] == 1]
    n_biodeg = data[data["ReadyBiodegradability"] == 0]
    polar_plot(biodeg, name="BiodegPolar.png")
    polar_plot(n_biodeg, name="NBiodegPolar.png")
