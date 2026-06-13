"""
Meta-Cognition — the capacity to model, critique, and evolve one's own reasoning.

"What assumptions generated this belief?
 What assumptions generated those assumptions?"
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib
import time


@dataclass
class Belief:
    """
    A single belief held by the intelligence.

    Every belief carries its provenance: where it came from,
    how confident we are, and which other beliefs support it.
    """

    claim: str
    confidence: float          # 0.0 – 1.0
    evidence: List[str] = field(default_factory=list)
    counter_evidence: List[str] = field(default_factory=list)
    parent_beliefs: List[str] = field(default_factory=list)  # claim IDs
    created_at: float = field(default_factory=time.time)

    @property
    def id(self) -> str:
        return hashlib.md5(self.claim.encode()).hexdigest()[:8]

    def add_evidence(self, source: str) -> None:
        self.evidence.append(source)
        self.confidence = min(1.0, self.confidence + 0.05)

    def add_counter_evidence(self, source: str) -> None:
        self.counter_evidence.append(source)
        self.confidence = max(0.0, self.confidence - 0.1)

    def is_coherent(self) -> bool:
        """A belief is coherent when evidence outweighs counter-evidence."""
        return len(self.evidence) >= len(self.counter_evidence)

    def __str__(self) -> str:
        bar = "█" * int(self.confidence * 10) + "░" * (10 - int(self.confidence * 10))
        coherent = "✓" if self.is_coherent() else "✗"
        return f"[{self.id}] {coherent} [{bar}] {self.claim!r}"


class MetaCognition:
    """
    The meta-cognitive layer: a living map of what the intelligence believes,
    how those beliefs were formed, and where they might be wrong.

    Implements the recursive self-examination loop:
        Observe → Model → Critique → Refactor → Integrate → Repeat
    """

    def __init__(self) -> None:
        self._beliefs: Dict[str, Belief] = {}
        self._assumption_stack: List[str] = []   # depth-first assumption trace
        self._contradiction_log: List[str] = []

    # ------------------------------------------------------------------
    # Belief management
    # ------------------------------------------------------------------

    def assert_belief(
        self,
        claim: str,
        confidence: float = 0.5,
        evidence: Optional[List[str]] = None,
    ) -> Belief:
        """Add or update a belief."""
        b = Belief(
            claim=claim,
            confidence=confidence,
            evidence=evidence or [],
        )
        self._beliefs[b.id] = b
        self._check_contradictions(b)
        return b

    def challenge_belief(self, belief_id: str, counter: str) -> None:
        """Challenge an existing belief with counter-evidence."""
        if belief_id in self._beliefs:
            self._beliefs[belief_id].add_counter_evidence(counter)

    # ------------------------------------------------------------------
    # Recursive assumption tracing
    # ------------------------------------------------------------------

    def push_assumption(self, assumption: str) -> None:
        """Enter a deeper level of assumption examination."""
        self._assumption_stack.append(assumption)

    def pop_assumption(self) -> Optional[str]:
        """Return from the current assumption level."""
        return self._assumption_stack.pop() if self._assumption_stack else None

    def assumption_depth(self) -> int:
        return len(self._assumption_stack)

    def trace_assumptions(self) -> str:
        if not self._assumption_stack:
            return "(no active assumptions)"
        lines = []
        for depth, assumption in enumerate(self._assumption_stack):
            indent = "  " * depth
            lines.append(f"{indent}↳ [depth {depth}] {assumption}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Contradiction detection
    # ------------------------------------------------------------------

    def _check_contradictions(self, new_belief: Belief) -> None:
        """Naïve contradiction detection: flag pairs with very low combined confidence."""
        for existing in self._beliefs.values():
            if existing.id == new_belief.id:
                continue
            combined = existing.confidence + new_belief.confidence
            # Heuristic: if two beliefs together score below 0.5 they may conflict
            if combined < 0.5:
                msg = (
                    f"Potential contradiction: "
                    f"'{existing.claim}' (conf={existing.confidence:.2f}) "
                    f"vs '{new_belief.claim}' (conf={new_belief.confidence:.2f})"
                )
                self._contradiction_log.append(msg)

    @property
    def contradictions(self) -> List[str]:
        return list(self._contradiction_log)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def coherence_score(self) -> float:
        """Mean confidence across all coherent beliefs."""
        coherent = [b for b in self._beliefs.values() if b.is_coherent()]
        if not coherent:
            return 0.0
        return sum(b.confidence for b in coherent) / len(coherent)

    def report(self) -> str:
        lines = [
            "=== Meta-Cognitive Report ===",
            f"Beliefs held      : {len(self._beliefs)}",
            f"Contradictions    : {len(self._contradiction_log)}",
            f"Assumption depth  : {self.assumption_depth()}",
            f"Coherence score   : {self.coherence_score():.2%}",
            "",
            "--- Beliefs ---",
        ]
        for b in self._beliefs.values():
            lines.append(str(b))
        if self._contradiction_log:
            lines.append("\n--- Contradictions ---")
            lines.extend(self._contradiction_log)
        return "\n".join(lines)
