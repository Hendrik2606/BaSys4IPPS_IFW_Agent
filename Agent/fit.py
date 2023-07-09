# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:24:30 2023

@author: Noske
"""


## Fit the Baseline model
#Input X_train

## Generate General purpose features for X_train
    
mean = np.mean(X_train, axis=0)
std = np.std(X_train, axis=0)
rms = np.sqrt(np.mean(X_train**2, axis=0))
skewness = skew(X_train, axis=0)
kurt = kurtosis(X_train, axis=0)
SNR = np.log10( (mean**2 / std**2))
peaktopeak = abs(np.max(abs(X_train), axis=0) - np.min(abs(X_train), axis=0))
crest_factor = np.max(abs(X_train), axis=0) / rms
shape_factor = rms / np.mean(abs(X_train), axis=0)
iqr7525 = iqr(X_train, axis=0)
integral = np.trapz(X_train, axis=0)
ma = np.max(X_train, axis=0)
mi = np.max(X_train, axis=0)

##############

# Building Feature Vector
X_train_feat = np.concatenate((mean.reshape(-1, 1), std.reshape(-1, 1), rms.reshape(-1, 1), skewness.reshape(-1, 1), kurt.reshape(-1, 1), SNR.reshape(-1, 1), peaktopeak.reshape(-1, 1), shape_factor.reshape(-1, 1), crest_factor.reshape(-1, 1), iqr7525.reshape(-1, 1), integral.reshape(-1, 1)), axis=1)

# Scale the feature vector
scaler = StandardScaler()
scaler.fit(X_train_feat)
X_train_std = scaler.transform(X_train_feat)

# Compute regularized Scores

#Baseline model
#KNN######
        
from pyod.models.knn import KNN
                
clf_name = 'KNN'
clf = KNN(n_neighbors=5, method='largest')
clf.fit(X_train_std)
y_train_scores = clf.decision_scores_

#Regularize scores based on basis
o_scores_regular_train = y_train_scores - np.min(y_train_scores)

#############