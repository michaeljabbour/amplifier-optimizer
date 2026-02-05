"""Trajectory Analyzer: Phase detection and trajectory prediction.

Detects agent's current workflow phase (exploration, implementation, etc.) and
predicts trajectory based on tool usage patterns. Provides "mission control"
visibility into where the agent is going and why.
"""

import time
from collections import deque
from typing import Any

from amplifier_core.hooks import HookResult


# Phase definitions with tool indicators
PHASES = {
    "exploration": {
        "description": "Discovering codebase structure",
        "indicators": ["glob", "grep", "read_file", "LSP"],
        "weight": {"glob": 2, "grep": 2, "read_file": 1, "LSP": 2},
    },
    "analysis": {
        "description": "Understanding code and requirements",
        "indicators": ["read_file", "LSP", "web_search", "load_skill"],
        "weight": {"read_file": 2, "LSP": 3, "web_search": 1, "load_skill": 1},
    },
    "planning": {
        "description": "Designing solution architecture",
        "indicators": ["read_file", "delegate"],
        "weight": {"read_file": 1, "delegate": 2},
        "low_activity": True,  # Few tools, long reasoning
    },
    "implementation": {
        "description": "Writing code",
        "indicators": ["write_file", "edit_file", "bash"],
        "weight": {"write_file": 3, "edit_file": 3, "bash": 1},
    },
    "verification": {
        "description": "Testing and validation",
        "indicators": ["bash", "read_file", "python_check"],
        "weight": {"bash": 3, "python_check": 3, "read_file": 1},
    },
    "debugging": {
        "description": "Investigating errors",
        "indicators": ["grep", "read_file", "LSP", "bash"],
        "weight": {"grep": 2, "read_file": 2, "LSP": 2, "bash": 1},
        "error_context": True,  # Triggered by tool errors
    },
}

# Trajectory transitions (phase → likely next phases)
TRAJECTORIES = {
    "exploration": ["analysis", "exploration"],
    "analysis": ["planning", "exploration"],
    "planning": ["implementation", "analysis"],
    "implementation": ["verification", "implementation"],
    "verification": ["debugging", "implementation"],
    "debugging": ["implementation", "exploration"],
}


