# 🔗 Guide de Connexion - Architecture Logique (If/Else)

Ce guide explique comment câbler précisément votre projet en utilisant les **Nœuds de Condition** pour créer un workflow propre et professionnel.

> **📘 Port Reference**: Pour une documentation complète des ports de chaque nœud, consultez `NODE_PORT_REFERENCE.md`

---

## 🏗️ Structure du Workflow

Le secret d'un bon workflow Tyboo est la séparation des tâches. Ne connectez pas tout à un seul agent. Suivez ces sections :

### 📡 Phase 1 : Entrée & Identification
1. **Chat Input** ➡ **Transcription Node** (audio_url)
2. **Transcription Node** (text) ➡ **Intent Classifier** (user_message)

---

### 🚦 Phase 2 : Le Branchement Logique (Le cœur du n8n-style)
Ici, nous créons la cascade de conditions.

#### 1. Branche Tenant (Recherche)
- **Nœud If-Else (A)** (Label: "If-Else") :
  - **Match Text** : `TENANT`
  - **Operator** : `equals`
  - **Input Text** (`input_text`) : Connectez la sortie `intent` de l'Intent Classifier.
- **Sortie TRUE** ➡ Dirigez vers l'étape **[Module Recherche]**.

#### 2. Branche Owner (Listing)
- **Nœud If-Else (B)** :
  - **Match Text** : `OWNER`
  - **Operator** : `equals`
  - **Input Text** (`input_text`) : Connectez la sortie **FALSE** du nœud Condition (A).
- **Sortie TRUE** ➡ Dirigez vers l'étape **[Module Listing]**.

#### 3. Branche Else (Support)
- **Sortie FALSE** du nœud Condition (B) ➡ Dirigez vers l'étape **[Module Support]**.

---

### 📦 Phase 3 : Les Modules Spécialisés

