"""Module for feature extraction"""

import numpy as np
from numpy.typing import NDArray
import pandas as pd
from scipy.stats import kurtosis, skew, iqr

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
    """Extract features from numpy array"""
    x_features["mean"] = (mean := np.mean(x_signal, axis=0))
    x_features["std"] = (std := np.std(x_signal, axis=0))
    x_features["rms"] = (rms := np.sqrt(np.mean(x_signal**2, axis=0)))
    # x_features["skewness"] = skew(x_signal, axis=0)
    #x_features["kurt"] = kurtosis(x_signal, axis=0)
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
