# 🎓 BEGINNER'S GUIDE: Linking Nodes Made Easy

## 🌟 Start Here - The Absolute Basics

### What Are Nodes?
**Nodes are like building blocks.** Each block does one job:
- 📥 **Chat Input** = Gets user's message
- 🤖 **Universal Agent** = Thinks and responds
- 💬 **Chat Output** = Shows response to user
- 🧠 **LiteLLM** = The "brain" (AI model)

### What is Linking?
**Linking = Drawing arrows between blocks**

Like this:
```
Block A ──→ Block B ──→ Block C
```

---

## 🎯 The ONE Rule You Need

### ⭐ Connect RIGHT side to LEFT side

```
Every node has:
- LEFT side = INPUTS (◀ arrows pointing IN)
- RIGHT side = OUTPUTS (▶ arrows pointing OUT)

ALWAYS connect:
  Node A (RIGHT side) ──→ Node B (LEFT side)
         OUTPUT                  INPUT
```

**Visual**:
```
┌──────────┐              ┌──────────┐
│  Node A  │              │  Node B  │
│          │              │          │
│       ▶──┼──────────────┼▶         │
│  OUTPUT  │              │  INPUT   │
└──────────┘              └──────────┘
    ↑                          ↑
  RIGHT side              LEFT side
```

---

## 🚀 Your First Workflow (3 Minutes)

### Goal: Make a chatbot that answers questions

### You Need 4 Nodes:
1. **Chat Input** - Gets user's question
2. **LiteLLM** - The AI brain
3. **Universal Agent** - Processes and responds
4. **Chat Output** - Shows answer

### Step-by-Step:

#### Step 1: Add the nodes to canvas
```
Drag these 4 nodes from the left panel:
- Chat Input
- LiteLLM
- Universal Agent
- Chat Output
```

#### Step 2: Make 3 connections

**Connection #1: User Question → Agent**
```
Find "Chat Input" node
Look at RIGHT side
Find port called "message" ▶
Click and drag to "Universal Agent"
Drop on LEFT side port "input_data" ◀
```

Visual:
```
┌─────────────┐              ┌──────────────────┐
│ Chat Input  │              │ Universal Agent  │
│             │              │                  │
│  message ▶──┼──────────────┼▶ input_data      │
└─────────────┘              └──────────────────┘
```

**Connection #2: AI Brain → Agent**
```
Find "LiteLLM" node
Look at RIGHT side
Find port called "response" ▶
Click and drag to "Universal Agent"
Drop on LEFT side port "llm" ◀
```

Visual:
```
┌─────────────┐              ┌──────────────────┐
│  LiteLLM    │              │ Universal Agent  │
│             │              │                  │
│ response ▶──┼──────────────┼▶ llm             │
└─────────────┘              └──────────────────┘
```

**Connection #3: Agent → Show Answer**
```
Find "Universal Agent" node
Look at RIGHT side
Find port called "output" ▶
Click and drag to "Chat Output"
Drop on LEFT side port "message" ◀
```

Visual:
```
┌──────────────────┐              ┌─────────────┐
│ Universal Agent  │              │ Chat Output │
│                  │              │             │
│  output ▶────────┼──────────────┼▶ message    │
└──────────────────┘              └─────────────┘
```

#### Step 3: Complete Picture
```
Chat Input ──message──▶ Universal Agent ◀──llm──── LiteLLM
                        Universal Agent ──output──▶ Chat Output
```

**Done! Click "Run" to test!** ✅

---

## 🎨 Visual Learning - See the Flow

### Example 1: Simple Chat
```
USER TYPES: "What is AI?"
     │
     ↓
┌─────────────┐
│ Chat Input  │ Captures: "What is AI?"
└──────┬──────┘
       │ message
       ↓
┌──────────────────┐
│ Universal Agent  │◀─ Uses LiteLLM brain
│                  │  Thinks about question
└──────┬───────────┘
       │ output
       ↓
┌─────────────┐
│ Chat Output │ Shows: "AI is artificial intelligence..."
└─────────────┘
     │
     ↓
USER SEES ANSWER
```

### Example 2: Search Database
```
USER TYPES: "Find apartments in Maarif"
     │
     ↓
┌─────────────┐
│ Chat Input  │ Captures: "Find apartments in Maarif"
└──────┬──────┘
       │ message
       ↓
┌──────────────────┐
│ Universal Agent  │◀─ Uses LiteLLM brain
│                  │◀─ Uses Supabase to search
│                  │  Finds matching apartments
└──────┬───────────┘
       │ output
       ↓
┌─────────────┐
│ Chat Output │ Shows: "Found 5 apartments in Maarif..."
└─────────────┘
     │
     ↓
USER SEES RESULTS
```

---

## 🔧 Port Names - Simple Version

### You Only Need to Know These 6 Ports

#### On Universal Agent (LEFT side - INPUTS):
```
1. input_data ◀ ─── Connect user's message here
2. llm ◀ ────────── Connect LiteLLM here
3. tools ◀ ───────── Connect Supabase/SmartDB here
4. memory ◀ ──────── Connect Memory here (optional)
```

