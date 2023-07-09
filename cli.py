"""Click module for accessing the agent"""

from pathlib import Path
import sys
import click
import yaml
from basys4ipps_ifw_agent import CONFIG_PATH, VERSION


@click.group()
def main():
    print("IFW Hannover - Leibniz Universität Hannover")
    print(f"Basys Agent ({VERSION}), 2023\n")


@main.command()
@click.option("--model-path", "-mp", prompt="Path to model file")
def add_paths(model_path: str):
    """Add paths to training/tests files"""
    if not CONFIG_PATH.exists():
        print(f"Error, config path does not exist!")
        sys.exit(1)

    print(f"Using config file '{CONFIG_PATH.resolve().as_posix()}'")

    with open(CONFIG_PATH, "r", encoding="utf-8") as config_stream:
        config_map = yaml.safe_load(config_stream)

    config_map["model_path"] = Path(model_path).as_posix()

    with open(CONFIG_PATH, "w", encoding="utf-8") as config_stream:
        yaml.safe_dump(config_map, config_stream)

    print("Update successfull!")


if __name__ == "__main__":
    main()
