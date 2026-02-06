---
bundle:
  name: optimizer
  version: "1.0.0"
  description: "Real-time cost, speed, and trajectory tracking for Amplifier sessions"
  authors:
    - "Amplifier Team"

includes:
  - bundle: foundation

hooks:
  - module: hooks-observability
    source: optimizer:modules/observability_hook.py:ObservabilityHook
    config:
      model: "claude-sonnet-4-5"
      cost_threshold: 1.0
      speed_threshold: 10.0
      inject_frequency: 5
    events:
      - "session:start"
      - "tool:pre"
      - "tool:post"
      - "provider:post"
      - "session:end"
      
  - module: hooks-trajectory
    source: optimizer:modules/trajectory_analyzer.py:TrajectoryAnalyzer
    config:
      window_size: 10
      inject_frequency: 3
    events:
      - "tool:post"
      - "provider:post"

context:
  - path: optimizer:context/observability-instructions.md
    description: "Explains observability metrics and trajectory awareness to agents"
---

# Amplifier Optimizer

> **Mission control for your AI agent sessions** - Real-time cost, speed, and trajectory tracking

@optimizer:context/observability-instructions.md

---

## What This Gives You

**🚀 Mission Control Visibility:**
- 💰 Real-time cost tracking with threshold warnings
- ⚡ Tool execution timing and slow operation alerts
- 🎯 Automatic workflow phase detection (exploration → implementation → verification)
- 🛰️ Live trajectory tracking showing where your agent is heading

**📊 How It Works:**
- Two hooks observe session events (passive, no interference)
- ObservabilityHook tracks cost, tokens, and timing
- TrajectoryAnalyzer detects workflow phase from tool patterns
- Both inject ephemeral awareness (agent sees data, history stays clean)
- Final summary report at session end

**🎨 The Amplifier Way:**
- Built entirely on hooks system (zero kernel modifications)
- Mechanisms, not policies (awareness, not control)
- Composable and optional
- ~500 lines, no external dependencies

---

## Example Output

### During Session
```
🚀 Phase: Exploration → Discovering codebase structure
📊 Cost: $0.02 | Tokens: 4,567 | Time: 34s
💰 Cost threshold exceeded: $0.10
⚠️ Slow tool: bash took 11.3s
🚀 Phase: Implementation → Writing code
```

### At Session End
```
================================================================================
📊 SESSION SUMMARY
================================================================================
💰 Cost: $0.12
🎯 Tokens: 28,456 (18,234 in, 10,222 out)
⏱️  Time: 512s (8.5 min)

🔧 Tool Usage:
   read_file            18× calls, avg: 0.52s, total: 9.4s
   write_file            4× calls, avg: 0.31s, total: 1.2s
```

---

For complete documentation, see README.md.
