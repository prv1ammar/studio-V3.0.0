# 🎯 DEFINITIVE GUIDE: Node Configuration & Naming Conventions

## Table of Contents
1. [Node Naming Conventions](#node-naming-conventions)
2. [Port Naming Standards](#port-naming-standards)
3. [Complete Node Configuration Guide](#complete-node-configuration-guide)
4. [Connection Rules](#connection-rules)
5. [Common Mistakes to Avoid](#common-mistakes-to-avoid)

---

# Node Naming Conventions

## Rule 1: Node IDs (Backend)

**Format**: `camelCase` or `snake_case` with category prefix

### Standard Node IDs
```
✅ CORRECT:
- universalAgent
- langchainAgent
- liteLLM
- smartDB
- intentClassifierNode
- propertyExtractorNode
- supabase_SupabaseVectorStore
- flow_controls_ConditionalRouter

❌ WRONG:
- Universal Agent (spaces not allowed)
- universal-agent (hyphens not allowed)
- UniversalAgent (PascalCase - avoid)
```

### Naming Pattern by Category

| Category | Pattern | Examples |
|----------|---------|----------|
| **Tyboo Core** | `camelCase` | `liteLLM`, `smartDB`, `universalAgent` |
| **AI Services** | `descriptiveNode` | `intentClassifierNode`, `chatInput`, `chatOutput` |
| **LangChain** | `category_ComponentName` | `flow_controls_ConditionalRouter` |
| **Vector Stores** | `provider_ProviderName` | `supabase_SupabaseVectorStore`, `pinecone_Pinecone` |
| **Tools** | `provider_ToolName` | `composio_ComposioGmailAPIComponent` |

## Rule 2: Node Labels (UI Display)

**Format**: Human-readable with proper capitalization

```
✅ CORRECT:
- "Universal Agent"
- "Intent Classifier"
- "Lite LLM (Tybot)"
- "SmartDB (NocoDB)"
- "Conditional Router"

❌ WRONG:
- "universalAgent" (not user-friendly)
- "UNIVERSAL AGENT" (all caps - too aggressive)
- "universal agent" (no capitalization)
```

## Rule 3: Node Descriptions

**Format**: Clear, concise sentence describing purpose

```
✅ CORRECT:
- "Dynamic LangChain agent with three orchestration tiers: Simple (LCEL), Standard (Tool-Calling), and Planner (ReAct)."
- "Classifies user intent: TENANT, OWNER, or GENERAL"
- "High-performance company-specific LLM router."

❌ WRONG:
- "Agent" (too vague)
- "This node does agent stuff" (unprofessional)
- "" (empty - never acceptable)
```

---

# Port Naming Standards

## Input Port Names

### Standard Input Ports (Use These Exact Names)

| Port Name | Type | Used For | Example Nodes |
|-----------|------|----------|---------------|
| **`input_data`** | handle | Main data input | Universal Agent, Processors, Tools |
| **`llm`** | handle | LLM provider connection | Universal Agent, LangChain Agents |
| **`tools`** | handle | Tool connections (multi) | Universal Agent, CrewAI |
| **`memory`** | handle | Conversation history | Universal Agent, Chat Agents |
| **`embedding`** | handle | Embedding model | Vector Stores, Lead Ingestor |
| **`user_message`** | handle | User's text input | Intent Classifier, Property Extractor |
| **`ingest_data`** | handle | Data to ingest | Vector Stores |
| **`search_query`** | text | Search text | Vector Stores |
| **`system_prompt`** | textarea | Agent instructions | Universal Agent |
| **`agent_pattern`** | dropdown | Orchestration tier | Universal Agent |

### Port Naming Rules

```
✅ CORRECT:
- input_data (snake_case, descriptive)
- user_message (clear purpose)
- llm (standard abbreviation)
- embedding_model (explicit)

❌ WRONG:
- inputData (camelCase - inconsistent)
- input (too vague)
- msg (unclear abbreviation)
- LLM (uppercase - avoid)
```

## Output Port Names

### Standard Output Ports (Use These Exact Names)

| Port Name | Type | Used For | Example Nodes |
|-----------|------|----------|---------------|
| **`output`** | Text/Message | Main output | Universal Agent, Processors |
| **`response`** | Text/Message | LLM response | LiteLLM, OpenAI |
| **`result`** | Data | Query/operation result | SmartDB, API calls |
| **`search_results`** | Data | Search results | Vector Stores |
| **`status`** | Text | Operation status | Lead Ingestor, Notifications |
| **`intent`** | Text | Classification result | Intent Classifier |
| **`confidence`** | Number | Confidence score | Intent Classifier |
| **`true_result`** | Message | Condition true path | Conditional Router |
| **`false_result`** | Message | Condition false path | Conditional Router |

---

# Complete Node Configuration Guide

## 1. Universal Agent Configuration

### Node ID
```
universalAgent  OR  langchainAgent
```

### Port Configuration (6 Inputs, 1 Output)

#### Inputs
```json
1. input_data (handle, REQUIRED)
   - Display Name: "User Input"
   - Types: ["Text", "Message"]
   - Description: "The user's message or query"
   
2. llm (handle, RECOMMENDED)
   - Display Name: "LLM"
   - Types: ["LLM", "LanguageModel"]
   - Description: "Connect an LLM node (LiteLLM, OpenAI, etc.)"
   
3. tools (handle, OPTIONAL)
   - Display Name: "Tools"
   - Types: ["Tool"]
   - Description: "Connect tool nodes (can connect multiple)"
   
4. memory (handle, OPTIONAL)
   - Display Name: "Memory"
   - Types: ["Memory"]
   - Description: "Connect a memory node for conversation history"
   
5. system_prompt (textarea, OPTIONAL)
   - Display Name: "System Prompt"
   - Default: "You are a helpful AI assistant."
   - Description: "Custom instructions for the agent"
   
6. agent_pattern (dropdown, OPTIONAL)
   - Display Name: "Agent Pattern"
   - Options: ["simple", "standard", "planner"]
   - Default: "standard"
   - Description: "Orchestration tier"
```

#### Output
```json
1. output
   - Display Name: "Agent Response"
   - Types: ["Text", "Message"]
```

### Configuration Example
```
Node Name in UI: "Search Agent"
Node ID: universalAgent
Settings:
  - agent_pattern: "planner"
  - system_prompt: "You are a property search assistant..."

Connections:
  input_data ← Transcription Node (text port)
  llm ← LiteLLM (response port)
  tools ← Supabase Vector Store (search_results port)
  tools ← SmartDB (result port)
  memory ← Memory Node (memory port)
  output → Carousel Builder (matches port)
```

---

## 2. LiteLLM Configuration

### Node ID
```
liteLLM
```

### Port Configuration (5 Inputs, 1 Output)

#### Inputs
```json
1. input_data (handle, REQUIRED)
   - Display Name: "Input Text"
   - Types: ["Text", "Message", "Data"]
   
2. api_key (password, REQUIRED)
   - Display Name: "API Key"
   - Default: "sk-RVApjtnPznKZ4UXosZYEOQ"
   
3. base_url (text)
   - Display Name: "Base URL"
   - Default: "https://toknroutertybot.tybotflow.com/"
   
4. model_name (text)
   - Display Name: "Model Name"
   - Default: "gpt-4.1-mini"
   
5. temperature (number)
   - Display Name: "Temperature"
   - Default: 0.1
```

#### Output
```json
1. response
   - Display Name: "Assistant Response"
   - Types: ["Text"]
```

### Configuration Example
```
Node Name in UI: "Main LLM"
Node ID: liteLLM
Settings:
  - model_name: "gpt-4o"
  - temperature: 0.3

Connections:
  input_data ← (Usually not connected directly - used via agent)
  response → Universal Agent (llm port)
```

---

## 3. Conditional Router Configuration

### Node ID
```
flow_controls_ConditionalRouter
```

### Port Configuration (4 Inputs, 2 Outputs)

#### Inputs
```json
1. input_text (text, REQUIRED)
   - Display Name: "Input Text"
   - Types: ["Text", "Message"]
   
2. match_text (text, REQUIRED)
   - Display Name: "Match Text"
   - Example: "TENANT"
   
3. operator (dropdown)
   - Display Name: "Operator"
   - Options: ["equals", "not equals", "contains", "starts with", "ends with", "regex"]
   - Default: "equals"
   
4. true_case_message (text, OPTIONAL)
   - Display Name: "Case True"
   - Description: "Message to pass if condition is true"
```

#### Outputs
```json
1. true_result
   - Display Name: "True"
   - Types: ["Message"]
   
2. false_result
   - Display Name: "False"
   - Types: ["Message"]
```

### Configuration Example
```
Node Name in UI: "Is Tenant?"
Node ID: flow_controls_ConditionalRouter
Settings:
  - match_text: "TENANT"
  - operator: "equals"

Connections:
  input_text ← Intent Classifier (intent port)
  true_result → Property Extractor (user_message port)
  false_result → Next Condition Node (input_text port)
```

---

## 4. Intent Classifier Configuration

### Node ID
```
intentClassifierNode
```

### Port Configuration (1 Input, 2 Outputs)

#### Input
```json
1. user_message (handle, REQUIRED)
   - Display Name: "User Message"
   - Types: ["Text", "Message"]
```

#### Outputs
```json
1. intent
   - Display Name: "Intent"
   - Types: ["Text", "Tool"]
   - Values: "TENANT" | "OWNER" | "GENERAL"
   
2. confidence
   - Display Name: "Confidence"
   - Types: ["Number"]
```

### Configuration Example
```
Node Name in UI: "Intent Classifier"
Node ID: intentClassifierNode

Connections:
  user_message ← Transcription Node (text port)
  intent → Conditional Router (input_text port)
```

---

## 5. Supabase Vector Store Configuration

### Node ID
```
supabase_SupabaseVectorStore
```

### Port Configuration (9 Inputs, 2 Outputs)

#### Critical Inputs
```json
1. embedding (handle, REQUIRED)
   - Display Name: "Embedding"
   - Types: ["Embeddings"]
   - ⚠️ MUST be connected for vector operations
   
2. supabase_url (text, REQUIRED)
   - Display Name: "Supabase URL"
   - Example: "https://your-project.supabase.co"
   
3. supabase_service_key (password, REQUIRED)
   - Display Name: "Supabase Service Key"
   
4. table_name (multiselect)
   - Display Name: "Table Name(s)"
   - Description: "Select tables for vector storage/search"
   
5. search_query (text, OPTIONAL)
   - Display Name: "Search Query"
   - Description: "Text to search for"
   
6. ingest_data (handle, OPTIONAL)
   - Display Name: "Ingest Data"
   - Types: ["Data"]
```

#### Outputs
```json
1. search_results
   - Display Name: "Search Results"
   - Types: ["Data"]
   
2. dataframe
   - Display Name: "DataFrame"
   - Types: ["DataFrame"]
```

### Configuration Example
```
Node Name in UI: "Property Search DB"
Node ID: supabase_SupabaseVectorStore
Settings:
  - supabase_url: "https://xyz.supabase.co"
  - table_name: ["properties"]

Connections:
  embedding ← Lite Embedding Node (output port)
  search_results → Universal Agent (tools port)
```

---

## 6. SmartDB (NocoDB) Configuration

### Node ID
```
smartDB
```

### Port Configuration (6 Inputs, 1 Output)

#### Inputs
```json
1. input_data (handle, OPTIONAL)
   - Display Name: "Operation Data"
   - Types: ["Text", "Message", "Data"]
   
2. base_url (text, REQUIRED)
   - Display Name: "NocoDB URL"
   - Example: "https://nocodb.yourcompany.com"
   
3. api_key (password, REQUIRED)
   - Display Name: "API Key"
   
4. project_id (dropdown)
   - Display Name: "Select Database"
   - Auto-populated after connection
   
5. table_id (multiselect)
   - Display Name: "Select Table(s)"
   - Description: "Leave empty to expose ALL tables"
   
6. operations (dropdown)
   - Display Name: "Operations"
   - Options: ["Create", "Read", "Update", "Delete", "All"]
```

#### Output
```json
1. result
   - Display Name: "Query Result"
   - Types: ["Any"]
```

### Configuration Example
```
Node Name in UI: "Properties DB"
Node ID: smartDB
Settings:
  - base_url: "https://app.nocodb.com"
  - table_id: ["properties", "leads"]
  - operations: "All"

Connections:
  result → Universal Agent (tools port)
```

---

## 7. Memory Node Configuration

### Node ID
```
memoryNode
```

### Port Configuration (5 Inputs, 1 Output)

#### Inputs
```json
1. backend (dropdown, REQUIRED)
   - Display Name: "Memory Backend"
   - Options: ["in_memory", "redis", "windowed"]
   - Default: "in_memory"
   
2. redis_url (text, CONDITIONAL)
   - Display Name: "Redis URL"
   - Default: "redis://localhost:6379/0"
   - Show if: backend = "redis"
   
3. session_id (text, CONDITIONAL)
   - Display Name: "Session ID"
   - Default: "default_session"
   - Show if: backend = "redis"
   
4. ttl (number, CONDITIONAL)
   - Display Name: "TTL (seconds)"
   - Show if: backend = "redis"
   
5. window_size (number, CONDITIONAL)
   - Display Name: "Window Size"
   - Default: 10
   - Show if: backend = "windowed"
```

#### Output
```json
1. memory
   - Display Name: "Memory Object"
   - Types: ["Memory"]
```

### Configuration Example
```
Node Name in UI: "Conversation Memory"
Node ID: memoryNode
Settings:
  - backend: "redis"
  - redis_url: "redis://localhost:6379/0"
  - session_id: "{user_phone_number}"

Connections:
  memory → Universal Agent (memory port)
```

---

## 8. Lead Ingestor (Dual Storage) Configuration

### Node ID
```
dualIngestorNode
```

### Port Configuration (11 Inputs, 2 Outputs)

#### Critical Inputs
```json
1. input_data (handle, REQUIRED)
   - Display Name: "Formatted Lead"
   - Types: ["Text", "Message", "Data"]
   
2. embedding (handle, REQUIRED)
   - Display Name: "Embedding Model"
   - Types: ["Embeddings"]
   - ⚠️ MANDATORY for Supabase ingestion
   
3. nocodb_url (text)
   - Display Name: "NocoDB URL"
   
4. nocodb_api_key (password)
   - Display Name: "NocoDB API Key"
   
5. nocodb_table_id (text)
   - Display Name: "Table ID"
   
6. supabase_url (text)
   - Display Name: "Supabase URL"
   
7. supabase_service_key (password)
   - Display Name: "Supabase Service Key"
   
8. supabase_table_name (text)
   - Display Name: "Table Name"
```

#### Outputs
```json
1. status
   - Display Name: "Ingestion Status"
   - Types: ["Text", "Tool"]
   
2. data
   - Display Name: "Ingested Data"
   - Types: ["Data", "Text"]
```

### Configuration Example
```
Node Name in UI: "Lead Storage"
Node ID: dualIngestorNode

Connections:
  input_data ← Lead Formatter (formatted_lead port)
  embedding ← Lite Embedding (output port)
  status → Notification Node (message port)
```

---

# Connection Rules

## Rule 1: Type Matching

**Ports must have compatible types to connect**

### Compatible Type Pairs
```
✅ ALLOWED:
[Text] → [Text, Message]
[Message] → [Text, Message]
[Data] → [Data, Any]
[LLM] → [LLM, LanguageModel]
[Tool] → [Tool]
[Memory] → [Memory, BaseChatMessageHistory]
[Embeddings] → [Embeddings]

❌ NOT ALLOWED:
[Text] → [Number]
[LLM] → [Tool]
[Memory] → [Data]
```

## Rule 2: Multiple Connections

**Some ports accept multiple connections**

```
✅ CAN CONNECT MULTIPLE:
- Universal Agent (tools port) ← Can receive multiple tool nodes
- Agent (tools port) ← SmartDB + Supabase + Custom API

❌ SINGLE CONNECTION ONLY:
- Universal Agent (llm port) ← Only one LLM
- Universal Agent (memory port) ← Only one memory node
- Universal Agent (input_data port) ← Only one input source
```

## Rule 3: Required vs Optional

```
✅ REQUIRED (Must connect):
- Universal Agent: input_data
- LiteLLM: input_data, api_key
- Supabase: embedding, supabase_url, supabase_service_key
- Lead Ingestor: input_data, embedding

⚠️ RECOMMENDED (Should connect):
- Universal Agent: llm (without it, agent can't function)

❌ OPTIONAL (Can skip):
- Universal Agent: tools, memory, system_prompt
- Supabase: search_query, ingest_data
```

## Rule 4: Port Direction

```
OUTPUTS connect TO INPUTS (never output-to-output or input-to-input)

✅ CORRECT:
Node A (output) → Node B (input_data)
LiteLLM (response) → Universal Agent (llm)

❌ WRONG:
Node A (output) → Node B (output)
Node A (input) → Node B (input)
```

---

# Common Mistakes to Avoid

## ❌ Mistake 1: Wrong Port Names
```
❌ WRONG:
- inputData (should be: input_data)
- userMessage (should be: user_message)
- LLM (should be: llm)
- systemPrompt (should be: system_prompt)

✅ CORRECT:
- input_data
- user_message
- llm
- system_prompt
```

## ❌ Mistake 2: Missing Embedding Model
```
❌ WRONG:
Lead Data → Lead Ingestor (input_data)
            Lead Ingestor (status) → Output
# ERROR: "Embedding required for Supabase"

✅ CORRECT:
Lead Data → Lead Ingestor (input_data)
Embedding Model → Lead Ingestor (embedding)
Lead Ingestor (status) → Output
```

## ❌ Mistake 3: No LLM Connected to Agent
```
❌ WRONG:
User Input → Universal Agent (input_data)
             Universal Agent (output) → Chat Output
# ERROR: "No LLM connected to Agent"

✅ CORRECT:
User Input → Universal Agent (input_data)
LiteLLM → Universal Agent (llm)
Universal Agent (output) → Chat Output
```

## ❌ Mistake 4: Type Mismatch
```
❌ WRONG:
Intent Classifier (confidence) → Condition (input_text)
# confidence is [Number], input_text expects [Text, Message]

✅ CORRECT:
Intent Classifier (intent) → Condition (input_text)
# intent is [Text], matches input_text [Text, Message]
```

## ❌ Mistake 5: Connecting Output to Output
```
❌ WRONG:
Agent A (output) → Agent B (output)

✅ CORRECT:
Agent A (output) → Agent B (input_data)
```

---

# Quick Reference Cheat Sheet

## Most Common Ports

| Port Name | Direction | Type | Used In |
|-----------|-----------|------|---------|
| `input_data` | Input | [Text, Message, Data] | Agents, Processors |
| `llm` | Input | [LLM] | Agents |
| `tools` | Input | [Tool] | Agents |
| `memory` | Input | [Memory] | Agents |
| `embedding` | Input | [Embeddings] | Vector Stores, Ingestors |
| `user_message` | Input | [Text, Message] | Classifiers, Extractors |
| `output` | Output | [Text, Message] | Agents, Processors |
| `response` | Output | [Text] | LLMs |
| `result` | Output | [Data] | Databases, APIs |
| `status` | Output | [Text] | Operations |

## Node ID Patterns

| Node Type | ID Pattern | Example |
|-----------|------------|---------|
| Tyboo Core | camelCase | `liteLLM`, `smartDB` |
| AI Services | descriptiveNode | `intentClassifierNode` |
| LangChain | category_Name | `flow_controls_ConditionalRouter` |
| Vector Stores | provider_Name | `supabase_SupabaseVectorStore` |

---

**Last Updated**: 2026-02-08
**Version**: 3.0 (Production)
**Status**: ✅ Definitive Reference
