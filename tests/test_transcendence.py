"""
Full test suite for Transcendence research-grade modules.
Tests cover: exceptions, knowledge graph, reasoning, evolution, consciousness, ethics, emergence, persistence.
"""

from __future__ import annotations
import time
import pytest

# ─── Exceptions ──────────────────────────────────────────────────────────────
from transcendence.exceptions import (
    TranscendenceError, StageError, StageTransitionError, InvalidStageError,
    BeliefError, BeliefNotFoundError, BeliefConflictError,
    ValidationError, ConfidenceError, EmptyInputError,
    SerializationError, SerializeError, DeserializeError,
    KnowledgeGraphError, NodeNotFoundError, EdgeNotFoundError,
    ReasoningError, CircularReasoningError, InvalidInferenceError,
    EvolutionError, PopulationExtinctError,
    ConsciousnessError, IntegrationError,
    EthicsError, DilemmaUnresolvableError,
    EmergenceError, ComplexityComputationError,
)

class TestExceptionHierarchy:
    def test_all_inherit_from_base(self):
        leaf_classes = [
            StageTransitionError, InvalidStageError,
            BeliefNotFoundError, BeliefConflictError,
            ConfidenceError, EmptyInputError,
            SerializeError, DeserializeError,
            NodeNotFoundError, EdgeNotFoundError,
            CircularReasoningError, InvalidInferenceError,
            PopulationExtinctError, IntegrationError,
            DilemmaUnresolvableError, ComplexityComputationError,
        ]
        for cls in leaf_classes:
            assert issubclass(cls, TranscendenceError), f"{cls} must inherit from TranscendenceError"

    def test_exception_context(self):
        err = TranscendenceError("test msg", context={"key": "value"})
        assert err.context == {"key": "value"}
        assert str(err) == "test msg"

    def test_stage_hierarchy(self):
        assert issubclass(StageTransitionError, StageError)
        assert issubclass(InvalidStageError, StageError)

    def test_knowledge_graph_hierarchy(self):
        assert issubclass(NodeNotFoundError, KnowledgeGraphError)
        assert issubclass(EdgeNotFoundError, KnowledgeGraphError)

    def test_reasoning_hierarchy(self):
        assert issubclass(CircularReasoningError, ReasoningError)
        assert issubclass(InvalidInferenceError, ReasoningError)


# ─── Knowledge Graph ─────────────────────────────────────────────────────────
from transcendence.knowledge_graph import KnowledgeGraph, NodeType, EdgeType

class TestKnowledgeGraph:
    def setup_method(self):
        self.kg = KnowledgeGraph()

    def test_add_node(self):
        n = self.kg.add_node("Consciousness", NodeType.CONCEPT, 0.9)
        assert n.label == "Consciousness"
        assert n.node_type == NodeType.CONCEPT
        assert n.id in self.kg.nodes

    def test_node_id_deterministic(self):
        n1 = self.kg.add_node("X", NodeType.BELIEF, 0.5)
        n2 = self.kg.add_node("X", NodeType.BELIEF, 0.5)
        assert n1.id == n2.id

    def test_add_edge(self):
        a = self.kg.add_node("A", NodeType.AXIOM, 0.99)
        b = self.kg.add_node("B", NodeType.HYPOTHESIS, 0.6)
        e = self.kg.add_edge(a.id, b.id, EdgeType.SUPPORTS, 0.8)
        assert e.source_id == a.id
        assert e.target_id == b.id

    def test_invalid_confidence_raises(self):
        with pytest.raises(ValueError):
            self.kg.add_node("bad", NodeType.CONCEPT, 1.5)
        with pytest.raises(ValueError):
            self.kg.add_node("bad", NodeType.CONCEPT, -0.1)

    def test_invalid_edge_weight_raises(self):
        a = self.kg.add_node("A", NodeType.CONCEPT, 0.5)
        b = self.kg.add_node("B", NodeType.CONCEPT, 0.5)
        with pytest.raises(ValueError):
            self.kg.add_edge(a.id, b.id, EdgeType.CAUSES, 1.5)

    def test_missing_node_edge_raises(self):
        a = self.kg.add_node("A", NodeType.CONCEPT, 0.5)
        with pytest.raises(NodeNotFoundError):
            self.kg.add_edge(a.id, "fake_id", EdgeType.CAUSES, 0.5)

    def test_remove_node(self):
        n = self.kg.add_node("Temp", NodeType.CONCEPT, 0.5)
        self.kg.remove_node(n.id)
        assert n.id not in self.kg.nodes

    def test_find_path_bfs(self):
        a = self.kg.add_node("A", NodeType.CONCEPT, 0.9)
        b = self.kg.add_node("B", NodeType.CONCEPT, 0.9)
        c = self.kg.add_node("C", NodeType.CONCEPT, 0.9)
        self.kg.add_edge(a.id, b.id, EdgeType.DERIVES_FROM, 0.9)
        self.kg.add_edge(b.id, c.id, EdgeType.DERIVES_FROM, 0.9)
        path = self.kg.find_path(a.id, c.id)
        assert len(path) == 3
        assert path[0].id == a.id
        assert path[-1].id == c.id

    def test_find_path_no_path_returns_empty(self):
        a = self.kg.add_node("A", NodeType.CONCEPT, 0.9)
        b = self.kg.add_node("B", NodeType.CONCEPT, 0.9)
        path = self.kg.find_path(a.id, b.id)
        assert path == []

    def test_connected_component(self):
        a = self.kg.add_node("A", NodeType.CONCEPT, 0.9)
        b = self.kg.add_node("B", NodeType.CONCEPT, 0.9)
        c = self.kg.add_node("C", NodeType.CONCEPT, 0.9)
        self.kg.add_edge(a.id, b.id, EdgeType.SUPPORTS, 0.9)
        component = self.kg.get_connected_component(a.id)
        assert a.id in component
        assert b.id in component
        assert c.id not in component

    def test_pagerank_returns_all_nodes(self):
        for i in range(5):
            self.kg.add_node(f"N{i}", NodeType.CONCEPT, 0.8)
        ranks = self.kg.pagerank(iterations=10)
        assert set(ranks.keys()) == set(self.kg.nodes.keys())

    def test_to_dot(self):
        a = self.kg.add_node("A", NodeType.CONCEPT, 0.9)
        b = self.kg.add_node("B", NodeType.LAW, 0.7)
        self.kg.add_edge(a.id, b.id, EdgeType.CAUSES, 0.8)
        dot = self.kg.to_dot()
        assert "digraph KnowledgeGraph" in dot
        assert "CAUSES" in dot


