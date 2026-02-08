# 🚀 EasySpace AI - Complete Testing & Deployment Checklist

## 📋 Workflow Overview
**Name**: EasySpace AI Real Estate Automation  
**Purpose**: Automated AI agent for managing property rentals in Casablanca  
**User Types**: Tenants (Locataires), Owners (Propriétaires), Partners (Partenaires B2B)

---

## 🏗️ Architecture Components

### Core Nodes:
1. **Chat Input** → User message entry point
2. **Transcription** → Whisper audio-to-text conversion
3. **LiteLLM** → LLM provider (GPT-4.1-mini)
4. **LangChain Agent** → Main orchestrator with French/Darija support
5. **Redis Memory** → Conversation history storage
6. **SmartDB (NocoDB)** → Database with `properties`, `leads`, `partners` tables
7. **Supabase Vector Store** → Semantic search across all tables
8. **Lite Embedding** → text-embedding-3-small for vectors

### Real Estate AI Tools:
9. **Intent Classifier** → Identifies TENANT/OWNER/PARTNER
10. **Property Extractor** → Extracts location, budget, bedrooms criteria
11. **Real Estate Scraper** → Scrapes Avito/Mubawab links
12. **Lead Formatter** → Structures scraped data for database
13. **Carousel Builder** → Creates WhatsApp/Web property carousels
14. **Notification Node** → Sends WhatsApp/Email/SMS notifications

---

## ✅ PRE-DEPLOYMENT CHECKLIST

### 1. Environment Variables & Credentials

#### LiteLLM (Tybot Router)
- [ ] **API Key**: Verify `sk-RVApjtnPznKZ4UXosZYEOQ` is valid
- [ ] **Base URL**: Test `https://toknroutertybot.tybotflow.com/` is accessible
- [ ] **Model**: Confirm `gpt-4.1-mini` is available
- [ ] **Test Command**:
```bash
curl -X POST https://toknroutertybot.tybotflow.com/v1/chat/completions \
  -H "Authorization: Bearer sk-RVApjtnPznKZ4UXosZYEOQ" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4.1-mini","messages":[{"role":"user","content":"Test"}]}'
```

#### Redis Memory
- [ ] **Host**: Verify Redis is running at `localhost:6379`
- [ ] **Database**: Using database `0`
- [ ] **Session ID**: Configured as `user_id`
- [ ] **Test Command**:
```bash
redis-cli ping
# Should return: PONG
```

#### SmartDB (NocoDB)
- [ ] **URL**: `https://nocodb.tybot.ma` is accessible
- [ ] **API Key**: `s-m7Ue3MzAsf7AuNrzYyhL0Oz5NQoyEuT18vcI7X` is valid
- [ ] **Project**: "studio tyboo" exists
- [ ] **Tables**: Verify these exist with correct schema:
  - `properties` (mkf64o30qn37uh4)
  - `leads` (memyqo3xlmmlx4o)
  - `partners` (mt0xl7p6ggpinb4)
- [ ] **Test Command**:
```bash
curl -H "xc-token: s-m7Ue3MzAsf7AuNrzYyhL0Oz5NQoyEuT18vcI7X" \
  https://nocodb.tybot.ma/api/v1/db/meta/projects
```

#### Supabase Vector Store
- [ ] **URL**: `https://vvqbtimkusvbujuocgbg.supabase.co` is accessible
- [ ] **Service Key**: Verify the JWT token is not expired
- [ ] **Tables**: Check these exist in Supabase:
  - `properties`
  - `partners`
  - `leads`
  - `chatbot_env_configs`
  - `property_embeddings`
- [ ] **pgvector Extension**: Installed and enabled
- [ ] **RPC Function**: Verify `match_documents` function exists
- [ ] **Test Command**:
```bash
curl -H "apikey: YOUR_SERVICE_KEY" \
  -H "Authorization: Bearer YOUR_SERVICE_KEY" \
  https://vvqbtimkusvbujuocgbg.supabase.co/rest/v1/
```

