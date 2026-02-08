# ✅ VERIFIED: Correct Port Names for All Nodes

## 🎯 The Issue You Found

You were **100% correct!** The Conditional Router does NOT have a port called `input_message`.

**The correct port name is: `input_text`**

---

## ✅ Verified Port Names

### Conditional Router (`flow_controls_ConditionalRouter`)

#### INPUTS:
```
1. input_text (text, REQUIRED) ← Main input port
2. match_text (text, REQUIRED) ← Text to compare against
3. operator (dropdown) ← equals/contains/starts with/etc.
4. case_sensitive (boolean) ← Default: true
5. true_case_message (text) ← Optional message for TRUE path
6. false_case_message (text) ← Optional message for FALSE path
7. max_iterations (number) ← Default: 10
8. default_route (dropdown) ← true_result or false_result
```

#### OUTPUTS:
```
1. true_result (Message) ← Goes here if condition is TRUE
2. false_result (Message) ← Goes here if condition is FALSE
```

---

## 🔧 How to Connect Conditional Router (CORRECT)

### Example: Route Based on Intent

```
Step 1: Get the intent
┌──────────────────┐
│ Intent Classifier│
│                  │
│  intent ▶        │ Outputs: "TENANT" or "OWNER" or "GENERAL"
└──────┬───────────┘
       │
       │
       ↓
Step 2: Route based on intent
┌──────────────────┐
│ Conditional      │
│ Router           │
│                  │
│ input_text       │ ← Type or connect the text to check
│ match_text       │ ← Type: "TENANT"
│ operator         │ ← Select: "equals"
└──────┬───────────┘
       │
       ├─ true_result ──→ Tenant Agent
       │
       └─ false_result ──→ Next Condition
```

---

## 📝 Complete Working Example

### Workflow: 3-Way Intent Routing (TENANT / OWNER / GENERAL)

**Nodes Needed:**
1. Chat Input
2. Intent Classifier
3. Condition A (check for TENANT)
4. Condition B (check for OWNER)
5. Agent A (for TENANT)
6. Agent B (for OWNER)
7. Agent C (for GENERAL)
8. LiteLLM
9. Chat Output

**Connections:**

```
Connection 1: User Input → Classifier
  Chat Input (message) → Intent Classifier (user_message)

Connection 2: Classifier → First Condition
  Intent Classifier (intent) → Condition A (input_text)
  
  Condition A Settings:
    - input_text: (connected from Intent Classifier)
    - match_text: "TENANT"
    - operator: "equals"

Connection 3: First Condition Outputs
  Condition A (true_result) → Agent A (input_data)
  Condition A (false_result) → Condition B (input_text)

Connection 4: Second Condition
  Condition B Settings:
    - input_text: (connected from Condition A false_result)
    - match_text: "OWNER"
    - operator: "equals"

Connection 5: Second Condition Outputs
  Condition B (true_result) → Agent B (input_data)
  Condition B (false_result) → Agent C (input_data)

Connection 6: LLM to All Agents
  LiteLLM (response) → Agent A (llm)
  LiteLLM (response) → Agent B (llm)
  LiteLLM (response) → Agent C (llm)

Connection 7: Agents to Output
  Agent A (output) → Chat Output (message)
  Agent B (output) → Chat Output (message)
  Agent C (output) → Chat Output (message)
```

**Visual Flow:**
```
Chat Input
    │
    ↓
Intent Classifier
    │ intent
    ↓
┌─────────────────────┐
│ Condition A         │
│ input_text: (intent)│
│ match_text: "TENANT"│
└─────┬───────────────┘
      │
      ├─ TRUE ──→ Agent A (TENANT) ──→ Chat Output
      │              ↑
      │              └─ llm ← LiteLLM
      │
      └─ FALSE ──→ Condition B
                   │ input_text: (from Condition A)
                   │ match_text: "OWNER"
                   │
                   ├─ TRUE ──→ Agent B (OWNER) ──→ Chat Output
                   │              ↑
                   │              └─ llm ← LiteLLM
                   │
                   └─ FALSE ──→ Agent C (GENERAL) ──→ Chat Output
                                  ↑
                                  └─ llm ← LiteLLM
```

---

## 🎯 Key Points to Remember

### 1. Port Name is `input_text` (NOT `input_message`)
```
✅ CORRECT:
Intent Classifier (intent) → Conditional Router (input_text)

❌ WRONG:
Intent Classifier (intent) → Conditional Router (input_message)
                                                   ↑
                                            This port doesn't exist!
```

### 2. You Can Use `input_text` Two Ways

**Option A: Connect from another node**
```
Intent Classifier (intent) → Conditional Router (input_text)
```

**Option B: Type directly**
```
Conditional Router:
  - input_text: "some hardcoded text"
  - match_text: "expected value"
```

### 3. Case Sensitivity Matters
```
If case_sensitive = true:
  "TENANT" ≠ "tenant" ≠ "Tenant"

If case_sensitive = false:
  "TENANT" = "tenant" = "Tenant"
```

---

## 🔍 All Conditional Router Operators

| Operator | Example | Result |
|----------|---------|--------|
| `equals` | "TENANT" equals "TENANT" | TRUE |
| `not equals` | "TENANT" not equals "OWNER" | TRUE |
| `contains` | "I am a TENANT" contains "TENANT" | TRUE |
| `starts with` | "TENANT looking for..." starts with "TENANT" | TRUE |
| `ends with` | "...for TENANT" ends with "TENANT" | TRUE |
| `regex` | "TENANT123" regex "TENANT\d+" | TRUE |
| `less than` | "5" less than "10" | TRUE (numeric) |
| `less than or equal` | "5" less than or equal "5" | TRUE |
| `greater than` | "10" greater than "5" | TRUE |
| `greater than or equal` | "10" greater than or equal "10" | TRUE |

---

## 💡 Pro Tips

### Tip 1: Chain Conditions for Multiple Paths
```
Condition A (false) → Condition B (input_text)
Condition B (false) → Condition C (input_text)
Condition C (false) → Default Agent
```

### Tip 2: Use "contains" for Flexible Matching
```
Settings:
  - operator: "contains"
  - match_text: "help"

Matches:
  - "I need help"
  - "Can you help me?"
  - "HELP!"
```

### Tip 3: Use Regex for Complex Patterns
```
Settings:
  - operator: "regex"
  - match_text: "^(TENANT|OWNER)$"

Matches:
  - "TENANT" ✅
  - "OWNER" ✅
  - "GENERAL" ❌
```

---

## 🆘 Troubleshooting

### Problem: "Can't find input_message port"
**Solution**: The port is called `input_text`, not `input_message`

### Problem: "Condition always goes to false"
**Check**:
1. Is `match_text` spelled exactly right?
2. Is `case_sensitive` set correctly?
3. Is the correct `operator` selected?
4. Is `input_text` actually receiving the expected value?

### Problem: "How do I debug what value input_text is receiving?"
**Solution**: Add a `true_case_message` and `false_case_message` to see which path is taken

---

## 📚 Related Nodes

### DataConditionalRouter
If you need to route **Data objects** instead of text, use:
- Node ID: `flow_controls_DataConditionalRouter`
- Similar ports but works with Data type

---

**Last Updated**: 2026-02-08
**Status**: ✅ Verified with actual node library
**Verified By**: Direct inspection of `backend/data/node_library.json`
