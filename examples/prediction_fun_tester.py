"""Module for example execution of prediction functions"""

from basys4ipps_ifw_agent.prediction_functions.counter_failure_probability import (
    counter_failure_probability,
)
from basys4ipps_ifw_agent.prediction_functions.failure_duration import (
    get_failure_duration,
)
from basys4ipps_ifw_agent.prediction_functions.remaining_useful_life import estimate_rul

file_path = "./examples/failure_duration_list.xlsx"

component_names = [
    "Achsen",
    "Elektrik/Elektronik",
    "Fluidik",
    "Werkzeugsystem/Spindel",
    "Spaenefoerderer",
    "Sonstige",
]

for component_name in component_names:
    tmp = get_failure_duration(file_path, component_name)
    print(f"Output for component {component_name}: {tmp}")

actual_runtime = 50.0
maximum_runtime = 100.0

est_rul = estimate_rul(maximum_runtime, actual_runtime)
print(
    f"Estimated rul for actual runime {actual_runtime} vs maximum runtime {maximum_runtime}: {est_rul}"
)

est_fail_prob, alarm = counter_failure_probability(
    maximum_runtime, actual_runtime, threshold=0.51
)
print(
    f"Estimated failure probability for actual runime {actual_runtime} vs maximum runtime {maximum_runtime}: {est_fail_prob} (alarm: {alarm})"
)

est_fail_prob, alarm = counter_failure_probability(
    maximum_runtime, actual_runtime, threshold=0.49
)
print(
    f"Estimated failure probability for actual runime {actual_runtime} vs maximum runtime {maximum_runtime}: {est_fail_prob} (alarm: {alarm})"
)
