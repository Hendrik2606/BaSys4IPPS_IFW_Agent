import logging
import pandas as pd
import glob
import math
from matplotlib import pyplot as plt
import numpy as np
import csv
import time
import gc
import scipy.stats
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import iqr
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
from scipy.stats import entropy
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA
from pandas import read_csv
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot
from statsmodels.graphics.tsaplots import plot_acf
#import pywt
from scipy import signal
import matplotlib.pyplot as plt
from scipy import special
from pathlib import Path
import re
from basys4ipps_ifw_agent.agent.basys_agent import BasysAgent

from basys4ipps_ifw_agent.agent.extract_features import convert_sensor_data_to_tsfresh_format
from basys4ipps_ifw_agent.basys_config import BasysConfig
from examples.test_data_generator import example_sensor_data, get_test_files

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    all_files = get_test_files("./examples/train" )

    training_index = list(range(20))

    x_train, x_test = example_sensor_data(all_files, training_index, test_index=115, sensor=5)
    
    basys_config = BasysConfig.load(create_if_none=True)
    basys_config.alpha_safety_factor = 0.999
    basys_config.use_tsfresh_features = True

    agent = BasysAgent(basys_config)

    logging.info("Start training")
    agent.fit(x_train, basys_config)

    logging.info("Start testing")
    score_prob, alarm, exp_downtime = agent.predict(x_test, basys_config)