class TrajectoryAnalyzer:
    """Phase detection and trajectory prediction.
    
    Analyzes tool usage patterns to detect current workflow phase and predict
    where the agent is heading next. Provides "space shuttle mission control"
    visibility via ephemeral context injection.
    """
    
    def __init__(
        self,
        window_size: int = 10,
        inject_frequency: int = 3,
    ):
        """Initialize trajectory analyzer.
        
        Args:
            window_size: Number of recent tools to analyze for phase detection
            inject_frequency: Inject ephemeral trajectory awareness every N turns
        """
        self.window_size = window_size
        self.inject_frequency = inject_frequency
        
        # State
        self.tool_history: deque = deque(maxlen=window_size)
        self.current_phase = "exploration"  # Start assumption
        self.phase_confidence = 0.5
        self.phase_start_time = time.time()
        self.phase_history: list[dict[str, Any]] = []
        self.turn_count = 0
        self.last_injection_turn = 0
        self.recent_errors: list[dict[str, Any]] = []
    
    async def on_tool_post(self, event: str, data: dict[str, Any]) -> HookResult:
        """Track tool usage for phase detection."""
        tool_name = data.get("name", "unknown")
        success = not data.get("error")
        
        self.tool_history.append({
            "tool": tool_name,
            "timestamp": time.time(),
            "success": success,
        })
        
        # Track errors for debugging phase detection
        if not success:
            self.recent_errors.append({
                "tool": tool_name,
                "timestamp": time.time(),
            })
            # Trim old errors (last minute)
            cutoff = time.time() - 60
            self.recent_errors = [e for e in self.recent_errors if e["timestamp"] > cutoff]
        
        return HookResult(action="continue")
    
    async def on_provider_post(self, event: str, data: dict[str, Any]) -> HookResult:
        """Analyze phase and inject trajectory awareness."""
        self.turn_count += 1
        
        # Detect phase
        new_phase, confidence = self._detect_phase()
        
        # Check for phase transition
        if new_phase != self.current_phase and confidence > 0.6:
            self._transition_phase(new_phase, confidence)
            
            # Show user message for major transitions
            return HookResult(
                action="continue",
                user_message=f"🚀 Phase: {new_phase.title()} → {PHASES[new_phase]['description']}",
                user_message_level="info",
            )
        
        # Inject ephemeral trajectory awareness
        if self.turn_count - self.last_injection_turn >= self.inject_frequency:
            self.last_injection_turn = self.turn_count
            return self._create_trajectory_injection()
        
        return HookResult(action="continue")
    
    def _detect_phase(self) -> tuple[str, float]:
        """Detect current phase from tool usage patterns.
        
        Returns:
            Tuple of (phase_name, confidence_score)
        """
        if not self.tool_history:
            return self.current_phase, self.phase_confidence
        
        # Calculate scores for each phase
        scores = {}
        for phase_name, phase_def in PHASES.items():
            score = 0.0
            
            # Score based on tool matches
            for tool_event in self.tool_history:
                tool = tool_event["tool"]
                for indicator, weight in phase_def.get("weight", {}).items():
                    if indicator.lower() in tool.lower():
                        score += weight
            
            # Special handling for low-activity phases (planning)
            if phase_def.get("low_activity") and len(self.tool_history) < 3:
                score += 5  # Bonus for few tools
            
            # Special handling for error-triggered phases (debugging)
            if phase_def.get("error_context") and len(self.recent_errors) >= 2:
                score += 10  # Strong signal
            
            scores[phase_name] = score
        
        # Find highest score
        if not scores or max(scores.values()) == 0:
            return self.current_phase, 0.5
        
        best_phase = max(scores, key=scores.get)
        max_score = scores[best_phase]
        total_score = sum(scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.5
        
        return best_phase, confidence
    
    def _transition_phase(self, new_phase: str, confidence: float):
        """Record phase transition."""
        phase_duration = time.time() - self.phase_start_time
        
        self.phase_history.append({
            "phase": self.current_phase,
            "duration": phase_duration,
            "timestamp": self.phase_start_time,
        })
        
        self.current_phase = new_phase
        self.phase_confidence = confidence
        self.phase_start_time = time.time()
    
    def _predict_trajectory(self) -> list[str]:
        """Predict next likely phases.
        
        Returns:
            List of predicted next phases (up to 3)
        """
        possible_next = TRAJECTORIES.get(self.current_phase, [])
        
        # If high confidence, next phase is likely
        # If low confidence, might stay in current phase
        if self.phase_confidence < 0.7:
            return [self.current_phase] + possible_next[:2]
        else:
            return possible_next[:3]
    
    def _create_trajectory_injection(self) -> HookResult:
        """Create ephemeral injection with trajectory."""
        phase_duration = time.time() - self.phase_start_time
        predicted = self._predict_trajectory()
        
        # Build trajectory visualization
        trajectory_viz = " → ".join([
            f"**{self.current_phase}**" if i == 0 else p
            for i, p in enumerate([self.current_phase] + predicted[:2])
        ])
        
        # Recent tools summary
        recent_tools = [t["tool"] for t in list(self.tool_history)[-3:]]
        tools_summary = ", ".join(recent_tools) if recent_tools else "none"
        
        injection = f"""
🚀 **Trajectory Awareness** (Ephemeral)
├─ Phase: {self.current_phase.title()} ({PHASES[self.current_phase]['description']})
├─ Confidence: {self.phase_confidence:.0%}
├─ Duration: {phase_duration:.0f}s in this phase
├─ Recent Tools: {tools_summary}
└─ Predicted Path: {trajectory_viz}

This is mission control - you're on track. Continue your current work.
""".strip()
        
        return HookResult(
            action="continue",
            context_injection=injection,
            context_injection_role="system",
            ephemeral=True,
            suppress_output=True,
        )
    
    def print_trajectory_report(self):
        """Print trajectory history."""
        print("\n" + "=" * 80)
        print("🚀 TRAJECTORY REPORT")
        print("=" * 80)
        
        print(f"\nCurrent Phase: {self.current_phase.title()}")
        print(f"Confidence: {self.phase_confidence:.0%}")
        
        if self.phase_history:
            print("\nPhase History:")
            for entry in self.phase_history:
                print(f"  {entry['phase']:15} {entry['duration']:.0f}s")
