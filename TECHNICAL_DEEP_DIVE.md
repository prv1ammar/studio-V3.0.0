# Tyboo Studio: Deep Technical Architecture & Workflow Execution

This document provides an exhaustive, step-by-step technical breakdown of the Tyboo Studio architecture. It is designed to prepare technical teams for in-depth inquiries regarding the system's inner workings.

---

## 1. The Core Data Structure: The JSON Graph
Every workflow in Tyboo Studio is represented as a **Directed Acyclic Graph (DAG)**. This graph is serialized into a JSON object containing two main arrays:

- **`nodes`**: Each node object contains:
    - `id`: A unique UUID or string (e.g., `agent-177...`).
    - `type`: Maps to a specific Python class (e.g., `agentNode`).
    - `data`: Stores configuration parameters (API keys, model names, prompt templates) and visual state.
- **`edges`**: Objects defining the data flow:
    - `source`: The ID of the originating node.
    - `target`: The ID of the recipient node.
    - `sourceHandle` / `targetHandle`: Specific ports (e.g., "Result" to "Query").

---

## 2. Backend Execution Lifecycle: Step-by-Step

When the user clicks "Run" or sends a message, the following sequence occurs in the FastAPI backend:

### Step 1: Request Reception & Graph Parsing
The endpoint `/run` (or `/run/node`) receives the JSON graph. The backend uses a **Validation Layer** to:
- Verify that all mandatory fields (API keys, URLs) are populated.
- Identify the "Entry Point" (usually a Chat Input or a specific trigger node).

### Step 2: Dependency Resolution (Topological Sort)
The system calculates the execution order. It looks at the `edges` to identify which nodes are "precursors."
- If Node B depends on an output from Node A, Node A must finish first.
- The system builds an execution queue based on these dependencies.

### Step 3: Node Factory Instantiation
For each node in the queue, the **Node Factory** (`factory.py`) instantiates the corresponding Python class. 
- All nodes inherit from a common `BaseNode` interface.
- This ensures consistency: every node has an `execute()` method and a `get_langchain_object()` method.

### Step 4: The Execution Context (State Management)
As nodes execute, the backend maintains a **Context Dictionary**.
- **Key**: The Node ID.
- **Value**: The output of that node.
- This context is passed into every subsequent node, allowing them to "look back" and retrieve data from any previous step in the chain.

---

## 3. Inside the Agent Nodes (The AI Brain)

The `LangChainAgentNode` is the most complex component. Here is what happens inside:

1.  **Tool Initialization**: The agent dynamically instantiates "Tools." For example, if connected to a `SupabaseSearch` node, it converts that node's logic into a `langchain.tools.BaseTool`.
2.  **Model Agnostic Layer (LiteLLM)**: We use LiteLLM to interface with models. This allows the agent to switch between GPT-4, Claude 3, or Llama 3 without changing a single line of code.
3.  **Prompt Engineering**: The `PromptNode` feeds a structured system prompt into the agent, defining its persona and strict rules (e.g., *"Only show images if the caption matches exactly"*).
4.  **ReAct Logic (Reasoning & Action)**: The agent enters a loop:
    - **Thought**: "The user wants a graph of sales."
    - **Action**: Call the `SupabaseSearch` tool with query "Sales graph".
    - **Observation**: Retrieves a chunk with an image URL and caption "Figure 43: Sales 2023".
    - **Final Answer**: Displays the image and text.

---

## 4. Advanced RAG Pipeline: Visual-First Ingestion

### A. Document Decomposition (Docling)
When a document is uploaded, we don't just "read text." We use the **Docling** engine:
- **Vision/OCR**: Analyzes the visual layout of the page.
- **Element Detection**: Distinguishes between `Paragraph`, `Heading`, `Table`, and `Figure`.
- **Image Extraction**: Crops images/graphs from the PDF and saves them to local storage.

### B. Intelligent Chunking & Content Linking
- **Context Injection**: For every image extracted, the system looks at the 2000 characters of text *before* and *after* it. 
- **Title Discovery**: It uses regex and NLP to find labels like "Figure XIV" or "Table 1".
- **Vectorization**: Only the text and metadata (captions) are embedded using OpenAI `text-embedding-3-small`. The image URL is stored as a reference in the metadata.

### C. The Retrieval Logic (Supabase + Re-ranking)
Standard vector search often fails on specific queries (like "Show Figure 43"). We solve this with **Smart Re-ranking**:
1.  **Semantic Search**: Fetch top 10 results from Supabase via cosine similarity.
2.  **Keyword Boosting**: A post-processing step scans the retrieved chunks. If the user query contains a number (e.g., "43") and a chunk's metadata contains "Figure 43", that chunk is forced to the #1 position.

---

## 5. Smart DB Node: Dynamic Data Orchestration

This node connects to External REST APIs (NocoDB / TybotFlow) using a generic adapter pattern:

- **JWT Auth Flow**: Specifically handles `Authorization: Bearer` tokens.
- **Metadata Discovery**: 
    - The `GET /nodes/smartdb/metadata` endpoint allows the UI to fetch databases and tables dynamically *before* execution.
    - It maps disparate API fields (e.g., `base_name` vs `title`) into a unified `label/value` format for the Studio dropdowns.
- **Operation Execution**: When the workflow runs, the node performs REST actions (GET, POST, PATCH) against the specific `table_id` using the configuration defined in the graph.

---

## 6. Memory & Persistence
- **Redis/JSON Storage**: The `MemoryNode` captures the sliding window of the conversation. 
- **Session Management**: Each user interaction is tagged with a `SessionID`, allowing the backend to retrieve the relevant history for the LLM's `ChatHistory` window.

---

## 7. Technical Differentiators (Why this is unique)
1.  **No Hallucination Enforcer**: Strict prompt rules + metadata boosting ensure the agent doesn't guess when an image is missing.
2.  **Hybrid RAG**: Combines visual (tables/graphs) and textual data in a single searchable vector space.
3.  **Low-Code Modularity**: New nodes can be added by creating a single Python file; the UI automatically discovers them via the `/nodes` endpoint.
