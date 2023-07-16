"""Module for training and prediction"""

from dataclasses import dataclass
import logging
from pyod.models.knn import KNN
from pyod.models.base import BaseDetector

import numpy as np
from numpy.typing import NDArray
from scipy import special
from sklearn.preprocessing import StandardScaler

from basys4ipps_ifw_agent import BASYS_LOGGER
from basys4ipps_ifw_agent.agent.extract_features import (
    extract_default_features,
    extract_tsfresh_features,
)
from basys4ipps_ifw_agent.basys_config import BasysConfig


@dataclass
class BasysAgent:
    """Class for training and prediction"""
    basys_config: BasysConfig
    scaler: StandardScaler = None
    outlier_detector: BaseDetector = None  # default: KNN
    outlier_detector_name: str = None
    y_train_scores: NDArray = None
    o_scores_regularized_train: NDArray = None
    logger: logging.Logger = None

    def __post_init__(self):
        if self.logger is None:
            self.logger = logging.getLogger(BASYS_LOGGER)
            self.logger.setLevel(logging.INFO)

        if self.scaler is None:
            self.logger.info("Using default StandardScaler")
            self.scaler = StandardScaler()

        if self.outlier_detector is None:
            self.logger.info(
                "Using KNN outlier detection n_neighbors=5, method=largest"
            )
            self.outlier_detector_name = self.basys_config.outlier_detector_name

            if self.outlier_detector_name == "KNN":
                self.outlier_detector = KNN(
                    **self.basys_config.outlier_detection_model_paramters["KNN"]
                )
            else:
                raise NotImplementedError(
                    f"Outlier model detection not implemented for {self.outlier_detector_name}"
                )

    def fit(self, x_train: NDArray, basys_config: BasysConfig):
        """Generate general purpose features for the given training data and fit the model

        Parameters
        ---
        x_train: NDArray, training data
        basys_config: BasysConfig, configuration object

        Returns
        ---
        regularized decision score: NDArray
        """

        self.logger.info("Extract features from training data")

        if not basys_config.use_tsfresh_features:
            x_train_feat = extract_default_features(x_train)
        else:
            x_train_feat = extract_tsfresh_features(
                x_train,
                basys_config.tsfresh_features,
                basys_config.tsfresh_random_forest,
            )

        # Scale the feature vector

        self.scaler.fit(x_train_feat)
        x_train_std = self.scaler.transform(x_train_feat)

        # Compute regularized Scores

        self.logger.info("Fit the outlier detection model")

        self.outlier_detector.fit(x_train_std)

        self.y_train_scores = np.array(self.outlier_detector.decision_scores_)

        # Regularize scores based on basis
        self.o_scores_regularized_train = self.y_train_scores - np.min(
            self.y_train_scores
        )

    def predict(self, x_test: NDArray, basys_config: BasysConfig) -> NDArray:
        """Generate general purpose features for the given test data and generate predictions

        Parameters
        ---
        x_train: NDArray, training data
        basys_config: BasysConfig, configuration object

        Returns
        ---
        regularized decision score: NDArray, alarm: NDArray
        """

        self.logger.info("Extract features from test data")

        if not basys_config.use_tsfresh_features:
            x_test_feat = extract_default_features(x_test)
        else:
            x_test_feat = extract_tsfresh_features(
                x_test,
                basys_config.tsfresh_features,
                basys_config.tsfresh_random_forest,
            )

        # standardize test data
        x_test_std = self.scaler.transform(x_test_feat)

        # regularize test data
        # get the prediction on the test data
        self.logger.info("Execute decision function")

        y_test_scores = self.outlier_detector.decision_function(
            x_test_std
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

        alarm = o_scores_gaussian_test > self.basys_config.alpha_safety_factor
        expected_downtime_h: float = 1  # todo

        self.logger.info(
            "safety_factor=%f,\nscore_prob=%s\nalarm=%s\nexp_downtime=%s",
            self.basys_config.alpha_safety_factor,
            str(o_scores_gaussian_test),
            str(alarm),
            expected_downtime_h,
        )

        return o_scores_gaussian_test, alarm, expected_downtime_h
