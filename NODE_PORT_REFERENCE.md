# 🔌 Node Port Configuration Guide

## Overview
This document provides the **definitive reference** for all node input and output ports in Tyboo Studio. Use this guide to understand which handles are available on each node and how to connect them properly.

---

## 🧠 Agent Nodes

### Universal Agent (`universalAgent` / `langchainAgent`)
**Purpose**: Dynamic LangChain agent with three orchestration tiers (Simple/Standard/Planner).

**Inputs** (6):
- `input_data` (handle) - **Required** - User's message or query [Text, Message]
- `llm` (handle) - Connect an LLM node (LiteLLM, OpenAI, etc.) [LLM]
- `tools` (handle) - Connect tool nodes (SmartDB, Supabase, etc.) [Tool]
- `memory` (handle) - Connect a memory node for conversation history [Memory]
- `system_prompt` (textarea) - Custom instructions for the agent (Advanced)
- `agent_pattern` (dropdown) - Orchestration tier: simple/standard/planner (Advanced)

**Outputs** (1):
- `output` - Agent's response [Text, Message]

**Connection Example**:
```
Chat Input → Universal Agent (input_data)
LiteLLM → Universal Agent (llm)
SmartDB → Universal Agent (tools)
Memory Node → Universal Agent (memory)
Universal Agent (output) → Chat Output
```

---

## 🤖 LLM Nodes

### LiteLLM (`liteLLM`)
**Purpose**: High-performance company-specific LLM router.

**Inputs** (5):
- `input_data` (handle) - **Required** - Input text
- `api_key` (password) - **Required** - API Key
- `base_url` (text) - Base URL
- `model_name` (text) - Model name (default: gpt-4.1-mini)
- `temperature` (number) - Temperature (default: 0.1)

**Outputs** (1):
- `response` - Assistant response [Text]

**Note**: When connected to an agent's `llm` port, this node provides the language model capability.

---

## 💾 Storage & Database Nodes

### SmartDB (`smartDB`)
**Purpose**: NocoDB connector with automated schema discovery.

**Inputs** (6):
- `input_data` (handle) - Operation data
- `base_url` (text) - NocoDB URL
- `api_key` (password) - API Key
- `project_id` (dropdown) - Select Database
- `table_id` (multiselect) - Select Table(s)
- `operations` (dropdown) - Create/Read/Update/Delete/All

**Outputs** (1):
- `result` - Query result [Any]

**Connection Example**:
```
Universal Agent (tools) ← SmartDB (result)
```

### Supabase Vector Store (`supabase_SupabaseVectorStore`)
**Purpose**: Vector search with RAG capabilities.

**Inputs** (9):
- `embedding` (handle) - **Connect an embedding model**
- `ingest_data` (handle) - Data to ingest
- `number_of_results` (number) - Number of results (default: 4)
- `query_name` (text) - Query name
- `search_query` (text) - Search query
- `should_cache_vector_store` (boolean) - Cache vector store
- `supabase_service_key` (password) - **Required**
- `supabase_url` (text) - **Required**
- `table_name` (multiselect) - Table name(s)

**Outputs** (2):
- `search_results` - Search results [Data]
- `dataframe` - DataFrame [DataFrame]

**Connection Example**:
```
Embedding Model → Supabase (embedding)
Universal Agent (tools) ← Supabase (search_results)
```

---

## 🧠 Memory Nodes

### Memory Node (`memoryNode`)
**Purpose**: Conversation history storage (Redis/In-Memory/Windowed).

**Inputs** (5):
- `backend` (dropdown) - Memory backend: in_memory/redis/windowed
- `redis_url` (text) - Redis URL (if backend=redis)
- `session_id` (text) - Session ID (if backend=redis)
- `ttl` (number) - TTL in seconds (if backend=redis)
- `window_size` (number) - Window size (if backend=windowed)

**Outputs** (1):
- `memory` - Memory object [Memory]

**Connection Example**:
```
Memory Node (memory) → Universal Agent (memory)
```

---

## 🎯 Classification & Extraction Nodes

### Intent Classifier (`intentClassifierNode`)
**Purpose**: Classifies user intent (TENANT/OWNER/GENERAL).

**Inputs** (1):
- `user_message` (handle) - **Required** - User message

**Outputs** (2):
- `intent` - Intent classification [Text, Tool]
- `confidence` - Confidence score [Number]

