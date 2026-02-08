# 🚀 EasySpace AI - Quick Testing Guide

## Prerequisites

Before testing, ensure you have:
- ✅ Backend server running on `localhost:8000`
- ✅ Frontend server running on `localhost:5173` (or configured port)
- ✅ Redis server running on `localhost:6379`
- ✅ Python environment with required packages

## Installation

1. **Install Python dependencies** (if not already installed):
```bash
pip install requests redis
```

2. **Verify servers are running**:

**Backend** (Terminal 1):
```bash
cd c:\Users\PC\Downloads\studio_final-main
.\venv\Scripts\activate
python -m uvicorn backend.app.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend** (Terminal 2):
```bash
cd c:\Users\PC\Downloads\studio_final-main\studio
npm run dev
```

**Redis** (Terminal 3):
```bash
redis-server
# Or if installed as service on Windows: net start Redis
```

## Running the Tests

### Option 1: Automated Test Script

Run the comprehensive automated test:

```bash
python test_easyspace_workflow.py
```

**Expected Output:**
```
======================================================================
  EasySpace AI - Workflow Testing Suite
======================================================================

🧪 Testing: LiteLLM Connection & Model
✅ LiteLLM API responding (Status: 200)
✅ Model 'gpt-4.1-mini' is available and responding

🧪 Testing: Redis Connection
✅ Redis is running and responding to PING
✅ Redis read/write operations working

🧪 Testing: NocoDB (SmartDB) Connection
✅ NocoDB API accessible (88 projects found)
✅ Project 'studio tyboo' found
✅ Tables accessible: properties, leads, partners
  ✓ Table 'properties' exists
  ✓ Table 'leads' exists
  ✓ Table 'partners' exists

🧪 Testing: Supabase Vector Store Connection
✅ Supabase PostgREST API accessible
✅ Found 6 tables/views
  ✓ Table 'properties' exists
  ✓ Table 'leads' exists
  ✓ Table 'partners' exists
  ✓ Table 'property_embeddings' exists

🧪 Testing: Backend API Endpoints
✅ Backend API is running
✅ Supabase tables endpoint working (6 tables)

======================================================================
  Test Summary
======================================================================

  LiteLLM................................................... PASS
  Redis..................................................... PASS
  NocoDB.................................................... PASS
  Supabase.................................................. PASS
  Backend API............................................... PASS
  TENANT Workflow........................................... PASS
  OWNER Workflow............................................ PASS

Total: 7/7 tests passed

🎉 All tests passed! Workflow is ready for deployment.
```

### Option 2: Manual Component Testing

#### Test 1: LiteLLM API
```bash
curl -X POST https://toknroutertybot.tybotflow.com/v1/chat/completions \
  -H "Authorization: Bearer sk-RVApjtnPznKZ4UXosZYEOQ" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4.1-mini","messages":[{"role":"user","content":"Bonjour"}],"max_tokens":50}'
```

#### Test 2: Redis
```bash
redis-cli ping
# Should return: PONG
```

#### Test 3: NocoDB
```bash
curl -H "xc-token: s-m7Ue3MzAsf7AuNrzYyhL0Oz5NQoyEuT18vcI7X" \
  https://nocodb.tybot.ma/api/v1/db/meta/projects
```

#### Test 4: Supabase
```bash
curl -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  https://vvqbtimkusvbujuocgbg.supabase.co/rest/v1/
```

#### Test 5: Backend Supabase Endpoint
```bash
curl "http://localhost:8000/nodes/supabase/tables?supabase_url=https://vvqbtimkusvbujuocgbg.supabase.co&supabase_key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Testing the Workflow in the UI

### 1. Load the Workflow

1. Open the frontend: `http://localhost:5173`
2. In the Studio interface, **import the workflow**:
   - Click on **File** → **Import Workflow**
   - Select `workflow-1770423902690.json`
   - The workflow canvas should populate with all nodes

### 2. Verify Node Connections

Check that all connections are intact:
- **Chat Input** → **Transcription** → **LangChain Agent** → **Chat Output**
- **LiteLLM** → **LangChain Agent** (llm)
- **Redis Memory** → **LangChain Agent** (memory)
- **SmartDB** → **LangChain Agent** (tools)
- **Supabase** → **LangChain Agent** (tools)
- **Embedding** → **Supabase** (embedding)
- All RE AI tools → **LangChain Agent** (tools)

### 3. Test Scenario 1: TENANT (Property Search)

1. **Click on the Chat Icon** at the bottom
2. **Send a message**:
   ```
   Salam, je cherche un F3 à Maarif budget max 8000 DH
   ```

3. **Expected Response**:
   ```
   Salam ! J'ai trouvé X appartements F3 à Maarif dans votre budget.
   Voici les meilleures options : [carousel with properties]
   ```

4. **Verify**:
   - ✅ Intent classified as TENANT
   - ✅ Location extracted: Maarif
   - ✅ Budget extracted: 8000
   - ✅ Bedrooms extracted: 3
   - ✅ Properties returned from SmartDB
   - ✅ Semantic search from Supabase
   - ✅ Carousel built correctly
   - ✅ Response in French

### 4. Test Scenario 2: OWNER (List Property)

