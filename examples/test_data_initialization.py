import glob
from os import PathLike
from pathlib import Path
from typing import List
import numpy as np
import pandas as pd

from basys4ipps_ifw_agent.agent.extract_features import (
    convert_sensor_data_to_tsfresh_format,
)
from basys4ipps_ifw_agent.basys_config import BasysConfig


def get_test_files(directory: str) -> list:
    """Get all csv files in the given directory

    Returns
    ---
    path_files: List[PathLike], list containing path to the sensor data csv files
    """
    if not isinstance(directory, str) or not (path := Path(directory)).is_dir():
        raise ValueError(f"Input {directory} is not a valid directory!")

    all_files = glob.glob(path.as_posix() + "/*.csv")

    if len(all_files) == 0:
        raise Exception("No files. Abort.")

    print(f"Found {len(all_files)} files!")

    return all_files


def load_sensor_data(all_files: List[PathLike], sensor: int, basys_config: BasysConfig):
    """Prepare the sensor data given a list of csv files. Each csv file
    represents a sensor

    Returns
    ---
    sensor_data: pd.DataFrame, df_time: pd.DataFrame
    """
    np.random.seed(1234)
    # Segmentieren der Zeitreihen

    # Loesche ab begin_Del 1769 / 710
    begin_Del = basys_config.test_data_config.segmentation_end
    # Loesche die ersten Teil
    to_Del = basys_config.test_data_config.segmentation_start

    num_pro = 139

    # Laden der Trainingsdaten
    sensor_data = pd.read_csv(all_files[sensor - 1], decimal=",", sep=";", header=0, low_memory=False)

    # Segmentieren der Daten

    sensor_data = sensor_data.drop(sensor_data.index[begin_Del : len(sensor_data)])
    sensor_data = sensor_data.drop(sensor_data.index[0:to_Del])

    # Datenformat float
    sensor_data = sensor_data.to_numpy().astype("float64")

    # Variable for time entries
    df_time = sensor_data[:, 0]

    # delete nan columns
    sensor_data = sensor_data[:, ~np.isnan(sensor_data).any(axis=0)]

    # delete first column (time entries)
    sensor_data = sensor_data[:, 1 : num_pro + 1]

    # Convert
    sensor_data[sensor_data == -2.8026e-45] = -0.0001
    sensor_data[sensor_data == 2.8026e-45] = 0.0001

    sensor_data[sensor_data == -2.8e-41] = -0.0001
    sensor_data[sensor_data == 2.8e-41] = 0.0001

    return sensor_data, df_time


def split_sensor_data(
    sensor_data: pd.DataFrame,
    df_time: pd.DataFrame,
    sensor: int,
    training_index: list,
    test_index: int,
    basys_config: BasysConfig
):
    """Split the given sensor data into test and training data
    and return the data frames in tsfresh format

    Returns
    ---
    x_test: pd.DataFrame (tsfresh format), x_train: pd.DataFrame (tsfresh format)
    """
    x_train = sensor_data[:, training_index]
    x_test = sensor_data[:, test_index]

    x_test = x_test.transpose().reshape(-1, 1)
    
    if basys_config.use_tsfresh_features:
        x_train = convert_sensor_data_to_tsfresh_format(
            x_train, f"sensor_{sensor}", time_column=df_time
        )
        x_test = convert_sensor_data_to_tsfresh_format(
            x_test, f"sensor_{sensor}", time_column=df_time
        )

    return x_train, x_test


def example_sensor_data(
    all_files: List[PathLike],
    training_index,
    test_index: int,
    sensor: int,
    basys_config: BasysConfig,
):
    """Get example sensor data for training test data and testing on a single timeseries

    Parameters
    ---

    Returns
    ---

    x_train: pd.DataFrame, training data in tsfresh format
    x_test: pd.DataFrame, test column
    """
    sensor_data, df_time = load_sensor_data(all_files, sensor, basys_config)

    ## Define x_train and x_test

    x_train_tsfresh, x_test_tsfresh = split_sensor_data(
        sensor_data, df_time, sensor, training_index, test_index, basys_config
    )

    return x_train_tsfresh, x_test_tsfresh
