"""Command line interface module"""

from pathlib import Path
import sys
import click
import yaml
from basys4ipps_ifw_agent import CONFIG_PATH, VERSION
from basys4ipps_ifw_agent.access_config import read_config
from basys4ipps_ifw_agent.basys_config import BasysConfig


@click.group()
def main():
    print("IFW Hannover - Leibniz Universität Hannover")
    print(f"Basys Agent ({VERSION}), 2023\n")


@main.command()
@click.option("--alpha-safety-factor", "-af", prompt="Path to model file", type=float)
def set_alpha_safety_factor(alpha_safety_factor: float):
    """Set the alpha safety factor in the config"""
    if not CONFIG_PATH.exists():
        print(
            f"Error, config path '{CONFIG_PATH.resolve().as_posix()}' does not exist!"
        )
        sys.exit(1)

    config_map = read_config(BasysConfig)
   
    config_map.alpha_safety_factor = alpha_safety_factor

    config_map.save()

    print("Update successful!")


# @main.command()
# @click.option("--model-path", "-mp", prompt="Path to model file", type=str)
# def add_paths(model_path: str):
#     """Add paths to training/tests files"""
#     if not CONFIG_PATH.exists():
#         print(
#             f"Error, config path '{CONFIG_PATH.resolve().as_posix()}' does not exist!"
#         )
#         sys.exit(1)   

#     config_map = read_config()

#     config_map.model_path = Path(model_path).as_posix()

#     config_map.model_path

#     print("Update successful!")


if __name__ == "__main__":
    main()
