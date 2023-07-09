from datetime import datetime
from pathlib import Path
import yaml

VERSION = "0.0.1"
CONFIG_PATH = Path("./config.yaml")


def read_config() -> dict:
    """Read the config file"""
    print(f"Reading config file '{CONFIG_PATH.resolve().as_posix()}'")

    with open(CONFIG_PATH, "r", encoding="utf-8") as config_stream:
        config_map = yaml.safe_load(config_stream)
    return config_map


def write_config(config_map: dict):
    """Read the config file"""
    print(f"Writing to config file '{CONFIG_PATH.resolve().as_posix()}'")

    with open(CONFIG_PATH, "w", encoding="utf-8") as config_stream:
        yaml.safe_dump(config_map, config_stream)


default_config_map = {
    "created": str(datetime.now()),
}


if not CONFIG_PATH.exists():
    write_config(default_config_map)
    print(
        f"Config file '{CONFIG_PATH.resolve().as_posix()}' does not exist and is created!"
    )
else:
    config_map = read_config()
    missing_keys = set(default_config_map).difference(config_map)

    for k in missing_keys:
        config_map[k] = default_config_map[k]

    if missing_keys:
        write_config(config_map)
