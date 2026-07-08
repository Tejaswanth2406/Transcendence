"""
Auto-visualization — generate performance and scaling charts.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

try:
    import matplotlib
    matplotlib.use("Agg")  # headless
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


COLORS = {
    "performance": "#4F8EF7",
    "knowledge_graph": "#A259FF",
    "reasoning": "#F7864F",
    "cognition": "#4FC97A",
    "evolution": "#F7C34F",
    "robustness": "#F74F6A",
    "scalability": "#4FD9F7",
}


def plot_research_scores(scores: Dict[str, float], out_dir: Path) -> None:
    if not HAS_MATPLOTLIB:
        return
    out_dir.mkdir(parents=True, exist_ok=True)

    categories = [k for k in scores if k != "overall"]
    values = [scores[k] for k in categories]
    colors = [COLORS.get(k, "#aaa") for k in categories]

    fig, (ax_bar, ax_radar) = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor("#0F1117")

    # --- Bar chart ---
    ax_bar.set_facecolor("#1A1D2E")
    bars = ax_bar.barh(categories, values, color=colors, edgecolor="#ffffff22", height=0.6)
    ax_bar.set_xlim(0, 105)
    ax_bar.set_xlabel("Score", color="white", fontsize=12)
    ax_bar.set_title("Transcendence Research Evaluation\nCategory Scores", color="white", fontsize=14, fontweight="bold")
    ax_bar.tick_params(colors="white")
    for spine in ax_bar.spines.values():
        spine.set_edgecolor("#ffffff22")
    for bar, val in zip(bars, values):
        ax_bar.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                    f"{val:.1f}", va="center", ha="left", color="white", fontsize=10)

    # Overall score annotation
    overall = scores.get("overall", 0)
    ax_bar.axvline(overall, color="#FFD700", linestyle="--", linewidth=1.5, alpha=0.7, label=f"Overall: {overall:.1f}")
    ax_bar.legend(facecolor="#1A1D2E", edgecolor="#ffffff44", labelcolor="white")

    # --- Radar chart ---
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    radar_values = values + values[:1]

    ax_radar.set_facecolor("#1A1D2E")
    ax_radar = plt.subplot(1, 2, 2, polar=True, facecolor="#1A1D2E")
    ax_radar.set_facecolor("#1A1D2E")
    ax_radar.plot(angles, radar_values, color="#4F8EF7", linewidth=2)
    ax_radar.fill(angles, radar_values, color="#4F8EF7", alpha=0.25)
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels([c.replace("_", "\n") for c in categories], color="white", fontsize=9)
    ax_radar.set_yticks([25, 50, 75, 100])
    ax_radar.set_yticklabels(["25", "50", "75", "100"], color="#aaa", fontsize=8)
    ax_radar.set_ylim(0, 100)
    ax_radar.grid(color="#ffffff22")
    ax_radar.set_title(f"Overall Score: {overall:.1f}/100", color="#FFD700", fontsize=13, fontweight="bold", pad=20)
    ax_radar.spines["polar"].set_edgecolor("#ffffff22")

    plt.tight_layout(pad=2)
    path = out_dir / "research_scores.png"
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Saved: {path}")


def plot_kg_scalability(raw_results: Dict[str, Any], out_dir: Path) -> None:
    if not HAS_MATPLOTLIB:
        return
    out_dir.mkdir(parents=True, exist_ok=True)

    sizes, times = [], []
    for key, val in raw_results.get("knowledge_graph", {}).items():
        if key.startswith("build_") and "_nodes" in key:
            sz = int(key.split("_")[1])
            t = val.get("runtime_sec", 0)
            sizes.append(sz)
            times.append(t * 1000)  # ms

    if not sizes:
        return

    sizes, times = zip(*sorted(zip(sizes, times)))

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#1A1D2E")
    ax.plot(sizes, times, marker="o", color=COLORS["knowledge_graph"], linewidth=2.5, markersize=8)
    ax.fill_between(sizes, times, alpha=0.15, color=COLORS["knowledge_graph"])
    ax.set_xscale("log")
    ax.set_xlabel("Number of Nodes (log scale)", color="white", fontsize=12)
    ax.set_ylabel("Build Time (ms)", color="white", fontsize=12)
    ax.set_title("Knowledge Graph — Scalability", color="white", fontsize=14, fontweight="bold")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#ffffff22")
    ax.grid(color="#ffffff11")

    plt.tight_layout()
    path = out_dir / "kg_scalability.png"
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Saved: {path}")


def generate_all_plots(report_json_path: Path, out_dir: Path) -> None:
    if not HAS_MATPLOTLIB:
        print("  matplotlib not available — skipping visualization")
        return

    with open(report_json_path) as f:
        report = json.load(f)

    scores = report.get("scores", {})
    raw = report.get("raw_results", {})

    plot_research_scores(scores, out_dir)
    plot_kg_scalability(raw, out_dir)
    print("  All plots generated.")


if __name__ == "__main__":
    generate_all_plots(
        Path("benchmark_results/eval_results.json"),
        Path("reports/plots")
    )
