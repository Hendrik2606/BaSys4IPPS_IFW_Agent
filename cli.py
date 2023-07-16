"""Command line interface module"""

import logging
from os import PathLike
from pathlib import Path
import sys
import click
import yaml
from basys4ipps_ifw_agent import CONFIG_PATH, CONFIG_VERSION, VERSION
from basys4ipps_ifw_agent import basys_config
from basys4ipps_ifw_agent.access_config import read_config
from basys4ipps_ifw_agent.agent.basys_agent import BasysAgent
from basys4ipps_ifw_agent.basys_config import BasysConfig
from examples.test_data_initialization import (
    get_test_files,
    load_sensor_data,
    split_sensor_data,
)


@click.group()
@click.option("--basys-config-path", "-p", type=str, default=None, help="Path to the basys config yaml. Use default path if None")
@click.pass_context
def main(ctx: click.Context, basys_config_path: str):
    print("IFW Hannover - Leibniz Universität Hannover")
    print(f"Basys Agent ({VERSION}), 2023\n")

    logging.basicConfig(level=logging.INFO)

    if isinstance(basys_config_path, str) and not Path(basys_config_path).exists():
        print("Error, path does not exist: ", basys_config_path)
        sys.exit(1)

    ctx.ensure_object(dict)

    basys_config = BasysConfig.load(path=basys_config_path)
    ctx.obj["basys_config"] = basys_config


@main.group(chain=True)
@click.option(
    "--csv-dir",
    "-sd",
    type=str,
    default=None,
    help="Path to directory with csv files. Use default path if None.",
)
@click.option("--sensor", "-s", type=int, default=5)
@click.pass_context
def load_data(ctx: click.Context, csv_dir: PathLike, sensor: int):
    """load data from the given path"""    

    basys_config = ctx.obj["basys_config"]

    csv_dir = basys_config.default_csv_dir_path if csv_dir is None else csv_dir
    print("Loading csv files from", csv_dir)

    all_files = get_test_files(csv_dir)
    sensor_data, df_time = load_sensor_data(all_files, sensor, basys_config)
    ctx.obj["sensor_data"] = sensor_data
    ctx.obj["df_time"] = df_time
    ctx.obj["sensor"] = sensor
    ctx.obj["basys_config"] = basys_config


@load_data.command()
@click.option(
    "--train-start",
    "-trs",
    type=int,
    default=0,
    help="Start index of the training range",
)
@click.option(
    "--train-end", "-tre", type=int, default=20, help="End index of the training range"
)
@click.option(
    "--test-index",
    "-tei",
    type=int,
    default=115,
    help="Test index of the test timeseires",
)
@click.pass_context
def fit_predict(ctx: click.Context, train_start: int, train_end: int, test_index: int):
    """Execute training and testing for a given training range and a given test index
    in the sensor input data
    """
    if any(
        (missing := x) not in ctx.obj
        for x in ["sensor_data", "df_time", "sensor", "basys_config"]
    ):
        click.echo(f"Missing object in cli context: '{missing}'")
        sys.exit(1)

    sensor_data = ctx.obj.get("sensor_data")
    df_time = ctx.obj.get("df_time")
    sensor = ctx.obj.get("sensor")
    basys_config: BasysConfig = ctx.obj.get("basys_config")

    training_index = range(train_start, train_end)
    print("Using training index", training_index)
    training_index = list(training_index)

    if sensor_data is None or df_time is None:
        click.echo("Error, sensor_data/time is None. Abort.")
        sys.exit(1)

    x_train, x_test = split_sensor_data(
        sensor_data, df_time, sensor, training_index, test_index, basys_config
    )

    print("dimensions: ", "x_train", x_train.shape, "x_test", x_test.shape)

    agent = BasysAgent(basys_config)

    logging.info("Start training")
    agent.fit(x_train, basys_config)

    logging.info("Start testing")
    agent.predict(x_test, basys_config)

    print(f"Prediction successully executed!")


@main.command()
@click.argument("alpha-safety-factor", type=float)
def save_alpha_safety_factor(alpha_safety_factor: float):
    """Set the alpha safety factor in the config"""
    if not CONFIG_PATH.exists():
        print(
            f"Error, config path '{CONFIG_PATH.resolve().as_posix()}' does not exist!"
        )
        sys.exit(1)

    config_map: BasysConfig = read_config(BasysConfig)

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
    main(["load-data", "fit-predict"])
