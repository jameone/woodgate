"""
external_datasets.py - The
external_datasets.py module
contains the DatasetsConfiguration class definition.
"""
import os
import json
from typing import List, Set, Dict, Union, Any
# TODO - Remove dependency on Pandas
import pandas as pd
from ..woodgate_settings import FileSystem


class ExternalDatasets:
    """
    ExternalDatasets - The ExternalDataset class encapsulates
    logic related to training, testing, evaluation, and
    regression datasets.
    """

    #: The `training_dataset_id` attribute represents the
    #: location of the training dataset. This attribute should be
    #: a valid ID and accessible via the web. The
    #: ID will be passed to the DatasetRetrievalStrategy class
    #: whose corresponding retrieve method will be responsible
    #: for using the ID to download a copy of the dataset.
    training_dataset_id: str = os.getenv(
        "TRAINING_DATASET_ID",
        "1OlcvGWReJMuyYQuOZm149vHWwPtlboR6"
    )

    #: The `testing_dataset_id` attribute represents the
    #: location of the testing dataset. This attribute should be
    #: a valid ID and accessible via the web. The ID will be
    #: passed to the DatasetRetrievalStrategy class whose
    #: corresponding retrieve method will be responsible for
    #: using the ID to download a copy of the dataset.
    testing_dataset_id: str = os.getenv(
        "TESTING_DATASET_ID",
        "1ep9H6-HvhB4utJRLVcLzieWNUSG3P_uF"
    )

    #: The `evaluation_dataset_id` attribute represents the
    #: location of the evaluation dataset. This attribute should
    #: be a valid ID and accessible via the web. The ID will be
    #: passed to the DatasetRetrievalStrategy class whose
    #: corresponding retrieve method will be responsible for
    #: using the ID to download a copy of the dataset.
    evaluation_dataset_id: str = os.getenv(
        "EVALUATION_DATASET_ID",
        "1Oi5cRlTybuIF2Fl5Bfsr-KkqrXrdt77w"
    )

    #: The `regression_dataset_id` attribute represents the
    #: location of the regression dataset. This attribute should
    #: be a valid ID and accessible via the web. The ID will be
    #: passed to the DatasetRetrievalStrategy class whose
    #: corresponding retrieve method will be responsible for
    #: using the ID to download a copy of the dataset.
    regression_dataset_id: str = os.getenv(
        "REGRESSION_DATASET_ID",
        "1Oi5cRlTybuIF2Fl5Bfsr-KkqrXrdt77w"
    )

    #: The `training_data` attribute represents the fine
    #: tuning data designated as "training data". This dataset
    #: is used to tune the hyper-parameters during the evaluator
    #: training iterations. This dataset should be a CSV file
    #: having a `.csv` file extension and contain at least two
    #: (2) columns, one (1) for `text` i.e. the user phrase
    #: (labelled fine_tuning_text_processor.data_column_title)
    #: , and one (1) for `label` i.e. the intent (labelled
    #: fine_tuning_text_processor.label_column_title)
    training_data: Union[pd.DataFrame, None] = None

    @classmethod
    def set_training_data(
            cls,
            file_system: FileSystem
    ) -> None:
        """This method will attempt to set the `training_data`
        attribute by reading the file located on the host
        file system at `$TRAINING_PATH` into a
        `pandas.DataFrame`. It is assumed the file located at
        `$TRAINING_PATH` is in CSV format and having a `.csv`
        file extension.


        :return: None
        :rtype: NoneType
        """
        cls.training_data = pd.read_csv(
            file_system.get_training_path()
        )

        return None

    @classmethod
    def get_training_data(
            cls
    ) -> pd.DataFrame:
        """This method is a simple getter which will return the
        `training_data` attribute. Be sure to call the
        `set_training_data` method or else the
        `training_data` attribute will be undefined.

        :return: This method returns the `training_data` \
        attribute.
        :rtype: pd.DataFrame
        """
        return cls.training_data

    #: The `training_intents_list` attribute represents a list
    #: of unique intents found in the `training_data`.
    #: By definition the `training_intents_list` attribute is
    #: a Python list of all unique values found in the column
    #: with title "intent" in the `training_data`
    #: dataframe.
    @classmethod
    def training_intents_list(
            cls
    ) -> List[str]:
        """This method calls the `get_training_data` method and
        then extracts unique values from the "intent" column. The
        resulting values are returned in a sorted Python list.

        :return: A list of unique intents found in training data.
        :rtype: List[str]
        """
        return sorted(
            cls.get_training_data().intent.unique().tolist()
        )

    #: The `training_set` attribute represents a set
    #: of unique intents found in the `training_data`.
    #: By definition the `training_set` attribute is
    #: a Python set of values found in the column
    #: with title "intent" in the `training_data`
    #: dataframe.
    @classmethod
    def training_intents_set(
            cls
    ) -> Set[str]:
        """This method returns the result of
        `training_intents_list` wrapped in a call to the
        build_history in `set` function.

        :return: A set of intents from training data.
        :rtype: Set[str]
        """
        return set(cls.training_intents_list())

    #: The `training_intents_counts` attribute represents a
    #: set of unique intents found in the `training_data`
    #: . The `training_intents_counts` attribute is set by
    #: calling `training_data.intent.value_counts()`
    #: dataframe.
    @classmethod
    def training_intents_counts(
            cls
    ) -> pd.Series:
        """This method gets the training data via the
        `get_training_data` method and then returns the result of
        calling the `pd.Series.value_counts` method on the series
        representing intents.

        :return: A value counts series.
        :rtype: pd.Series
        """
        return cls.get_training_data().intent.value_counts()

    #: The `testing_data` attribute represents the fine
    #: tuning data designated as "testing data". This dataset
    #: is used to tune the hyper-parameters during the evaluator
    #: testing iterations. This dataset should be a CSV file
    #: having a `.csv` file extension and contain at least two
    #: (2) columns, one (1) for `text` i.e. the user phrase
    #: (labelled fine_tuning_text_processor.data_column_title)
    #: , and one (1) for `label` i.e. the intent (labelled
    #: fine_tuning_text_processor.label_column_title)
    testing_data: Union[pd.DataFrame, None] = None

    @classmethod
    def set_testing_data(
            cls,
            file_system: FileSystem
    ) -> None:
        """This method will attempt to set the `testing_data`
        attribute by reading the file located on the host
        file system at `$TESTING_PATH` into a `pandas.DataFrame`.
        It is assumed the file located at `$TESTING_PATH` is in
        CSV format and having a `.csv` file extension.


        :return: None
        :rtype: NoneType
        """
        cls.testing_data = pd.read_csv(
            file_system.get_testing_path()
        )
        return None

    @classmethod
    def get_testing_data(
            cls
    ) -> pd.DataFrame:
        """This method is a simple getter which will return the
        `testing_data` attribute. Be sure to call the
        `set_testing_data` method or else the
        `testing_data` attribute will be undefined.

        :return: This method returns the `testing_data` \
        attribute.
        :rtype: pd.DataFrame
        """
        return cls.testing_data

    #: The `testing_intents_list` attribute represents a list
    #: of unique intents found in the `testing_data`.
    #: By definition the `testing_intents_list` attribute is
    #: a Python list of all unique values found in the column
    #: with title "intent" in the `testing_data`
    #: dataframe.
    @classmethod
    def testing_intents_list(
            cls
    ) -> List[str]:
        """This method calls the `get_testing_data` method and
        then extracts unique values from the "intent" column. The
        resulting values are returned in a sorted Python list.

        :return: A list of unique intents found in testing data.
        :rtype: List[str]
        """
        return sorted(
            cls.get_testing_data().intent.unique().tolist()
        )

    #: The `testing_set` attribute represents a set
    #: of unique intents found in the `testing_data`.
    #: By definition the `testing_set` attribute is
    #: a Python set of values found in the column
    #: with title "intent" in the `testing_data`
    #: dataframe.
    @classmethod
    def testing_intents_set(
            cls
    ) -> Set[str]:
        """This method returns the result of
        `testing_intents_list` wrapped in a call to the
        build_history in `set` function.

        :return: A set of intents from testing data.
        :rtype: Set[str]
        """
        return set(cls.testing_intents_list())

    #: The `testing_counts` attribute represents a
    #: set of unique intents found in the `testing_data`
    #: . The `testing_counts` attribute is set by
    #: calling `testing_data.intent.value_counts()`
    #: dataframe.
    @classmethod
    def testing_intents_counts(
            cls
    ) -> pd.Series:
        """This method gets the testing data via the
        `get_testing_data` method and then returns the result of
        calling the `pd.Series.value_counts` method on the series
        representing intents.

        :return: A value counts series.
        :rtype: pd.Series
        """
        return cls.get_testing_data().intent.value_counts()

    #: The `evaluation_data` attribute represents the fine
    #: tuning data designated as "evaluation data". This
    #: dataset is used to tune the hyper-parameters during the
    #: evaluator evaluation iterations. This dataset should be a
    #: CSV file having a `.csv` file extension and contain at
    #: least two (2) columns, one (1) for `text` i.e. the user
    #: phrase
    #: (labelled fine_tuning_text_processor.data_column_title)
    #: , and one (1) for `label` i.e. the intent (labelled
    #: fine_tuning_text_processor.label_column_title)
    evaluation_data: Union[pd.DataFrame, None] = None

    @classmethod
    def set_evaluation_data(
            cls,
            file_system: FileSystem
    ):
        """This method will attempt to set the `testing_data`
        attribute by reading the file located on the host
        file system at `$EVALUATION_PATH` into a
        `pandas.DataFrame`. It is assumed the file located at
        `$EVALUATION_PATH` is in CSV format and having a `.csv`
        file extension.


        :return: None
        :rtype: NoneType
        """
        cls.evaluation_data = pd.read_csv(
            file_system.get_evaluation_path()
        )
        return None

    @classmethod
    def get_evaluation_data(
            cls
    ) -> pd.DataFrame:
        """This method is a simple getter which will return the
        `testing_data` attribute. Be sure to call the
        `set_testing_data` method or else the
        `testing_data` attribute will be undefined.

        :return: This method returns the `testing_data` \
        attribute.
        :rtype: pd.DataFrame
        """
        return cls.evaluation_data

    #: The `evaluation_list` attribute represents a
    #: list of unique intents found in the
    #: `evaluation_data`. By definition the
    #: `evaluation_list` attribute is
    #: a Python list of all unique values found in the column
    #: with title "intent" in the `evaluation_data`
    #: dataframe.
    @classmethod
    def evaluation_intents_list(
            cls
    ) -> List[str]:
        """This method calls the `get_testing_data` method and
        then extracts unique values from the "intent" column. The
        resulting values are returned in a sorted Python list.

        :return: A list of unique intents found in testing data.
        :rtype: List[str]
        """
        return sorted(
            cls.get_evaluation_data().intent.unique().tolist()
        )

    #: The `evaluation_set` attribute represents a set
    #: of unique intents found in the `evaluation_data`.
    #: By definition the `evaluation_set` attribute is
    #: a Python set of values found in the column
    #: with title "intent" in the `evaluation_data`
    #: dataframe.
    @classmethod
    def evaluation_intents_set(
            cls
    ) -> Set[str]:
        """This method returns the result of
        `evaluation_intents_list` wrapped in a call to the
        build_history in `set` function.

        :return: A set of intents from evaluation data.
        :rtype: Set[str]
        """
        return set(cls.evaluation_intents_list())

    #: The `evaluation_counts` attribute represents a
    #: set of unique intents found in the
    #: `evaluation_data`. The `evaluation_counts`
    #: attribute is set by calling
    #: `testing_data.intent.value_counts()`
    #: dataframe.
    @classmethod
    def evaluation_intents_counts(
            cls
    ) -> pd.Series:
        """This method gets the testing data via the
        `get_evaluation_data` method and then returns the result
        of calling the `pd.Series.value_counts` method on the
        series representing intents.

        :return: A value counts series.
        :rtype: pd.Series
        """
        return cls.get_evaluation_data().intent.value_counts()

    #: The `regression_data` attribute represents the fine
    #: tuning data designated as "regression data". This
    #: dataset is used to tune the hyper-parameters during the
    #: evaluator regression iterations. This dataset should be a
    #: CSV file having a `.csv` file extension and contain at
    #: least two (2) columns, one (1) for `text` i.e. the user
    #: phrase
    #: (labelled fine_tuning_text_processor.data_column_title)
    #: , and one (1) for `label` i.e. the intent (labelled
    #: fine_tuning_text_processor.label_column_title)
    regression_data: pd.DataFrame = None

    @classmethod
    def set_regression_data(
            cls,
            file_system: FileSystem
    ) -> None:
        """This method will attempt to set the `regression_data`
        attribute by reading the file located on the host
        file system at `$REGRESSION_PATH` into a
        `pandas.DataFrame`. It is assumed the file located at
        `$REGRESSION_PATH` is in CSV format and having a `.csv`
        file extension.


        :return: None
        :rtype: NoneType
        """
        cls.regression_data = pd.read_csv(
            file_system.get_regression_path()
        )
        return None

    @classmethod
    def get_regression_data(
            cls
    ) -> pd.DataFrame:
        """This method is a simple getter which will return the
        `regression_data` attribute. Be sure to call the
        `set_regression_data` method or else the
        `regression_data` attribute will be undefined.

        :return: This method returns the `regression_data` \
        attribute.
        :rtype: pd.DataFrame
        """
        return cls.regression_data

    #: The `regression_list` attribute represents a
    #: list of unique intents found in the
    #: `regression_data`. By definition the
    #: `regression_list` attribute is
    #: a Python list of all unique values found in the column
    #: with title "intent" in the `regression_data`
    #: dataframe.
    @classmethod
    def regression_intents_list(
            cls
    ) -> List[str]:
        """This method calls the `get_regression_data` method and
        then extracts unique values from the "intent" column. The
        resulting values are returned in a sorted Python list.

        :return: A list of unique intents found in regression \
        data.
        :rtype: List[str]
        """
        return sorted(
            cls.get_regression_data().intent.unique().tolist()
        )

    #: The `regression_set` attribute represents a set
    #: of unique intents found in the `regression_data`.
    #: By definition the `regression_set` attribute is
    #: a Python set of values found in the column
    #: with title "intent" in the `regression_data`
    #: dataframe.
    @classmethod
    def regression_intents_set(
            cls
    ) -> Set[str]:
        """This method returns the result of
        `regression_intents_list` wrapped in a call to the
        build_history in `set` function.

        :return: A set of intents from regression data.
        :rtype: Set[str]
        """
        return set(cls.regression_intents_list())

    #: The `regression_counts` attribute represents a
    #: set of unique intents found in the
    #: `regression_data`. The `regression_counts`
    #: attribute is set by calling
    #: `testing_data.intent.value_counts()`
    #: dataframe.
    @classmethod
    def regression_intents_counts(
            cls
    ) -> pd.Series:
        """This method gets the testing data via the
        `get_evaluation_data` method and then returns the result
        of calling the `pd.Series.value_counts` method on the
        series representing intents.

        :return: A value counts series.
        :rtype: pd.Series
        """
        return cls.get_regression_data().intent.value_counts()

    #: The `all_intents` attribute represents a list of all
    #: unique intents present in the training, testing,
    #: evaluation, and regression datasets.
    @classmethod
    def all_intents(
            cls
    ) -> List[str]:
        """This method will call all `*_intents_list` methods and
        compile them into a single list and then call the
        build_history in `set` function on the list. The result
        is then converted back into a list and returned.

        :return: A list of unique intents found across all \
        datasets.
        :rtype: List[str]
        """
        return sorted(
            list(
                set(
                    cls.training_intents_list()
                    + cls.testing_intents_list()
                    + cls.evaluation_intents_list()
                    + cls.regression_intents_list()
                )
            )
        )

    @classmethod
    def assert_intents_intersect(
            cls
    ) -> None:
        """This method will perform a check on the intents found
        across all datasets and throws a ValueError if the sorted
        testing, evaluation, or regression intent sets do not
        completely intersect i.e. are equal sets.

        :return: None
        :rtype: NoneType
        """

        # It would be unusual for the set of testing intents to
        # be unequal to the set of training intents.
        if cls.training_intents_list() \
                != cls.testing_intents_list():
            raise ValueError(
                "training intents and "
                + "testing intents do not intersect"
            )

        # It would be unusual for the set of evaluation intents
        # to be unequal to the set of training intents.
        if cls.training_intents_list() \
                != cls.evaluation_intents_list():
            raise ValueError(
                "training intents and "
                + "evaluation intents do not intersect"
            )

        # It would be unusual for the set of regression intents
        # to be unequal to the set of training intents.
        if cls.training_intents_list() \
                != cls.regression_intents_list():
            raise ValueError(
                "training intents and "
                + "regression intents do not intersect"
            )

        return None

    #: The `intents_data` attribute represents a Python
    #: dictionary containing key-value pairs of the type
    #: str-List[str] or str-List[int]. These items are
    #: intent lists or intent count lists respectively.
    @classmethod
    def intents_dict(cls) -> Dict[str, Any]:
        """This method will return a Python dictionary containing
        the intents data found across all datasets.

        :return:  A dictionary representing each dataset and \
        their respective intents and intent counts.
        :rtype: Dict[str, Union[List[str], List[int]]]
        """
        return {
            "intents": cls.all_intents(),
            "training_set": {
                "intents": cls.training_intents_list(),
                "counts": cls.training_intents_counts()
                .to_dict()
            },
            "testing_set": {
                "intents": cls.testing_intents_list(),
                "counts": cls.testing_intents_counts()
                .to_dict()
            },
            "evaluation_set": {
                "intents": cls.evaluation_intents_list(),
                "counts": cls.evaluation_intents_counts()
                .to_dict()
            },
            "regression_set": {
                "intents": cls.regression_intents_list(),
                "counts": cls.regression_intents_counts()
                .to_dict()
            }
        }

    @classmethod
    def create_intents_data_json(
            cls,
            file_system: FileSystem
    ) -> None:
        """This method will create one (1) file containing data
        which describes the distribution of intents across fine
        tuning datasets. The file will be stored in the
        `file_system.datasets_summary_dir` directory
        in JSON format with `.json` file extension.

        1 - Intents Data
                * `intentsData.json`


        :return: None
        :rtype: NoneType
        """
        intents_data_json = os.path.join(
            file_system.datasets_summary_dir,
            "intentsData.json"
        )
        with open(intents_data_json, "w+") as file:
            file.write(
                json.dumps(cls.intents_dict())
            )

        return None
