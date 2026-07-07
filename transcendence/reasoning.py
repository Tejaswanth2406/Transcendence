"""
Reasoning Engine — Formal inference framework for Transcendence.

Allows deduction, induction, abduction, and analogical reasoning
over a set of propositions.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple

from .exceptions import InvalidInferenceError, CircularReasoningError


class RuleType(Enum):
    DEDUCTIVE = auto()
    INDUCTIVE = auto()
    ABDUCTIVE = auto()
    ANALOGICAL = auto()
    TRANSCENDENT = auto()


@dataclass
class Proposition:
    statement: str
    truth_value: Optional[float]
    domain: str
    
    @property
    def id(self) -> str:
        return hashlib.sha256(self.statement.encode("utf-8")).hexdigest()[:16]


@dataclass
class InferenceRule:
    name: str
    premises: List[str]
    conclusion: str
    rule_type: RuleType
    confidence: float


@dataclass
class Argument:
    premises: List[Proposition]
    conclusion: Proposition
    rule: InferenceRule
    strength: float


class ReasoningEngine:
    def __init__(self) -> None:
        self.propositions: Dict[str, Proposition] = {}
        self.rules: List[InferenceRule] = []

    def add_proposition(self, statement: str, truth_value: Optional[float], domain: str) -> Proposition:
        if truth_value is not None and not (0.0 <= truth_value <= 1.0):
            raise ValueError(f"Truth value must be between 0.0 and 1.0, got {truth_value}")
        prop = Proposition(statement=statement, truth_value=truth_value, domain=domain)
        self.propositions[prop.id] = prop
        return prop

    def add_rule(self, name: str, premise_ids: List[str], conclusion_id: str, rule_type: RuleType, confidence: float) -> InferenceRule:
        if not (0.0 <= confidence <= 1.0):
            raise ValueError("Confidence must be in [0.0, 1.0]")
            
        for pid in premise_ids:
            if pid not in self.propositions:
                raise ValueError(f"Premise proposition {pid} not found")
        if conclusion_id not in self.propositions:
            raise ValueError(f"Conclusion proposition {conclusion_id} not found")
            
        rule = InferenceRule(name, premise_ids, conclusion_id, rule_type, confidence)
        self.rules.append(rule)
        return rule

    def forward_chain(self, max_iterations: int = 100) -> List[Proposition]:
        derived = []
        for _ in range(max_iterations):
            changed = False
            for rule in self.rules:
                premise_truths = []
                for pid in rule.premises:
                    tv = self.propositions[pid].truth_value
                    if tv is None:
                        break
                    premise_truths.append(tv)
                    
                if len(premise_truths) == len(rule.premises) and all(pt > 0.5 for pt in premise_truths):
                    strength = (sum(premise_truths) / len(premise_truths)) * rule.confidence
                    conclusion = self.propositions[rule.conclusion]
                    
                    if conclusion.truth_value is None or conclusion.truth_value < strength:
                        conclusion.truth_value = strength
                        derived.append(conclusion)
                        changed = True
            if not changed:
                break
        return derived

    def backward_chain(self, goal_id: str, _visited: Optional[Set[str]] = None) -> Optional[List[Argument]]:
        if _visited is None:
            _visited = set()
            
        if goal_id in _visited:
            raise CircularReasoningError(f"Cycle detected at {goal_id}")
            
        _visited.add(goal_id)
        goal = self.propositions.get(goal_id)
        if not goal:
            return None
            
        if goal.truth_value is not None and goal.truth_value > 0.8:
            return []
            
        for rule in self.rules:
            if rule.conclusion == goal_id:
                sub_proofs = []
                success = True
                for pid in rule.premises:
                    proof = self.backward_chain(pid, _visited.copy())
                    if proof is None:
                        success = False
                        break
                    sub_proofs.extend(proof)
                    
                if success:
                    premise_props = [self.propositions[p] for p in rule.premises]
                    strength = rule.confidence
                    arg = Argument(premise_props, goal, rule, strength)
                    sub_proofs.append(arg)
                    return sub_proofs
                    
        return None

    def find_contradictions(self) -> List[Tuple[Proposition, Proposition]]:
        return []

    def coherence_check(self) -> Dict[str, Any]:
        valid_rules = sum(1 for r in self.rules if r.confidence > 0.5)
        return {
            "total_propositions": len(self.propositions),
            "known_truths": sum(1 for p in self.propositions.values() if p.truth_value is not None and p.truth_value > 0.5),
            "total_rules": len(self.rules),
            "valid_rules": valid_rules,
            "coherence_score": valid_rules / max(1, len(self.rules))
        }

    def summary(self) -> str:
        return f"ReasoningEngine(propositions={len(self.propositions)}, rules={len(self.rules)})"
