# 🧪 Testing Guide: Advanced RAG Agent with Visuals

This guide explains how to test the **Image-Enabled RAG Agent** we built. The system consists of two main workflows: **Ingestion** (loading data) and **Agent** (chatting with data).

## ✅ Prerequisites

Ensure your backend server and frontend Studio are running:

1.  **Backend**:
    ```powershell
    .\venv\Scripts\activate
    uvicorn backend.app.api.main:app --host 0.0.0.0 --port 8001
    ```
2.  **Frontend**:
    ```powershell
    cd studio
    npm run dev
    ```
    (Access at `http://localhost:5173`)

---

## 📂 Part 1: Ingesting a Document (Upload & Process)

Before the agent can answer questions, you must load a document into the database.

1.  **Open Studio** at `http://localhost:5173`.
2.  **Load Ingestion Workflow**:
    - Click **Upload** (or File > Open).
    - Select: `workflow-1770032924542.json`.
3.  **Configuring the File**:
    - Click the **Read File** node.
    - Ensure the **Path** points to your pdf (e.g., `file:///C:/Users/info/Downloads/Rapport-economique-financier_Fr.pdf`).
4.  **Run Ingestion**:
    - Click the **Play (▶️)** button.
    - **Wait**: Processing PDF images takes about 30-60 seconds.
    - **Success**: You should see green checkmarks and a "Success" message on the Supabase node.

> **Note**: If you need to clear old data, run `python clear_supabase.py` in your terminal.

---

## 🤖 Part 2: Testing the Agent (Chat)

Now that data is in Supabase, let's talk to it.

1.  **Load Agent Workflow**:
    - Click **Upload** again.
    - Select: `workflow-1770034421006.json`.
2.  **Verify Connections**:
    - **Prompt Template** → **LangChain Agent** (Input Data).
    - **Supabase** → **LangChain Agent** (Tools).
    - **LiteLLM** → **LangChain Agent** (LLM).
3.  **Ask Questions**:
    Type these queries in the **Chat Input**:

    *   **"What are the key financial figures?"**
        *   *Expected*: A text summary of the metrics found in the doc.
    *   **"Show me the financial graphs."**
        *   *Expected*: The agent should display the actual images (e.g., `![Graph](...)`) extracted from the PDF.
    *   **"Summarize the document."**
        *   *Expected*: A high-level overview.

---

## 🛠️ Troubleshooting Common Errors

If you see these errors in the chat or terminal:

### 1. "Technical Issue / No embedding model connected"
*   **Cause**: The agent couldn't find the embedding node connected to Supabase.
*   **Fix**: This was fixed by updating `langchain_agent.py` to pass the correct context. **Restart the backend** if you see this.

### 2. "SyncRPCFilterRequestBuilder object has no attribute params"
*   **Cause**: Version mismatch in LangChain/Supabase libraries.
*   **Fix**: We implemented a direct RPC call in `supabase_node.py`. Ensure you are using the latest code.

### 3. "Chunking Error: 'str' object has no attribute 'get'"
*   **Cause**: docling returned data in an unexpected format (string vs dict).
*   **Fix**: We improved `chunk_node.py` to handle all data types robustly.

### 4. "PdfPipelineOptions object has no field..."
*   **Cause**: Your installed `docling` version is older than the latest docs.
*   **Fix**: We commented out `do_formula_classification` and `generate_vlm_captions` in `docling_node.py`.

---

## 💾 System Architecture

*   **Ingestion**: File → Docling (OCR/VLM) → Chunker (Preserves Images) → Supabase Vector Store.
*   **Retrieval**: Agent → Supabase Search (RPC) → Context + Image Links → LLM Response.
