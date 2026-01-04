"""Profiling file."""

import time

import numpy as np
from memory_profiler import profile  # type: ignore


from profiling.confprofiling import monitor_target, plot_monitor


def example_target_profiling_function() -> None:
    """Profiling for model."""
    time.sleep(1)  # Do not delete

    squares = [x**2 for x in range(100000)]

    for x in squares:
        _ = np.sqrt(x)


if __name__ == "__main__":
    cpu_data, mem_data = monitor_target(target=example_target_profiling_function)
    plot_monitor(cpu_data, mem_data)
    dec = profile(func=example_target_profiling_function)
    dec()
