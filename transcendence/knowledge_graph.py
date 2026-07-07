"""
Knowledge Graph — graph-based representation of epistemic relationships.

Provides classes to construct a directed graph where nodes are concepts,
beliefs, or insights, and edges denote logical relationships.
"""

from __future__ import annotations

import collections
import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple

from .exceptions import EdgeNotFoundError, NodeNotFoundError


class NodeType(Enum):
    CONCEPT = auto()
    BELIEF = auto()
    INSIGHT = auto()
    AXIOM = auto()
    HYPOTHESIS = auto()
    LAW = auto()


class EdgeType(Enum):
    SUPPORTS = auto()
    CONTRADICTS = auto()
    DERIVES_FROM = auto()
    GENERALIZES = auto()
    SPECIALIZES = auto()
    ANALOGOUS_TO = auto()
    CAUSES = auto()
    CORRELATES = auto()
    REQUIRES = auto()
    SUPERSEDES = auto()


@dataclass
class KnowledgeNode:
    label: str
    node_type: NodeType
    confidence: float
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    
    @property
    def id(self) -> str:
        return hashlib.sha256(self.label.encode("utf-8")).hexdigest()[:16]


@dataclass
class KnowledgeEdge:
    source_id: str
    target_id: str
    edge_type: EdgeType
    weight: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class KnowledgeGraph:
    def __init__(self) -> None:
        self.nodes: Dict[str, KnowledgeNode] = {}
        # adjacency list: source_id -> target_id -> edge
        self.edges: Dict[str, Dict[str, KnowledgeEdge]] = collections.defaultdict(dict)
        # reverse adjacency list: target_id -> source_id -> edge
        self.reverse_edges: Dict[str, Dict[str, KnowledgeEdge]] = collections.defaultdict(dict)

    def add_node(self, label: str, node_type: NodeType, confidence: float, **properties: Any) -> KnowledgeNode:
        if not (0.0 <= confidence <= 1.0):
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {confidence}")
        
        node = KnowledgeNode(label=label, node_type=node_type, confidence=confidence, properties=properties)
        self.nodes[node.id] = node
        return node

    def add_edge(self, source_id: str, target_id: str, edge_type: EdgeType, weight: float = 1.0, **metadata: Any) -> KnowledgeEdge:
        if source_id not in self.nodes:
            raise NodeNotFoundError(source_id)
        if target_id not in self.nodes:
            raise NodeNotFoundError(target_id)
        if not (0.0 <= weight <= 1.0):
            raise ValueError(f"Weight must be between 0.0 and 1.0, got {weight}")

        edge = KnowledgeEdge(source_id, target_id, edge_type, weight, metadata)
        self.edges[source_id][target_id] = edge
        self.reverse_edges[target_id][source_id] = edge
        return edge

    def remove_node(self, node_id: str) -> None:
        if node_id not in self.nodes:
            raise NodeNotFoundError(node_id)
        
        for target_id in list(self.edges[node_id].keys()):
            self.remove_edge(node_id, target_id)
        for source_id in list(self.reverse_edges[node_id].keys()):
            self.remove_edge(source_id, node_id)
            
        del self.nodes[node_id]
        del self.edges[node_id]
        del self.reverse_edges[node_id]

    def remove_edge(self, source_id: str, target_id: str) -> None:
        if source_id in self.edges and target_id in self.edges[source_id]:
            del self.edges[source_id][target_id]
            del self.reverse_edges[target_id][source_id]
        else:
            raise EdgeNotFoundError(f"No edge from {source_id} to {target_id}")

    def get_node(self, node_id: str) -> KnowledgeNode:
        if node_id not in self.nodes:
            raise NodeNotFoundError(node_id)
        return self.nodes[node_id]

    def get_neighbors(self, node_id: str, edge_type: Optional[EdgeType] = None) -> List[Tuple[KnowledgeNode, KnowledgeEdge]]:
        if node_id not in self.nodes:
            raise NodeNotFoundError(node_id)
        
        neighbors = []
        for target_id, edge in self.edges.get(node_id, {}).items():
            if edge_type is None or edge.edge_type == edge_type:
                neighbors.append((self.nodes[target_id], edge))
        return neighbors

    def find_path(self, source_id: str, target_id: str) -> List[KnowledgeNode]:
        if source_id not in self.nodes:
            raise NodeNotFoundError(source_id)
        if target_id not in self.nodes:
            raise NodeNotFoundError(target_id)
            
        queue = collections.deque([[source_id]])
        seen = {source_id}
        
        while queue:
            path = queue.popleft()
            node_id = path[-1]
            
            if node_id == target_id:
                return [self.nodes[nid] for nid in path]
                
            for neighbor_id in self.edges.get(node_id, {}):
                if neighbor_id not in seen:
                    seen.add(neighbor_id)
                    new_path = list(path)
                    new_path.append(neighbor_id)
                    queue.append(new_path)
                    
        return []

    def get_connected_component(self, node_id: str) -> Set[str]:
        if node_id not in self.nodes:
            raise NodeNotFoundError(node_id)
            
        component = set()
        queue = collections.deque([node_id])
        
        while queue:
            curr = queue.popleft()
            if curr not in component:
                component.add(curr)
                for neighbor in self.edges.get(curr, {}):
                    if neighbor not in component:
                        queue.append(neighbor)
                for neighbor in self.reverse_edges.get(curr, {}):
                    if neighbor not in component:
                        queue.append(neighbor)
                        
        return component

    def pagerank(self, damping: float = 0.85, iterations: int = 100) -> Dict[str, float]:
        n = len(self.nodes)
        if n == 0:
            return {}
            
        ranks = {node_id: 1.0 / n for node_id in self.nodes}
        
        for _ in range(iterations):
            new_ranks = {}
            for node_id in self.nodes:
                rank_sum = 0.0
                for source_id in self.reverse_edges.get(node_id, {}):
                    out_degree = len(self.edges.get(source_id, {}))
                    if out_degree > 0:
                        rank_sum += ranks[source_id] / out_degree
                new_ranks[node_id] = (1 - damping) / n + damping * rank_sum
            ranks = new_ranks
            
        return ranks

    def to_dot(self) -> str:
        lines = ["digraph KnowledgeGraph {", '  node [shape=box, style=filled, fillcolor="#f0f0f0"];']
        for node_id, node in self.nodes.items():
            safe_label = node.label.replace('"', '\\"')
            lines.append(f'  "{node_id}" [label="{safe_label}\\n({node.node_type.name})"];')
            
        for source_id, targets in self.edges.items():
            for target_id, edge in targets.items():
                lines.append(f'  "{source_id}" -> "{target_id}" [label="{edge.edge_type.name}", weight={edge.weight}];')
                
        lines.append("}")
        return "\n".join(lines)
