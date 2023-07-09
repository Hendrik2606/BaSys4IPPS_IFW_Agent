# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:54:48 2023

@author: Noske
"""

##Input X_test / o_scores_regular_train


# extract features

## Generate General purpose features for X_test
    
mean = np.mean(X_test, axis=0)
std = np.std(X_test, axis=0)
rms = np.sqrt(np.mean(X_test**2, axis=0))
skewness = skew(X_test, axis=0)
kurt = kurtosis(X_test, axis=0)
SNR = np.log10( (mean**2 / std**2))
peaktopeak = abs(np.max(abs(X_test), axis=0) - np.min(abs(X_test), axis=0))
crest_factor = np.max(abs(X_test), axis=0) / rms
shape_factor = rms / np.mean(abs(X_test), axis=0)
iqr7525 = iqr(X_test, axis=0)
integral = np.trapz(X_test, axis=0)
ma = np.max(X_test, axis=0)
mi = np.max(X_test, axis=0)

##############

# Building Feature Vector
X_test_feat = np.array((mean, std, rms, skewness, kurt, SNR, peaktopeak, shape_factor, crest_factor, iqr7525, integral ) ).reshape(1,-1)


# standardize test data
X_test_std = scaler.transform(X_test_feat)

# regularize test data
# get the prediction on the test data
y_test_scores = clf.decision_function(X_test_std)  # outlier scores
    
o_scores_regular_test = y_test_scores - np.min(y_train_scores)
        
o_scores_regular_test[o_scores_regular_test<0] = 0

# normalize test data

# gaussian scaling
        
o_scores_gaussian_test = special.erf((o_scores_regular_test - np.mean(o_scores_regular_train)) / (np.std(o_scores_regular_train) * np.sqrt(2)) ) 
        
o_scores_gaussian_test[o_scores_gaussian_test<0] = 0

Alarm = o_scores_gaussian_test > alpha_safety_factor

print("Score_prob=", o_scores_gaussian_test, "Alarm=", Alarm, "exp_downtime", "63 h")
        
