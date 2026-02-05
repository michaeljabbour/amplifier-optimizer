"""Basic import and instantiation tests for observability modules."""

from __future__ import annotations

import sys
from pathlib import Path

# Add modules directory to path
modules_dir = Path(__file__).parent.parent / "modules"
sys.path.insert(0, str(modules_dir))

# Imports after path modification (intentional for testing)
from observability_hook import ObservabilityHook  # noqa: E402
from trajectory_analyzer import TrajectoryAnalyzer  # noqa: E402


def test_observability_hook_instantiation():
    """Test that ObservabilityHook can be instantiated."""
    hook = ObservabilityHook(
        model="claude-sonnet-4-5",
        cost_threshold=1.0,
        speed_threshold=10.0,
        inject_frequency=5,
    )
    
    assert hook.model == "claude-sonnet-4-5"
    assert hook.cost_threshold == 1.0
    assert hook.speed_threshold == 10.0
    assert hook.inject_frequency == 5
    assert hook.total_cost == 0.0
    assert hook.turn_count == 0
    print("✅ ObservabilityHook instantiation test passed")


def test_trajectory_analyzer_instantiation():
    """Test that TrajectoryAnalyzer can be instantiated."""
    analyzer = TrajectoryAnalyzer(
        window_size=10,
        inject_frequency=3,
    )
    
    assert analyzer.window_size == 10
    assert analyzer.inject_frequency == 3
    assert analyzer.current_phase == "exploration"
    assert analyzer.turn_count == 0
    print("✅ TrajectoryAnalyzer instantiation test passed")


def test_pricing_table():
    """Test that pricing table has expected models."""
    hook = ObservabilityHook()
    
    assert "claude-sonnet-4-5" in hook.PRICING
    assert "gpt-4o" in hook.PRICING
    assert hook.PRICING["claude-sonnet-4-5"]["input"] == 3.00
    assert hook.PRICING["claude-sonnet-4-5"]["output"] == 15.00
    print("✅ Pricing table test passed")


def test_phase_definitions():
    """Test that phase definitions are properly structured."""
    from trajectory_analyzer import PHASES, TRAJECTORIES
    
    assert "exploration" in PHASES
    assert "implementation" in PHASES
    assert "description" in PHASES["exploration"]
    assert "weight" in PHASES["exploration"]
    
    assert "exploration" in TRAJECTORIES
    assert isinstance(TRAJECTORIES["exploration"], list)
    print("✅ Phase definitions test passed")


if __name__ == "__main__":
    print("Running observability module tests...\n")
    
    try:
        test_observability_hook_instantiation()
        test_trajectory_analyzer_instantiation()
        test_pricing_table()
        test_phase_definitions()
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED")
        print("=" * 80)
        print("\nObservability modules are ready to use!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
