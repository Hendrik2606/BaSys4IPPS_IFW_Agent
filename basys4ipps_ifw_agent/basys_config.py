""""""

from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Tuple

from basys4ipps_ifw_agent import read_config, write_config


@dataclass
class BasysConfig:
    """Config for training and prediction"""

    base_model: Tuple[str] = ("KNN",)
    outlier_score_scaling: Tuple[str] = ("gaussian",)
    alpha_safety_factor: Tuple[float] = (0.99999,)
    feature_group: Tuple[str] = ("general_purpose",)
    feature_scaling_method: Tuple[str] = ("standardize",)
    learning_type: Tuple[str] = ("static",)
    machine_component: Tuple[str] = ("axis_drive",)
    segementation_start: Tuple[int] = (20,)
    segmentation_end: Tuple[int] = (710,)

    def save(self):
        """safe the config"""
        config_map = read_config()
        config_map["init_values"] = asdict(self)
        write_config(config_map)

    @classmethod
    def load(cls) -> BasysConfig:
        """load the config"""
        config_map = read_config()

        if not isinstance(config_map, dict) or "init_values" not in config_map:
            print("Could not find key 'init_values' in the config! Abort.")
            return None

        config = BasysConfig(**config_map["init_values"])
        return config


if __name__ == "__main__":
    BasysConfig().save()

    config = BasysConfig.load()
    pass
