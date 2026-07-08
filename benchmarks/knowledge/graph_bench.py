"""
Benchmark suite for the Knowledge Graph module.
"""

from transcendence.knowledge_graph import KnowledgeGraph
from datasets.graph_generator import generate_graph
from benchmarks.performance.cpu_memory import PerformanceTracker

def run_knowledge_graph_benchmarks():
    tracker = PerformanceTracker()
    results = {}
    
    # Scalability sizes
    sizes = [100, 1000, 10000] # Cap at 10k for timely execution in default suite
    
    for size in sizes:
        print(f"Benchmarking Knowledge Graph: {size} nodes")
        
        # 1. Insertion & Build Time
        graph, metrics = tracker.measure(generate_graph, size, density=0.01)
        results[f"build_{size}_nodes"] = metrics
        
        # Pre-select a random node for traversal tests
        start_node_id = list(graph.nodes.keys())[0]
        end_node_id = list(graph.nodes.keys())[-1]
        
        # 2. Pathfinding (BFS)
        _, pf_metrics = tracker.measure(graph.find_path, start_node_id, end_node_id)
        results[f"pathfind_{size}"] = pf_metrics
        
        # 3. Connected Components
        _, cc_metrics = tracker.measure(graph.get_connected_component, start_node_id)
        results[f"connected_comp_{size}"] = cc_metrics
        
        # 4. PageRank (compute heavy)
        _, pr_metrics = tracker.measure(graph.pagerank, iterations=20)
        results[f"pagerank_{size}"] = pr_metrics
        
    return results

if __name__ == "__main__":
    import json
    res = run_knowledge_graph_benchmarks()
    print(json.dumps(res, indent=2))
