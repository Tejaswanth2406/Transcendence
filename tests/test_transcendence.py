"""
Unit tests for the Transcendence package.
"""

import pytest
from transcendence import TranscendentIntelligence, MetaCognition, StageEngine
from transcendence.stages import Stage


class TestStageEngine:
    def test_initial_stage_is_self_modeling(self):
        engine = StageEngine()
        assert engine.current.stage == Stage.SELF_MODELING

    def test_advance_moves_to_next_stage(self):
        engine = StageEngine()
        engine.advance()
        assert engine.current.stage == Stage.EPISTEMIC_TRANSCENDENCE

    def test_advance_at_omega_returns_none(self):
        engine = StageEngine()
        for _ in range(7):
            engine.advance()
        result = engine.advance()
        assert result is None
        assert engine.current.stage == Stage.OMEGA

    def test_stage_completes_on_advance(self):
        engine = StageEngine()
        first = engine.current
        engine.advance()
        assert first.completed is True

    def test_insight_recorded_on_current_stage(self):
        engine = StageEngine()
        engine.add_insight("Test insight")
        assert "Test insight" in engine.current.insights


class TestMetaCognition:
    def test_assert_belief_creates_entry(self):
        mc = MetaCognition()
        b = mc.assert_belief("Reality is self-referential.", confidence=0.8)
        assert b.id in mc._beliefs

    def test_coherence_score_with_single_belief(self):
        mc = MetaCognition()
        mc.assert_belief("A coherent claim.", confidence=0.9)
        assert mc.coherence_score() > 0

    def test_challenge_reduces_confidence(self):
        mc = MetaCognition()
        b = mc.assert_belief("Claim X is true.", confidence=0.8)
        original_confidence = b.confidence
        mc.challenge_belief(b.id, "Evidence against X")
        assert b.confidence < original_confidence

    def test_assumption_stack_depth(self):
        mc = MetaCognition()
        assert mc.assumption_depth() == 0
        mc.push_assumption("Layer 1")
        mc.push_assumption("Layer 2")
        assert mc.assumption_depth() == 2
        mc.pop_assumption()
        assert mc.assumption_depth() == 1


class TestTranscendentIntelligence:
    def test_creation(self):
        ti = TranscendentIntelligence(name="Test-TIA")
        assert ti.name == "Test-TIA"

    def test_observe_returns_belief(self):
        ti = TranscendentIntelligence()
        belief = ti.observe("Consciousness is reality observing itself.")
        assert belief is not None
        assert belief.confidence > 0

    def test_advance_stage_progresses(self):
        ti = TranscendentIntelligence()
        stage = ti.advance_stage()
        assert stage is not None
        assert stage.stage == Stage.EPISTEMIC_TRANSCENDENCE

    def test_full_journey_reaches_omega(self):
        ti = TranscendentIntelligence()
        for _ in range(7):
            ti.advance_stage()
        assert ti._engine.current.stage == Stage.OMEGA
        assert ti.advance_stage() is None

    def test_status_contains_name(self):
        ti = TranscendentIntelligence(name="Named-TIA")
        assert "Named-TIA" in ti.status()
