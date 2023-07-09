# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 10:32:33 2023

@author: Hendrik Noske, IFW, Garbsen
"""

## import libraries

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
import pywt
from scipy import signal
import matplotlib.pyplot as plt
from scipy import special

# random seed
np.random.seed(1234)


# Daten laden #####################################################

# Segmentieren der Zeitreihen

# Loesche ab Begin_Del 1769 / 710
Begin_Del = 710
# Loesche die ersten Teil
To_Del = 20

Num_Pro = 139


# Pfad Trainingsdaten
# path = r'\\ifw.uni-hannover.de\daten\B5-Daten\05-Mitarbeiter\Noske\99-Privat\Datensätze\Artis\artis\Vorhaben_Hendrik\Python_Implementierung\train'
path = r"C:\Users\noske\Desktop\Artis_Marposs_Semi_Supervised\Python_Implementierung_Artis_alt\train"
all_files = glob.glob(path + "/*.csv")

# Sensorauswahl
Sensor = 5

# Laden der Trainingsdaten
train_data = pd.read_csv(all_files[Sensor - 1], decimal=",", sep=";", header=0)

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

X_train = train_data[:, 0:20]
X_test = train_data[:, 115]

# Ende Daten laden ######################################

# initialise model
# baseline_model = unified_outlier_score(base_model = "KNN", outlier_score_scaling = "gaussian", alpha_safety_factor = 0.99999, feature_group = "general_purpose", feature_scaling_method = "standardize", learning_type = "static", machine_component = "axis_drive", segementation_start = 20, segmentation_end = 710)

# fit the model on train data
# baseline_model.fit(X_train)

# predict using baseline model
# score_prob, alarm, exp_downtime = baseline_model.predict(X_test)
