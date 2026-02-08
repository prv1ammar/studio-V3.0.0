# 🏗️ Detailed RAG Workflow Guide

This guide provides an exact, node-by-node construction plan for your Multi-Modal RAG pipeline, including **Tyboo LLM** and **Redis Memory**.

## 📋 Required Component Library
Use the exact nodes listed below found in the Studio sidebar.

| Component Category | Node Display Name (Label) | Purpose |
| :--- | :--- | :--- |
| **Tyboo** | **Lite LLM (Tybot)** | The Intelligence (Model). |
| **Tyboo** | **Tyboo Embedding** | Converts text to vectors. |
| **Tyboo** | **Configurable Agent (LangChain)** | The Orchestrator. |
| **Redis** | **Redis Chat Memory** | Stores conversation history. |
| **Supabase** | **Supabase** | Hybrid storage & search. |
| **Docling** | **Docling** | Extracts text/tables/images. |
| **Input/Output** | **Read File** | Uploads your PDF/Image. |
| **Processing** | **Data to Message** | Converts data to context. |
| **Input/Output** | **Chat Input** | Takes your question. |
| **Input/Output** | **Chat Output** | Shows the answer. |

---

## 🛠️ Step-by-Step Configuration

### 1️⃣ Ingestion Stage (Load & Store)
*Run this once to upload your document.*

**1. Node: [Read File]**
*   **Path**: Upload your file (e.g., `invoice.pdf`).

**2. Node: [Docling]**
*   **Connection**: `Read File` [Data] → `Docling` [Input].
*   **Settings**:
    *   **Pipeline**: `vlm` (for visuals) or `standard`.
    *   **OCR** (Optional): `easyocr`.

**3. Node: [Tyboo Embedding]**
*   **Settings**: Enter API Key.

**4. Node: [Supabase]**
*   **Connections**:
    *   `Docling` [Data] → `Ingest Data`.
    *   `Tyboo Embedding` [Embeddings] → `Embedding`.
*   **Settings**:
    *   **Supabase URL**: Your Project URL.
    *   **Service Key**: Your Key.
    *   **Table Name**: Select table (e.g. `documents`) from the **new Dropdown**.
*   **Action**: Click **Play** to ingest.

---

### 2️⃣ Agent Stage (Chat with Tools)
*In this setup, the Agent decides when to search the document.*

**1. Node: [Redis Chat Memory]**
*   **Settings**:
    *   **Redis URL**: `redis://localhost:6379/0`
    *   **Session ID**: `rag_session_1`

**2. Node: [Lite LLM (Tybot)]**
*   **Settings**:
    *   **Model**: `gpt-4.1-mini` or similar.

**3. Node: [Configurable Agent (LangChain)]**
*   **Connections**:
    *   **LLM Provider**: Connect `Lite LLM`.
    *   **Memory**: Connect `Redis Chat Memory`.
    *   **Tools**: Connect the **Supabase** node. *(Note: Connect either the Right edge or the specific Tool handle if visible)*.
    *   **User Question**: Connect `Chat Input` [Message].

**4. Node: [Chat Input]**
*   **Connection**: Connect ONLY to the `Agent` [User Question].

**5. (Optional) Node: [Prompt Template]**
*   **Purpose**: Give the Agent a specific "personality" or "rules."
*   **Connection**: `Prompt Template` [Prompt] → `Configurable Agent`.
*   **Settings**: 
    *   **Template**: "You are a specialized invoice analyst. Always explain the tax calculations in detail."
*   **Intelligence Note**: If you connect this node, the Agent will prioritize your custom instructions over its built-in rules!

**6. Node: [Chat Output]**
*   **Connection**: Connect `Agent` [Response] → `Chat Output`.

---

## 🚀 Execution
1.  **Ingest First**: Click Play on the **Supabase** node to process the document.
2.  **Ask**: Type a question in Chat Input.
3.  **Observe**: The Agent will now use its "Tool Calling" ability to search Supabase automatically only when relevant!

---

## 🧠 Studio Interface Guide (Understanding the Logic)

If the interface feels confusing, use these 6 simple rules to understand how to configure any box on the screen:

### 🟢 1. The Interaction Points (The Circles)
Every box has small circles on its sides. These are the "ports" for data:
*   **Left Side Circles (Inputs):** These are like "waiting rooms." The node cannot finish its work until these circles receive something from a previous box.
*   **Right Side Circles (Outputs):** These are "delivery docks." Once the box finishes its calculation or task, it pushes the result out through these circles to the next box in line.
*   **Color Matching:** You can only connect circles that speak the same "language." For example, a "Model" output must go into a "Model" input.

### 🔐 2. Authentication (The Shield/Lock Fields)
Any field with an **Eye Icon** or labeled as a **Secret** is for your private keys (like API passwords). 
*   **The Permission Rule:** Without these, the node has no permission to talk to the internet or your databases.
*   **Dependency:** If a dropdown menu below a secret field is empty, it usually means the Key hasn't been entered yet. The node needs the key first to "log in" and see your options.

### 📂 3. The "Discovery" Dropdowns
These are the smart menus that list your specific data (like folder names or database tables).
*   **Real-Time Refresh:** Once you paste your URL or Key, the system "handshakes" with your project. If the list doesn't update immediately, click outside the box or re-select the node to trigger the discovery.

### ⚙️ 4. Advanced Toggles (The Hidden Gears)
Sometimes you will see fields marked as **Advanced**. 
*   **What they do:** These control the "fine-tuning" (e.g., "How many documents should I return?" or "How creative should the reply be?").
*   **When to use them:** You can usually leave these at their default values. Only touch them if you want to change the *speed* or *depth* of the result.

### 📝 5. Text Areas & Prompting
Large, multi-line boxes are your **Instructions**.
*   **Input Data:** Sometimes used to provide a starting point (like a starting message).
*   **System Instructions:** Used to define the "personality" or "rules" of that specific step (e.g., "Always reply in French" or "Summarize this data into 3 bullet points").

### ⚡ 6. Execution Logic (How to Run)
When you click **Run**:
1.  The system traces the path from **Left to Right**.
2.  **Green Border:** Success! The node finished its task and passed data forward.
3.  **Red Border:** Error. Something is missing (usually an API Key or a broken line between circles).
4.  **Loading Spin:** The node is currently working (e.g., the LLM is thinking).
