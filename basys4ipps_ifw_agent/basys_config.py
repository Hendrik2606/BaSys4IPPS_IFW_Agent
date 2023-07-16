"""Module providing configuration options for the basys agent"""
# pylint: disable=too-many-instance-attributes

from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime
from os import PathLike
from basys4ipps_ifw_agent import CONFIG_VERSION

from basys4ipps_ifw_agent.access_config import read_config, write_config


@dataclass
class TestDataConfig:
    """Class containing config for preparing test data"""

    segmentation_start: int = 20
    segmentation_end: int = 710


@dataclass
class BasysConfig:
    """Config for training and prediction"""

    version: str
    created: str = str(datetime.min)

    use_tsfresh_features: bool = True
    tsfresh_features: str = "./examples/tsfresh_features.json"
    tsfresh_random_forest: str = "./examples/tsfresh_random_forest.json"
    default_csv_dir_path: str = "./examples/train"

    outlier_detector_name: str = "KNN"
    outlier_score_scaling: str = "gaussian"
    alpha_safety_factor: float = 0.99999
    feature_group: str = "general_purpose"
    feature_scaling_method: str = "standardize"
    learning_type: str = "static"
    machine_component: str = "axis_drive"
    outlier_detection_model_paramters: dict = None
    test_data_config: TestDataConfig = None

    def __post_init__(self):
        if self.outlier_detection_model_paramters is None:
            self.outlier_detection_model_paramters = {
                "KNN": {"n_neighbors": 5, "method": "largest"}
            }

        if self.test_data_config is None:
            self.test_data_config = TestDataConfig()

        if isinstance(self.test_data_config, dict):
            self.test_data_config = TestDataConfig(**self.test_data_config)

    def save(self):
        """safe the config"""
        self.created = str(datetime.now())
        config_map = asdict(self)
        write_config(config_map)

    @classmethod
    def load(cls, path: PathLike = None, create_if_none: bool = False) -> BasysConfig:
        """load the config"""
        config: BasysConfig = read_config(BasysConfig, path=path)

        if not isinstance(config, BasysConfig) and create_if_none:
            new_config = BasysConfig(version=CONFIG_VERSION)
            new_config.save()
            return new_config

        if not isinstance(config, BasysConfig):
            print("Could not load basys config")
            return None

        return config


if __name__ == "__main__":
    # BasysConfig(CONFIG_VERSION).save()

    example_config = BasysConfig.load(create_if_none=True)
    example_config.save()
    pass
