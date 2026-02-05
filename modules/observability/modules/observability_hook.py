"""Observability Hook: Real-time cost, speed, and token tracking.

Tracks API costs, token usage, and tool execution timing with transparent reporting
to both user and agent via ephemeral context injection.
"""

import math
import time
from collections import defaultdict
from typing import Any

from amplifier_core.hooks import HookResult


class ObservabilityHook:
    """Real-time cost, speed, and token tracking.
    
    Provides transparent visibility into:
    - API costs (model-specific pricing)
    - Token usage (input/output breakdown)
    - Tool execution timing
    - Session metrics
    
    Injects ephemeral awareness every N turns to give agent cost/speed context
    without polluting conversation history.
    """
    
    # Pricing per 1M tokens (as of 2024)
    PRICING = {
        "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
        "claude-sonnet-4": {"input": 3.00, "output": 15.00},
        "claude-opus-4": {"input": 15.00, "output": 75.00},
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-5-sonnet-20240620": {"input": 3.00, "output": 15.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    }
    
    def __init__(
        self,
        model: str = "claude-sonnet-4-5",
        cost_threshold: float = 1.0,
        speed_threshold: float = 10.0,
        inject_frequency: int = 5,
    ):
        """Initialize observability hook.
        
        Args:
            model: Model name for cost calculations
            cost_threshold: Warn user when cost exceeds this (dollars)
            speed_threshold: Warn user when tool execution exceeds this (seconds)
            inject_frequency: Inject ephemeral metrics every N turns
        """
        self.model = model
        self.cost_threshold = cost_threshold
        self.speed_threshold = speed_threshold
        self.inject_frequency = inject_frequency
        
        # State
        self.total_cost = 0.0
        self.token_usage = {"input": 0, "output": 0}
        self.tool_timings: dict[str, list[float]] = defaultdict(list)
        self.start_times: dict[str, float] = {}
        self.session_start: float | None = None
        self.turn_count = 0
        self.last_injection_turn = 0
        
    async def on_session_start(self, event: str, data: dict[str, Any]) -> HookResult:
        """Record session start time."""
        self.session_start = time.time()
        return HookResult(action="continue")
    
    async def on_tool_pre(self, event: str, data: dict[str, Any]) -> HookResult:
        """Record tool start time."""
        tool_name = data.get("name", "unknown")
        # Use id(data) to make key unique per invocation
        key = f"tool:{tool_name}:{id(data)}"
        self.start_times[key] = time.time()
        return HookResult(action="continue")
    
    async def on_tool_post(self, event: str, data: dict[str, Any]) -> HookResult:
        """Record tool timing and check thresholds."""
        tool_name = data.get("name", "unknown")
        key = f"tool:{tool_name}:{id(data)}"
        
        if key in self.start_times:
            duration = time.time() - self.start_times[key]
            self.tool_timings[tool_name].append(duration)
            del self.start_times[key]
            
            # Warn on slow tools
            if duration > self.speed_threshold:
                return HookResult(
                    action="continue",
                    user_message=f"⚠️ Slow tool: {tool_name} took {duration:.1f}s",
                    user_message_level="warning",
                )
        
        return HookResult(action="continue")
    
    async def on_provider_post(self, event: str, data: dict[str, Any]) -> HookResult:
        """Track token usage and cost, inject ephemeral awareness."""
        self.turn_count += 1
        
        # Update metrics
        usage = data.get("usage", {})
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        
        self.token_usage["input"] += input_tokens
        self.token_usage["output"] += output_tokens
        
        # Calculate cost
        pricing = self.PRICING.get(self.model, self.PRICING["claude-sonnet-4-5"])
        turn_cost = (
            (input_tokens / 1_000_000) * pricing["input"]
            + (output_tokens / 1_000_000) * pricing["output"]
        )
        self.total_cost += turn_cost
        
        # Check cost threshold
        if self.total_cost > self.cost_threshold:
            # Reset threshold to next dollar to avoid spam
            self.cost_threshold = math.ceil(self.total_cost)
            return HookResult(
                action="continue",
                user_message=f"💰 Cost threshold exceeded: ${self.total_cost:.4f}",
                user_message_level="warning",
            )
        
        # Inject ephemeral awareness every N turns
        if self.turn_count - self.last_injection_turn >= self.inject_frequency:
            self.last_injection_turn = self.turn_count
            return self._create_ephemeral_injection()
        
        return HookResult(action="continue")
    
    def _create_ephemeral_injection(self) -> HookResult:
        """Create ephemeral context injection with current metrics."""
        elapsed = time.time() - self.session_start if self.session_start else 0
        
        # Calculate averages
        avg_tool_time = self._average_tool_time()
        total_tokens = sum(self.token_usage.values())
        
        injection = f"""
📊 **Session Metrics** (Ephemeral - for your awareness)
├─ Cost: ${self.total_cost:.4f}
├─ Tokens: {total_tokens:,} ({self.token_usage['input']:,} in, {self.token_usage['output']:,} out)
├─ Time: {elapsed:.0f}s elapsed
├─ Tools: {len(self.tool_timings)} types used, avg {avg_tool_time:.2f}s per call
└─ Turn: {self.turn_count}

This is live awareness - metrics update automatically. Focus on your task.
""".strip()
        
        return HookResult(
            action="continue",
            context_injection=injection,
            context_injection_role="system",
            ephemeral=True,
            suppress_output=True,
        )
    
    def _average_tool_time(self) -> float:
        """Calculate average tool execution time."""
        all_times = [t for times in self.tool_timings.values() for t in times]
        return sum(all_times) / len(all_times) if all_times else 0.0
    
    async def on_session_end(self, event: str, data: dict[str, Any]) -> HookResult:
        """Print final summary."""
        self.print_summary()
        return HookResult(action="continue")
    
    def print_summary(self):
        """Print final summary to user."""
        print("\n" + "=" * 80)
        print("📊 SESSION SUMMARY")
        print("=" * 80)
        print(f"\n💰 Cost: ${self.total_cost:.4f}")
        print(f"🎯 Tokens: {sum(self.token_usage.values()):,}")
        print(f"   ├─ Input:  {self.token_usage['input']:,}")
        print(f"   └─ Output: {self.token_usage['output']:,}")
        
        if self.session_start:
            elapsed = time.time() - self.session_start
            print(f"\n⏱️  Time: {elapsed:.0f}s ({elapsed/60:.1f} min)")
        
        if self.tool_timings:
            print("\n🔧 Tool Usage:")
            for tool, times in sorted(self.tool_timings.items()):
                avg = sum(times) / len(times)
                total = sum(times)
                print(f"   {tool:20} {len(times):3}× calls, avg: {avg:.2f}s, total: {total:.1f}s")
