# ⚠️ CORRECTED PORT NAMES - Conditional Router

## 🔴 IMPORTANT CORRECTION!

The Conditional Router node uses **`input_text`** NOT `input_message`

---

## ✅ CORRECT Port Names for Conditional Router

### Node ID: `flow_controls_ConditionalRouter`

### Input Ports (8 total):

| Port Name | Type | Required | Description |
|-----------|------|----------|-------------|
| **`input_text`** | text | ✅ YES | The text to evaluate (THIS IS THE MAIN INPUT!) |
| **`match_text`** | text | ✅ YES | The text to compare against |
| `operator` | dropdown | ❌ No | equals/contains/starts with/etc. (default: "equals") |
| `case_sensitive` | boolean | ❌ No | Case sensitive comparison (default: true) |
| `true_case_message` | text | ❌ No | Message to pass if TRUE |
| `false_case_message` | text | ❌ No | Message to pass if FALSE |
| `max_iterations` | number | ❌ No | Max iterations (default: 10) |
| `default_route` | dropdown | ❌ No | Default route (true_result/false_result) |

### Output Ports (2 total):

| Port Name | Type | Description |
|-----------|------|-------------|
| **`true_result`** | Message | Output if condition is TRUE |
| **`false_result`** | Message | Output if condition is FALSE |

---

## 🔧 How to Use Conditional Router (CORRECTED)

### Example: Route Based on Intent

```
Step 1: Connect Intent to Router
┌──────────────────┐
│ Intent Classifier│
│                  │
│  intent ▶────────┼──────┐
└──────────────────┘      │
                          │
                          ↓
                   ┌──────────────────┐
                   │ Conditional      │
                   │ Router           │
                   │                  │
                   │ ◀ input_text     │ ← Connect HERE (not input_message!)
                   └──────────────────┘

Step 2: Configure the Router
Settings:
  - input_text: (connected from Intent Classifier)
  - match_text: "TENANT"
  - operator: "equals"

Step 3: Connect Outputs
┌──────────────────┐
│ Conditional      │
│ Router           │
│                  │
│  true_result ▶───┼──→ Search Agent
│  false_result ▶──┼──→ Next Condition
└──────────────────┘
```

---

## ✅ CORRECTED Complete Example

### Workflow: Intent-Based Routing

**Connections:**
```
1. Intent Classifier (intent) → Conditional Router (input_text)
   ❌ WRONG: → (input_message)
   ✅ CORRECT: → (input_text)

2. Conditional Router Settings:
   - match_text: "TENANT"
   - operator: "equals"

3. Conditional Router (true_result) → Agent A (input_data)
4. Conditional Router (false_result) → Agent B (input_data)
```

**Visual:**
```
Intent Classifier
    │
    │ intent
    ↓
Conditional Router
    │ input_text: (from Intent Classifier)
    │ match_text: "TENANT"
    │ operator: "equals"
    │
    ├─ true_result ──→ Search Agent (input_data)
    │
    └─ false_result ──→ FAQ Agent (input_data)
```

---

## 📋 Quick Reference - Conditional Router

### Minimal Configuration:
```yaml
INPUTS:
  ✅ input_text (text, REQUIRED)
     - Connect from: Intent Classifier (intent)
     - Or type directly: "some text"
  
  ✅ match_text (text, REQUIRED)
     - Type: "TENANT" or "OWNER" or any text to match
  
  ❌ operator (dropdown, OPTIONAL)
     - Default: "equals"
     - Options: equals, contains, starts with, etc.

OUTPUTS:
  true_result → Goes to TRUE path
  false_result → Goes to FALSE path
```

---

## 🔄 Migration Guide

If you followed the old guides, update your connections:

### OLD (WRONG):
```
Intent Classifier (intent) → Conditional Router (input_message)
                                                   ↑
                                            This port doesn't exist!
```

### NEW (CORRECT):
```
Intent Classifier (intent) → Conditional Router (input_text)
                                                   ↑
                                            Correct port name!
```

---

## 🎯 Common Use Cases

### Use Case 1: Route by Intent
```
Intent Classifier (intent) → Conditional Router (input_text)
Settings:
  - match_text: "TENANT"
  - operator: "equals"

Outputs:
  - true_result → Tenant Agent
  - false_result → Next Condition
```

### Use Case 2: Route by Keyword
```
User Message → Conditional Router (input_text)
Settings:
  - match_text: "help"
  - operator: "contains"

Outputs:
  - true_result → Help Agent
  - false_result → Main Agent
```

### Use Case 3: Chain Multiple Conditions
```
Condition A (false_result) → Condition B (input_text)
Settings for B:
  - match_text: "OWNER"
  - operator: "equals"

Outputs:
  - true_result → Owner Agent
  - false_result → Default Agent
```

---

## ⚠️ Important Notes

1. **`input_text` is a TEXT field**, not a handle port
   - You can either:
     - Type text directly into it
     - OR connect from another node's output

2. **Case sensitivity matters!**
   - "TENANT" ≠ "tenant" (if case_sensitive = true)
   - Set case_sensitive = false to ignore case

3. **Operator options:**
   - `equals` - Exact match
   - `contains` - Text contains the match
   - `starts with` - Text starts with match
   - `ends with` - Text ends with match
   - `regex` - Regular expression match

---

## 🔧 Troubleshooting

### "Can't find input_message port"
**Solution**: Use `input_text` instead

### "Condition always goes to false_result"
**Check**:
1. Is `match_text` exactly correct? (check spelling)
2. Is case_sensitive set correctly?
3. Is the right operator selected?

### "How do I connect Intent Classifier?"
**Answer**:
```
Intent Classifier (intent) → Conditional Router (input_text)
                                                   ↑
                                            Use this port!
```

---

**Last Updated**: 2026-02-08 (CORRECTED)
**Status**: ✅ Verified with actual node library
