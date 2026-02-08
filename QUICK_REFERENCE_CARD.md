# 📋 NODE CONFIGURATION QUICK REFERENCE CARD

## 🎯 THE GOLDEN RULES

### 1. Node IDs (Backend)
```
✅ USE: camelCase or snake_case
   liteLLM, smartDB, universalAgent
   flow_controls_ConditionalRouter (Label: If-Else)
   supabase_SupabaseVectorStore

❌ NEVER: spaces, hyphens, PascalCase
   "Universal Agent", universal-agent, UniversalAgent
```

### 2. Port Names (Always snake_case)
```
✅ USE: input_data, user_message, llm, tools, memory
❌ NEVER: inputData, userMessage, LLM, Tools, Memory
```

### 3. Connection Direction
```
✅ ALWAYS: Output → Input
   Node A (output) → Node B (input_data)

❌ NEVER: Output → Output or Input → Input
```

---

## 🔌 STANDARD PORT NAMES (Use These Exactly!)

### Input Ports
| Port Name | Type | Purpose |
|-----------|------|---------|
| `input_data` | handle | Main data input |
| `llm` | handle | LLM provider |
| `tools` | handle | Agent tools (multi) |
| `memory` | handle | Conversation history |
| `embedding` | handle | Embedding model |
| `user_message` | handle | User text input |
| `ingest_data` | handle | Data to ingest |
| `search_query` | text | Search text |
| `system_prompt` | textarea | Agent instructions |
| `agent_pattern` | dropdown | simple/standard/planner |

### Output Ports
| Port Name | Type | Purpose |
|-----------|------|---------|
| `output` | Text/Message | Main output |
| `response` | Text | LLM response |
| `result` | Data | Query result |
| `search_results` | Data | Search results |
| `status` | Text | Operation status |
| `intent` | Text | Classification |
| `confidence` | Number | Confidence score |
| `true_result` | Message | Condition true |
| `false_result` | Message | Condition false |

---

## 🏗️ ESSENTIAL NODE CONFIGURATIONS

### Universal Agent
```yaml
ID: universalAgent or langchainAgent
Label: "Universal Agent"

INPUTS (6):
  ✅ input_data (handle, REQUIRED) [Text, Message]
  ⚠️  llm (handle, RECOMMENDED) [LLM]
  ❌ tools (handle, OPTIONAL) [Tool] - can connect multiple
  ❌ memory (handle, OPTIONAL) [Memory]
  ❌ system_prompt (textarea, OPTIONAL)
  ❌ agent_pattern (dropdown, OPTIONAL) simple/standard/planner

OUTPUTS (1):
  output [Text, Message]

EXAMPLE CONNECTION:
  User Input → input_data
  LiteLLM → llm
  SmartDB → tools
  Supabase → tools
  Memory Node → memory
  output → Chat Output
```

### LiteLLM
```yaml
ID: liteLLM
Label: "Lite LLM (Tybot)"

INPUTS (5):
  ✅ input_data (handle, REQUIRED) [Text, Message, Data]
  ✅ api_key (password, REQUIRED)
  ❌ base_url (text)
  ❌ model_name (text) - default: "gpt-4.1-mini"
  ❌ temperature (number) - default: 0.1

OUTPUTS (1):
  response [Text]

EXAMPLE CONNECTION:
  (Usually not connected directly to input_data)
  response → Universal Agent (llm)
```

### If-Else (Conditional Router)
```yaml
ID: flow_controls_ConditionalRouter
Label: "If-Else" (was Conditional Router)

INPUTS (4):
  ✅ input_text (text, REQUIRED) [Message, Text]
  ✅ match_text (text, REQUIRED) - e.g., "TENANT"
  ❌ operator (dropdown) - equals/contains/starts with/etc.
  ❌ true_case_message (text)

OUTPUTS (2):
  true_result [Message]
  false_result [Message]

EXAMPLE CONNECTION:
  Intent Classifier (intent) → input_text
  true_result → Search Module
  false_result → Next Condition
```

### Intent Classifier
```yaml
ID: intentClassifierNode
Label: "Intent Classifier"

INPUTS (1):
  ✅ user_message (handle, REQUIRED) [Text, Message]

OUTPUTS (2):
  intent [Text, Tool] - Returns: "TENANT" | "OWNER" | "GENERAL"
  confidence [Number]

EXAMPLE CONNECTION:
  Transcription (text) → user_message
  intent → Conditional Router (input_text)
```

### Supabase Vector Store
```yaml
ID: supabase_SupabaseVectorStore
Label: "Supabase"

INPUTS (9):
  ✅ embedding (handle, REQUIRED) [Embeddings] ⚠️ MANDATORY!
  ✅ supabase_url (text, REQUIRED)
  ✅ supabase_service_key (password, REQUIRED)
  ❌ table_name (multiselect)
  ❌ search_query (text)
  ❌ ingest_data (handle) [Data]
  ❌ number_of_results (number) - default: 4
  ❌ should_cache_vector_store (boolean)

OUTPUTS (2):
  search_results [Data]
  dataframe [DataFrame]

EXAMPLE CONNECTION:
  Lite Embedding → embedding ⚠️ REQUIRED!
  search_results → Universal Agent (tools)
```

