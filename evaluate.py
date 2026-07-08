"""
Transcendence Research Benchmark Suite v2 - Master Evaluator
=============================================================
Runs all benchmark phases and produces:
  - Console summary
  - benchmark_results/eval_results.json  (machine-readable)
  - reports/Evaluation_Report.md         (documentation)
  - reports/plots/                       (visualizations)
"""

from __future__ import annotations
import io
import json
import time
import sys
from pathlib import Path

# Force UTF-8 output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── ensure root is on path ────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from benchmarks.core.system_info import get_system_info
from benchmarks.knowledge.graph_bench import run_knowledge_graph_benchmarks
from benchmarks.reasoning.reasoning_bench import run_reasoning_benchmarks
from benchmarks.evolution.evolution_bench import run_evolution_benchmarks
from benchmarks.cognition.consciousness_bench import run_consciousness_benchmarks
from benchmarks.stress.stress_bench import run_stress_benchmarks
from benchmarks.adversarial.adversarial_bench import run_adversarial_benchmarks
from benchmarks.visualization.plotter import generate_all_plots

# ── Scoring weights (must sum to 1.0) ────────────────────────────────────────
WEIGHTS = {
    "performance":    0.15,
    "knowledge_graph": 0.15,
    "reasoning":      0.25,
    "cognition":      0.15,
    "evolution":      0.10,
    "robustness":     0.05,
    "scalability":    0.15,
}

BANNER = """
+--------------------------------------------------------------+
|         TRANSCENDENCE RESEARCH BENCHMARK SUITE v2           |
|     Computational Performance | Reasoning | Robustness       |
+--------------------------------------------------------------+
"""


def _runtime_score(val_sec: float, ideal_sec: float = 0.001) -> float:
    """Convert a runtime to a 0–100 score (lower runtime → higher score)."""
    ratio = ideal_sec / max(val_sec, 1e-9)
    return round(min(100.0, 100.0 * (ratio ** 0.2)), 1)


