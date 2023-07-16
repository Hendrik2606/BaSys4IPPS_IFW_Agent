"""Module for configuration management"""

from os import PathLike
from pathlib import Path
import yaml
from packaging import version
from basys4ipps_ifw_agent import CONFIG_PATH, CONFIG_VERSION


def read_config(config_type: type, path: PathLike = None) -> type:
    """Read the config file"""
    path = CONFIG_PATH if path is None else Path(path)

    print(f"Reading config file '{path.resolve().as_posix()}'")

    if not path.exists():
        print("Config file not found!")
        return None

    with open(path, "r", encoding="utf-8") as config_stream:
        _config_map: dict = yaml.safe_load(config_stream)

    if version.parse(_config_map.get("version")) < version.parse(CONFIG_VERSION):
        raise ValueError(f"Found deprecated config file version {_config_map.get('version')}!")

    return config_type(**_config_map)


def write_config(_config_map: dict, path: PathLike = None):
    """Read the config file"""
    path = CONFIG_PATH if path is None else Path(path)

    print(f"Writing to config file '{path.resolve().as_posix()}'")

    with open(path, "w", encoding="utf-8") as config_stream:
        yaml.safe_dump(_config_map, config_stream, sort_keys=False)
