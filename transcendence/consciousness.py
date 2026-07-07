"""
Consciousness Model — computational consciousness modelling based on IIT and GWT.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set


class QualiaCategory(Enum):
    PERCEPTUAL = auto()
    EMOTIONAL = auto()
    COGNITIVE = auto()
    AESTHETIC = auto()
    EXISTENTIAL = auto()
    TRANSCENDENT = auto()


@dataclass
class Qualia:
    experience: str
    intensity: float
    valence: float
    category: QualiaCategory
    timestamp: float = field(default_factory=time.time)
    
    @property
    def id(self) -> str:
        return hashlib.sha256(self.experience.encode("utf-8")).hexdigest()[:16]


@dataclass
class ConsciousnessState:
    phi: float
    awareness_level: float
    active_qualia: List[Qualia]
    global_workspace: List[str]
    attention_focus: Optional[str]
    metacognitive_depth: int


class GlobalWorkspace:
    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.workspace: List[str] = []
        
    def broadcast(self, information: str, priority: float) -> None:
        if len(self.workspace) >= self.capacity:
            self.workspace.pop(0) # FIFO for simplicity
        self.workspace.append(information)
        
    def current_broadcast(self) -> List[str]:
        return list(self.workspace)


class ConsciousnessModel:
    def __init__(self, name: str):
        self.name = name
        self.workspace = GlobalWorkspace()
        self.qualia_stream: List[Qualia] = []
        self.attention_focus: Optional[str] = None
        
    def experience(self, description: str, intensity: float, valence: float, category: QualiaCategory) -> Qualia:
        q = Qualia(description, intensity, valence, category)
        self.qualia_stream.append(q)
        return q
        
    def integrate(self) -> float:
        # Mock calculation of Integrated Information (Phi)
        if not self.qualia_stream:
            return 0.0
        return sum(q.intensity for q in self.qualia_stream[-10:]) / 10.0
        
    def broadcast(self, information: str, priority: float) -> None:
        self.workspace.broadcast(information, priority)
        
    def introspect(self) -> ConsciousnessState:
        return ConsciousnessState(
            phi=self.integrate(),
            awareness_level=min(1.0, len(self.workspace.workspace) / self.workspace.capacity),
            active_qualia=self.qualia_stream[-5:],
            global_workspace=self.workspace.current_broadcast(),
            attention_focus=self.attention_focus,
            metacognitive_depth=1
        )
        
    def summary(self) -> str:
        state = self.introspect()
        return f"ConsciousnessModel({self.name} | Phi={state.phi:.2f} | Workspace={len(state.global_workspace)})"