#### Embedding Model
- [ ] **API Key**: Same as LiteLLM key
- [ ] **Model**: `text-embedding-3-small` is available
- [ ] **Test embedding generation**

---

## 🧪 FUNCTIONAL TESTING

### Test Scenario 1: TENANT Flow (Cherche à Louer)

#### Input Message:
```
"Salam, je cherche un F3 à Maarif budget max 8000 DH"
```

#### Expected Workflow:
1. **Chat Input** → Receives message
2. **Transcription** → Passes text through (or transcribes if audio)
3. **LangChain Agent** → Receives input
4. **Intent Classifier** → Returns "TENANT"
5. **Property Extractor** → Extracts:
   - Location: "Maarif"
   - Budget: 8000
   - Bedrooms: 3
   - Type: "Appartement"
6. **SmartDB** → Queries `properties` table with SQL filter
7. **Supabase** → Semantic search in `property_embeddings`
8. **Carousel Builder** → Creates WhatsApp carousel JSON
9. **Chat Output** → Returns French response with property listings

#### Expected Output:
```
"Salam ! J'ai trouvé X appartements F3 à Maarif dans votre budget. 
Voici les meilleures options : [carousel with images and details]"
```

#### Test Checklist:
- [ ] Intent correctly identified as TENANT
- [ ] Location extracted: "Maarif"
- [ ] Budget extracted: 8000
- [ ] Bedrooms extracted: 3
- [ ] SmartDB query returns results
- [ ] Supabase vector search returns relevant properties
- [ ] Results are combined and deduplicated
- [ ] Carousel JSON is properly formatted
- [ ] Response is in French
- [ ] Memory saves conversation for follow-ups

---

### Test Scenario 2: OWNER Flow (Veut Lister)

#### Input Message:
```
"Je veux ajouter mon appartement, voici le lien: 
https://www.avito.ma/fr/maarif/local/Local_commercial_de_luxe_214m²___Proche_de_Twin_Center_Casablanca_57465092.htm"
```

#### Expected Workflow:
1. **Chat Input** → Receives message with link
2. **LangChain Agent** → Detects URL
3. **Intent Classifier** → Returns "OWNER"
4. **Real Estate Scraper** → Scrapes Avito link, extracts:
   - Title, Price, Location, Bedrooms, Bathrooms, Surface, Description, Images
5. **Lead Formatter** → Structures data for NocoDB
6. **SmartDB** → Inserts into `leads` table
7. **Notification Node** → Sends confirmation to admin
8. **Chat Output** → Thanks owner and explains next steps

#### Expected Output:
```
"Merci ! Votre propriété a bien été enregistrée. 
Nos agents vont la vérifier et vous contacter sous 24-48h.
Référence: #LEAD-12345"
```

#### Test Checklist:
- [ ] Intent correctly identified as OWNER
- [ ] Avito/Mubawab link recognized
- [ ] Scraper extracts all fields correctly
- [ ] Lead formatter structures data properly
- [ ] SmartDB creates new record in `leads` table
- [ ] Notification sent successfully
- [ ] Response in French with professional tone
- [ ] Reference number generated

---

### Test Scenario 3: PARTNER Flow (Collaboration B2B)

#### Input Message:
```
"Bonjour, je suis agent immobilier. Je voudrais collaborer avec vous.
Nom: Ahmed Benani
Tel: +212600123456
Email: ahmed@example.com"
```

#### Expected Workflow:
1. **Chat Input** → Receives message
2. **LangChain Agent** → Processes
3. **Intent Classifier** → Returns "PARTNER"
4. **Property Extractor** → Extracts contact info
5. **SmartDB** → Inserts into `partners` table with:
   - Name, Phone, Email, Type (agent/broker/developer)
6. **Notification Node** → Alerts admin
7. **Chat Output** → Confirms registration

