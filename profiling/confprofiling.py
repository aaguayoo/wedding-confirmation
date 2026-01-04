"""Config Profiling."""

import multiprocessing as mp
import time
from typing import Callable, Optional

import matplotlib.pyplot as plt  # type: ignore
import numpy as np
import psutil  # type: ignore


def monitor_target(
    target: Callable, args: Optional[tuple] = None
) -> tuple[np.ndarray, np.ndarray]:
    """Monitor CPU and memory usage.

    This function starts a multiprocessing object to monitor target function and measure
    the CPU percentage and RAM memory usage.

    Args:
        target (callable):
            Target function to monitor.

        args (tuple):
            Passing arguments for the target function.
            Default: None

    Returns:
        tuple[np.ndarray, np.ndarray]: Tuple with arrays of CPU percentage and memory
        usage.
    """
    cpu_percents = []
    mem_usage = []

    # log cpu usage of `worker_process` every 10 ms
    if args:
        worker_process = mp.Process(target=target, args=args)
    else:
        worker_process = mp.Process(target=target)

    worker_process.start()
    p = psutil.Process(worker_process.pid)
    while worker_process.is_alive():
        cpu_percents.append(p.cpu_percent(interval=0))
        mem_usage.append(p.memory_info().rss / float(2**20))
        time.sleep(0.1)

    worker_process.join()
    return np.array(cpu_percents), np.array(mem_usage)


def plot_monitor(cpu_data: np.ndarray, mem_data: np.ndarray) -> None:
    """Plot monitor results.

    This function return a graph with the CPU and memory profile
    versus time.

    Args:
        cpu_data (np.ndarray):
            Array with CPU usage percentage.

        mem_data (np.ndarray):
            Array with RAM memory usage.
    """
    if mem_data[-1] <= 0.0:
        mem_data[-1] = mem_data[-2]
    time_ = np.linspace(0, len(cpu_data[9:]) * 0.1, len(cpu_data[9:]))
    _, ax1 = plt.subplots(figsize=(10, 7))
    ax2 = ax1.twinx()
    ax1.plot(time_, cpu_data[9:], alpha=0.9, color="#1f77b4")
    ax2.plot(time_, mem_data[9:] - mem_data[:-1].min(), alpha=0.9, color="orange")
    ax1.set_ylabel("CPU usage (\\%)", color="#1f77b4")
    ax2.set_ylabel("Memory usage (MiB)", color="orange", rotation=270, labelpad=20)
    ax1.set_xlabel("Time (s)")
    plt.tight_layout()
    plt.savefig("plot.png", dpi=300)
