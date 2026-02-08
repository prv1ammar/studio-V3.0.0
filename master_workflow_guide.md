# 🏢 MASTER GUIDE: Complete Real Estate AI Workflow

This is your step-by-step instruction manual to build the entire system from scratch.

---

## 🗺️ The Big Picture

We are building a **3-Branch Workflow**:
1.  **Branch A (Tenant)**: User wants to rent → Search properties in Database
2.  **Branch B (Owner)**: User wants to list → Scrape listing URL & Save to Database
3.  **Branch C (General)**: User has a question → Answer with AI Memory

---

## 🛠️ PHASE 1: Input & Routing (The Brain)

### Step 1: Add Input Nodes

**1. Chat Input**
- **Action**: Drag to canvas.
- **Config**: None.

**2. Transcription Node** (Optional - for voice)
- **Node ID**: `transcriptionNode`
- **Config**: None.
- **Connection**:
  - `Chat Input` (audio) → `Transcription` (audio_url)

**3. Intent Classifier**
- **Node ID**: `intentClassifierNode`
- **Label**: "Intent Classifier"
- **Config**: None (Model detects: "TENANT", "OWNER", "GENERAL").
- **Connection**:
  - `Chat Input` (message) → `Intent Classifier` (user_message)
  - *OR* `Transcription` (text) → `Intent Classifier` (user_message)

### Step 2: Add Logic Nodes (If-Else)

**4. If-Else (Check for Tenant)**
- **Node ID**: `flow_controls_ConditionalRouter`
- **Label**: "Is Tenant?"
- **Config**:
  - `match_text`: **TENANT**
  - `operator`: **equals**
- **Connection**:
  - `Intent Classifier` (intent) → `Is Tenant?` (input_text / IN: Value to Check)

**5. If-Else (Check for Owner)**
- **Node ID**: `flow_controls_ConditionalRouter`
- **Label**: "Is Owner?"
- **Config**:
  - `match_text`: **OWNER**
  - `operator`: **equals**
- **Connection**:
  - `Is Tenant?` (false_result) → `Is Owner?` (input_text / IN: Value to Check)

---

## 🏠 PHASE 2: Tenant Branch (Property Search) [True Path of Node 4]

**skipped** (Not needed - The Search Agent is smart enough!)

**7. Universal Agent (Search Agent)**
- **Node ID**: `universalAgent`
- **Label**: "Search Agent"
- **Config**:
  - `agent_pattern`: **planner** (Required for complex search)
  - `system_prompt`:
    ```
    You are a helpful real estate assistant.
    Your goal is to help users find properties to rent.
    ALWAYS use the 'search_properties' tool to find listings.
    If you find matches, show them to the user.
    ```
- **Connections (CRITICAL)**:
  - **Input**: `Is Tenant?` (true_result) → `Search Agent` (input_data)
  - **LLM**: `LiteLLM` (response) → `Search Agent` (llm)
  - **Tools**: `Supabase` (search_results) → `Search Agent` (tools)
  - **Tools**: `SmartDB` (result) → `Search Agent` (tools)

**8. Supabase Vector Store (The Database)**
- **Node ID**: `supabase_SupabaseVectorStore`
- **Label**: "Property DB"
- **Config**:
  - `table_name`: **properties**
  - `supabase_url`: (Your URL)
  - `supabase_service_key`: (Your Key)
- **Connection**:
  - `Lite Embedding` (output) → `Supabase` (embedding) ⚠️ **REQUIRED**

**9. Carousel Builder**
- **Node ID**: `carouselNode`
- **Config**: None.
- **Connection**:
  - `Search Agent` (output) → `Carousel Builder` (matches) ⚠️ **Use 'matches' port!**

**10. Chat Output (Tenant)**
- **Connection**:
  - `Carousel Builder` (summary_message) → `Chat Output` (message)
  - *OR* `Carousel Builder` (carousel_json) → `Chat Output` (message) (If your UI supports JSON rendering)

---

## 📝 PHASE 3: Owner Branch (Lead Capture) [True Path of Node 5]

**11. Universal Agent (URL Extractor) [OPTIONAL BUT RECOMMENDED]**
*   **Why?** To extract *just* the link if the user sends a full sentence.
*   **Node ID**: `universalAgent`
*   **Label**: "URL Extractor"
*   **Config**:
    *   `agent_pattern`: **simple**
    *   `system_prompt`: "Extract ONLY the URL from the user message. Return nothing else."