#### Expected Output:
```
"Merci pour votre intérêt ! Vos informations ont été enregistrées.
Notre équipe vous contactera sous 24h pour discuter de la collaboration.
Référence Partenaire: #PARTNER-678"
```

#### Test Checklist:
- [ ] Intent correctly identified as PARTNER
- [ ] Name, Phone, Email extracted
- [ ] SmartDB creates record in `partners` table
- [ ] Admin notification sent
- [ ] Professional B2B tone maintained
- [ ] Reference number provided

---

### Test Scenario 4: Audio Input (Transcription)

#### Input:
Voice note in Arabic/Darija: *"Salam, bghit chi studio f CIL budget 4000 dirham"*

#### Expected Workflow:
1. **Chat Input** → Receives audio URL
2. **Transcription Node** → Whisper converts to text
3. **LangChain Agent** → Processes in French/Darija
4. **Rest of flow** → Same as TENANT scenario

#### Test Checklist:
- [ ] Audio file accepted (MP3/OGG/M4A formats)
- [ ] Transcription accurate for Darija
- [ ] Flow continues normally after transcription
- [ ] Agent responds in appropriate language

---

### Test Scenario 5: Memory & Follow-ups

#### Conversation 1:
```
User: "Je cherche un F2 à Gauthier"
Agent: [Returns properties]
```

#### Conversation 2 (Same user_id):
```
User: "Qu'est-ce que je cherchais déjà?"
Agent: "Vous cherchiez un F2 à Gauthier. Voulez-vous voir d'autres options?"
```

#### Test Checklist:
- [ ] Redis stores conversation with `session_id = user_id`
- [ ] Agent remembers previous queries
- [ ] Personalization works across sessions
- [ ] Memory cleared on logout/timeout

---

## 🔧 INTEGRATION TESTING

### 1. SmartDB + Supabase Hybrid Search
- [ ] Both return results for same query
- [ ] Results are properly merged (no duplicates)
- [ ] Semantic search enhances SQL results
- [ ] Exact matches prioritized over semantic

### 2. Scraper → Formatter → Database Pipeline
- [ ] Test with Avito links
- [ ] Test with Mubawab links
- [ ] Handle missing fields gracefully
- [ ] Validate data before insertion

### 3. Agent Tool Calling
- [ ] Agent correctly selects tools based on intent
- [ ] Multiple tools can be chained
- [ ] Error handling when tool fails
- [ ] Retry logic for failed API calls

---

## 🚨 ERROR HANDLING TESTS

### Test Invalid Inputs:
- [ ] Empty message → Polite request for input
- [ ] Gibberish text → Clarification request
- [ ] Invalid URL → "Lien invalide, veuillez vérifier"
- [ ] Out-of-scope query → Redirect to real estate topics

### Test API Failures:
- [ ] LiteLLM timeout → Graceful error message
- [ ] Redis connection lost → Fallback to stateless mode
- [ ] NocoDB unavailable → Queue request or retry
- [ ] Supabase slow → Timeout and fall back to SQL only
- [ ] Scraper blocked → Manual entry prompt

### Test Data Validation:
- [ ] Budget non-numeric → Ask for clarification
- [ ] Location not in Casablanca → Suggest alternatives
- [ ] Phone number invalid → Validation message
- [ ] Email malformed → Request correction

---

## 📊 PERFORMANCE TESTING

### Response Time Targets:
- [ ] Simple query (TENANT search): < 3 seconds
- [ ] Scraping (OWNER): < 10 seconds
- [ ] Complex multi-tool chain: < 15 seconds

### Load Testing:
- [ ] 10 concurrent users → Stable
- [ ] 50 concurrent users → Check for bottlenecks
- [ ] 100+ concurrent users → Scale strategy needed

### Resource Monitoring:
- [ ] Redis memory usage
- [ ] NocoDB connection pool
- [ ] Supabase query performance
- [ ] LLM API rate limits

