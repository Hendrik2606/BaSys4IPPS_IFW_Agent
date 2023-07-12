from datetime import datetime
import yaml
from basys4ipps_ifw_agent import CONFIG_PATH


def read_config() -> dict:
    """Read the config file"""
    print(f"Reading config file '{CONFIG_PATH.resolve().as_posix()}'")

    with open(CONFIG_PATH, "r", encoding="utf-8") as config_stream:
        _config_map = yaml.safe_load(config_stream)
    return _config_map


def write_config(_config_map: dict):
    """Read the config file"""
    print(f"Writing to config file '{CONFIG_PATH.resolve().as_posix()}'")

    with open(CONFIG_PATH, "w", encoding="utf-8") as config_stream:
        yaml.safe_dump(_config_map, config_stream)


_default_config_map = {
    "created": str(datetime.now()),
}


if not CONFIG_PATH.exists():
    write_config(_default_config_map)
    print(
        f"Config file '{CONFIG_PATH.resolve().as_posix()}' does not exist and is created!"
    )
else:
    _config_map = read_config()
    missing_keys = set(_default_config_map).difference(_config_map)

    for k in missing_keys:
        _config_map[k] = _default_config_map[k]

    if missing_keys:
        write_config(_config_map)
