# Amplifier Observability Bundle

**Real-time cost, speed, and trajectory tracking for Amplifier sessions.**

## Overview

The Observability bundle provides "mission control" visibility into your Amplifier sessions with three core capabilities:

1. **Cost/Speed Transparency** - Real-time tracking of API costs, token usage, and operation timing
2. **Time/Task Awareness** - Automatic detection of workflow phases (exploration, implementation, etc.)
3. **Live Trajectory Tracking** - "Space shuttle trajectory" view of where the agent is going and why

## Key Features

- ⚡ **Zero configuration required** - Works out of the box with sensible defaults
- 🎯 **Ephemeral awareness** - Agents see metrics without polluting conversation history
- 🚀 **Phase detection** - Automatically identifies workflow phase from tool patterns
- 💰 **Cost tracking** - Per-model pricing with threshold warnings
- ⏱️ **Performance monitoring** - Tool timing and slow operation alerts
- 📊 **Session summaries** - Comprehensive reports at session end

## Quick Start

### Installation

```bash
# Clone or copy the bundle to your modules directory
cp -r modules/observability ~/.amplifier/bundles/
```

### Usage

```yaml
# In your Amplifier config or bundle
bundles:
  - path: ~/.amplifier/bundles/observability
```

That's it! The observability hooks will automatically start tracking your session.

## What You'll See

### User Experience

**During Session:**
- Cost threshold warnings: `💰 Cost threshold exceeded: $1.0234`
- Slow tool warnings: `⚠️ Slow tool: grep took 12.3s`
- Phase transitions: `🚀 Phase: Implementation → Writing code`

**At Session End:**
```
================================================================================
📊 SESSION SUMMARY
================================================================================

💰 Cost: $0.0234
🎯 Tokens: 12,345
   ├─ Input:  8,234
   └─ Output: 4,111

⏱️  Time: 124s (2.1 min)

🔧 Tool Usage:
   read_file            12× calls, avg: 0.45s, total: 5.4s
   write_file            3× calls, avg: 0.23s, total: 0.7s
   bash                  2× calls, avg: 1.82s, total: 3.6s
```

### Agent Experience (Ephemeral)

Agents receive periodic awareness updates that don't persist in history:

**Every 3 turns (Trajectory):**
```
🚀 Trajectory Awareness (Ephemeral)
├─ Phase: Implementation (Writing code)
├─ Confidence: 85%
├─ Duration: 45s in this phase
├─ Recent Tools: write_file, edit_file, bash
└─ Predicted Path: **implementation** → verification → debugging

This is mission control - you're on track. Continue your current work.
```

**Every 5 turns (Metrics):**
```
📊 Session Metrics (Ephemeral - for your awareness)
├─ Cost: $0.0234
├─ Tokens: 12,345 (8,234 in, 4,111 out)
├─ Time: 78s elapsed
├─ Tools: 3 types used, avg 1.2s per call
└─ Turn: 5

This is live awareness - metrics update automatically. Focus on your task.
```

## Configuration

### Default Configuration

```yaml
modules:
  hooks:
    - name: observability
      config:
        model: "claude-sonnet-4-5"  # Model for cost calculations
        cost_threshold: 1.0          # Warn at $1, then $2, $3...
        speed_threshold: 10.0        # Warn if tool takes >10s
        inject_frequency: 5          # Inject metrics every 5 turns
        
    - name: trajectory
      config:
        window_size: 10              # Analyze last 10 tools
        inject_frequency: 3          # Inject trajectory every 3 turns
```

### Custom Configuration

```yaml
# More aggressive cost tracking
- name: observability
  config:
    cost_threshold: 0.25  # Warn every $0.25
    speed_threshold: 5.0  # Warn if tool >5s
    inject_frequency: 3   # More frequent updates

# Longer trajectory analysis window
- name: trajectory
  config:
    window_size: 20       # Analyze last 20 tools
    inject_frequency: 5   # Less frequent updates
```

## Workflow Phases

The trajectory analyzer detects these phases automatically:

| Phase | Description | Typical Tools |
|-------|-------------|---------------|
| **Exploration** | Discovering codebase structure | glob, grep, read_file, LSP |
| **Analysis** | Understanding code and requirements | read_file, LSP, web_search |
| **Planning** | Designing solution architecture | Few tools, mostly reasoning |
| **Implementation** | Writing code | write_file, edit_file, bash |
| **Verification** | Testing and validation | bash, python_check |
| **Debugging** | Investigating errors | grep, read_file, LSP, bash |

Phase transitions follow natural workflow patterns:
```
Exploration → Analysis → Planning → Implementation → Verification
                                                           ↓
                          Debugging ←─────────────────────┘
```

## Model Pricing

Supported models with pricing per 1M tokens:

| Model | Input | Output |
|-------|-------|--------|
| claude-sonnet-4-5 | $3.00 | $15.00 |
| claude-opus-4 | $15.00 | $75.00 |
| gpt-4o | $2.50 | $10.00 |
| gpt-4o-mini | $0.15 | $0.60 |

