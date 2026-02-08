# 🔗 HOW TO LINK NODES - Simple Step-by-Step Guide

## 🎯 The Basics (Start Here!)

### What is "Linking Nodes"?

**Linking = Connecting the OUTPUT of one node to the INPUT of another node**

Think of it like connecting LEGO blocks:
- Each node has **connection points** (called "ports")
- **Output ports** send data OUT
- **Input ports** receive data IN
- You draw a line from OUTPUT → INPUT

---

## 📍 Step 1: Understanding Ports

### Every Node Has Two Sides

```
┌─────────────────────────┐
│      NODE NAME          │
├─────────────────────────┤
│ ◀ INPUT PORTS           │  ← Left side = INPUTS (receive data)
│   (receive data)        │
│                         │
│   OUTPUT PORTS ▶        │  ← Right side = OUTPUTS (send data)
│   (send data)           │
└─────────────────────────┘
```

### Example: Chat Input Node
```
┌─────────────────────────┐
│     CHAT INPUT          │
├─────────────────────────┤
│ (no inputs)             │  ← This node starts the flow
│                         │
│   message ▶             │  ← Sends the user's message
└─────────────────────────┘
```

### Example: Universal Agent Node
```
┌─────────────────────────┐
│   UNIVERSAL AGENT       │
├─────────────────────────┤
│ ◀ input_data            │  ← Receives user message
│ ◀ llm                   │  ← Receives LLM connection
│ ◀ tools                 │  ← Receives tools
│ ◀ memory                │  ← Receives memory
│                         │
│   output ▶              │  ← Sends agent's response
└─────────────────────────┘
```

---

## 📍 Step 2: The Golden Rule

### ⭐ ALWAYS Connect: OUTPUT → INPUT

```
✅ CORRECT:
Node A (output) ──────→ Node B (input_data)
       ↑                      ↑
    OUTPUT                 INPUT

❌ WRONG:
Node A (output) ──────→ Node B (output)
       ↑                      ↑
    OUTPUT                 OUTPUT
    (Can't connect output to output!)

❌ WRONG:
Node A (input) ──────→ Node B (input)
       ↑                    ↑
    INPUT                INPUT
    (Can't connect input to input!)
```

---

## 📍 Step 3: Your First Connection

### Example: Simple Chat

**Goal**: User types message → Agent responds

**Nodes You Need**:
1. Chat Input
2. Universal Agent
3. LiteLLM
4. Chat Output

**How to Connect**:

```
Step 1: Chat Input → Universal Agent
┌─────────────┐
│ Chat Input  │
│             │
│  message ▶──┼──────┐
└─────────────┘      │
                     │
                     ↓
              ┌──────────────────┐
              │ Universal Agent  │
              │                  │
              │ ◀ input_data     │ ← Connect HERE
              └──────────────────┘

HOW: Drag from "message" port to "input_data" port
```

```
Step 2: LiteLLM → Universal Agent
┌─────────────┐
│  LiteLLM    │
│             │
│ response ▶──┼──────┐
└─────────────┘      │
                     │
                     ↓
              ┌──────────────────┐
              │ Universal Agent  │
              │                  │
              │ ◀ llm            │ ← Connect HERE
              └──────────────────┘

HOW: Drag from "response" port to "llm" port
```

```
Step 3: Universal Agent → Chat Output
┌──────────────────┐
│ Universal Agent  │
│                  │
│  output ▶────────┼──────┐
└──────────────────┘      │
                          │
                          ↓
                   ┌──────────────┐
                   │ Chat Output  │
                   │              │
                   │ ◀ message    │ ← Connect HERE
                   └──────────────┘

HOW: Drag from "output" port to "message" port
```

**Complete Flow**:
```
Chat Input (message) → Universal Agent (input_data)
LiteLLM (response) → Universal Agent (llm)
Universal Agent (output) → Chat Output (message)
```

---

## 📍 Step 4: Common Workflows

### Workflow 1: Simple Question & Answer

**What You Need**:
- Chat Input
- Universal Agent
- LiteLLM
- Chat Output

**Connections** (in order):
```
1. Chat Input (message) → Universal Agent (input_data)
2. LiteLLM (response) → Universal Agent (llm)
3. Universal Agent (output) → Chat Output (message)
```