---

## 🌍 PRODUCTION DEPLOYMENT

### 1. Server Setup
- [ ] Deploy backend on production server
- [ ] Configure environment variables
- [ ] Set up reverse proxy (Nginx/Caddy)
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS for production domains

### 2. Database Migration
- [ ] Backup existing data
- [ ] Run production NocoDB migrations
- [ ] Populate Supabase with initial embeddings
- [ ] Set up automated backups (daily)

### 3. Monitoring & Logging
- [ ] Set up application logs
- [ ] Configure error tracking (Sentry/Rollbar)
- [ ] Set up uptime monitoring
- [ ] Create dashboard for key metrics
- [ ] Alert system for critical errors

### 4. Security Hardening
- [ ] Rotate all API keys for production
- [ ] Implement rate limiting
- [ ] Add input sanitization
- [ ] Set up WAF if public-facing
- [ ] Regular security audits

---

## 📱 WHATSAPP INTEGRATION (If Applicable)

### Prerequisites:
- [ ] WhatsApp Business API account
- [ ] Webhook configured for incoming messages
- [ ] Media download capability for audio/images
- [ ] Carousel template approved by Meta

### Testing:
- [ ] Send text message → Workflow triggers
- [ ] Send voice note → Transcribed correctly
- [ ] Receive carousel → Displays properly
- [ ] Buttons/Quick replies work
- [ ] Session management per phone number

---

## 📝 POST-DEPLOYMENT VALIDATION

### Week 1: Monitoring
- [ ] Track all error rates
- [ ] Monitor API costs (LiteLLM usage)
- [ ] Check Redis memory growth
- [ ] Review user feedback
- [ ] Identify common failure points

### Week 2-4: Optimization
- [ ] Optimize slow queries
- [ ] Add missing error handlers
- [ ] Improve prompt engineering
- [ ] A/B test different responses
- [ ] Fine-tune ranking algorithms

---

## 🎯 SUCCESS METRICS

### KPIs to Track:
- **Response Accuracy**: > 90% correct intent classification
- **Response Time**: < 5 seconds average
- **User Satisfaction**: > 4/5 rating
- **Conversion Rate**: % of tenants who book visits
- **Lead Quality**: % of owner listings that convert
- **Uptime**: > 99.5%
- **Cost per Conversation**: Target < $0.05

---

## 📞 SUPPORT & MAINTENANCE

### Daily:
- [ ] Check error logs
- [ ] Monitor API rate limits
- [ ] Review unusual patterns

### Weekly:
- [ ] Database cleanup
- [ ] Update property embeddings
- [ ] Review and improve responses

### Monthly:
- [ ] Performance audit
- [ ] Security updates
- [ ] Feature enhancements
- [ ] User feedback review

---

## 🔄 ROLLBACK PLAN

### If Critical Issues Arise:
1. **Stop workflow execution**
2. **Redirect users to fallback (manual support)**
3. **Identify root cause**
4. **Apply hotfix or rollback to previous version**
5. **Test thoroughly before re-deployment**

### Backup Strategy:
- [ ] Code: Git version control
- [ ] Database: Daily snapshots
- [ ] Configuration: Version controlled .env
- [ ] Logs: Retained for 30 days

---

## ✅ FINAL SIGN-OFF

Before going live, confirm:
- [ ] All test scenarios passed
- [ ] Performance meets targets
- [ ] Error handling comprehensive
- [ ] Monitoring in place
- [ ] Team trained on troubleshooting
- [ ] Documentation complete
- [ ] Stakeholder approval obtained

---

**Deployment Date**: _____________  
**Deployed By**: _____________  
**Approved By**: _____________  

**Status**: ⬜ Ready | ⬜ Needs Work | ⬜ LIVE

---

*Document Version: 1.0*  
*Last Updated: 2026-02-07*
