"""Module for reading the expected failure duration from an excel/csv file"""

from enum import Enum
from pathlib import Path
from typing import Union
import pandas as pd


class DurationMeasure(Enum):
    """Enum for target measure"""
    EXPECTATION = "Erwartungswert [h]"
    STANDARD_DEVIATION = "Standardabweichung [h]"


def get_failure_duration(
    file_path: Union[Path, str],
    component_name: str,
    target_measure: DurationMeasure = DurationMeasure.EXPECTATION,
) -> float:
    """Read the target measure of the failure duration for the given component name given the path of the excel/csv file
    
    Parameters
    ---
    file_path: Union[Path, str], file path of datasheet with failure duration information
    component_name: str, name of the component for which the expected failure duration is read
    target_measure: DurationMeasure, specifies target measure e.g. expectation

    Returns
    ---
    float
        value of the target measure for the given component stored in the given excel sheet
    """
    if not isinstance(file_path, (str, Path)):
        raise ValueError("Excel file name invalid")

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError("Excel file does not exist")

    if file_path.suffix == ".csv":
        df = pd.read_csv(file_path, decimal=",", sep=";", header=0, low_memory=False)
    elif file_path.suffix == ".xlsx":
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Error, unexpected file suffix!")

    target_value = df.loc[
        df["Komponente"] == component_name, target_measure.value
    ].values[0]

    return target_value
