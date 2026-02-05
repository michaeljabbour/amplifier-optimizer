# Quick Start Guide

Get up and running with Amplifier Observability in 5 minutes.

## Installation

```bash
# Copy to your Amplifier bundles directory
cp -r modules/observability ~/.amplifier/bundles/

# Or use from project directory
export AMPLIFIER_BUNDLES_DIR=/path/to/amplifier-optimizer/modules
```

## Basic Usage

### Option 1: Add to Your Bundle

```yaml
# In your bundle.yaml or config
bundles:
  - path: observability
```

### Option 2: Use Directly

```python
from amplifier_core import AmplifierSession
from observability.modules import ObservabilityHook, TrajectoryAnalyzer

# Create session
session = AmplifierSession()

# Register hooks
session.coordinator.hooks.register("*", ObservabilityHook())
session.coordinator.hooks.register("*", TrajectoryAnalyzer())

# Run your session
await session.execute("Your task here")
```

## What Happens

### During Execution

**Turn 1:**
```
User: "Refactor the authentication module"
Agent: [starts working]
```

**Turn 3:** (Agent sees trajectory update)
```
🚀 Trajectory Awareness (Ephemeral)
├─ Phase: Exploration (Discovering codebase structure)
├─ Confidence: 78%
├─ Duration: 12s in this phase
├─ Recent Tools: glob, read_file, grep
└─ Predicted Path: **exploration** → analysis → planning
```

**Turn 5:** (Agent sees metrics update)
```
📊 Session Metrics (Ephemeral)
├─ Cost: $0.0123
├─ Tokens: 5,234 (3,456 in, 1,778 out)
├─ Time: 45s elapsed
├─ Tools: 3 types used, avg 0.8s per call
└─ Turn: 5
```

**Turn 8:** (Phase transition)
```
🚀 Phase: Implementation → Writing code
```

**If cost threshold hit:**
```
💰 Cost threshold exceeded: $1.0234
```

**If tool is slow:**
```
⚠️ Slow tool: grep took 12.3s
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

## Customization

### Tighter Budget Tracking

```yaml
- name: observability
  config:
    cost_threshold: 0.25  # Warn every $0.25
    inject_frequency: 3   # More frequent updates
```

### Performance Focus

```yaml
- name: observability
  config:
    speed_threshold: 5.0  # Warn on tools >5s
```

### Extended Trajectory Analysis

```yaml
- name: trajectory
  config:
    window_size: 20       # Analyze more history
```

## Verification

Test that it's working:

```python
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

## Troubleshooting

### "Module not found"

Make sure the bundle path is correct:
```bash
ls -la ~/.amplifier/bundles/observability/
# Should show: bundle.yaml, modules/, context/, README.md
```

### "Hook not registering"

Check event patterns in bundle.yaml match your Amplifier version's event names.

### "No metrics showing"

Verify hooks are registered:
```python
print(session.coordinator.hooks.list_registered())
# Should show: observability, trajectory
```

## Next Steps

- Read the full [README.md](README.md) for architecture details
- Customize phases in `modules/trajectory_analyzer.py`
- Add custom metrics by extending `ObservabilityHook`
- Export metrics to external monitoring systems

## Support

This bundle follows Amplifier's governance model. For issues or questions, see the Amplifier repository.

---

**You're now tracking cost, speed, and trajectory in real-time! 🚀**
