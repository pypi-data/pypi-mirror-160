from chembee_datasets.DataSet import DataSet
import pandas as pd
from sklearn.model_selection import train_test_split
from rdkit import Chem
from rdkit.Chem import (
    PandasTools,
)

from file_utils import prepare_file_name_saving


class BioDegDataSet(DataSet):

    name = "biodeg"

    def __init__(self, data_set_path, target, split_ratio=0.7):

        self.data, self.mols = self.load_data_set(data_set_path)
        self.split_ratio = split_ratio
        (
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test,
        ) = self.make_train_test_split(self.data, self.split_ratio, y_col=target)

        self.feature_names = self.get_feature_names(self.data, target=target)

    def clean_data(self, data):
        """
        The clean_data function takes in a dataframe and cleans it by removing the SMILES, CASRN, ID and Dataset columns.
        It also converts all of the dtypes to float64 or int64. It returns a cleaned dataframe.

        :param self: Used to Reference the class itself.
        :param data: Used to Pass the data that is to be cleaned.
        :return: A dataframe with the columns "smiles", "dataset", "casrn" and "id" dropped, and all other columns converted to numeric type.

        :doc-author: Trelent
        """

        data = data.drop(columns=["SMILES", "Dataset", "CASRN", "ID"])
        data = data.convert_dtypes()
        bad_types = data.select_dtypes(
            exclude=["string", "int64", "float64"]
        ).columns.to_list()
        data = data.drop(columns=bad_types)
        return data

    def load_data_set(self, file_name: str):
        """
        The load_data function loads the data from a sdf file and returns it as a Pandas DataFrame.

        :param file_path:str: Used to Specify the location of the.
        :return: A dataframe with the following columns:.

        :doc-author: Trelent
        """
        mols = Chem.SDMolSupplier(file_name)
        frame = PandasTools.LoadSDF(
            file_name,
            smilesName="SMILES",
            molColName="Molecule",
            includeFingerprints=True,
            removeHs=False,
            strictParsing=True,
        )
        return frame, mols

    def load_data_set_from_csv(self, file_name: str) -> pd.DataFrame:
        """
        The load_data_set_from_csv function loads a csv file into a pandas dataframe.
        The function's purpose is to improve readability. Nothing special
        The function takes one argument, the name of the csv file to be loaded.
        The function returns a pandas dataframe containing all of the information in
        the specified csv file.

        :param self: Used to Access variables that belongs to the class.
        :param file_name:str: Used to Specify the name of the csv file that will be used to load data from.
        :return: A pandas data frame.

        :doc-author: Julian M. Kleber
        """

        return pd.from_csv(file_name)

    def make_train_test_split(self, data, split_ratio: float, y_col: str, shuffle=True):
        """
        The make_train_test_split function splits the data into a training set and test set.
        The split_ratio parameter determines how much of the data is used for training, and how much is used for testing.
        The y_col parameter specifies which column in the dataset contains labels (y). The shuffle parameter allows you to specify whether or not to shuffle your data before splitting it into train/test sets.

        :param self: Used to Reference the class itself.
        :param data: Used to Specify the dataframe that is used for splitting.
        :param split_ratio:float: Used to Determine the ratio of data that will be used for training.
        :param y_col:str: Used to Specify the column name of the dependent variable.
        :param shuffle=True: Used to Shuffle the data before splitting it into training and testing sets.
        :return: The X_train, X_test, y_train and y_test dataframes.

        :doc-author: Julian M. Kleber
        """

        X = data.drop([y_col], axis=1)
        y = data[y_col]
        train_samples = int(split_ratio * len(X))
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            shuffle=shuffle,
            test_size=len(X) - train_samples,
        )
        return (
            X_train,
            X_test,
            y_train,
            y_test,
        )

    def save_data_csv(self, data: pd.DataFrame, file_name, prefix):
        """
        The save_data_csv function saves the data of the instance to a csv file.

        :param self: Used to Access the attributes and methods of the class in python.
        :param data:pd.DataFrame: Used to Save the data that is passed to it.
        :param file_name: Used to Specify the name of the file to be saved.
        :param prefix: Used to Add a prefix to the file name.
        :return: The name of the file where the data was saved.

        :doc-author: Julian M. Kleber
        """

        assert type(data) == type(pd.DataFrame()), "Data must be a pandas.DataFrame"
        file_name = prepare_file_name_saving(
            prefix=prefix, file_name=file_name, ending=".csv"
        )
        data.to_csv(file_name)

    def save_data_sdf(self, data, file_name, prefix, molColName="Molecule"):
        """
        The save_data_sdf function saves the data in a pandas DataFrame to an sdf file.

        :param self: Used to access the attributes and methods of the class in a method.
        :param data: Used to specify the dataframe that is to be saved.
        :param file_name: Used to specify the name of the file to which data is saved.
        :param prefix: Used to add a prefix to the file name.
        :param molColName="Molecule": Used to specify the name of the molecule column in the sdf file.
        :return: A dataframe with the same number of rows as the input data and one column named "romol" containing a mol object.

        :doc-author: Julian M. Kleber
        """

        file_name = prepare_file_name_saving(
            prefix=prefix, file_name=file_name, ending=".sdf"
        )
        PandasTools.WriteSDF(
            data, file_name, molColName="Molecule", properties=list(data.columns)
        )

    def get_feature_names(self, data, target):
        """
        The get_feature_names function takes in a dataframe and returns the feature names.
        It does this by iterating through the columns of the dataframe and appending them to a list.
        The function then returns that list.

        :param self: Used to reference the class itself.
        :param data: Used to drop the target column from the dataframe.
        :param target: Used to determine if the function is being used for a training or testing set.
        :return: The names of the features.

        :doc-author: Trelent
        """

        if not target:
            data = data.drop(columns=[target])
        return data.columns.to_list()