**Connection Example**:
```
Transcription (text) → Intent Classifier (user_message)
Intent Classifier (intent) → Condition Node (data_input)
```

### Property Extractor (`propertyExtractorNode`)
**Purpose**: Extracts search criteria from user messages.

**Inputs** (1):
- `user_message` (handle) - **Required** - User message

**Outputs** (4):
- `location` - Location [Text, Tool]
- `budget_max` - Max budget [Number]
- `bedrooms` - Number of bedrooms [Number]
- `property_type` - Property type [Text]

---

## 🔀 Logic & Flow Nodes

### Conditional Router (`flow_controls_ConditionalRouter`)
**Purpose**: Route messages based on conditions (if/else).

**Inputs** (4):
- `input_message` (handle) - Input message
- `match_text` (text) - Text to match
- `operator` (dropdown) - equals/not equals/contains/starts with/ends with/regex/less than/greater than
- `true_case_message` (text) - Message if condition is true

**Outputs** (2):
- `true_result` - Output if condition is true [Message]
- `false_result` - Output if condition is false [Message]

**Connection Example**:
```
Intent Classifier (intent) → Condition (input_message)
  Match Text: "TENANT"
  Operator: equals
Condition (true_result) → [Search Module]
Condition (false_result) → [Next Condition]
```

### Data Conditional Router (`flow_controls_DataConditionalRouter`)
**Purpose**: Route data objects based on key-value conditions.

**Inputs** (4):
- `data_input` (text) - Data object or list
- `key_name` (text) - Key name to check
- `compare_value` (text) - Value to compare against
- `operator` (dropdown) - equals/not equals/contains/starts with/ends with/boolean validator

**Outputs** (2):
- `true_output` - Data if condition is true [Data]
- `false_output` - Data if condition is false [Data]

---

## 🔧 Real Estate AI Nodes

### Lead Ingestor (`leadIngestorNode`)
**Purpose**: Dual storage (NocoDB + Supabase) with automatic vectorization.

**Inputs** (11):
- `input_data` (handle) - Formatted lead [Object, Data, Text]
- `embedding` (handle) - **Required** - Embedding model [Vector, Embeddings]
- `nocodb_url` (text) - NocoDB URL
- `nocodb_api_key` (password) - NocoDB API Key
- `nocodb_project_id` (text) - Project ID
- `nocodb_table_id` (text) - Table ID
- `supabase_url` (text) - Supabase URL
- `supabase_service_key` (password) - Supabase Service Key
- `supabase_table_name` (text) - Table name
- `supabase_query_name` (text) - RPC query name

**Outputs** (2):
- `status` - Ingestion status [Text, Tool]
- `data` - Ingested data [Object, Data, Text]

---

## ✅ Port Connection Rules

### 1. **Type Matching**
Ports must have compatible types:
- `[Text]` can connect to `[Text, Message]`
- `[Tool]` can connect to agent's `tools` port
- `[LLM]` can connect to agent's `llm` port
- `[Memory]` can connect to agent's `memory` port

### 2. **Required vs Optional**
- **Required ports** (marked with `required: true`) must be connected for the node to execute
- **Optional ports** can be left unconnected; the node will use defaults

### 3. **Handle Types**
- `handle` - Connection port (visual edge on canvas)
- `text` - Text input field
- `textarea` - Multi-line text input
- `password` - Secure credential input
- `dropdown` - Single selection
- `multiselect` - Multiple selections
- `number` - Numeric input
- `boolean` - True/false toggle

---

## 🎨 Visual Port Layout

### Universal Agent Node
```
┌─────────────────────────────────┐
│      UNIVERSAL AGENT            │
├─────────────────────────────────┤
│ ◀ input_data (User Input)       │
│ ◀ llm (LLM)                      │
│ ◀ tools (Tools)                  │
│ ◀ memory (Memory)                │
│ □ system_prompt                  │
│ ▼ agent_pattern                  │
├─────────────────────────────────┤
│ output (Agent Response) ▶        │
└─────────────────────────────────┘
```

### Condition Node
```
┌─────────────────────────────────┐
│      CONDITION                   │
├─────────────────────────────────┤
│ ◀ input_message                  │
│ □ match_text                     │
│ ▼ operator                       │
├─────────────────────────────────┤
│ true_result ▶                    │
│ false_result ▶                   │
└─────────────────────────────────┘
```

---

**Last Updated**: 2026-02-08
**Version**: 2.0 (Post-Standardization)
