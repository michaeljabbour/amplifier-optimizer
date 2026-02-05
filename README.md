# 🚀 Amplifier Observability

> **Mission control for your AI agent sessions** - Real-time cost, speed, and trajectory tracking

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Amplifier](https://img.shields.io/badge/amplifier-compatible-green.svg)](https://github.com/microsoft/amplifier)

---

## 📖 Overview

Ever wonder what your AI agent is doing, where it's going, or how much it's costing? **Amplifier Observability** gives you complete visibility into your agent sessions with three core capabilities:

| Capability | What You Get |
|------------|--------------|
| 💰 **Cost/Speed Transparency** | Real-time API costs, token usage, and operation timing |
| 🎯 **Time/Task Awareness** | Automatic workflow phase detection (exploration → implementation → verification) |
| 🛰️ **Live Trajectory Tracking** | "Space shuttle mission control" view of where your agent is heading and why |

Built following Amplifier's philosophy: **mechanisms, not policies**. This bundle gives you *awareness*, not *control*.

---

## ✨ Key Features

- ⚡ **Zero configuration** - Works out of the box with sensible defaults
- 🎯 **Ephemeral awareness** - Agents see metrics without polluting conversation history
- 🚀 **Phase detection** - Automatically identifies workflow phase from tool patterns
- 💰 **Cost tracking** - Per-model pricing with configurable threshold warnings
- ⏱️ **Performance monitoring** - Tool timing with slow operation alerts
- 📊 **Session summaries** - Comprehensive reports when sessions complete
- 🔧 **Modular design** - Use cost tracking, trajectory, or both independently

---

## 🎬 Quick Start

### Installation

```bash
# Add the bundle from GitHub
amplifier bundle add git+https://github.com/michaeljabbour/amplifier-optimizer@main

# Activate it
amplifier bundle use observability

# Start a session - tracking is now active!
amplifier
```

That's it! All your sessions now have mission control visibility.

### Testing First?

```bash
# Run a quick test to verify the bundle works
amplifier bundle add git+https://github.com/michaeljabbour/amplifier-optimizer@main
cd ~/.amplifier/cache/amplifier-optimizer-*/
python modules/observability/tests/test_basic_import.py
```

### Local Development

```bash
# Clone for local development
git clone https://github.com/michaeljabbour/amplifier-optimizer.git
cd amplifier-optimizer

# Test the modules
python modules/observability/tests/test_basic_import.py

# Use locally (bypasses bundle registry)
amplifier --bundle modules/observability
```

---

## 📊 What You'll See

### During Your Session

#### Phase Transitions
```
🚀 Phase: Exploration → Discovering codebase structure
🚀 Phase: Analysis → Understanding code and requirements
🚀 Phase: Implementation → Writing code
🚀 Phase: Verification → Testing and validation
```

#### Real-Time Warnings
```
💰 Cost threshold exceeded: $1.0234
⚠️ Slow tool: grep took 12.3s
```

#### Trajectory Updates (Every 3 turns)
```
🚀 Trajectory Awareness (Ephemeral)
├─ Phase: Implementation (Writing code)
├─ Confidence: 85%
├─ Duration: 45s in this phase
├─ Recent Tools: write_file, edit_file, bash
└─ Predicted Path: **implementation** → verification → debugging

This is mission control - you're on track. Continue your current work.
```

#### Metrics Updates (Every 5 turns)
```
📊 Session Metrics (Ephemeral)
├─ Cost: $0.0234
├─ Tokens: 12,345 (8,234 in, 4,111 out)
├─ Time: 78s elapsed
├─ Tools: 3 types used, avg 1.2s per call
└─ Turn: 5

This is live awareness - metrics update automatically. Focus on your task.
```

### At Session End

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

---

## 🎯 Real-World Example

**Task:** *"Refactor the authentication module to use OAuth2"*

```
Turn 1: User gives task
└─ Agent starts working

Turn 3: First trajectory update
🚀 Trajectory: **exploration** → analysis → planning
├─ Phase: Exploration (Discovering codebase structure)
├─ Recent Tools: glob, read_file, grep
└─ Confidence: 78%

Turn 5: First metrics update
📊 Metrics
├─ Cost: $0.01
├─ Time: 23s elapsed
└─ Tokens: 3,456

Turn 8: Phase transition
🚀 Phase: Analysis → Understanding code and requirements

Turn 11: Another phase transition
🚀 Phase: Planning → Designing solution architecture

Turn 14: 
🚀 Phase: Implementation → Writing code
💰 Cost threshold exceeded: $0.10

Turn 18:
🚀 Phase: Verification → Testing and validation
⚠️ Slow tool: bash took 11.2s  ← Running tests

Turn 20: Session complete
📊 SESSION SUMMARY
💰 Cost: $0.12
⏱️  Time: 8.5 min
✅ OAuth2 authentication implemented and tested
```

**What your son learns:**
- The task cost $0.12 (not $0.01 or $10)
- It took 8.5 minutes start to finish
- The agent followed a logical path: explore → analyze → plan → implement → verify
- Tests were slow (11.2s) - maybe optimize next time

---

## 🏗️ How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  User: "Refactor the auth module"                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Amplifier Agent Session                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Agent thinks and acts                                │   │
│  │  ├─ Uses tools (read_file, write_file, bash)         │   │
│  │  ├─ Calls LLM APIs                                    │   │
│  │  └─ Gets periodic awareness updates (ephemeral)      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Observability Hooks (invisible background)          │   │
│  │                                                        │   │
│  │  ObservabilityHook:                                   │   │
│  │  ├─ Listens to tool:pre/post → tracks timing         │   │
│  │  ├─ Listens to provider:post → tracks cost/tokens    │   │
│  │  └─ Injects metrics every 5 turns (ephemeral)        │   │
│  │                                                        │   │
│  │  TrajectoryAnalyzer:                                  │   │
│  │  ├─ Listens to tool:post → builds tool history       │   │
│  │  ├─ Detects phase from patterns                      │   │
│  │  └─ Injects trajectory every 3 turns (ephemeral)     │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  User sees:                                                 │
│  - Phase transitions (🚀)                                   │
│  - Cost warnings (💰)                                        │
│  - Slow tool warnings (⚠️)                                  │
│  - Final summary (📊)                                        │
└─────────────────────────────────────────────────────────────┘
```

### Workflow Phases

The system automatically detects these phases from tool usage:

```
┌─────────────┐
│ Exploration │ ─────┐
└─────────────┘      │
                     ▼
              ┌──────────┐
              │ Analysis │ ─────┐
              └──────────┘      │
                                ▼
                         ┌──────────┐
                         │ Planning │ ─────┐
                         └──────────┘      │
                                           ▼
                                  ┌────────────────┐
                                  │ Implementation │ ─────┐
                                  └────────────────┘      │
                                                          ▼
                                                 ┌──────────────┐
                                                 │ Verification │
                                                 └──────┬───────┘
                                                        │
                                  ┌─────────────────────┴─────┐
                                  ▼                           ▼
                            ┌──────────┐                 ✅ Success
                            │ Debugging│
                            └─────┬────┘
                                  │
                                  └─────→ (back to Implementation)
```

---

## ⚙️ Configuration

### Default Settings

Works great out of the box, but you can customize:

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

### Budget-Focused Configuration

```yaml
- name: observability
  config:
    cost_threshold: 0.25  # Warn every $0.25
    inject_frequency: 3   # More frequent cost awareness
```

### Performance-Focused Configuration

```yaml
- name: observability
  config:
    speed_threshold: 5.0  # Strict timing requirements
```

### Supported Models

Built-in pricing for:
- Claude Sonnet 4/4.5, Opus 4, Haiku 3
- GPT-4, GPT-4 Turbo, GPT-4o, GPT-4o Mini
- GPT-3.5 Turbo

*See `modules/observability_hook.py` for full pricing table*

---

## 🧪 Testing

Verify installation:

```bash
python modules/observability/tests/test_basic_import.py
```

Expected output:
```
✅ ObservabilityHook instantiation test passed
✅ TrajectoryAnalyzer instantiation test passed
✅ Pricing table test passed
✅ Phase definitions test passed

✅ ALL TESTS PASSED
```

---

## 📂 Project Structure

```
amplifier-optimizer/
└── modules/
    └── observability/
        ├── bundle.yaml                           # Bundle composition
        ├── modules/
        │   ├── __init__.py                       # Module exports
        │   ├── observability_hook.py             # Cost/speed/token tracking
        │   └── trajectory_analyzer.py            # Phase detection
        ├── context/
        │   └── observability-instructions.md     # Agent guidance
        ├── tests/
        │   └── test_basic_import.py              # Basic tests
        ├── README.md                             # Full documentation
        └── QUICKSTART.md                         # 5-minute setup guide
```

**Total code**: ~500 lines across 2 modules  
**Dependencies**: Python stdlib + Amplifier Core only  
**Complexity**: Minimal - ruthlessly simple design

---

## 🎨 Design Philosophy

Built following **The Amplifier Way**:

| Principle | Implementation |
|-----------|----------------|
| **Mechanism, not policy** | Provides observability primitives, doesn't enforce budgets |
| **Event-driven** | Built entirely on Amplifier's hooks system |
| **Composable** | Each hook works independently |
| **Optional** | Add/remove without breaking anything |
| **Simple** | ~500 lines, no external dependencies |
| **Context sinks** | Ephemeral awareness doesn't pollute history |

### Why Hooks?

Hooks are **passive observers** - they watch without interfering. The agent gets automatic awareness without needing to remember to check metrics.

### Why Ephemeral Injection?

**Zero clutter** - metrics don't pollute conversation history. The agent has temporary awareness that updates automatically, like a HUD overlay.

### Why Staggered Updates?

**Balance awareness vs cost** - injecting every turn would be expensive. Staggering (metrics every 5, trajectory every 3) provides regular updates without token waste.

---

## 🔧 Advanced Usage

### Custom Phase Detection

Add your own workflow phases:

```python
# In modules/trajectory_analyzer.py

PHASES["code_review"] = {
    "description": "Reviewing code quality",
    "indicators": ["read_file", "grep", "python_check"],
    "weight": {"read_file": 2, "grep": 1, "python_check": 3},
}

TRAJECTORIES["implementation"] = ["verification", "code_review"]
```

### Export Metrics to External Systems

Extend `ObservabilityHook` for custom integrations:

```python
class PrometheusObservability(ObservabilityHook):
    async def on_provider_post(self, event: str, data: dict) -> HookResult:
        result = await super().on_provider_post(event, data)
        
        # Export to Prometheus
        prometheus_client.gauge('amplifier_cost').set(self.total_cost)
        prometheus_client.gauge('amplifier_tokens').set(sum(self.token_usage.values()))
        
        return result
```

---

## 💡 Use Cases

### For Individual Developers
- **Budget management**: Track spending on API calls
- **Performance optimization**: Identify slow operations
- **Workflow understanding**: See how agents approach tasks
- **Debugging**: Detect when agents get stuck in loops

### For Teams
- **Cost allocation**: Track spending per project or user
- **Benchmark workflows**: Compare agent efficiency across tasks
- **Quality assurance**: Verify agents follow expected workflows
- **Training**: Understand agent behavior patterns

### For Research
- **Agent behavior analysis**: Study decision-making patterns
- **Efficiency metrics**: Compare different prompting strategies
- **Cost modeling**: Predict session costs from early signals

---

## 🤝 Contributing

This bundle is part of the [Amplifier ecosystem](https://github.com/microsoft/amplifier). Contributions welcome!

**Development Setup:**

```bash
# Clone repository
git clone https://github.com/microsoft/amplifier-optimizer.git
cd amplifier-optimizer

# Run tests
python modules/observability/tests/test_basic_import.py

# Test with Amplifier
amplifier --bundle modules/observability
```

---

## 📚 Documentation

- **[QUICKSTART.md](modules/observability/QUICKSTART.md)** - 5-minute setup guide
- **[Full README](modules/observability/README.md)** - Complete documentation
- **[Context Instructions](modules/observability/context/observability-instructions.md)** - How agents use this

---

## 🌟 Example Session Output

**Task:** "Add user authentication to my web app"

```
🚀 Phase: Exploration → Discovering codebase structure

[Agent searches files...]

🚀 Trajectory: **exploration** → analysis → planning
📊 Cost: $0.02 | Tokens: 4,567 | Time: 34s

🚀 Phase: Analysis → Understanding code and requirements

[Agent reads auth-related code...]

🚀 Phase: Planning → Designing solution architecture

[Agent designs OAuth2 flow...]

💰 Cost threshold exceeded: $0.10

🚀 Phase: Implementation → Writing code

[Agent writes auth code...]

🚀 Phase: Verification → Testing and validation

⚠️ Slow tool: bash took 11.3s

[Session ends]

================================================================================
📊 SESSION SUMMARY
================================================================================

💰 Cost: $0.12
🎯 Tokens: 28,456
   ├─ Input:  18,234
   └─ Output: 10,222

⏱️  Time: 512s (8.5 min)

🔧 Tool Usage:
   read_file            18× calls, avg: 0.52s, total: 9.4s
   write_file            4× calls, avg: 0.31s, total: 1.2s
   edit_file             2× calls, avg: 0.28s, total: 0.6s
   bash                  3× calls, avg: 5.82s, total: 17.5s
   LSP                   6× calls, avg: 0.89s, total: 5.3s

✅ OAuth2 authentication implemented and tested
```

---

## 📈 Metrics Tracked

### Cost Metrics
- Total API cost in USD
- Input/output token breakdown
- Per-turn cost
- Model-specific pricing

### Speed Metrics
- Tool execution timing
- Average/total time per tool type
- Session elapsed time
- Slow operation detection

### Trajectory Metrics
- Current workflow phase
- Phase confidence score
- Phase duration
- Predicted next phases
- Recent tool usage

---

## 🧠 How Phase Detection Works

The trajectory analyzer uses **weighted scoring** based on tool patterns:

| Phase | Key Indicators | Example Pattern |
|-------|----------------|-----------------|
| Exploration | glob, grep, read_file | `glob("**/*.py")` → `read_file()` |
| Analysis | read_file, LSP, web_search | `LSP.hover()` → `read_file()` |
| Planning | Few tools, long reasoning | Minimal tool use, long LLM responses |
| Implementation | write_file, edit_file | `write_file()` → `edit_file()` |
| Verification | bash, python_check | `bash("pytest")` → `python_check()` |
| Debugging | grep, read_file + errors | Tool errors → intensive searching |

**Confidence threshold**: 60% required for phase transition to avoid false positives.

---

## 🎓 Design Decisions

### Why Hooks Instead of Tools?

**Hooks are passive** - they observe without requiring agent action. The agent gets automatic awareness without needing to remember to check metrics.

### Why Ephemeral Injection?

**Zero clutter** - metrics don't pollute conversation history. The agent has temporary awareness that updates automatically, like a HUD overlay in a video game.

### Why Staggered Updates?

**Balance awareness vs cost** - Metrics every 5 turns, trajectory every 3 turns. This provides regular updates without excessive token consumption.

### Why Weighted Phase Scoring?

**Robust detection** - Simple keyword matching is too brittle. Weighted scoring handles mixed tool usage and provides confidence scores.

---

## 🚦 Requirements

- **Python**: 3.11+
- **Amplifier Core**: Latest version with hooks API
- **Dependencies**: None (uses stdlib only)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

Built with ❤️ following the Amplifier philosophy:

> *"The center stays still so the edges can move fast."*

Inspired by the need for transparency, awareness, and control in AI agent sessions.

---

## 🔗 Links

- **[Amplifier](https://github.com/microsoft/amplifier)** - The AI agent framework
- **[Amplifier Foundation](https://github.com/microsoft/amplifier-foundation)** - Bundle primitives and patterns
- **[Documentation](modules/observability/README.md)** - Full technical documentation

---

<div align="center">

**Give your AI agents mission control visibility** 🚀

[Get Started](#-quick-start) • [Documentation](modules/observability/README.md) • [Report Issue](https://github.com/microsoft/amplifier-optimizer/issues)

</div>