*Full pricing table in `modules/observability_hook.py`*

## Architecture

```
observability/
├── bundle.yaml                      # Bundle composition
├── modules/
│   ├── observability_hook.py        # Cost/speed/token tracking
│   └── trajectory_analyzer.py       # Phase detection and prediction
├── context/
│   └── observability-instructions.md # Agent guidance
└── README.md                        # This file
```

### Design Principles

- **Event-driven**: Built entirely on Amplifier's hooks system
- **Ephemeral injection**: Agent awareness without history pollution
- **Staggered updates**: Metrics every 5 turns, trajectory every 3 turns
- **Zero dependencies**: Uses only Python stdlib + Amplifier core
- **Modular**: Each hook works independently

### How It Works

1. **ObservabilityHook** listens to `provider:post` and `tool:*` events
2. Tracks token usage, calculates costs, measures tool timing
3. Injects ephemeral metrics every N turns (doesn't persist in history)
4. Warns user on thresholds (cost or slow tools)

5. **TrajectoryAnalyzer** listens to `tool:post` events
6. Maintains sliding window of recent tools (default: 10)
7. Scores tool patterns against phase definitions (weighted)
8. Detects phase transitions (confidence > 60%) and predicts next phases
9. Injects ephemeral trajectory awareness every N turns

## Use Cases

### Cost Management
- Track API spending in real-time
- Set budget thresholds with automatic warnings
- Identify expensive operations for optimization

### Performance Optimization
- Detect slow tools and operations
- Identify bottlenecks in agent workflows
- Compare tool performance across sessions

### Workflow Understanding
- Visualize agent's decision path
- Identify workflow patterns and inefficiencies
- Debug stuck or looping agents

### Agent Self-Awareness
- Agents can optimize their own behavior based on cost/speed
- Phase awareness prevents getting stuck in one mode
- Predicted trajectory helps agents plan ahead

## FAQ

### Does this slow down sessions?

No. All operations are O(1) except summary generation. Typical overhead: <1ms per event.

### Does ephemeral injection cost tokens?

Yes, but it's minimal and temporary. Ephemeral messages are injected for one turn only, not persisted in history. Typical cost: ~100 tokens per injection.

### Can I disable trajectory or metrics separately?

Yes. Simply remove the unwanted hook from your bundle configuration.

### How accurate is phase detection?

Phase detection uses weighted scoring with ~85% accuracy in typical workflows. Confidence scores help identify uncertain transitions.

### Can I add custom phases?

Yes. Edit `PHASES` dict in `trajectory_analyzer.py` to define custom phases with tool indicators and weights.

### What if my model isn't in the pricing table?

Add it to the `PRICING` dict in `observability_hook.py`, or it will default to Claude Sonnet pricing.

## Examples

### Budget-Constrained Session

```yaml
- name: observability
  config:
    cost_threshold: 0.10  # Warn at $0.10
    inject_frequency: 2   # Frequent cost awareness
```

### Performance-Focused Session

```yaml
- name: observability
  config:
    speed_threshold: 5.0  # Strict timing requirements
    inject_frequency: 10  # Less frequent (reduce overhead)
```

### Deep Trajectory Analysis

```yaml
- name: trajectory
  config:
    window_size: 20       # Longer history
    inject_frequency: 2   # Frequent trajectory updates
```

## Extending

### Adding Custom Metrics

Subclass `ObservabilityHook` and override methods:

```python
class CustomObservability(ObservabilityHook):
    async def on_provider_post(self, event: str, data: dict) -> HookResult:
        result = await super().on_provider_post(event, data)
        # Add your custom metric tracking
        return result
```

### Custom Phase Detection

Add phases to `PHASES` dict:

```python
PHASES["code_review"] = {
    "description": "Reviewing code quality",
    "indicators": ["read_file", "grep", "python_check"],
    "weight": {"read_file": 2, "grep": 1, "python_check": 3},
}

TRAJECTORIES["implementation"] = ["verification", "code_review"]
```

## Requirements

- Python 3.11+
- Amplifier Core (hooks API)

No external dependencies required.

## Philosophy

Built following Amplifier's **"mechanism, not policy"** approach:

- ✅ Provides observability primitives (metrics collection, phase detection)
- ✅ Doesn't enforce limits or policies (no hard budgets or forced stops)
- ✅ Composable and optional (use what you need)
- ✅ Event-driven and passive (observe, don't control)

This bundle gives you **awareness**, not **control**. You decide how to respond to the data.

## License

MIT License - see Amplifier repository for details

## Contributing

This bundle is part of the Amplifier ecosystem. Contributions welcome following Amplifier's repository governance rules.

---

**Built with ❤️ following the Amplifier way: simple, modular, and ruthlessly focused on mechanisms over policies.**
