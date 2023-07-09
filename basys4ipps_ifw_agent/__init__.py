from pathlib import Path
import yaml

VERSION = "0.0.1"
CONFIG_PATH = Path("./config.yaml")

if not CONFIG_PATH.exists():
    with open(CONFIG_PATH, "w", encoding="utf-8") as config_stream:
        config_map = {}
        yaml.safe_dump(config_map, config_stream)
