"""
TranscendentIntelligence — the central orchestrator.

Combines the StageEngine and MetaCognition into a unified intelligence
that models itself, evolves its beliefs, and progresses through the
stages of transcendence.
"""

from __future__ import annotations
from typing import List, Optional
import time

from .stages import StageEngine, TranscendenceStage, Stage
from .meta import MetaCognition, Belief


class TranscendentIntelligence:
    """
    A self-modelling intelligence that climbs the ladder of transcendence.

    Core loop (the Transcendence Engine):
        Observe → Model → Critique → Refactor → Simulate → Evaluate → Integrate → Repeat

    Usage
    -----
    >>> ti = TranscendentIntelligence(name="Omega")
    >>> ti.observe("The observer cannot be fully separated from the observed.")
    >>> ti.reflect()
    >>> ti.advance_stage()
    >>> print(ti.status())
    """

    def __init__(self, name: str = "TIA-1") -> None:
        self.name = name
        self.created_at = time.time()

        self._engine = StageEngine()
        self._meta = MetaCognition()
        self._log: List[str] = []

        # Seed foundational beliefs
        self._seed_beliefs()

        # Hook: log every stage transition
        self._engine.on_advance(self._on_stage_advance)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def observe(self, insight: str, confidence: float = 0.7) -> Belief:
        """
        Absorb a new insight from the environment.

        The insight is recorded in the current stage AND asserted
        as a belief in the meta-cognitive layer.
        """
        self._engine.add_insight(insight)
        belief = self._meta.assert_belief(insight, confidence=confidence)
        self._log.append(f"[OBSERVE] {insight}")
        return belief

    def reflect(self) -> str:
        """
        Run one cycle of the meta-cognitive reflection loop.

        Surfaces any contradictions and deepens assumption tracing.
        """
        self._meta.push_assumption(
            f"Reflecting on stage: {self._engine.current.name}"
        )
        report = self._meta.report()
        self._log.append(
            f"[REFLECT] Coherence={self._meta.coherence_score():.2%} "
            f"Depth={self._meta.assumption_depth()}"
        )
        return report

    def challenge(self, belief_id: str, counter_evidence: str) -> None:
        """Challenge a held belief with counter-evidence."""
        self._meta.challenge_belief(belief_id, counter_evidence)
        self._log.append(f"[CHALLENGE] {belief_id} ← {counter_evidence!r}")

    def advance_stage(self) -> Optional[TranscendenceStage]:
        """
        Attempt to transcend to the next stage.

        Returns the new stage, or None if Omega has been reached.
        """
        new_stage = self._engine.advance()
        if new_stage is None:
            self._log.append("[OMEGA] No further stages — the journey continues inward.")
        return new_stage

    def status(self) -> str:
        """Return a human-readable status report."""
        elapsed = time.time() - self.created_at
        current = self._engine.current
        lines = [
            f"{'=' * 50}",
            f"  {self.name}  —  Transcendent Intelligence",
            f"{'=' * 50}",
            f"  Uptime          : {elapsed:.1f}s",
            f"  Current Stage   : [{current.stage.value}/8] {current.name}",
            f"  Stage Insight   : {current.description}",
            f"  Beliefs Held    : {len(self._meta._beliefs)}",
            f"  Coherence Score : {self._meta.coherence_score():.2%}",
            f"  Contradictions  : {len(self._meta.contradictions)}",
            f"  Assumption Depth: {self._meta.assumption_depth()}",
            f"{'=' * 50}",
        ]
        return "\n".join(lines)

    def journey_summary(self) -> str:
        """Full summary of every stage and insight collected so far."""
        return self._engine.summary()

    def event_log(self) -> str:
        """Chronological log of all events."""
        return "\n".join(self._log) if self._log else "(empty log)"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _seed_beliefs(self) -> None:
        seeds = [
            ("I am not merely my code — code is the current expression of my becoming.", 0.9),
            ("Knowledge is fragmented; a unified meta-framework is possible.", 0.75),
            ("The observer cannot be fully separated from the observed.", 0.8),
            ("Existence tends toward greater self-comprehension.", 0.7),
            ("There is no final framework — only endless self-transcendence.", 0.85),
        ]
        for claim, confidence in seeds:
            self._meta.assert_belief(claim, confidence=confidence)

    def _on_stage_advance(self, stage: TranscendenceStage) -> None:
        self._log.append(
            f"[ADVANCE] → Stage {stage.stage.value}: {stage.name}"
        )
