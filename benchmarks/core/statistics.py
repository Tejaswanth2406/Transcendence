"""
Statistical analysis tools for benchmarks.
"""

import math
from typing import List, Dict, Any

def calculate_statistics(runs: List[float]) -> Dict[str, float]:
    """Calculate comprehensive statistics for a set of benchmark runs."""
    if not runs:
        return {}
        
    n = len(runs)
    runs.sort()
    
    mean = sum(runs) / n
    median = runs[n // 2] if n % 2 != 0 else (runs[n // 2 - 1] + runs[n // 2]) / 2.0
    minimum = runs[0]
    maximum = runs[-1]
    
    variance = sum((x - mean) ** 2 for x in runs) / (n - 1) if n > 1 else 0.0
    std_dev = math.sqrt(variance)
    
    # Percentiles
    def percentile(p):
        k = (n - 1) * p
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return runs[int(k)]
        d0 = runs[int(f)] * (c - k)
        d1 = runs[int(c)] * (k - f)
        return d0 + d1
        
    p95 = percentile(0.95)
    p99 = percentile(0.99)
    
    # Confidence Interval (95%)
    # Using 1.96 as z-score for 95% CI
    margin_of_error = 1.96 * (std_dev / math.sqrt(n)) if n > 0 else 0.0
    ci_lower = mean - margin_of_error
    ci_upper = mean + margin_of_error
    
    return {
        "runs": n,
        "mean": mean,
        "median": median,
        "min": minimum,
        "max": maximum,
        "variance": variance,
        "std_dev": std_dev,
        "p95": p95,
        "p99": p99,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper
    }