# ─── Reasoning ───────────────────────────────────────────────────────────────
from transcendence.reasoning import ReasoningEngine, RuleType

class TestReasoningEngine:
    def setup_method(self):
        self.engine = ReasoningEngine()

    def test_add_proposition(self):
        p = self.engine.add_proposition("All humans are mortal.", 0.99, "logic")
        assert p.id in self.engine.propositions
        assert p.truth_value == 0.99

    def test_invalid_truth_value_raises(self):
        with pytest.raises(ValueError):
            self.engine.add_proposition("X", 1.5, "test")
        with pytest.raises(ValueError):
            self.engine.add_proposition("X", -0.1, "test")

    def test_forward_chain_derives_truths(self):
        p1 = self.engine.add_proposition("Socrates is human.", 0.99, "logic")
        p2 = self.engine.add_proposition("All humans are mortal.", 0.99, "logic")
        p3 = self.engine.add_proposition("Socrates is mortal.", None, "logic")
        self.engine.add_rule("modus_ponens", [p1.id, p2.id], p3.id, RuleType.DEDUCTIVE, 0.95)
        derived = self.engine.forward_chain()
        assert any(d.id == p3.id for d in derived)
        assert self.engine.propositions[p3.id].truth_value is not None

    def test_coherence_check_structure(self):
        self.engine.add_proposition("P1", 0.9, "test")
        result = self.engine.coherence_check()
        assert "total_propositions" in result
        assert "coherence_score" in result
        assert 0.0 <= result["coherence_score"] <= 1.0

    def test_summary(self):
        s = self.engine.summary()
        assert "ReasoningEngine" in s


# ─── Evolution ───────────────────────────────────────────────────────────────
from transcendence.evolution import EvolutionEngine, Genome

class TestEvolutionEngine:
    def test_initialize_population(self):
        engine = EvolutionEngine(population_size=20)
        traits = ["Curiosity", "Rigor", "Humility"]
        pop = engine.initialize_population(traits)
        assert len(pop) == 20
        assert all(len(g.genes) == len(traits) for g in pop)

    def test_evolve_generation(self):
        engine = EvolutionEngine(population_size=10)
        engine.initialize_population(["T1", "T2", "T3"])
        engine.evaluate_population(lambda g: sum(x.mutation_rate for x in g.genes))
        new_pop = engine.evolve_generation()
        assert len(new_pop) == 10

    def test_crossover_produces_child(self):
        engine = EvolutionEngine(population_size=5)
        pop = engine.initialize_population(["A", "B", "C"])
        child = pop[0].crossover(pop[1])
        assert len(child.genes) == 3

    def test_summary_after_run(self):
        engine = EvolutionEngine(population_size=5)
        engine.initialize_population(["X", "Y"])
        engine.evaluate_population(lambda g: 0.5)
        s = engine.summary()
        assert "EvolutionEngine" in s


# ─── Consciousness ────────────────────────────────────────────────────────────
from transcendence.consciousness import ConsciousnessModel, QualiaCategory

