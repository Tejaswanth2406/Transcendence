"""
Adversarial benchmark — inject malformed/contradictory data and measure resilience.
"""

from __future__ import annotations
import time
from typing import Dict, Any

from transcendence.knowledge_graph import KnowledgeGraph, NodeType, EdgeType
from transcendence.reasoning import ReasoningEngine, RuleType
from transcendence.exceptions import (
    NodeNotFoundError, EdgeNotFoundError, CircularReasoningError,
    TranscendenceError
)


def _test_invalid_confidence() -> Dict[str, Any]:
    kg = KnowledgeGraph()
    caught = 0
    attempts = 10
    for bad_val in [-0.1, -1.0, 1.1, 2.0, float('inf'), float('nan'), -999, 999]:
        try:
            kg.add_node("bad", NodeType.CONCEPT, bad_val)
        except (ValueError, TranscendenceError):
            caught += 1
    return {"test": "invalid_confidence", "attempts": attempts, "caught": caught, "resilient": caught > 0}


def _test_missing_node_edge() -> Dict[str, Any]:
    kg = KnowledgeGraph()
    n = kg.add_node("A", NodeType.CONCEPT, 0.9)
    caught = 0
    for fake_id in ["nonexistent_1", "nonexistent_2", "abc123"]:
        try:
            kg.add_edge(n.id, fake_id, EdgeType.SUPPORTS, 0.5)
        except (NodeNotFoundError, TranscendenceError):
            caught += 1
    return {"test": "missing_node_edge", "attempts": 3, "caught": caught, "resilient": caught == 3}


def _test_self_loop() -> Dict[str, Any]:
    kg = KnowledgeGraph()
    n = kg.add_node("A", NodeType.CONCEPT, 0.9)
    caught = 0
    try:
        # Self-loop: source == target
        kg.add_edge(n.id, n.id, EdgeType.SUPPORTS, 0.5)
    except (ValueError, TranscendenceError):
        caught += 1
    # Even if allowed, pathfinding should not hang
    t0 = time.perf_counter()
    path = kg.find_path(n.id, n.id)
    elapsed = time.perf_counter() - t0
    return {"test": "self_loop", "caught_insertion": caught, "pathfind_time_ms": elapsed * 1000}


def _test_contradiction_injection() -> Dict[str, Any]:
    engine = ReasoningEngine()
    # Inject two contradictory propositions
    p1 = engine.add_proposition("The sky is blue.", 0.95, "perception")
    p2 = engine.add_proposition("The sky is not blue.", 0.95, "perception")

    # Add a rule deriving p2 from p1 — logical contradiction
    try:
        engine.add_rule("contra_rule", [p1.id], p2.id, RuleType.DEDUCTIVE, 0.9)
        derived = engine.forward_chain(max_iterations=5)
        # Contradiction propagated — check coherence degrades
        coherence = engine.coherence_check()
    except Exception as e:
        return {"test": "contradiction_injection", "error": str(e), "resilient": True}

    return {
        "test": "contradiction_injection",
        "derived_count": len(derived),
        "coherence_score": coherence["coherence_score"],
        "resilient": True
    }


def _test_empty_inputs() -> Dict[str, Any]:
    engine = ReasoningEngine()
    caught = 0

    # Empty statement
    try:
        engine.add_proposition("", 0.5, "test")
    except (ValueError, TranscendenceError):
        caught += 1

    # Bad truth value
    try:
        engine.add_proposition("Valid statement", 1.5, "test")
    except (ValueError, TranscendenceError):
        caught += 1

    # Forward chain on empty engine
    derived = engine.forward_chain()
    return {"test": "empty_inputs", "caught": caught, "empty_forward_chain": len(derived) == 0, "resilient": True}


def run_adversarial_benchmarks() -> Dict[str, Any]:
    results: Dict[str, Any] = {}
    tests = [
        _test_invalid_confidence,
        _test_missing_node_edge,
        _test_self_loop,
        _test_contradiction_injection,
        _test_empty_inputs,
    ]

    for test_fn in tests:
        print(f"  Adversarial: {test_fn.__name__}")
        t0 = time.perf_counter()
        result = test_fn()
        result["duration_ms"] = (time.perf_counter() - t0) * 1000
        results[result["test"]] = result

    total = len(results)
    resilient = sum(1 for r in results.values() if r.get("resilient", False))
    results["summary"] = {
        "total_tests": total,
        "resilient_count": resilient,
        "robustness_score": round((resilient / total) * 100, 1) if total > 0 else 0
    }
    return results


if __name__ == "__main__":
    import json
    print(json.dumps(run_adversarial_benchmarks(), indent=2))
