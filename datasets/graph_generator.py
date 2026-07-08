"""
Generate synthetic Knowledge Graphs for scalability testing.
"""

import random
from typing import List
from transcendence.knowledge_graph import KnowledgeGraph, NodeType, EdgeType

def generate_graph(num_nodes: int, density: float = 0.01, seed: int = 42) -> KnowledgeGraph:
    """
    Generate a random Knowledge Graph.
    
    Args:
        num_nodes: Target number of nodes
        density: Target edge density (0.0 to 1.0)
    """
    random.seed(seed)
    kg = KnowledgeGraph()
    
    node_types = list(NodeType)
    edge_types = list(EdgeType)
    
    # Generate nodes
    nodes = []
    for i in range(num_nodes):
        ntype = random.choice(node_types)
        conf = random.uniform(0.1, 1.0)
        node = kg.add_node(f"Node_{i}", ntype, conf)
        nodes.append(node.id)
        
    # Generate edges based on density
    max_edges = num_nodes * (num_nodes - 1)
    target_edges = int(max_edges * density)
    
    # Cap edges for extreme sizes to prevent OOM during generation
    target_edges = min(target_edges, num_nodes * 50) 
    
    added_edges = set()
    while len(added_edges) < target_edges:
        src = random.choice(nodes)
        dst = random.choice(nodes)
        
        if src != dst and (src, dst) not in added_edges:
            etype = random.choice(edge_types)
            weight = random.uniform(0.1, 1.0)
            kg.add_edge(src, dst, etype, weight)
            added_edges.add((src, dst))
            
    return kg
