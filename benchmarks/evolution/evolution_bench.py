"""
Benchmark suite for the Evolution Engine module.
"""

from transcendence.evolution import EvolutionEngine, Genome
from benchmarks.performance.cpu_memory import PerformanceTracker

def dummy_fitness(genome: Genome) -> float:
    return sum(g.mutation_rate for g in genome.genes) / len(genome.genes)

def run_evolution_benchmarks():
    tracker = PerformanceTracker()
    results = {}
    
    scenarios = [
        (100, 20),    # Small: 100 population, 20 gens
        (500, 50),    # Medium: 500 population, 50 gens
    ]
    
    for pop_size, gens in scenarios:
        print(f"Benchmarking Evolution: pop={pop_size}, gens={gens}")
        
        engine = EvolutionEngine(population_size=pop_size)
        
        # 1. Initialization
        traits = [f"Trait_{i}" for i in range(10)]
        _, init_metrics = tracker.measure(engine.initialize_population, traits)
        results[f"init_pop_{pop_size}"] = init_metrics
        
        # 2. Evaluation & Selection
        _, eval_metrics = tracker.measure(engine.evaluate_population, dummy_fitness)
        results[f"eval_pop_{pop_size}"] = eval_metrics
        
        # 3. Full generational loop
        def run_generations(n):
            for _ in range(n):
                engine.evaluate_population(dummy_fitness)
                engine.evolve_generation()
                
        _, run_metrics = tracker.measure(run_generations, gens)
        results[f"run_{pop_size}_pop_{gens}_gens"] = run_metrics
        
        if engine.stats:
            results[f"run_{pop_size}_pop_{gens}_gens"]["final_diversity"] = engine.stats[-1].diversity
        
    return results

if __name__ == "__main__":
    import json
    res = run_evolution_benchmarks()
    print(json.dumps(res, indent=2))
