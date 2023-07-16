import glob
from os import PathLike
from pathlib import Path
from typing import List
import numpy as np
import pandas as pd

from basys4ipps_ifw_agent.agent.extract_features import convert_sensor_data_to_tsfresh_format
from basys4ipps_ifw_agent.basys_config import BasysConfig


def get_test_files(directory: str) -> list:
    """Get all csv files in the given directory
    """
    if not isinstance(directory, str) or not (path:=Path(directory)).is_dir():
        raise ValueError(f"Input {directory} is not a valid directory!")

    all_files = glob.glob(path.as_posix() + "/*.csv")

    if len(all_files) == 0:
        raise Exception("No files. Abort.")

    print(f"Found {len(all_files)} files!")

    return all_files


def example_sensor_data(all_files: List[PathLike], training_index, test_index: int, sensor: int,
                        basys_config: BasysConfig):
    """Get example sensor data for training test data and testing on a single timeseries
    
    Parameters
    ---

    Returns
    ---

    x_train: pd.DataFrame, x_test: pd.DataFrame,
    """
    np.random.seed(1234)
    # Segmentieren der Zeitreihen

    # Loesche ab Begin_Del 1769 / 710
    Begin_Del = basys_config.test_data_config.segmentation_end
    # Loesche die ersten Teil
    To_Del = basys_config.test_data_config.segementation_start

    Num_Pro = 139

    # Laden der Trainingsdaten
    train_data = pd.read_csv(all_files[sensor - 1], decimal=",", sep=";", header=0)

    # Segmentieren der Daten

    train_data = train_data.drop(train_data.index[Begin_Del : len(train_data)])
    train_data = train_data.drop(train_data.index[0:To_Del])

    # Datenformat float
    train_data = train_data.to_numpy().astype("float64")

    # Variable for time entries
    time = train_data[:, 0]

    # delete nan columns
    train_data = train_data[:, ~np.isnan(train_data).any(axis=0)]

    # delete first column (time entries)
    train_data = train_data[:, 1 : Num_Pro + 1]

    # Convert
    train_data[train_data == -2.8026e-45] = -0.0001
    train_data[train_data == 2.8026e-45] = 0.0001

    train_data[train_data == -2.8e-41] = -0.0001
    train_data[train_data == 2.8e-41] = 0.0001

    ## Define X_train and X_test

    x_train = train_data[:, training_index]
    x_test = train_data[:, test_index]

    x_test = x_test.transpose().reshape(-1, 1)

    x_train = convert_sensor_data_to_tsfresh_format(x_train, f"sensor_{sensor}", time_column=pd.DataFrame(time))
    x_test = convert_sensor_data_to_tsfresh_format(x_test, f"sensor_{sensor}", time_column=pd.DataFrame(time))

    return x_train, x_test