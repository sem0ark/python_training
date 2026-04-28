import multiprocessing
import threading
import time

import pytest

"""
Demonstrate the performance impact of the Global Interpreter Lock (GIL) on CPU-bound workloads.

Requirements:
1. `cpu_heavy_task(n)` must perform a CPU-bound computation whose runtime scales with `n`.
2. `ParallelRunner.run_threaded(workers)` must execute the task concurrently using threads and return elapsed wall-clock time.
3. `ParallelRunner.run_processed(workers)` must execute the task concurrently using processes and return elapsed wall-clock time.
4. The tests will compare timings to show that multiprocessing outperforms multithreading for CPU-bound work on a multi-core machine.
"""


def cpu_heavy_task(n: int):
    """A pure Python CPU-bound calculation."""
    # Use a loop that keeps the Python interpreter busy with bytecode
    raise NotImplementedError()


class ParallelRunner:
    def __init__(self, task_input: int):
        self.task_input = task_input

    def run_threaded(self, workers: int) -> float:
        """Executes task_input in N threads and returns elapsed time."""
        raise NotImplementedError()

    def run_processed(self, workers: int) -> float:
        """Executes task_input in N processes and returns elapsed time."""
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_threaded_performance_degradation():
    """Threads should be slower or equal to serial execution for CPU-bound tasks."""
    runner = ParallelRunner(10**6)

    # Run 4 workers
    start = time.perf_counter()
    duration = runner.run_threaded(workers=4)

    # Verification is done by comparing against Multiprocessing in the next test
    assert duration > 0


def test_process_vs_thread_speedup():
    """Processes should significantly outperform threads for CPU-bound math."""
    # Input size adjusted for reasonable test time
    runner = ParallelRunner(5 * 10**6)
    workers = 4

    thread_time = runner.run_threaded(workers)
    process_time = runner.run_processed(workers)

    # Multi-processing should be at least 1.5x faster on multi-core systems
    # In reality, it's often close to 3-4x faster.
    assert process_time < thread_time, (
        f"Threads ({thread_time}s) were faster than Processes ({process_time}s)!"
    )


def test_state_isolation_processes():
    """Verify that processes do not share global state, while threads do."""
    # This is a behavioral check of the chosen engine
    global_list = []

    def append_to_list():
        global_list.append(1)

    # Threading
    t = threading.Thread(target=append_to_list)
    t.start()
    t.join()
    assert len(global_list) == 1

    # Multiprocessing
    p = multiprocessing.Process(target=append_to_list)
    p.start()
    p.join()
    assert len(global_list) == 1  # Still 1 because P had its own isolated global_list


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints ---
# - For `cpu_heavy_task`, something like `sum(i * i for i in range(n))` is effective.
# - In `run_threaded`, remember to `start()` all threads before `join()`ing any of them.
# - For `run_processed`, use `multiprocessing.Process` or `multiprocessing.Pool`.
