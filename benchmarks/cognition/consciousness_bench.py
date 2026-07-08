"""
Benchmark suite for the Consciousness Model (GWT/IIT).
"""

from transcendence.consciousness import ConsciousnessModel, QualiaCategory
from benchmarks.performance.cpu_memory import PerformanceTracker

def run_consciousness_benchmarks():
    tracker = PerformanceTracker()
    results = {}
    
    scenarios = [
        (1000, 10),   # 1000 experiences, 10 broadcasts
        (10000, 100)  # 10000 experiences, 100 broadcasts
    ]
    
    for exps, broadcasts in scenarios:
        print(f"Benchmarking Consciousness: {exps} experiences, {broadcasts} broadcasts")
        model = ConsciousnessModel(name=f"Test_{exps}")
        
        # 1. Qualia Stream Ingestion
        def ingest_qualia():
            for i in range(exps):
                model.experience(f"Exp_{i}", 0.8, 0.5, QualiaCategory.PERCEPTUAL)
        
        _, ingest_metrics = tracker.measure(ingest_qualia)
        results[f"ingest_qualia_{exps}"] = ingest_metrics
        
        # 2. Phi Integration
        phi, phi_metrics = tracker.measure(model.integrate)
        results[f"integrate_{exps}"] = phi_metrics
        results[f"integrate_{exps}"]["phi_score"] = phi
        
        # 3. Workspace Broadcast
        def mass_broadcast():
            for i in range(broadcasts):
                model.broadcast(f"Info_{i}", priority=1.0)
                
        _, broadcast_metrics = tracker.measure(mass_broadcast)
        results[f"broadcast_{broadcasts}"] = broadcast_metrics
        
        # 4. Introspection
        state, intro_metrics = tracker.measure(model.introspect)
        results[f"introspect_{exps}"] = intro_metrics
        
    return results

if __name__ == "__main__":
    import json
    res = run_consciousness_benchmarks()
    print(json.dumps(res, indent=2))
