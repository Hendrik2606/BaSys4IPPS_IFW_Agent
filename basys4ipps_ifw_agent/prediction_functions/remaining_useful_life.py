"""Module for estimating the rul (remaining useful life) based on runtime"""


def estimate_rul(max_runtime: float, act_runtime: float) -> float:
    """Calculate the estimated remaining useful life based on actual
    runtime vs maximum runtime

    Parameters
    ---
    max_runtime: float, estimated maximum runtime
    act_runtime: float, actual runtime

    Returns
    ---
    float
        estimated value for the remaining useful life
    """
    estimated_rul = max_runtime - act_runtime

    return estimated_rul