1. **Send a message with an Avito link**:
   ```
   Je veux ajouter mon appartement:
   https://www.avito.ma/fr/maarif/local/Local_commercial_de_luxe_214m²___Proche_de_Twin_Center_Casablanca_57465092.htm
   ```

2. **Expected Response**:
   ```
   Merci ! Votre propriété a bien été enregistrée.
   Nos agents vont la vérifier et vous contacter sous 24-48h.
   Référence: #LEAD-XXXXX
   ```

3. **Verify**:
   - ✅ Intent classified as OWNER
   - ✅ URL recognized and scraped
   - ✅ Data formatted correctly
   - ✅ Inserted into `leads` table in NocoDB
   - ✅ Notification sent
   - ✅ Confirmation with reference number

### 5. Test Scenario 3: PARTNER (B2B Collaboration)

1. **Send a partner inquiry**:
   ```
   Bonjour, je suis agent immobilier et je voudrais collaborer.
   Nom: Ahmed Benani
   Tel: +212600123456
   Email: ahmed@example.com
   ```

2. **Expected Response**:
   ```
   Merci pour votre intérêt ! Vos informations ont été enregistrées.
   Notre équipe vous contactera sous 24h pour discuter de la collaboration.
   Référence Partenaire: #PARTNER-XXX
   ```

3. **Verify**:
   - ✅ Intent classified as PARTNER
   - ✅ Contact details extracted
   - ✅ Inserted into `partners` table
   - ✅ Admin notification sent
   - ✅ Professional B2B tone

### 6. Test Scenario 4: Audio Transcription

1. **Upload a voice note** (if audio upload is supported)
2. **Voice content** (in Darija): *"Bghit chi studio f CIL budget 4000 dirham"*
3. **Expected**: Should transcribe and process as TENANT search

4. **Verify**:
   - ✅ Audio accepted and transcribed
   - ✅ Darija/Arabic handled correctly
   - ✅ Workflow continues normally

### 7. Test Memory (Follow-up Conversation)

**Message 1**:
```
Je cherche un F2 à Gauthier
```

**Message 2** (same session):
```
Qu'est-ce que je cherchais déjà ?
```

**Expected Response**:
```
Vous cherchiez un F2 à Gauthier. Voulez-vous voir d'autres options ?
```

**Verify**:
- ✅ Redis stores conversation
- ✅ Agent remembers context
- ✅ Personalized response

---

## Monitoring During Tests

### Backend Logs
Watch for errors in the backend terminal:
```bash
# Should show:
INFO:     127.0.0.1:XXXX - "POST /execute HTTP/1.1" 200 OK
[Workflow execution logs...]
```

### Frontend Console
Open browser DevTools (F12):
- **Console**: Look for errors or warnings
- **Network**: Verify API calls succeed (Status 200)

### Redis Monitor
```bash
redis-cli MONITOR
# Watch real-time commands
```

---

## Troubleshooting

### ❌ LiteLLM Connection Failed
- **Check**: API key is valid
- **Check**: Base URL is accessible
- **Fix**: Update key in workflow node or contact admin

### ❌ Redis Connection Failed
- **Check**: Redis is running (`redis-cli ping`)
- **Fix**: Start Redis: `redis-server` or `net start Redis`

### ❌ NocoDB Tables Not Found
- **Check**: Project "studio tyboo" exists
- **Check**: Tables `properties`, `leads`, `partners` exist
- **Fix**: Create tables or update project selection

### ❌ Supabase Vector Search Failed
- **Check**: `property_embeddings` table exists
- **Check**: pgvector extension is installed
- **Check**: Service key has permissions
- **Fix**: Run Supabase migrations

### ❌ Workflow Execution Timeout
- **Check**: All services responding
- **Check**: Network connectivity
- **Increase**: Timeout settings in configuration

### ❌ Intent Classification Wrong
- **Check**: System prompt in LangChain Agent
- **Fix**: Improve prompt or add examples

---

## Performance Benchmarks

After testing, record these metrics:

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| TENANT Query Response Time | < 3s | ___s | ✅/❌ |
| OWNER Scraping Time | < 10s | ___s | ✅/❌ |
| PARTNER Registration | < 2s | ___s | ✅/❌ |
| Memory Retrieval | < 1s | ___s | ✅/❌ |
| LiteLLM Latency | < 2s | ___s | ✅/❌ |
| Database Query | < 500ms | ___ms | ✅/❌ |
| Vector Search | < 1s | ___s | ✅/❌ |

---

## Next Steps After Testing

If all tests pass:

1. ✅ **Mark checklist items** in `EASYSPACE_TESTING_DEPLOYMENT_CHECKLIST.md`
2. ✅ **Document any issues** found and how they were resolved
3. ✅ **Conduct load testing** with multiple concurrent users
4. ✅ **Review security** (API key rotation, input validation)
5. ✅ **Set up monitoring** (error tracking, uptime monitoring)
6. ✅ **Prepare deployment** (production environment variables)
7. ✅ **Train support team** on troubleshooting
8. ✅ **Get stakeholder approval** for production deployment

---

## Support & Questions

If you encounter issues:
1. Check logs (backend terminal)
2. Review error messages in browser console
3. Verify all services are running
4. Consult the detailed checklist: `EASYSPACE_TESTING_DEPLOYMENT_CHECKLIST.md`

---

**Good luck with testing! 🚀**