### SmartDB (NocoDB)
```yaml
ID: smartDB
Label: "SmartDB (NocoDB)"

INPUTS (6):
  ❌ input_data (handle, OPTIONAL) [Text, Message, Data]
  ✅ base_url (text, REQUIRED)
  ✅ api_key (password, REQUIRED)
  ❌ project_id (dropdown) - auto-populated
  ❌ table_id (multiselect) - empty = all tables
  ❌ operations (dropdown) - Create/Read/Update/Delete/All

OUTPUTS (1):
  result [Any]

EXAMPLE CONNECTION:
  result → Universal Agent (tools)
```

### Memory Node
```yaml
ID: memoryNode
Label: "Conversation Memory"

INPUTS (5):
  ✅ backend (dropdown, REQUIRED) in_memory/redis/windowed
  ❌ redis_url (text) - if backend=redis
  ❌ session_id (text) - if backend=redis
  ❌ ttl (number) - if backend=redis
  ❌ window_size (number) - if backend=windowed

OUTPUTS (1):
  memory [Memory]

EXAMPLE CONNECTION:
  memory → Universal Agent (memory)
```

### Lead Ingestor (Dual Storage)
```yaml
ID: dualIngestorNode
Label: "Lead Ingestor"

INPUTS (11):
  ✅ input_data (handle, REQUIRED) [Text, Message, Data]
  ✅ embedding (handle, REQUIRED) [Embeddings] ⚠️ MANDATORY!
  ❌ nocodb_url (text)
  ❌ nocodb_api_key (password)
  ❌ nocodb_table_id (text)
  ❌ supabase_url (text)
  ❌ supabase_service_key (password)
  ❌ supabase_table_name (text)
  ... (3 more config fields)

OUTPUTS (2):
  status [Text, Tool]
  data [Data, Text]

EXAMPLE CONNECTION:
  Lead Formatter (formatted_lead) → input_data
  Lite Embedding → embedding ⚠️ REQUIRED!
  status → Notification (message)
```

---

## ⚠️ CRITICAL WARNINGS

### 1. ALWAYS Connect Embedding Model
```
❌ WILL FAIL:
   Supabase Vector Store (no embedding connected)
   Lead Ingestor (no embedding connected)

✅ MUST DO:
   Lite Embedding → Supabase (embedding)
   Lite Embedding → Lead Ingestor (embedding)
```

### 2. ALWAYS Connect LLM to Agent
```
❌ WILL FAIL:
   Universal Agent (no llm connected)

✅ MUST DO:
   LiteLLM → Universal Agent (llm)
```

### 3. NEVER Connect Output to Output
```
❌ WRONG:
   Node A (output) → Node B (output)

✅ CORRECT:
   Node A (output) → Node B (input_data)
```

### 4. USE Exact Port Names
```
❌ WRONG:
   inputData, userMessage, systemPrompt

✅ CORRECT:
   input_data, user_message, system_prompt
```

---

## 🎨 TYPE COMPATIBILITY MATRIX

| From Type | Can Connect To |
|-----------|----------------|
| Text | Text, Message, Data, Any |
| Message | Text, Message, Any |
| Data | Data, Any |
| LLM | LLM, LanguageModel |
| Tool | Tool |
| Memory | Memory, BaseChatMessageHistory |
| Embeddings | Embeddings |
| Number | Number, Any |

---

## 🚀 COMPLETE WORKFLOW EXAMPLE

### Property Search with Conditional Routing
```
1. Chat Input (message)
   ↓
2. Transcription (text)
   ↓
3. Intent Classifier (intent)
   ↓
4. Condition A: "Is TENANT?"
   ├─ TRUE → Property Extractor
   │          ↓
   │       Universal Agent (Search Mode)
   │       - input_data ← Property Extractor
   │       - llm ← LiteLLM
   │       - tools ← Supabase (RAG)
   │       - tools ← SmartDB (SQL)
   │       - agent_pattern: "planner"
   │          ↓
   │       Carousel Builder
   │          ↓
   │       Chat Output
   │
   └─ FALSE → Condition B: "Is OWNER?"
              ├─ TRUE → RE Scraper
              │          ↓
              │       Lead Formatter
              │          ↓
              │       Lead Ingestor
              │       - input_data ← Lead Formatter
              │       - embedding ← Lite Embedding
              │          ↓
              │       Notification
              │          ↓
              │       Chat Output
              │
              └─ FALSE → Universal Agent (FAQ Mode)
                         - input_data ← Transcription
                         - llm ← LiteLLM
                         - memory ← Memory Node
                         - agent_pattern: "simple"
                            ↓
                         Chat Output
```

---

## 📚 LEGEND

| Symbol | Meaning |
|--------|---------|
| ✅ | Required / Must connect |
| ⚠️ | Strongly recommended |
| ❌ | Optional / Can skip |
| → | Connection direction |
| [Type] | Port type |

---

**Print this card and keep it handy!**
**Last Updated**: 2026-02-08 | Version 3.0