#### [Module Recherche]
**Nœuds requis**:
1. **Property Extractor** - Reçoit le texte original de la Transcription
2. **Universal Agent** (ID: `universalAgent` ou `langchainAgent`)
   - **Configuration**:
     - `agent_pattern`: `planner` (pour raisonnement complexe)
     - `system_prompt`: "You are a property search assistant..."
   
   - **Connexions** (6 ports d'entrée):
     - `input_data` ← Sortie du Property Extractor
     - `llm` ← LiteLLM node
     - `tools` ← Supabase Vector Store (pour recherche RAG)
     - `tools` ← SmartDB (pour recherche SQL)
     - `memory` ← Memory Node (optionnel)
     - `system_prompt` ← (configuré dans le nœud)

3. **Carousel Builder** - Reçoit la sortie `output` de l'agent
4. **Chat Output** - Affiche le carousel

**Flux complet**:
```
Property Extractor → Universal Agent (input_data)
LiteLLM → Universal Agent (llm)
Supabase → Universal Agent (tools)
SmartDB → Universal Agent (tools)
Universal Agent (output) → Carousel Builder → Chat Output
```

#### [Module Listing]
**Nœuds requis**:
1. **RE Scraper** - Reçoit le texte original (URL) de la Transcription
2. **Lead Formatter** - Reçoit la sortie `markdown` du Scraper
3. **Lead Ingestor**:
   - **Connexions critiques**:
     - `input_data` ← Lead Formatter (`formatted_lead`)
     - `embedding` ← **Embedding Model** (OBLIGATOIRE pour Supabase)
   - Sauvegarde automatiquement dans NocoDB ET Supabase
4. **Chat Output** - Affiche la confirmation

**Flux complet**:
```
RE Scraper → Lead Formatter → Lead Ingestor (input_data)
Embedding Model → Lead Ingestor (embedding)
Lead Ingestor (status) → Chat Output
```

#### [Module Support]
**Nœuds requis**:
1. **Universal Agent**
   - **Configuration**:
     - `agent_pattern`: `simple` (LCEL pour vitesse maximale)
     - `system_prompt`: "You are a helpful support assistant..."
   
   - **Connexions** (3 ports minimum):
     - `input_data` ← Transcription (text)
     - `llm` ← LiteLLM
     - `memory` ← Memory Node (pour contexte conversationnel)

2. **Chat Output** - Affiche la réponse

**Flux complet**:
```
Transcription → Universal Agent (input_data)
LiteLLM → Universal Agent (llm)
Memory Node → Universal Agent (memory)
Universal Agent (output) → Chat Output
```

---

## 🔧 Paramètres Cruciaux des Nœuds

### 🤖 Universal Agent (Ports standardisés)
Le nœud Universal Agent possède maintenant **6 ports d'entrée** bien définis:

| Port | Type | Requis | Description |
|------|------|--------|-------------|
| `input_data` | handle | ✅ Oui | Message utilisateur |
| `llm` | handle | ⚠️ Recommandé | Modèle de langage |
| `tools` | handle | ❌ Non | Outils (peut connecter plusieurs) |
| `memory` | handle | ❌ Non | Historique conversationnel |
| `system_prompt` | textarea | ❌ Non | Instructions personnalisées |
| `agent_pattern` | dropdown | ❌ Non | simple/standard/planner |

**Patterns disponibles**:
- `simple`: LCEL Chain (FAQ rapide, classification)
- `standard`: Tool-Calling Agent (recherche, booking)
- `planner`: ReAct Agent (workflows complexes multi-étapes)

### 💾 Lead Ingestor (Dual Sync)
**⚠️ ATTENTION**: Ce nœud nécessite OBLIGATOIREMENT un **Embedding Model** connecté au port `embedding`. Sans lui, l'ingestion Supabase échouera.

**Ports critiques**:
- `input_data` ← Lead Formatter
- `embedding` ← **Embedding Model** (text-embedding-3-small recommandé)

### 🔍 Intent Classifier
**Sortie**: Le port `intent` retourne une chaîne de caractères:
- `"TENANT"` - Utilisateur cherche à louer
- `"OWNER"` - Utilisateur veut lister un bien
- `"GENERAL"` - Question générale

Utilisez cette sortie directement dans les nœuds **Condition**.

---

## 🎯 Règles de Connexion des Ports

### 1. Types Compatibles
Les ports doivent avoir des types compatibles:
- `[Text]` peut se connecter à `[Text, Message]`
- `[Tool]` peut se connecter au port `tools` d'un agent
- `[LLM]` peut se connecter au port `llm` d'un agent
- `[Memory]` peut se connecter au port `memory` d'un agent

### 2. Connexions Multiples
Certains ports acceptent **plusieurs connexions**:
- Le port `tools` d'un agent peut recevoir plusieurs nœuds d'outils
- Chaque outil sera automatiquement ajouté à la liste disponible pour l'agent

### 3. Ports Obligatoires vs Optionnels
- ✅ **Obligatoire**: `input_data` (sur tous les agents)
- ⚠️ **Fortement recommandé**: `llm` (sans LLM, l'agent ne peut pas fonctionner)
- ❌ **Optionnel**: `tools`, `memory`, `system_prompt`

---

## ✅ Checklist Finale
1. **Le cascade de Conditions** : A (True) -> Recherche, A (False) -> B. B (True) -> Listing, B (False) -> Support.
2. **Les ports Universal Agent** : Vérifiez que `input_data` ET `llm` sont connectés au minimum.
3. **L'Embedding Model** : Si vous utilisez Lead Ingestor ou Supabase, connectez TOUJOURS un Embedding Model.
4. **Les Clefs API** : Vérifiez LiteLLM, Supabase et NocoDB dans chaque nœud.
5. **Le System Prompt** : Chaque branche de l'Universal Agent doit avoir un prompt spécifique (Instructions Recherche vs Instructions Support).

---

## 🔍 Diagnostic des Problèmes de Connexion

### Erreur: "No LLM connected to Agent"
**Cause**: Le port `llm` n'est pas connecté.
**Solution**: Connectez un nœud LiteLLM (ou OpenAI/Anthropic) au port `llm` de l'agent.

### Erreur: "Failed to load mapped node 'openai_chat'"
**Cause**: Problème d'encodage ou nœud manquant dans le registre.
**Solution**: Utilisez `liteLLM` au lieu de `openai_chat` directement.

### Erreur: "Embedding required for Supabase"
**Cause**: Lead Ingestor ou Supabase Vector Store sans Embedding Model.
**Solution**: Connectez un nœud `liteEmbedding` au port `embedding`.

---

**Votre workflow est maintenant "n8n-ready" : Propre, logique et ultra-performant ! 🚀**

**Dernière mise à jour**: 2026-02-08 (Post-Standardisation des Ports)
