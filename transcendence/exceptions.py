"""
Transcendence Exception Hierarchy
==================================

A structured hierarchy of exceptions for the Transcendence framework.
Every module raises domain-specific exceptions that inherit from
``TranscendenceError``, enabling callers to catch broadly or narrowly.

Exception Tree
--------------
TranscendenceError
├── StageError
│   ├── StageTransitionError
│   └── InvalidStageError
├── BeliefError
│   ├── BeliefNotFoundError
│   └── BeliefConflictError
├── ValidationError
│   ├── ConfidenceError
│   └── EmptyInputError
├── SerializationError
│   ├── SerializeError
│   └── DeserializeError
├── KnowledgeGraphError
│   ├── NodeNotFoundError
│   └── EdgeNotFoundError
├── ReasoningError
│   ├── CircularReasoningError
│   └── InvalidInferenceError
├── EvolutionError
│   └── PopulationExtinctError
├── ConsciousnessError
│   └── IntegrationError
├── EthicsError
│   └── DilemmaUnresolvableError
└── EmergenceError
    └── ComplexityComputationError
"""
from __future__ import annotations

# ── Base ──────────────────────────────────────────────────────────────

class TranscendenceError(Exception):
    """Root exception for every error raised by the Transcendence framework."""
    def __init__(self, message: str = "", *, context: dict | None = None) -> None:
        self.context = context or {}
        super().__init__(message)


# ── Stage Errors ──────────────────────────────────────────────────────

class StageError(TranscendenceError):
    """Base exception for stage-related errors."""


class StageTransitionError(StageError):
    """Raised when a stage transition is invalid."""


class InvalidStageError(StageError):
    """Raised when an invalid stage is specified."""


# ── Belief Errors ─────────────────────────────────────────────────────

class BeliefError(TranscendenceError):
    """Base exception for belief-related errors."""


class BeliefNotFoundError(BeliefError):
    """Raised when a specific belief cannot be found."""


class BeliefConflictError(BeliefError):
    """Raised when there is an irreconcilable conflict between beliefs."""


# ── Validation Errors ─────────────────────────────────────────────────

class ValidationError(TranscendenceError):
    """Base exception for validation errors."""


class ConfidenceError(ValidationError):
    """Raised when a confidence value is out of valid bounds."""


class EmptyInputError(ValidationError):
    """Raised when an input is unexpectedly empty."""


# ── Serialization Errors ──────────────────────────────────────────────

class SerializationError(TranscendenceError):
    """Base exception for serialization/deserialization errors."""


class SerializeError(SerializationError):
    """Raised when an object cannot be serialized."""


class DeserializeError(SerializationError):
    """Raised when data cannot be deserialized."""


# ── Knowledge Graph Errors ────────────────────────────────────────────

class KnowledgeGraphError(TranscendenceError):
    """Base exception for knowledge graph errors."""


class NodeNotFoundError(KnowledgeGraphError):
    """Raised when a node cannot be found in the knowledge graph."""


class EdgeNotFoundError(KnowledgeGraphError):
    """Raised when an edge cannot be found in the knowledge graph."""


# ── Reasoning Errors ──────────────────────────────────────────────────

class ReasoningError(TranscendenceError):
    """Base exception for reasoning engine errors."""


class CircularReasoningError(ReasoningError):
    """Raised when circular reasoning is detected."""


class InvalidInferenceError(ReasoningError):
    """Raised when an invalid inference is made."""


# ── Evolution Errors ──────────────────────────────────────────────────

class EvolutionError(TranscendenceError):
    """Base exception for evolution engine errors."""


class PopulationExtinctError(EvolutionError):
    """Raised when an evolutionary population goes extinct."""


# ── Consciousness Errors ──────────────────────────────────────────────

class ConsciousnessError(TranscendenceError):
    """Base exception for consciousness modeling errors."""


class IntegrationError(ConsciousnessError):
    """Raised when integration computation fails."""


# ── Ethics Errors ─────────────────────────────────────────────────────

class EthicsError(TranscendenceError):
    """Base exception for ethical framework errors."""


class DilemmaUnresolvableError(EthicsError):
    """Raised when an ethical dilemma cannot be resolved."""


# ── Emergence Errors ──────────────────────────────────────────────────

class EmergenceError(TranscendenceError):
    """Base exception for emergence and complexity errors."""


class ComplexityComputationError(EmergenceError):
    """Raised when a complexity metric cannot be computed."""
