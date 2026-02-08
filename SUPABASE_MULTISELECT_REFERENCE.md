## Supabase Table Selection - Quick Reference

### Selection Options

```
┌─────────────────────────────────────┐
│  Table Name(s) ▼                    │
├─────────────────────────────────────┤
│  ☑ 🌐 All Tables                    │  ← Select this for all tables
│  ☐ users                            │  
│  ☐ documents                        │
│  ☐ embeddings                       │
│  ☐ vectors                          │
│  ☐ chat_history                     │
└─────────────────────────────────────┘
```

### Usage Examples

#### Example 1: Select All Tables
- Click on "🌐 All Tables"
- Backend will automatically fetch and use all available tables

#### Example 2: Select Multiple Specific Tables
- Hold `Ctrl` (Windows/Linux) or `Cmd` (Mac)
- Click on "users"
- Keep holding and click on "documents"
- Keep holding and click on "embeddings"
- Release the key

Result: Only users, documents, and embeddings will be used

#### Example 3: Select Single Table
- Click on "documents"

Result: Only the documents table will be used

### How the Backend Handles Selections

```javascript
// If you select "All Tables" (value: "all")
table_name = ["all"]
→ Backend fetches all: ["users", "documents", "embeddings", "vectors", "chat_history"]

// If you select specific tables
table_name = ["users", "documents"]
→ Backend uses exactly: ["users", "documents"]

// If you select just one
table_name = ["documents"]
→ Backend uses: ["documents"]
```

### Multi-Table Search Behavior

When multiple tables are selected, the Supabase node creates **separate search tools** for each table:

```
Selected: ["users", "documents", "chat_history"]

Backend creates 3 tools:
├── search_supabase_users
├── search_supabase_documents
└── search_supabase_chat_history
```

An AI agent can then use any of these tools to search the respective tables!

### Tips & Tricks

✅ **DO**:
- Select "All Tables" if you want to search across your entire Supabase instance
- Use multiple specific tables when you know exactly which data sources you need
- Hold Ctrl/Cmd to select multiple tables

❌ **DON'T**:
- Don't select "All Tables" AND specific tables (All Tables takes precedence)
- Don't forget to hold Ctrl/Cmd when selecting multiple (otherwise it replaces the selection)