**Visual**:
```
Chat Input
    │
    │ message
    ↓
Universal Agent ← llm ← LiteLLM (response)
    │
    │ output
    ↓
Chat Output
```

---

### Workflow 2: Search with Database

**What You Need**:
- Chat Input
- Universal Agent
- LiteLLM
- Supabase Vector Store
- Lite Embedding
- Chat Output

**Connections** (in order):
```
1. Chat Input (message) → Universal Agent (input_data)
2. LiteLLM (response) → Universal Agent (llm)
3. Lite Embedding (output) → Supabase (embedding)
4. Supabase (search_results) → Universal Agent (tools)
5. Universal Agent (output) → Chat Output (message)
```

**Visual**:
```
Chat Input
    │
    │ message
    ↓
Universal Agent ← llm ← LiteLLM (response)
    ↑
    │ tools
    │
Supabase ← embedding ← Lite Embedding (output)
    │
    │ output
    ↓
Chat Output
```

---

### Workflow 3: Conditional Routing (If/Else)

**What You Need**:
- Chat Input
- Intent Classifier
- Conditional Router
- 2x Universal Agents (one for each path)
- LiteLLM
- Chat Output

**Connections** (in order):
```
1. Chat Input (message) → Intent Classifier (user_message)
2. Intent Classifier (intent) → Conditional Router (input_text)
3. If-Else (Conditional Router) (true_result) → Agent A (input_data)
4. Conditional Router (false_result) → Agent B (input_data)
5. LiteLLM (response) → Agent A (llm)
6. LiteLLM (response) → Agent B (llm)
7. Agent A (output) → Chat Output (message)
8. Agent B (output) → Chat Output (message)
```

**Visual**:
```
Chat Input
    │
    │ message
    ↓
Intent Classifier
    │
    │ intent
    ↓
If-Else
    ├─ true_result ──→ Agent A ← llm ← LiteLLM
    │                      │
    │                      │ output
    │                      ↓
    │                  Chat Output
    │
    └─ false_result ──→ Agent B ← llm ← LiteLLM
                           │
                           │ output
                           ↓
                       Chat Output
```

---

## 📍 Step 5: Port Names You MUST Know

### Input Ports (Where Data Goes IN)

| Port Name | What It Receives | Example |
|-----------|------------------|---------|
| `input_data` | User's message or data | Chat Input → Agent |
| `llm` | LLM connection | LiteLLM → Agent |
| `tools` | Tool connections | Supabase → Agent |
| `memory` | Memory connection | Memory Node → Agent |
| `embedding` | Embedding model | Lite Embedding → Supabase |
| `user_message` | User's text | Chat Input → Classifier |

### Output Ports (Where Data Comes OUT)

| Port Name | What It Sends | Example |
|-----------|---------------|---------|
| `output` | Agent's response | Agent → Chat Output |
| `response` | LLM's response | LiteLLM → Agent |
| `message` | User's message | Chat Input → Agent |
| `intent` | Classification result | Classifier → Router |
| `search_results` | Search results | Supabase → Agent |
| `result` | Query result | SmartDB → Agent |

---

## 📍 Step 6: Critical Connections (NEVER FORGET!)

### ⚠️ Rule 1: Agent MUST Have LLM
```
❌ WILL FAIL:
Chat Input → Universal Agent → Chat Output
             (no LLM connected!)

✅ CORRECT:
Chat Input → Universal Agent ← LiteLLM
             Universal Agent → Chat Output
```

### ⚠️ Rule 2: Vector Store MUST Have Embedding
```
❌ WILL FAIL:
Supabase → Universal Agent
(no embedding connected!)

✅ CORRECT:
Lite Embedding → Supabase → Universal Agent
```

### ⚠️ Rule 3: Lead Ingestor MUST Have Embedding
```
❌ WILL FAIL:
Lead Data → Lead Ingestor → Output
            (no embedding!)

✅ CORRECT:
Lead Data → Lead Ingestor ← Lite Embedding
            Lead Ingestor → Output
```

---

## 📍 Step 7: How to Actually Connect in the UI

### Method 1: Drag and Drop
```
1. Click on the OUTPUT port (right side of node)
2. Hold and drag to the INPUT port (left side of target node)
3. Release to create connection
```

### Method 2: Click and Click
```
1. Click on the OUTPUT port
2. Click on the INPUT port
3. Connection created automatically
```

