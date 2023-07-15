"""Module providing configuration options for the basys agent"""
# pylint: disable=too-many-instance-attributes

from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Tuple
from basys4ipps_ifw_agent import CONFIG_VERSION

from basys4ipps_ifw_agent.access_config import read_config, write_config


@dataclass
class BasysConfig:
    """Config for training and prediction"""

    version: str
    created: str = str(datetime.min)

    use_tsfresh_features: bool = False
    tsfresh_features: str = "./examples/tsfresh_features.json"
    tsfresh_random_forest: str = "./examples/tsfresh_random_forest.json"

    outlier_detector_name: str = "KNN"
    outlier_score_scaling: str = "gaussian"
    alpha_safety_factor: float = 0.99999
    feature_group: str = "general_purpose"
    feature_scaling_method: str = "standardize"
    learning_type: str = "static"
    machine_component: str = "axis_drive"
    segementation_start: int = 20
    segmentation_end: int = 710

    outlier_detection_model_paramters: dict = None

    def __post_init__(self):
        if self.outlier_detection_model_paramters is None:
            self.outlier_detection_model_paramters = {
            "KNN": {"n_neighbors": 5, "method": "largest"}
        }

    def save(self):
        """safe the config"""
        self.created = str(datetime.now())
        config_map = asdict(self)
        write_config(config_map)

    @classmethod
    def load(cls, create_if_none: bool = False) -> BasysConfig:
        """load the config"""
        config: BasysConfig = read_config(BasysConfig)

        if not isinstance(config, BasysConfig) and create_if_none:
            new_config = BasysConfig(version=CONFIG_VERSION)
            new_config.save()
            return new_config

        if not isinstance(config, BasysConfig):
            print("Could not load basys config")
            return None

        return config


if __name__ == "__main__":
    BasysConfig().save()

    example_config = BasysConfig.load()
