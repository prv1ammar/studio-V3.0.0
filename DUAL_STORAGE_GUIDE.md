# 🚀 EasySpace AI: Dual Storage & Ingestion Guide

Welcome to the new **Unified Ingestion System**! This feature ensures that every listing or lead provided by an agent is simultaneously available for **structured management** (NocoDB) and **semantic search** (Supabase Vector Store).

## 🌟 Key Features
- **One-Click Sync**: No need to connect multiple storage nodes. The `LeadIngestor` handled both.
- **Automated Embedding**: Data is automatically vectorized using the connected LLM Embedding model before being stored in Supabase.
- **Agent Intelligence**: The AI Agent now uses the `agent_content_dual_ingest` tool to handle both databases at once.

## 🛠 How it Works in the Workflow
1. **Input**: A real estate agent provides a link (Avito/Mubawab) or property details.
2. **Processing**: `RE Scraper` -> `Lead Formatter`.
3. **Storage**: The `Dual Storage (Sync)` node receives the structured data.
4. **Action**:
   - **NocoDB**: Data is inserted into the `leads` or `partners` table.
   - **Supabase**: Content is embedded and stored in the vector index for future RAG searches.

## 📍 Updated Components
- **Node**: `Dual Storage (Sync)` (ID: `leadIngestorNode`)
- **Tool**: `agent_content_dual_ingest`
- **Location**: Found under the **Real Estate AI** category in the Studio.

## 💡 Pro Tip
The AI Agent is now configured to use this tool automatically for both **Owners** (Listings) and **Partners** (B2B). If you want to change the target tables, you can do so in the `LeadIngestor` node settings!

---
*Created by Antigravity AI for Casablanca Real Estate Automation.*
