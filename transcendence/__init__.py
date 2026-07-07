"""
Transcendence — A Python framework for recursive self-improvement and epistemic evolution.
"""

from .stages import TranscendenceStage, StageEngine
from .intelligence import TranscendentIntelligence
from .meta import MetaCognition
from .knowledge_graph import KnowledgeGraph, KnowledgeNode, KnowledgeEdge
from .reasoning import ReasoningEngine, Proposition, InferenceRule, Argument
from .evolution import EvolutionEngine, Genome, Gene
from .consciousness import ConsciousnessModel, Qualia, ConsciousnessState
from .ethics import EthicalReasoner, Action, MoralJudgment
from .emergence import EmergenceEngine, EmergentPattern
from .persistence import save, load
from .exceptions import TranscendenceError

__version__ = "2.0.0"
__all__ = [
    "TranscendenceStage", "StageEngine", "TranscendentIntelligence", "MetaCognition",
    "KnowledgeGraph", "KnowledgeNode", "KnowledgeEdge",
    "ReasoningEngine", "Proposition", "InferenceRule", "Argument",
    "EvolutionEngine", "Genome", "Gene",
    "ConsciousnessModel", "Qualia", "ConsciousnessState",
    "EthicalReasoner", "Action", "MoralJudgment",
    "EmergenceEngine", "EmergentPattern",
    "save", "load",
    "TranscendenceError"
]
