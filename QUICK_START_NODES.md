# 🚀 Quick Start: Using Standardized Nodes

## For Users

### Finding the Right Node

**All 384 nodes are organized into 28 categories:**

```
Most Popular Categories:
├─ Tools & Utilities (106 nodes) - LangChain utilities, API integrations
├─ Models & AI Providers (47 nodes) - LLMs, Embeddings
├─ Vector Stores & Databases (43 nodes) - Supabase, Pinecone, Chroma
├─ Search & Scraping (37 nodes) - Web scrapers, Search APIs
├─ Data Processing (31 nodes) - Parsers, Splitters
├─ AI Services & Agents (26 nodes) - Universal Agent, CrewAI
└─ Tyboo (5 nodes) - LiteLLM, SmartDB, Universal Agent
```

### Understanding Port Types

When connecting nodes, match these types:

| If you see... | You can connect... |
|---------------|-------------------|
| `[LLM]` | LiteLLM, OpenAI, Anthropic, Claude |
| `[Tool]` | SmartDB, Supabase, Custom APIs, Web Scrapers |
| `[Memory]` | Redis Memory, Mem0, Chat Memory |
| `[Embeddings]` | OpenAI Embeddings, Cohere, LiteLLM Embeddings |
| `[Text, Message]` | Chat Input, Text processors, Agent outputs |
| `[Data]` | Parsers, Processors, Database results |
| `[VectorStore]` | Pinecone, Chroma, FAISS, Supabase |

### Building Your First Workflow

**Example 1: Simple Chat**
```
Chat Input → Universal Agent (input_data)
LiteLLM → Universal Agent (llm)
Universal Agent (output) → Chat Output
```

**Example 2: RAG Search**
```
Chat Input → Universal Agent (input_data)
LiteLLM → Universal Agent (llm)
Supabase Vector Store → Universal Agent (tools)
Embedding Model → Supabase (embedding)
Universal Agent (output) → Chat Output
```

**Example 3: Conditional Routing**
```
Chat Input → Intent Classifier
Intent Classifier → Condition Node
  ├─ TRUE → Agent A → Output
  └─ FALSE → Agent B → Output
```

---

## For Developers

### Adding a New Node

**1. Define the Node Structure**
```json
{
  "id": "my_custom_node",
  "name": "MyCustomNode",
  "label": "My Custom Node",
  "description": "Clear description of what this node does",
  "category": "Custom Components",
  "icon": "Zap",
  "color": "#8b5cf6",
  "inputs": [...],
  "outputs": [...],
  "base_classes": ["Component"],
  "beta": false,
  "documentation": ""
}
```

**2. Define Inputs (Follow Standards)**
```json
{
  "name": "input_data",
  "display_name": "Input Data",
  "type": "handle",
  "required": true,
  "description": "The data to process",
  "types": ["Text", "Data"]
}
```

**3. Define Outputs (Always Include Types)**
```json
{
  "name": "output",
  "display_name": "Processed Output",
  "types": ["Data", "Text"]
}
```

### Port Type Guidelines

**Use these standard types:**
- `LanguageModel`, `LLM` - For LLM providers
- `Tool` - For agent tools
- `Memory` - For conversation history
- `Embeddings` - For embedding models
- `Data` - For generic data objects
- `Text`, `Message` - For text content
- `VectorStore` - For vector databases
- `Agent` - For agent instances
- `Any` - Only as last resort

**Avoid:**
- Custom type names without documentation
- Missing type definitions
- Overly specific types that limit reusability

### Validation Checklist

Before adding a node to the library:
- [ ] Node has unique `id`
- [ ] Node has clear `description`
- [ ] All handle inputs have `types` array
- [ ] All outputs have `types` array
- [ ] `required` flag is set on all inputs
- [ ] Node is in appropriate category
- [ ] Icon and color are set
- [ ] No duplicate IDs in library

### Running Validation

```bash
# Audit the entire library
python audit_all_nodes.py

# Check for specific issues
python -c "import json; lib = json.load(open('backend/data/node_library.json')); print([n['id'] for cat in lib.values() for n in cat if not n.get('description')])"
```

---

## Common Patterns

### Pattern 1: Agent with Tools
```
Agent Node:
  - input_data (handle, required) [Text, Message]
  - llm (handle) [LLM]
  - tools (handle) [Tool] ← Can connect multiple
  - memory (handle) [Memory]
  - output (output) [Text, Message]
```

### Pattern 2: Vector Store
```
Vector Store Node:
  - embedding (handle, required) [Embeddings]
  - ingest_data (handle) [Data]
  - search_query (text) 
  - search_results (output) [Data]
```

### Pattern 3: Data Processor
```
Processor Node:
  - input_data (handle, required) [Data, Text]
  - config_param (text/number/dropdown)
  - output (output) [Data]
```

### Pattern 4: Conditional Router
```
Router Node:
  - input_message (handle, required) [Message, Text]
  - match_text (text)
  - operator (dropdown)
  - true_result (output) [Message]
  - false_result (output) [Message]
```

---

## Troubleshooting

### "Cannot connect nodes"
**Cause**: Type mismatch
**Solution**: Check port types. Use `[Any]` as intermediate if needed.

### "Node not found in registry"
**Cause**: Node ID doesn't exist or typo
**Solution**: Check `node_library.json` for exact ID.

### "Missing required input"
**Cause**: Required port not connected
**Solution**: Connect all ports marked `required: true`.

### "Type validation failed"
**Cause**: Connected incompatible types
**Solution**: Review type compatibility in `NODE_PORT_REFERENCE.md`.

---

## Resources

- **Full Port Reference**: `NODE_PORT_REFERENCE.md`
- **Visual Wiring Guide**: `VISUAL_PORT_GUIDE.md`
- **Connection Guide**: `detailed_connection_guide.md`
- **Standardization Report**: `NODE_STANDARDIZATION_REPORT.md`
- **Architecture Guide**: `architecture_n8n_style.md`

---

**Version**: 3.0 (Production)
**Last Updated**: 2026-02-08
