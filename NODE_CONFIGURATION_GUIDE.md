# ⚙️ DETAILED NODE CONFIGURATION GUIDE

This guide contains the **exact settings** you need to copy-paste into your nodes to make the Tyboo workflow run perfectly.

---

## 🧠 PHASE 1: The Brain (Routing)

### 1. Intent Classifier
*   **Node Label**: `Intent Classifier`
*   **No Configuration Needed**: (It automatically detects `TENANT`, `OWNER`, `GENERAL`).

### 2. If-Else Check #1 (Tenant)
*   **Node Label**: `If-Else` (First one connected to Intent Classifier)
*   **Settings**:
    *   **Match Text**: `SEARCH_RENTAL` ⚠️ (Must match this EXACTLY)
    *   **Operator**: `equals`

### 3. If-Else Check #2 (Owner)
*   **Node Label**: `If-Else` (Connected to the "False" output of Check #1)
*   **Settings**:
    *   **Match Text**: `LIST_PROPERTY` ⚠️ (Must match this EXACTLY)
    *   **Operator**: `equals`

---

## 🏠 PHASE 2: Tenant Configuration (Search Branch)

### 4. Search Agent (Universal Agent)
*   **Node ID**: `langchainAgent-1770562011651` (The one connected to Supabase/SmartDB)
*   **Settings**:
    *   **Agent Pattern**: `planner` (⚠️ CRITICAL: Must be "planner" to use tools effectively)
    *   **System Prompt**:
        ```text
        You are an expert Real Estate Agent assistant for Tyboo.
        Your goal is to help users find properties to rent (Tenant search).
        
        TOOLS AVAILABLE:
        1. 'supabase_search': Use this to find properties by description (e.g., "2 bedroom in Maarif").
        2. 'smartdb_query': Use this to check specific details if needed.
        
        INSTRUCTIONS:
        - ALWAYS use the search tools when a user asks for properties.
        - If you find multiple matches, summarize the top 3.
        - Be helpful, professional, and concise.
        - If no properties are found, apologize and ask for different criteria.
        ```

### 5. Supabase Vector Store
*   **Node Label**: `Supabase`
*   **Settings**:
    *   **Table Name**: `properties` (or your specific listings table)
    *   **Query Name**: `match_documents` (Default Supabase function)
    *   **Wrapper**: `SupabaseVectorStore`

---

## 📝 PHASE 3: Owner Configuration (Listing Branch)

### 6. URL Extractor Agent (Universal Agent)
*   **Node ID**: `langchainAgent-1770563172910` (The one before the Scraper)
*   **Settings**:
    *   **Agent Pattern**: `simple` (Fastest, no tools needed)
    *   **System Prompt**:
        ```text
        Your ONLY task is to extract the URL from the user's message.
        
        output format:
        Return ONLY the URL string. Do not add any text like "Here is the URL".
        
        Example:
        User: "I want to list this house https://avito.ma/house123"
        Output: "https://avito.ma/house123"
        ```

### 7. Lead Ingestor (Sync & Store)
*   **Node Label**: `Sync & Store (Dual)`
*   **Settings**:
    *   **Supabase Table**: `leads`
    *   **NocoDB Project ID**: (From your NocoDB dashboard)
    *   **Content Fields**: `["formatted_lead"]` (This maps the data correctly)

### 8. Notification Node
*   **Node Label**: `Notify Team`
*   **Settings**:
    *   **Channel**: `email` (Simplest to test) or `slack`
    *   **Recipient**: `admin@tyboo.com` ⚠️ (REQUIRED to avoid "Missing recipient" error!)
    *   **Subject**: `New Lead Detected!`

---

## 💬 PHASE 4: Support Configuration (General Branch)

### 9. Support Agent (Universal Agent)
*   **Node ID**: `langchainAgent-1770564530252` (The fallback agent)
*   **Settings**:
    *   **Agent Pattern**: `simple` (or `standard` if you want it to have tools later)
    *   **System Prompt**:
        ```text
        You are the friendly customer support AI for Tyboo.
        We help people buy, rent, and list properties in Morocco.
        
        - Be polite and helpful.
        - If you don't know an answer, direct them to support@tyboo.com.
        - Do NOT invent property listings. Only answer general questions here.
        ```

---

## 🔑 GLOBAL SETTINGS (Infrastructure)

### 10. LiteLLM (The Brain)
*   **Node Label**: `LiteLLM`
*   **Settings**:
    *   **Model Name**: `gpt-4o` or `gpt-4-turbo` (Recommended for best results)
    *   **Temperature**: `0.3` (Low temperature = more precise facts)

### 11. Lite Embedding
*   **Node Label**: `Lite Embedding`
*   **Settings**:
    *   **Model Name**: `text-embedding-3-small` (Industry standard, cheap & fast)

### 12. Redis Memory
*   **Node Label**: `Redis Chat Memory`
*   **Settings**:
    *   **Redis URL**: `redis://localhost:6379/0`
    *   **Session ID**: Leave blank (auto-generated) or map to `{user_id}`

---

## ✅ FINAL CONFIGURATION CHECKLIST

1.  [ ] **API Keys**: Did you enter your OpenAI & Supabase keys in the LiteLLM and Supabase nodes?
2.  [ ] **Agent Patterns**: Is the Search Agent set to `planner`? (Critical!)
3.  [ ] **Router Logic**: Is Router 1 checking `TENANT` and Router 2 checking `OWNER`?
4.  [ ] **Memory**: Is the Redis node connected to ALL 3 agents?

**Save this file and use it to configure your nodes one by one!** 🚀