#### On Universal Agent (RIGHT side - OUTPUT):
```
1. output ▶ ──────── Connect to Chat Output here
```

#### On Other Nodes:
```
Chat Input:
  - message ▶ (sends user's message)

LiteLLM:
  - response ▶ (sends AI response)

Supabase:
  - search_results ▶ (sends search results)
  - embedding ◀ (needs Lite Embedding)

Chat Output:
  - message ◀ (receives text to show)
```

---

## ⚠️ Common Mistakes (And How to Fix)

### Mistake 1: Forgot to Connect LLM
```
❌ WRONG:
Chat Input → Universal Agent → Chat Output
             (Agent has no brain!)

ERROR: "No LLM connected to Agent"

✅ FIX:
Chat Input → Universal Agent ← LiteLLM
             Universal Agent → Chat Output
```

### Mistake 2: Connected Backwards
```
❌ WRONG:
Universal Agent → Chat Input
(Can't send TO the input!)

✅ FIX:
Chat Input → Universal Agent
(Always go FROM input TO agent)
```

### Mistake 3: Forgot Embedding for Supabase
```
❌ WRONG:
Supabase → Universal Agent
(Supabase needs embedding!)

ERROR: "Embedding required for Supabase"

✅ FIX:
Lite Embedding → Supabase → Universal Agent
```

---

## 📝 Copy-Paste Workflows

### Workflow 1: Basic Chatbot
```
NODES:
1. Chat Input
2. LiteLLM
3. Universal Agent
4. Chat Output

CONNECTIONS:
Chat Input (message) → Universal Agent (input_data)
LiteLLM (response) → Universal Agent (llm)
Universal Agent (output) → Chat Output (message)
```

### Workflow 2: Search Assistant
```
NODES:
1. Chat Input
2. LiteLLM
3. Lite Embedding
4. Supabase
5. Universal Agent
6. Chat Output

CONNECTIONS:
Chat Input (message) → Universal Agent (input_data)
LiteLLM (response) → Universal Agent (llm)
Lite Embedding (output) → Supabase (embedding)
Supabase (search_results) → Universal Agent (tools)
Universal Agent (output) → Chat Output (message)
```

### Workflow 3: If/Else Logic
```
NODES:
1. Chat Input
2. Intent Classifier
3. If-Else (Conditional Router)
4. Universal Agent (for TRUE path)
5. Universal Agent (for FALSE path)
6. LiteLLM
7. Chat Output

CONNECTIONS:
Chat Input (message) → Intent Classifier (user_message)
Intent Classifier (intent) → Conditional Router (input_text)
If-Else (Conditional Router) (true_result) → Agent 1 (input_data)
If-Else (Conditional Router) (false_result) → Agent 2 (input_data)
LiteLLM (response) → Agent 1 (llm)
LiteLLM (response) → Agent 2 (llm)
Agent 1 (output) → Chat Output (message)
Agent 2 (output) → Chat Output (message)
```

---

## 🎯 Practice Exercise

### Try This: Build a Simple Q&A Bot

**Step 1**: Drag 4 nodes to canvas
- Chat Input
- LiteLLM
- Universal Agent
- Chat Output

**Step 2**: Make these 3 connections
1. Chat Input (message) → Universal Agent (input_data)
2. LiteLLM (response) → Universal Agent (llm)
3. Universal Agent (output) → Chat Output (message)

**Step 3**: Click "Run" and test!

**Expected Result**: You can ask questions and get answers! ✅

---

## 💡 Remember

### The 3 Golden Rules:
1. **RIGHT → LEFT** (Output to Input)
2. **Agent needs LLM** (Always connect LiteLLM)
3. **Supabase needs Embedding** (Always connect Lite Embedding)

### When You're Stuck:
1. Check if all arrows go RIGHT → LEFT
2. Check if Agent has LLM connected
3. Check if Supabase has Embedding connected

---

## 🆘 Quick Help

### "I can't connect these nodes!"
**Answer**: Check if you're going RIGHT → LEFT (Output → Input)

### "My agent doesn't respond!"
**Answer**: Connect LiteLLM to the agent's `llm` port

### "I get 'Embedding required' error!"
**Answer**: Connect Lite Embedding to Supabase's `embedding` port

### "Which port do I use?"
**Answer**: Look at the port name:
- `input_data` = main input
- `llm` = for LiteLLM
- `tools` = for Supabase/SmartDB
- `output` = main output
- `message` = for text

---

## 🎉 You're Ready!

**Start with Workflow 1 (Basic Chatbot) and build from there!**

The more you practice, the easier it gets. Don't worry about making mistakes - you can always delete connections and try again!

**Good luck!** 🚀

---

**Need more help?** Check these files:
- `HOW_TO_LINK_NODES.md` - More detailed examples
- `QUICK_REFERENCE_CARD.md` - Quick lookup
- `DEFINITIVE_NODE_GUIDE.md` - Complete reference
