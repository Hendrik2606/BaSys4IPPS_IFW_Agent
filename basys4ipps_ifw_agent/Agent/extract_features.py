"""Module for feature extraction"""

from os import PathLike
import numpy as np
from numpy.typing import NDArray
import pandas as pd
from scipy.stats import iqr  # , kurtosis, skew

from failure_recognition_signal_processing.feature_container import FeatureContainer


def convert_sensor_data_to_tsfresh_format(
    sensor_data: any, sensor_name: str, time_column: pd.DataFrame = None
) -> pd.DataFrame:
    """Convert the given sensor data to a pd.DataFrame in tsfresh format (id, time, name_sensor)

    Parameters
    ---
    sensor_data: ArrayLike
    name_time_column: str, name of the time column in the given timeseries
    time_column: pd.DataFrame, optional time column, otherwise the index is used

    Returns
    ---
    timeseries_tsfresh: pd.DataFrame, timeseries in tsfresh format
                        with 'time', 'id', 'sensor_name' columns
    """
    sensor_data = pd.DataFrame(sensor_data)
    out_frame = pd.DataFrame(columns=["id", "time", sensor_name])

    for ts_id in range(sensor_data.shape[1]):
        x_new_rows = pd.DataFrame({sensor_name: sensor_data.iloc[:, ts_id]})
        x_new_rows.insert(0, "id", ts_id * np.ones((x_new_rows.shape[0], 1)))
        x_new_rows.insert(
            0,
            "time",
            x_new_rows.index if time_column is None else pd.DataFrame(time_column),
        )

        if out_frame.shape[0] == 0:
            out_frame = pd.DataFrame(x_new_rows)
        else:
            out_frame = pd.concat(
                [out_frame.reset_index(drop=True), x_new_rows.reset_index(drop=True)],
                axis=0,
            )

    # out_frame.columns = ["id", "time", sensor_name]
    return out_frame


# def convert_timeseries_to_tsfresh(
#     timeseries: pd.DataFrame, name_time_column: str = None
# ) -> pd.DataFrame:
#     """Convert the given timeseries to the tsfresh format

#     Parameters
#     ---
#     timeseries: pd.DataFrame (time x sensors)
#     name_time_column: name of the time column in the given timeseries

#     Returns
#     ---
#     timeseries_tsfresh: pd.DataFrame, timeseries in tsfresh format with 'time' and 'id' columns
#     """
#     name_time_column = "time" if name_time_column is None else name_time_column
#     timeseries_tsfresh = timeseries.rename(
#         columns={name_time_column: "time"}, inplace=False
#     )
#     timeseries_tsfresh.insert(0, "id", np.zeros((timeseries.shape[0], 1)))
#     return timeseries_tsfresh


def extract_tsfresh_features(
    timeseries: pd.DataFrame,
    features_json: PathLike,
    forest_params_json: PathLike,
) -> pd.DataFrame:
    """Compute a tsfresh feature matrix given the time vector

    Parameters
    ---
    timeseries: timeseries matrix
    features_json: path to json file defining all active tsfresh features
    forest_params:  path to json file with random forest parameters
    tsfresh_convert: convert the given timeseries into tsfresh format with id column

    Returns
    ---
    feature_state: pd.DataFrame
    """

    if any(x not in timeseries.columns for x in ["time", "id"]):
        raise ValueError("Missing columns id or time!")

    container = FeatureContainer()
    container.load(features_json, forest_params_json)

    container.compute_feature_state(timeseries, cfg=None, compute_for_all_features=True)

    return container.feature_state


def extract_default_features(x_signal: NDArray) -> NDArray:
    """Extract the features from the given signal

    Parameters
    ---
    x_signal: NDArray, target signal

    Returns
    ---
    x_features: pandas.DataFrame, feature matrix
    """

    x_features = pd.DataFrame()
    # Extract features from numpy array
    x_features["mean"] = (mean := np.mean(x_signal, axis=0))
    x_features["std"] = (std := np.std(x_signal, axis=0))
    x_features["rms"] = (rms := np.sqrt(np.mean(x_signal**2, axis=0)))
    # x_features["skewness"] = skew(x_signal, axis=0)
    # x_features["kurt"] = kurtosis(x_signal, axis=0)
    x_features["SNR"] = np.log10((mean**2 / std**2))
    x_features["peaktopeak"] = abs(
        np.max(abs(x_signal), axis=0) - np.min(abs(x_signal), axis=0)
    )
    x_features["crest_factor"] = np.max(abs(x_signal), axis=0) / rms
    x_features["shape_factor"] = rms / np.mean(abs(x_signal), axis=0)
    x_features["iqr7525"] = iqr(x_signal, axis=0)
    x_features["integral"] = np.trapz(x_signal, axis=0)
    x_features["ma"] = np.max(x_signal, axis=0)
    x_features["mi"] = np.max(x_signal, axis=0)

    return x_features
