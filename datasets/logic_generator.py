"""
Generate synthetic reasoning rules and propositions.
"""

import random
from typing import List, Tuple
from transcendence.reasoning import ReasoningEngine, RuleType

def generate_reasoning_data(num_propositions: int, num_rules: int, depth: int, seed: int = 42) -> ReasoningEngine:
    random.seed(seed)
    engine = ReasoningEngine()
    
    # Generate propositions
    prop_ids = []
    for i in range(num_propositions):
        # Base facts are known (depth 0), others are unknown
        truth_value = random.uniform(0.6, 1.0) if i < (num_propositions * 0.2) else None
        domain = random.choice(["science", "philosophy", "ethics", "ontology"])
        prop = engine.add_proposition(f"Prop_{i}", truth_value, domain)
        prop_ids.append(prop.id)
        
    # Generate rules to form a deep chain
    rule_types = list(RuleType)
    
    for i in range(num_rules):
        num_premises = random.randint(1, 3)
        premises = random.sample(prop_ids, num_premises)
        
        # To ensure depth, mostly pick conclusions that are "further down" the list
        conclusion = random.choice(prop_ids)
        if conclusion in premises:
            continue
            
        rtype = random.choice(rule_types)
        confidence = random.uniform(0.5, 0.99)
        
        engine.add_rule(f"Rule_{i}", premises, conclusion, rtype, confidence)
        
    return engine