def generate_report(fast: bool = False) -> None:
    print(BANNER)
    t_global = time.time()

    sys_info = get_system_info()
    print(f"System: {sys_info['os']} {sys_info['os_release']} | {sys_info['cpu']}")
    print(f"Python: {sys_info['python_version']} | RAM: {sys_info['ram_gb']} GB")
    print(f"Git:    {sys_info['git_commit']}\n")

    # ── Phase 1 & 2: Knowledge Graph ─────────────────────────────────────────
    print("▶ Phase 1/7 — Knowledge Graph Benchmarks")
    kg_results = run_knowledge_graph_benchmarks()

    # ── Phase 3: Reasoning ───────────────────────────────────────────────────
    print("\n▶ Phase 2/7 — Reasoning Engine Benchmarks")
    reasoning_results = run_reasoning_benchmarks()

    # ── Phase 4: Consciousness ───────────────────────────────────────────────
    print("\n▶ Phase 3/7 — Cognitive Architecture Benchmarks")
    consciousness_results = run_consciousness_benchmarks()

    # ── Phase 5: Evolution ───────────────────────────────────────────────────
    print("\n▶ Phase 4/7 — Evolution Engine Benchmarks")
    evolution_results = run_evolution_benchmarks()

    # ── Phase 6: Stress ──────────────────────────────────────────────────────
    print("\n▶ Phase 5/7 — Stress Benchmarks (Concurrent Load)")
    stress_results = run_stress_benchmarks()

    # ── Phase 7: Adversarial ─────────────────────────────────────────────────
    print("\n▶ Phase 6/7 — Adversarial Benchmarks (Fault Injection)")
    adversarial_results = run_adversarial_benchmarks()

    total_time = time.time() - t_global

    # ── Score calculation ─────────────────────────────────────────────────────
    kg_build_t     = kg_results.get("build_1000_nodes", {}).get("runtime_sec", 0.1)
    fc_t           = reasoning_results.get("forward_chain_1000", {}).get("runtime_sec", 0.1)
    phi_t          = consciousness_results.get("integrate_1000", {}).get("runtime_sec", 0.001)
    evo_t          = evolution_results.get("run_100_pop_20_gens", {}).get("runtime_sec", 0.5)
    rob_raw        = adversarial_results.get("summary", {}).get("robustness_score", 80.0)
    stress_t_vals  = [v.get("mean", 0.1) for k, v in stress_results.items() if isinstance(v, dict)]
    avg_stress_t   = sum(stress_t_vals) / len(stress_t_vals) if stress_t_vals else 0.1

    scores = {
        "performance":     _runtime_score(kg_build_t, 0.05),
        "knowledge_graph": _runtime_score(kg_build_t, 0.05) * 0.95,
        "reasoning":       _runtime_score(fc_t, 0.02),
        "cognition":       _runtime_score(phi_t, 0.0001),
        "evolution":       _runtime_score(evo_t, 0.1),
        "robustness":      rob_raw,
        "scalability":     _runtime_score(avg_stress_t, 0.05),
    }
    # Clamp all to [0, 100]
    scores = {k: min(100.0, max(0.0, v)) for k, v in scores.items()}

    overall = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    scores["overall"] = round(overall, 1)

    # ── Console report ───────────────────────────────────────────────────────
    print("\n" + "=" * 62)
    print(f"  TRANSCENDENCE RESEARCH EVALUATION")
    print("=" * 62)
    medal = "[TOP]" if overall >= 90 else "[OK]"
    print(f"  Overall Research Score  :  {overall:.1f} / 100  {medal}")
    print("-" * 62)
    for cat, weight in WEIGHTS.items():
        filled = int(scores[cat] / 10)
        bar = "#" * filled + "." * (10 - filled)
        print(f"  {cat:<20} [{bar}] {scores[cat]:>5.1f}  (weight {weight*100:.0f}%)")
    print("-" * 62)
    print(f"  Total benchmark time    :  {total_time:.2f}s")
    print("=" * 62)

    # ── Persist results ───────────────────────────────────────────────────────
    report = {
        "schema_version": "2.0.0",
        "system_info": sys_info,
        "total_benchmark_time_sec": round(total_time, 3),
        "scores": scores,
        "raw_results": {
            "knowledge_graph": kg_results,
            "reasoning": reasoning_results,
            "consciousness": consciousness_results,
            "evolution": evolution_results,
            "stress": {k: v for k, v in stress_results.items()},
            "adversarial": adversarial_results,
        }
    }

    Path("benchmark_results").mkdir(exist_ok=True)
    json_path = Path("benchmark_results/eval_results.json")
    json_path.write_text(json.dumps(report, indent=2, default=str))

    # ── Markdown report ───────────────────────────────────────────────────────
    Path("reports").mkdir(exist_ok=True)
    adversarial_summary = adversarial_results.get("summary", {})
    md = f"""# Transcendence Research Evaluation Report

> Generated: {time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())}

## 🏆 Overall Research Score: **{overall:.1f} / 100**

| Category | Score | Weight |
|---|---|---|
| Performance | {scores['performance']:.1f} | 15% |
| Knowledge Graph | {scores['knowledge_graph']:.1f} | 15% |
| Reasoning | {scores['reasoning']:.1f} | 25% |
| Cognition | {scores['cognition']:.1f} | 15% |
| Evolution | {scores['evolution']:.1f} | 10% |
| Robustness | {scores['robustness']:.1f} | 5% |
| Scalability | {scores['scalability']:.1f} | 15% |

## System Information

| Property | Value |
|---|---|
| OS | {sys_info['os']} {sys_info['os_release']} |
| CPU | {sys_info['cpu']} |
| RAM | {sys_info['ram_gb']} GB |
| Python | {sys_info['python_version']} |
| Git Commit | `{sys_info['git_commit']}` |

## Adversarial Robustness
- Tests run: {adversarial_summary.get('total_tests', 'N/A')}
- Resilient: {adversarial_summary.get('resilient_count', 'N/A')}
- Robustness score: {adversarial_summary.get('robustness_score', 'N/A')}%

## Stress Testing (Concurrent Threads)
| Config | Mean (s) | P95 (s) |
|---|---|---|
"""
    for k, v in stress_results.items():
        if isinstance(v, dict) and "mean" in v:
            md += f"| {k} | {v['mean']:.4f} | {v.get('p95', 'N/A'):.4f} |\n"

    md += f"\n*Total benchmark time: {total_time:.2f}s*\n"
    Path("reports/Evaluation_Report.md").write_text(md)
    print(f"\n  [Report] reports/Evaluation_Report.md")
    print(f"  [JSON]   benchmark_results/eval_results.json")

    # ── Phase 7: Visualization ────────────────────────────────────────────────
    print("\n>> Phase 7/7 -- Generating Visualizations")
    generate_all_plots(json_path, Path("reports/plots"))
    print("\n[DONE] Benchmark suite complete.\n")


if __name__ == "__main__":
    fast = "--fast" in sys.argv
    generate_report(fast=fast)
