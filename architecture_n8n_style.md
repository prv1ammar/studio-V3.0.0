# 🏗️ Architecture EasySpace AI - Router-First Design (n8n Style)

## 🎯 Objectif
Passer d'une architecture "Mega Agent" (où l'agent fait tout) à une architecture **déterministe et visuelle**. 

Le workflow utilise désormais des **nœuds de condition** explicites pour router l'utilisateur vers des sous-systèmes spécialisés. C'est plus propre, plus rapide et beaucoup plus facile à débugger.

---

## 🧠 Architecture Logique

```
┌─────────────────────────────────────────────────────────────┐
│                    CHAT INPUT (WhatsApp/Web)                │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  TRANSCRIPTION (Audio ➡️ Texte)              │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│               INTENT CLASSIFIER (Le Dispatcher)             │
│    Détermine l'intention : TENANT, OWNER ou GENERAL         │
└──────────────────────┬──────────────────────────────────────┘
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
┌──────────────┐               ┌──────────────┐
│  CONDITION   │               │  CONDITION   │
│ (Is Tenant?) │──[FALSE]─────▶│ (Is Owner?)  │──[FALSE]───┐
└──────┬───────┘               └──────┬───────┘            │
       │                              │                    │
    [TRUE]                         [TRUE]               [DEFAULT]
       ▼                              ▼                    ▼
┌──────────────┐               ┌──────────────┐    ┌──────────────┐
│ WORKFLOW 1   │               │ WORKFLOW 2   │    │ WORKFLOW 3   │
│ (RECHERCHE)  │               │ (LISTING)    │    │ (SUPPORT)    │
└──────────────┘               └──────────────┘    └──────────────┘
```

---

## 📦 Les 3 Bio-Systèmes du Workflow

### 🔍 1. Système de Recherche (Tenant)
Utilisé quand un client cherche un bien.
- **Extracteur** : Récupère Location, Budget, Chambres.
- **Universal Agent (Tier 2/3)** : Utilise l'outil `Supabase Store` pour la recherche RAG.
- **Carousel** : Affiche les résultats en format WhatsApp.

### 📝 2. Système de Listing (Owner)
Utilisé quand un propriétaire veut lister un bien.
- **Scraper** : Extrait les infos d'un lien Avito/Mubawab.
- **Formatter** : Structure les données pour la base de données.
- **Ingestor** : Sauvegarde dans NocoDB ET Supabase simultanément.

### 💬 3. Système Support (General)
Le mode "par défaut" pour les questions générales.
- **Universal Agent (Tier 1)** : Chat direct via LCEL pour une réponse ultra-rapide.

---

## 🛠️ Configuration des Nœuds Clés

### 1. Intent Classifier (The Router)
- **ID**: `intentClassifierNode`
- **Output**: `intent`
- Ce nœud définit la variable qui sera testée par les nœuds de condition suivants.

### 2. Les Conditions (Router Nodes)
- **Condition A (Tenant Check)**:
  - Input: `intent`
  - Logic: `equals` -> `TENANT`
- **Condition B (Owner Check)**:
  - Input: `intent`
  - Logic: `equals` -> `OWNER`

### 3. Universal Agent (Power-Up)
N'utilisez plus le `langchainAgent` générique. Utilisez le **Universal Agent** :
- **Pattern "Planner"** pour la recherche (besoin de réflexion).
- **Pattern "Simple"** pour le support (vitesse).

---

## 🎨 Workflow Visuel Complet

1. **ENTRÉE**: `Chat Input` ➡️ `Transcription`
2. **ROUTAGE**: `Transcription` ➡️ `Intent Classifier`
3. **LOGIQUE**:
   - `Intent Classifier` ➡️ `Condition A`
     - **True** ➡️ `Property Extractor` ➡️ `Agent (Search)` ➡️ `Carousel` ➡️ `Chat Output`
     - **False** ➡️ `Condition B`
       - **True** ➡️ `RE Scraper` ➡️ `Lead Formatter` ➡️ `Lead Ingestor` ➡️ `Notification` ➡️ `Chat Output`
       - **False** ➡️ `Agent (FAQ)` ➡️ `Chat Output`

---

## 📋 Checklist de Propreté

✅ **Pas de spaghettis** : Chaque branche est isolée.
✅ **Visibilité** : On voit directement pourquoi une décision a été prise.
✅ **Performance** : On n'appelle le Scraper que si l'utilisateur est un Owner.
✅ **Scalabilité** : Pour ajouter un mode "Partner", il suffit d'ajouter une Condition C.

---

**Ce workflow est maintenant le standard professionnel pour Tyboo Studio. 🚀**