class TestConsciousnessModel:
    def setup_method(self):
        self.model = ConsciousnessModel("TestMind")

    def test_experience_creates_qualia(self):
        q = self.model.experience("Red glow", 0.9, 0.7, QualiaCategory.PERCEPTUAL)
        assert q.experience == "Red glow"
        assert q.intensity == 0.9
        assert len(self.model.qualia_stream) == 1

    def test_integrate_returns_float(self):
        phi = self.model.integrate()
        assert isinstance(phi, float)

    def test_broadcast_fills_workspace(self):
        self.model.broadcast("Consciousness is primary", 1.0)
        ws = self.model.workspace.current_broadcast()
        assert len(ws) > 0

    def test_introspect_returns_state(self):
        self.model.experience("Wonder", 0.8, 0.9, QualiaCategory.EXISTENTIAL)
        state = self.model.introspect()
        assert hasattr(state, "phi")
        assert hasattr(state, "global_workspace")
        assert 0.0 <= state.awareness_level <= 1.0

    def test_summary(self):
        s = self.model.summary()
        assert "TestMind" in s


# ─── Ethics ──────────────────────────────────────────────────────────────────
from transcendence.ethics import EthicalReasoner, Action, EthicalFramework

class TestEthicsReasoner:
    def setup_method(self):
        self.reasoner = EthicalReasoner()

    def test_define_virtue(self):
        v = self.reasoner.define_virtue("Courage", "Acting despite fear", ["Spoke up"], "Cowardice", "Recklessness")
        assert v.name == "Courage"
        assert "Courage" in self.reasoner.virtues

    def test_evaluate_action(self):
        action = Action(
            description="Share knowledge freely",
            agent="TIA",
            affected_parties=["students"],
            intended_consequences=["learning"],
            unintended_consequences=[]
        )
        judgment = self.reasoner.evaluate_action(action, EthicalFramework.UTILITARIAN)
        assert -1.0 <= judgment.verdict <= 1.0
        assert 0.0 <= judgment.confidence <= 1.0

    def test_kernel_alignment(self):
        action = Action("Expand understanding", "TIA", [], [], [])
        result = self.reasoner.kernel_alignment_check(action)
        assert isinstance(result, dict)
        assert len(result) == 7

    def test_summary(self):
        s = self.reasoner.summary()
        assert "EthicalReasoner" in s


# ─── Emergence ───────────────────────────────────────────────────────────────
from transcendence.emergence import EmergenceEngine, ComplexityAnalyzer

class TestEmergenceEngine:
    def test_shannon_entropy_uniform(self):
        data = [1, 2, 3, 4]  # uniform → max entropy for 4 symbols
        h = ComplexityAnalyzer.shannon_entropy(data)
        assert h == pytest.approx(2.0, abs=0.01)

    def test_shannon_entropy_constant(self):
        data = [1, 1, 1, 1]  # fully predictable → zero entropy
        h = ComplexityAnalyzer.shannon_entropy(data)
        assert h == 0.0

    def test_kolmogorov_estimate_random(self):
        import random, string
        random.seed(42)
        rand_str = "".join(random.choices(string.ascii_letters, k=500))
        k_rand = ComplexityAnalyzer.kolmogorov_estimate(rand_str)
        repeat_str = "AB" * 250
        k_repeat = ComplexityAnalyzer.kolmogorov_estimate(repeat_str)
        assert k_rand > k_repeat  # random is harder to compress

    def test_register_and_observe(self):
        engine = EmergenceEngine()
        engine.register_component("sensor", lambda: 0.75)
        obs = engine.observe()
        assert "sensor" in obs
        assert obs["sensor"] == 0.75


# ─── Persistence ─────────────────────────────────────────────────────────────
from transcendence.persistence import save, load
from transcendence.intelligence import TranscendentIntelligence
from transcendence.exceptions import DeserializeError
import tempfile, os

class TestPersistence:
    def test_save_and_load_roundtrip(self):
        ti = TranscendentIntelligence("SaveTest")
        ti.observe("Persistence must be reliable.", confidence=0.9)
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            save(ti, path)
            loaded = load(path)
            assert loaded.name == "SaveTest"
        finally:
            os.unlink(path)

    def test_load_missing_file_raises(self):
        with pytest.raises(DeserializeError):
            load("/nonexistent/path/file.json")

    def test_checksum_tamper_raises(self):
        ti = TranscendentIntelligence("TamperTest")
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            path = f.name
            f.write('{"schema_version":"2.0.0","checksum":"badhash","payload":{}}')
        try:
            with pytest.raises(DeserializeError):
                load(path, verify_checksum=True)
        finally:
            os.unlink(path)


# ─── Statistics core ─────────────────────────────────────────────────────────
from benchmarks.core.statistics import calculate_statistics

class TestStatistics:
    def test_basic_stats(self):
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        stats = calculate_statistics(data)
        assert stats["mean"] == pytest.approx(3.0)
        assert stats["min"] == 1.0
        assert stats["max"] == 5.0

    def test_single_element(self):
        stats = calculate_statistics([42.0])
        assert stats["mean"] == 42.0
        assert stats["variance"] == 0.0

    def test_p95_within_range(self):
        data = list(range(1, 101))
        stats = calculate_statistics([float(x) for x in data])
        assert 94 <= stats["p95"] <= 96
