"""
Performance tracking for CPU and Memory.
"""

import time
import psutil
import gc
from typing import Callable, Any, Dict, Tuple

class PerformanceTracker:
    def __init__(self):
        self.process = psutil.Process()
        
    def measure(self, func: Callable, *args, **kwargs) -> Tuple[Any, Dict[str, float]]:
        """Measure execution time, CPU, and Memory usage of a function."""
        # Force garbage collection before measuring for baseline
        gc.collect()
        
        mem_before = self.process.memory_info().rss
        allocs_before = gc.get_count()
        
        cpu_times_before = self.process.cpu_times()
        
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        
        cpu_times_after = self.process.cpu_times()
        
        mem_after = self.process.memory_info().rss
        allocs_after = gc.get_count()
        
        runtime = t1 - t0
        cpu_user = cpu_times_after.user - cpu_times_before.user
        cpu_sys = cpu_times_after.system - cpu_times_before.system
        
        metrics = {
            "runtime_sec": runtime,
            "cpu_user_sec": cpu_user,
            "cpu_system_sec": cpu_sys,
            "memory_peak_mb": max(mem_before, mem_after) / (1024 * 1024),
            "memory_delta_mb": (mem_after - mem_before) / (1024 * 1024),
            "allocations_estimated": sum(allocs_after) - sum(allocs_before)
        }
        
        return result, metrics
