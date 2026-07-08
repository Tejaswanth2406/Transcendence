"""
Benchmark suite for the Reasoning Engine module.
"""

from datasets.logic_generator import generate_reasoning_data
from benchmarks.performance.cpu_memory import PerformanceTracker

def run_reasoning_benchmarks():
    tracker = PerformanceTracker()
    results = {}
    
    scenarios = [
        (100, 200, 10),    # Small
        (1000, 2000, 50),  # Medium
        (5000, 10000, 100) # Large
    ]
    
    for props, rules, depth in scenarios:
        print(f"Benchmarking Reasoning: {props} props, {rules} rules")
        
        # Generate data
        engine = generate_reasoning_data(props, rules, depth)
        
        # 1. Forward Chaining
        derived, fc_metrics = tracker.measure(engine.forward_chain, max_iterations=20)
        results[f"forward_chain_{props}"] = fc_metrics
        results[f"forward_chain_{props}"]["derived_count"] = len(derived)
        
        # 2. Coherence Check
        coherence, ch_metrics = tracker.measure(engine.coherence_check)
        results[f"coherence_{props}"] = ch_metrics
        results[f"coherence_{props}"]["score"] = coherence["coherence_score"]
        
        # 3. Backward Chaining (pick a random unknown prop as goal)
        goal_id = list(engine.propositions.keys())[-1]
        try:
            proof, bc_metrics = tracker.measure(engine.backward_chain, goal_id)
            results[f"backward_chain_{props}"] = bc_metrics
        except Exception as e:
            results[f"backward_chain_{props}"] = {"error": str(e)}
        
    return results

if __name__ == "__main__":
    import json
    res = run_reasoning_benchmarks()
    print(json.dumps(res, indent=2))
