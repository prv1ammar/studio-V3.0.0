# 🎨 Visual Port Wiring Guide

## Universal Agent - Complete Port Map

```
                    ┌─────────────────────────────────────────┐
                    │      UNIVERSAL AGENT NODE               │
                    │   (universalAgent / langchainAgent)     │
                    ├─────────────────────────────────────────┤
                    │                                         │
 User Message  ────▶│ ◀ input_data (REQUIRED)                │
                    │                                         │
 LiteLLM       ────▶│ ◀ llm (Recommended)                    │
                    │                                         │
 SmartDB       ────▶│ ◀ tools (Multiple OK)                  │
 Supabase      ────▶│                                         │
 Custom Tool   ────▶│                                         │
                    │                                         │
 Memory Node   ────▶│ ◀ memory (Optional)                    │
                    │                                         │
                    │ □ system_prompt (Text Area)             │
                    │ ▼ agent_pattern (Dropdown)              │
                    │   ├─ simple (LCEL)                      │
                    │   ├─ standard (Tool-Calling)            │
                    │   └─ planner (ReAct)                    │
                    │                                         │
                    ├─────────────────────────────────────────┤
                    │                                         │
                    │ output (Agent Response) ▶──────────────┼──▶ Chat Output
                    │                                         │
                    └─────────────────────────────────────────┘
```

---

## Complete Workflow Example

### Scenario: Property Search with Conditional Routing

```
┌──────────────┐
│  Chat Input  │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Transcription   │ (Audio → Text)
└──────┬───────────┘
       │
       ▼
┌────────────────────┐
│ Intent Classifier  │
│  Output: "TENANT"  │
└──────┬─────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Condition Node A                    │
│  Match: "TENANT"                     │
│  Operator: equals                    │
└───┬──────────────────────────┬───────┘
    │ TRUE                     │ FALSE
    ▼                          ▼
┌─────────────────┐    ┌──────────────────┐
│ Property        │    │  Condition B     │
│ Extractor       │    │  Match: "OWNER"  │
└────┬────────────┘    └───┬──────────┬───┘
     │                     │ TRUE     │ FALSE
     ▼                     ▼          ▼
┌──────────────────────────────┐  ┌──────────────┐  ┌──────────────┐
│   UNIVERSAL AGENT (Search)   │  │  RE Scraper  │  │ UNIVERSAL    │
│                              │  │      ↓       │  │ AGENT (FAQ)  │
│  Inputs:                     │  │ Lead Format  │  │              │
│  • input_data ← Extractor    │  │      ↓       │  │  Inputs:     │
│  • llm ← LiteLLM             │  │ Lead Ingest  │  │  • input_data│
│  • tools ← Supabase (RAG)    │  │              │  │  • llm       │
│  • tools ← SmartDB (SQL)     │  │              │  │  • memory    │
│  • agent_pattern: planner    │  │              │  │  Pattern:    │
│                              │  │              │  │  simple      │
│  Output:                     │  │              │  │              │
│  • Match results             │  │              │  │              │
└────────┬─────────────────────┘  └──────┬───────┘  └──────┬───────┘
         │                               │                 │
         ▼                               ▼                 │
┌──────────────────┐            ┌──────────────┐          │
│ Carousel Builder │            │ Notification │          │
└────────┬─────────┘            └──────┬───────┘          │
         │                             │                  │
         └─────────────────┬───────────┴──────────────────┘
                           ▼
                  ┌─────────────────┐
                  │   Chat Output   │
                  └─────────────────┘
```

---

## Port Connection Patterns

### Pattern 1: Single LLM, Multiple Tools
```
LiteLLM ────────────────────────▶ Universal Agent (llm)
                                         ▲
SmartDB ─────────────────────────────────┤
Supabase ────────────────────────────────┤─ (tools)
Custom API ──────────────────────────────┘
```

### Pattern 2: Agent Chain (Multi-Step)
```
Agent A (output) ──▶ Agent B (input_data)
                     ▲
LiteLLM ─────────────┤─ (llm)
Memory ──────────────┘─ (memory)
```

### Pattern 3: Conditional Tool Selection
```
Condition (true) ──▶ Tool A ──▶ Agent (tools)
Condition (false) ─▶ Tool B ──▶ Agent (tools)
```

---

## Common Port Mistakes ❌ → ✅

### ❌ WRONG: Connecting output to output
```
Agent A (output) ──X──▶ Agent B (output)
```

### ✅ CORRECT: Connecting output to input
```
Agent A (output) ──────▶ Agent B (input_data)
```

---

### ❌ WRONG: Missing LLM connection
```
User Input ──▶ Universal Agent (input_data)
               Universal Agent (output) ──▶ Chat Output
```
**Error**: "No LLM connected to Agent"

### ✅ CORRECT: LLM properly connected
```
User Input ──▶ Universal Agent (input_data)
LiteLLM ──────▶ Universal Agent (llm)
               Universal Agent (output) ──▶ Chat Output
```

---

### ❌ WRONG: Embedding missing for Supabase
```
Lead Data ──▶ Lead Ingestor (input_data)
              Lead Ingestor (status) ──▶ Output
```
**Error**: "Embedding required for Supabase"

### ✅ CORRECT: Embedding connected
```
Lead Data ────────▶ Lead Ingestor (input_data)
Embedding Model ──▶ Lead Ingestor (embedding)
                    Lead Ingestor (status) ──▶ Output
```

---

## Port Type Reference

| Symbol | Meaning |
|--------|---------|
| ◀ | Input Handle (connection port) |
| ▶ | Output Handle (connection port) |
| □ | Text Input Field |
| ▼ | Dropdown Selection |
| ☑ | Checkbox/Boolean |
| # | Number Input |

---

## Quick Reference Table

| Node | Critical Ports | Optional Ports |
|------|----------------|----------------|
| **Universal Agent** | `input_data`, `llm` | `tools`, `memory`, `system_prompt`, `agent_pattern` |
| **LiteLLM** | `input_data`, `api_key` | `model_name`, `temperature` |
| **SmartDB** | `base_url`, `api_key` | `input_data`, `table_id` |
| **Supabase** | `supabase_url`, `supabase_service_key`, `embedding` | `search_query`, `ingest_data` |
| **Lead Ingestor** | `input_data`, `embedding` | All config fields |
| **Memory Node** | `backend` | `redis_url`, `session_id`, `ttl` |
| **Intent Classifier** | `user_message` | None |
| **Condition** | `input_message`, `match_text` | `operator` |

---

**Last Updated**: 2026-02-08
**Version**: 2.0 (Post-Port Standardization)
