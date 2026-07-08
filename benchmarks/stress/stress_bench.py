"""
Stress benchmark — concurrent load testing across Transcendence modules.
"""

from __future__ import annotations
import concurrent.futures
import threading
import time
from typing import Dict, Any

from transcendence.knowledge_graph import KnowledgeGraph, NodeType, EdgeType
from transcendence.reasoning import ReasoningEngine, RuleType
from benchmarks.core.statistics import calculate_statistics


def _kg_worker(worker_id: int, num_ops: int) -> Dict[str, Any]:
    """Each thread builds and queries its own Knowledge Graph."""
    kg = KnowledgeGraph()
    nodes = []
    t0 = time.perf_counter()

    for i in range(num_ops):
        n = kg.add_node(f"W{worker_id}_N{i}", NodeType.CONCEPT, 0.8)
        nodes.append(n.id)

    if len(nodes) > 1:
        for i in range(min(50, len(nodes) - 1)):
            try:
                kg.add_edge(nodes[i], nodes[i + 1], EdgeType.SUPPORTS, 0.9)
            except Exception:
                pass

    elapsed = time.perf_counter() - t0
    return {"worker_id": worker_id, "ops": num_ops, "time_sec": elapsed, "nodes": len(kg.nodes)}


def _reasoning_worker(worker_id: int, num_props: int) -> Dict[str, Any]:
    """Each thread builds and runs forward chaining."""
    engine = ReasoningEngine()
    t0 = time.perf_counter()

    props = []
    for i in range(num_props):
        tv = 0.8 if i < num_props // 5 else None
        p = engine.add_proposition(f"W{worker_id}_P{i}", tv, "stress_test")
        props.append(p.id)

    for i in range(0, len(props) - 2, 3):
        try:
            engine.add_rule(
                f"R{i}", [props[i], props[i + 1]], props[i + 2],
                RuleType.DEDUCTIVE, 0.85
            )
        except Exception:
            pass

    derived = engine.forward_chain(max_iterations=10)
    elapsed = time.perf_counter() - t0
    return {"worker_id": worker_id, "props": num_props, "derived": len(derived), "time_sec": elapsed}


def run_stress_benchmarks() -> Dict[str, Any]:
    results: Dict[str, Any] = {}
    thread_configs = [2, 4, 8, 16]

    for num_threads in thread_configs:
        print(f"  Stress: {num_threads} threads × Knowledge Graph")
        timings = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as ex:
            futures = [ex.submit(_kg_worker, i, 200) for i in range(num_threads)]
            for f in concurrent.futures.as_completed(futures):
                r = f.result()
                timings.append(r["time_sec"])
        results[f"kg_concurrent_{num_threads}t"] = calculate_statistics(timings)

    for num_threads in thread_configs:
        print(f"  Stress: {num_threads} threads × Reasoning")
        timings = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as ex:
            futures = [ex.submit(_reasoning_worker, i, 100) for i in range(num_threads)]
            for f in concurrent.futures.as_completed(futures):
                r = f.result()
                timings.append(r["time_sec"])
        results[f"reasoning_concurrent_{num_threads}t"] = calculate_statistics(timings)

    return results


if __name__ == "__main__":
    import json
    print(json.dumps(run_stress_benchmarks(), indent=2))