*   **Connection**:
    *   `Is Owner?` (true_result) → `URL Extractor` (input_data)
    *   `LiteLLM` (response) → `URL Extractor` (llm)

**12. Web Scraper**
- **Node ID**: `reScraperNode` (Label: "Web Scraper")
- **Config**: None.
- **Connection**:
  - `URL Extractor` (output) → `Web Scraper` (url)
  - *OR* `Is Owner?` (true_result) → `Web Scraper` (url) (If user sends ONLY the link)

**13. Lead Formatter**
- **Node ID**: `leadFormatterNode`
- **Label**: "Lead Formatter"
- **Config**: None.
- **Connection**:
  - `Web Scraper` (Extracted Content) → `Lead Formatter` (Input Markdown) ⚠️ **Use 'Extracted Content' port!**

**14. Sync & Store (Dual)**
- **Real UI Name**: `Sync & Store (Dual)` (Was called Lead Ingestor)
- **Node ID**: `dualIngestorNode`
- **Label**: "Lead Saver"
- **Config**:
  - `supabase_table_name`: **leads**
  - `supabase_url`: (Your URL)
  - `supabase_service_key`: (Your Key)
- **Connections (CRITICAL)**:
  - **Data**: `Lead Formatter` (formatted_lead) → `Sync & Store (Dual)` (input_data)
  - **Embedding**: `Lite Embedding` (output) → `Sync & Store (Dual)` (embedding) ⚠️ **REQUIRED**

**15. Notification Node**
- **Node ID**: `notificationNode`
- **Label**: "Notify Team"
- **Config**:
  - `channel`: **email** (or slack)
  - `recipient`: **admin@tyboo.com**
- **Connection**:
  - `Lead Ingestor` (status) → `Notification` (message) ⚠️ **Use 'message' input port!**

**16. Chat Output (Owner)**
- **Connection**:
  - `Notification` (status) → `Chat Output` (message)

---

## 💬 PHASE 4: General Branch (FAQ) [False Path of Node 5]

**16. Universal Agent (Support Agent)**
- **Node ID**: `universalAgent`
- **Label**: "Support Agent"
- **Config**:
  - `agent_pattern`: **simple** (Fast response)
  - `system_prompt`: "You are a friendly customer service agent. Answer general questions."
- **Connections**:
  - **Input**: `Is Owner?` (false_result) → `Support Agent` (input_data)
  - **LLM**: `LiteLLM` (response) → `Support Agent` (llm)
  - **Memory**: `Memory Node` (memory) → `Support Agent` (memory)

**17. Memory Node (Redis - Shared)**
- **Node ID**: `memoryNode`
- **Config**:
  - `backend`: **redis** ⚠️ **High Performance!**
  - `redis_url`: `redis://localhost:6379/0`
- **Connection**:
  - `Memory Node` (memory) → `Search Agent` (memory)
  - `Memory Node` (memory) → `Support Agent` (memory)
  - `Memory Node` (memory) → `URL Extractor` (memory) (If used)
- **Tip**: Connect this ONE node to ALL your agents to share history!

**18. Chat Output (General)**
- **Connection**:
  - `Support Agent` (output) → `Chat Output` (message)

---

## ⚡ CORE INFRASTRUCTURE (Connect These to Everything)

**A. LiteLLM (The Brain)**
- **Node ID**: `liteLLM`
- **Config**:
  - `model_name`: **gpt-4o** (Recommended)
  - `api_key`: (Your OpenAI Key)
- **Connect Output (`response`) TO**:
  - `Search Agent` (llm)
  - `Support Agent` (llm)
  - `Intent Classifier` (llm) [If applicable, though classifier usually runs standalone]

**B. Lite Embedding (The Translator)**
- **Node ID**: `liteEmbedding`
- **Config**:
  - `model_name`: **text-embedding-3-small**
- **Connect Output (`output`) TO**:
  - `Supabase Vector Store` (embedding)
  - `Lead Ingestor` (embedding)

---

## ✅ FINAL CHECKLIST

Before you run:
1.  **Check Embedding**: Is `Lite Embedding` connected to BOTH `Supabase` and `Lead Ingestor`? (Most common error!)
2.  **Check LLM**: Is `LiteLLM` connected to BOTH `Search Agent` and `Support Agent`?
3.  **Check Router**: Is `Intent Classifier` connected to `Is Tenant?` (Input Text/IN)?
4.  **Check API Keys**: Are your Supabase and OpenAI keys entered in the nodes?

**You are ready to build! Start dragging nodes!** 🚀
