"""Module for estimating the failure probability based on runtime"""

from typing import Tuple


def counter_failure_probability(
    max_runtime: float, act_runtime: float, threshold: float
) -> Tuple[float, float]:
    """Calculate the failure probability based on actual runtime vs maximum runtime

    Paramters
    ---
    max_runtime: float, estimated maximum runtime
    act_rutime: float, actual runtime
    threshold: float, threshold probability

    Returns
    ---
    Tuple[float, int]
        failure probability, alarm
    """
    p_fail = min(1, act_runtime / max_runtime)
    alarm = 1 if p_fail >= threshold else 0

    return p_fail, alarm