### Visual Guide:
```
Step 1: Click OUTPUT
┌─────────────┐
│   Node A    │
│             │
│  output ▶ ● │ ← Click this circle
└─────────────┘

Step 2: Drag to INPUT
                    ┌─────────────┐
                    │   Node B    │
                    │             │
● ─ ─ ─ ─ ─ ─ ─ ─ ▶│◀ input_data │ ← Release here
                    └─────────────┘

Step 3: Connection Created
┌─────────────┐              ┌─────────────┐
│   Node A    │              │   Node B    │
│             │              │             │
│  output ▶───┼──────────────┼▶ input_data │
└─────────────┘              └─────────────┘
```

---

## 📍 Step 8: Troubleshooting

### Problem: "Can't connect these nodes"
**Cause**: Type mismatch
**Solution**: Check if port types match

```
Example:
Intent Classifier (confidence) → Condition (input_text)
                  ↑                           ↑
               [Number]                   [Text, Message]
               
❌ Number can't connect to Text/Message

✅ Use this instead:
Intent Classifier (intent) → Condition (input_text)
                  ↑                      ↑
              [Text, Tool]           [Text, Message]
              
✅ Text can connect to Text/Message
```

### Problem: "Agent not responding"
**Cause**: Missing LLM connection
**Solution**: Connect LiteLLM to agent's `llm` port

```
❌ Missing:
Chat Input → Universal Agent → Chat Output

✅ Fixed:
Chat Input → Universal Agent ← LiteLLM (response → llm)
             Universal Agent → Chat Output
```

### Problem: "Embedding required"
**Cause**: Vector store or ingestor missing embedding
**Solution**: Connect Lite Embedding

```
❌ Missing:
Supabase → Agent

✅ Fixed:
Lite Embedding (output) → Supabase (embedding)
Supabase (search_results) → Agent (tools)
```

---

## 📍 Step 9: Complete Example (Copy This!)

### Build a Smart Search Assistant

**Nodes Needed** (7 total):
1. Chat Input
2. Universal Agent
3. LiteLLM
4. Supabase Vector Store
5. Lite Embedding
6. SmartDB
7. Chat Output

**Connections** (copy exactly):
```
Connection 1: Chat Input
  - From: Chat Input (message)
  - To: Universal Agent (input_data)

Connection 2: LLM
  - From: LiteLLM (response)
  - To: Universal Agent (llm)

Connection 3: Embedding for Supabase
  - From: Lite Embedding (output)
  - To: Supabase (embedding)

Connection 4: Supabase to Agent
  - From: Supabase (search_results)
  - To: Universal Agent (tools)

Connection 5: SmartDB to Agent
  - From: SmartDB (result)
  - To: Universal Agent (tools)

Connection 6: Agent to Output
  - From: Universal Agent (output)
  - To: Chat Output (message)
```

**Visual Diagram**:
```
        Chat Input
            │
            │ message
            ↓
    ┌───────────────┐
    │ Universal     │
    │ Agent         │◀─── llm ──── LiteLLM (response)
    │               │
    │               │◀─── tools ── Supabase ◀─ embedding ─ Lite Embedding
    │               │                                        (output)
    │               │◀─── tools ── SmartDB (result)
    └───────┬───────┘
            │
            │ output
            ↓
       Chat Output
```

**Settings**:
- Universal Agent: agent_pattern = "planner"
- LiteLLM: model_name = "gpt-4o"
- Supabase: table_name = ["properties"]
- SmartDB: table_id = ["properties"]

---

## 🎯 Quick Checklist

Before you test your workflow, check:

- [ ] Every node is connected (no floating nodes)
- [ ] All connections go OUTPUT → INPUT (never output to output)
- [ ] Universal Agent has LLM connected
- [ ] Vector stores have Embedding connected
- [ ] Input ports match output port types
- [ ] Required ports are connected (marked with ✅)

---

## 💡 Remember These 3 Rules

1. **OUTPUT → INPUT** (always this direction)
2. **Agent needs LLM** (or it won't work)
3. **Vector stores need Embedding** (or they fail)

---

**You're ready! Start with the simple Q&A example and build from there.** 🚀

**Need help?** Look at the visual diagrams and copy the connection patterns exactly!
