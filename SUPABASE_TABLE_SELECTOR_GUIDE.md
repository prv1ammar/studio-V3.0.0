# Supabase Table Selector - User Guide

## ✅ Feature Implemented

The Supabase node now automatically fetches and displays available tables from your Supabase instance in a **multiselect dropdown menu**, allowing you to:
- Select **all tables** at once with a single click
- Select **multiple specific tables** by holding Ctrl (Windows/Linux) or Cmd (Mac)
- Select **a single table**

No more manual typing required! 🎉

## 🎯 How It Works

### Step-by-Step Instructions:

1. **Add Supabase Node to Canvas**
   - Drag the "Supabase" node from the sidebar under the "Supabase" category
   - Click on the node to open the inspector panel on the right

2. **Configure Credentials**
   - Enter your **Supabase URL** (e.g., `https://your-project.supabase.co`)
   - Enter your **Supabase Service Key** (from your Supabase project settings)

3. **Select Tables from Multiselect Dropdown**
   - Once both URL and Service Key are entered, the system automatically fetches available tables
   - The **Table Name(s)** field will now show as a multiselect dropdown menu
   
   **Three Selection Options:**
   - **🌐 All Tables**: Click this option to select all available tables at once
   - **Multiple Tables**: Hold `Ctrl` (Windows/Linux) or `Cmd` (Mac) and click multiple tables
   - **Single Table**: Click on one specific table

### What Changed:

- **Before**: You had to manually type the table name
- **After**: Tables are automatically fetched and displayed in a multiselect dropdown for easy selection
- **New**: "🌐 All Tables" option appears at the top of the list for quick selection of all tables

## 🔧 Technical Details

### Backend API Endpoint:
```
GET /nodes/supabase/tables?supabase_url={url}&supabase_key={key}
```

Returns:
```json
{
  "tables": [
    {"label": "users", "value": "users"},
    {"label": "documents", "value": "documents"},
    {"label": "embeddings", "value": "embeddings"}
  ]
}
```

### Frontend Auto-Discovery:
The frontend automatically calls the API when both `supabase_url` and `supabase_service_key` fields are filled. It then:
1. Adds a `{"label": "🌐 All Tables", "value": "all"}` option at the top
2. Appends the actual table list from Supabase
3. Updates the multiselect dropdown in real-time

### Table Selection Handling:
- **"all" value**: The backend fetches all available tables dynamically
- **Array of tables**: Each table is processed individually
- **Multiple tables**: The node creates separate search tools for each selected table

### Table Discovery Method:
The system uses Supabase's PostgREST OpenAPI introspection to fetch table definitions automatically:
- Queries: `https://your-project.supabase.co/rest/v1/`
- Parses the OpenAPI spec to extract table names
- Filters out RPC functions and system tables

## 🐛 Troubleshooting

### Dropdown Shows Empty:
1. Verify your Supabase URL is correct
2. Check that your Service Key has the necessary permissions
3. Ensure PostgREST API is accessible (check Supabase dashboard)
4. Check browser console for error messages

### Tables Not Appearing:
1. Make sure you have tables created in your Supabase project
2. Verify the Service Key has read access to the schema
3. Check that PostgREST introspection is enabled (it's on by default)

## 📝 Notes

- The multiselect dropdown is populated automatically after you enter both URL and Service Key
- "🌐 All Tables" is always the first option for convenience
- To select multiple specific tables: Hold `Ctrl` (Windows/Linux) or `Cmd` (Mac) while clicking
- To deselect a table: Click it again while holding `Ctrl`/`Cmd`
- If you select "All Tables", individual table selections are ignored
- There's no manual "Refresh" button needed - it updates automatically when credentials change
- Only public schema tables are shown by default
- System tables and RPC functions are filtered out automatically

---

**Files Modified**: 
- `backend/data/node_library.json` - Changed `table_name` to multiselect type
- `studio/src/App.jsx` - Added "All Tables" option to fetched list

**Date**: 2026-02-07
