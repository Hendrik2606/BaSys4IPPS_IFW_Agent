from dataclasses import dataclass
import logging

from scipy import special
from basys4ipps_ifw_agent.Agent.extract_features import extract_default_features
from basys4ipps_ifw_agent.basys_config import BasysConfig
from sklearn.preprocessing import StandardScaler

from pyod.models.knn import KNN
from pyod.models.base import BaseDetector

import numpy as np
from numpy.typing import NDArray


@dataclass
class BasysAgent:
    basys_config: BasysConfig
    scaler: StandardScaler = None
    outlier_detector: BaseDetector = None  # default: KNN
    outlier_detector_name: str = None
    y_train_scores: NDArray = None
    o_scores_regularized_train: NDArray = None
    logger: logging.Logger = None

    def __post_init__(self):
        if self.logger is None:
            self.logger = logging.getLogger("BasysLogger")

        if self.scaler is None:
            self.logger.info("Using default StandardScaler")
            self.scaler = StandardScaler()

        if self.outlier_detector is None:
            self.logger.info(
                "Using KNN outlier detection n_neighbors=5, method=largest"
            )
            self.outlier_detector_name = "KNN"
            self.outlier_detector = KNN(n_neighbors=5, method="largest")
            self.outlier_detector.decision_scores_

    def fit_outlier_detector(self, X_train: NDArray):
        """Generate general purpose features for the given training data and fit the model

        Parameters
        ---
        X_train: NDArray, training data

        Returns
        ---
        regularized decision score: NDArray
        """

        self.logger.info("Extract features from training data")
        X_train_feat = extract_default_features(X_train)

        # Scale the feature vector

        self.scaler.fit(X_train_feat)
        X_train_std = self.scaler.transform(X_train_feat)

        # Compute regularized Scores

        self.logger.info("Fit the outlier detection model")

        self.outlier_detector.fit(X_train_std)
        y_train_scores = self.outlier_detector.decision_scores_

        # Regularize scores based on basis
        self.o_scores_regularized_train = y_train_scores - np.min(y_train_scores)

    def predict(self, X_test: NDArray) -> NDArray:
        """Generate general purpose features for the given test data and generate predictions

        Parameters
        ---
        X_train: NDArray, training data

        Returns
        ---
        regularized decision score: NDArray
        """

        self.logger.info("Extract features from test data")
        X_test_feat = extract_default_features(X_test)

        # standardize test data
        X_test_std = self.scaler.transform(X_test_feat)

        # regularize test data
        # get the prediction on the test data
        self.logger.info("Execute decision function")

        y_test_scores = self.outlier_detector.decision_function(
            X_test_std
        )  # outlier scores

        o_scores_regular_test = y_test_scores - np.min(self.y_train_scores)

        o_scores_regular_test[o_scores_regular_test < 0] = 0

        # normalize test data

        # gaussian scaling

        o_scores_gaussian_test = special.erf(
            (o_scores_regular_test - np.mean(self.o_scores_regularized_train))
            / (np.std(self.o_scores_regularized_train) * np.sqrt(2))
        )

        o_scores_gaussian_test[o_scores_gaussian_test < 0] = 0

        Alarm = o_scores_gaussian_test > self.basys_config.alpha_safety_factor

        self.logger.info(
            "safety_factor=",
            self.basys_config.alpha_safety_factor,
            "Score_prob=",
            o_scores_gaussian_test,
            "Alarm=",
            Alarm,
            "exp_downtime",
            "63 h",
        )
