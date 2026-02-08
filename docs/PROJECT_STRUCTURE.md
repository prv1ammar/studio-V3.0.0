# 🚀 AI Agent Studio - Projet RAG & Multi-Agents

Bienvenue dans le **AI Agent Studio**, une plateforme modulaire pour concevoir, tester et déployer des agents d'intelligence artificielle sophistiqués avec une architecture RAG (Retrieval-Augmented Generation) avancée.

## 📁 Structure du Projet

Suite à la réorganisation professionnelle, le projet est structuré comme suit :

### 1. 🧠 `backend/app/` (Le Cœur)
C'est ici que réside toute l'intelligence du système.
- **`api/`** : Contient `main.py`, le serveur FastAPI qui gère les requêtes du Studio, les sauvegardes et l'exécution des flux.
- **`core/`** : Contient `engine.py`, le moteur d'exécution qui parcourt le graphe de nœuds et orchestre les appels aux agents.
- **`models/`** : Définit les schémas de données (Pydantic) pour assurer la validité des échanges entre le frontend et le backend.
- **`agents/`** : Regroupe tous les agents spécialisés :
  - `agent_orchestrator` : Le cerveau central qui délègue les tâches.
  - `agent_FAQ` : Expert en recherche documentaire (RAG).
  - `agent_booking` & `agent_availability` : Gestion des rendez-vous.
  - `utils/` : Composants transverses (mémoire Redis, routeurs).

### 2. 🛠️ `backend/scripts/` & `backend/data/`
- **`scripts/`** : Utilitaires pour injecter des composants dans la bibliothèque, tester les agents individuellement ou migrer les données.
- **`data/`** : Stockage sécurisé des clés API (`credentials.json`), jetons (`token.pickle`) et métadonnées de la bibliothèque de composants.

### 3. 📝 `backend/workflows/`
Stocke tous vos designs de flux au format JSON. Chaque fichier ici représente un "cerveau" visuel que vous avez créé dans le Studio.

### 4. 💻 `studio/`
L'interface utilisateur visuelle (React + React Flow) qui vous permet de construire vos agents par glisser-déposer.

---

## 🌟 Fonctionnalités Clés

### 🔒 Isolation des Données (Multi-Tenant RAG)
Le système utilise une architecture de **Collections** dans Supabase. Chaque fichier PDF ou document ingéré est stocké avec un `collection_id` unique. Cela garantit que l'Agent ne mélange jamais les informations entre deux documents différents.

### ⚡ Ingestion Autonome
Plus besoin de cliquer sur "Play" pour charger un fichier. Dès que vous posez une question sur un nouveau document :
1. Le moteur détecte le fichier.
2. Il le découpe en morceaux (chunks) automatiquement.
3. Il génère les embeddings et les stocke dans Supabase.
4. Il répond à votre question instantanément.

### 🔗 Orchestration Intelligente
Grâce au nœud `Main RAG Agent`, le studio peut :
- Rechercher dans une base de données vectorielle (Supabase).
- Maintenir une mémoire de conversation (Redis).
- Utiliser différents modèles LLM via la passerelle Tybot.

---

## 📖 Catalogue des Nœuds (Registry)

Chaque nœud du Studio a été conçu pour remplir une fonction précise et s'imbriquer dans un écosystème modulaire.

### 🔵 Nœuds Essentiels (Interface & Core)
- **Chat Input & Chat Output**
  - **Origine** : Composants de base du Studio.
  - **Rôle** : Points d'entrée (utilisateur) et de sortie (réponse de l'IA) du système. Ils gèrent la communication texte brute.
- **Lite LLM (Tybot)**
  - **Origine** : Intégration via la passerelle LiteLLM.
  - **Rôle** : Le moteur de raisonnement. Il reçoit un prompt et génère une réponse en utilisant des modèles comme GPT-4.
- **Lite Embedding (Tybot)**
  - **Origine** : Intégration via OpenAI/Tybot.
  - **Rôle** : Transforme le texte en vecteurs numériques (listes de nombres) pour permettre la recherche de similarité.

### 📂 Nœuds de Données & RAG
- **File Extraction**
  - **Origine** : Ajouté pour le support multi-format (PDF, DOCX, TXT).
  - **Rôle** : Extrait le texte des fichiers locaux et suggère automatiquement un identifiant de collection basé sur le nom du fichier.
- **Supabase Hybrid Store**
  - **Origine** : Intégration de la base de données vectorielle Supabase.
  - **Rôle** : Agit comme un "cerveau de stockage". Il conserve les fragments de texte et leurs vecteurs pour une récupération ultérieure.
- **Main RAG Agent**
  - **Origine** : L'orchestrateur central du Studio, introduit pour unifier la recherche et la réponse.
  - **Rôle** : **Le cerveau du workflow**. Il détecte automatiquement les fichiers connectés, gère l'ingestion transparente (chunking) et fusionne le contexte trouvé avec la question de l'utilisateur pour l'envoyer au LLM.

### 🏥 Nœuds Spécialistes (Cas d'Usage Clinique)
*Ces nœuds sont hérités de la migration des agents spécialisés dans le dossier `backend/app/agents/`.*
- **FAQ Node** : Expert en recherche documentaire sur les bases de connaissances statiques.
- **Booking & Availability Nodes** : Connectés à Google Calendar et Airtable pour gérer les rendez-vous en temps réel.
- **Patient Node** : Accède aux dossiers patients sécurisés.
- **Orchestrator Node** : Un agent de haut niveau capable de router les demandes entre les différents spécialistes ci-dessus.

### ⚙️ Nœuds d'Infrastructure & Logique
- **Redis Chat Memory**
  - **Origine** : Infrastructure de mise en cache haute performance.
  - **Rôle** : Fournit une mémoire à court terme au chat pour que l'IA se souvienne des messages précédents.
- **Router Node**
  - **Origine** : Logique de branchement conditionnel.
  - **Rôle** : Permet de créer des chemins différents dans le workflow selon le contenu du message (ex: si "Rendez-vous" alors aller vers Booking).

### 🛠️ Bibliothèque Étendue (Héritage Langflow)
Le Studio intègre une vaste bibliothèque de nœuds "prêts à l'emploi" issus d'un projet de migration (scraping) du framework Langflow. Ces nœuds permettent d'étendre les capacités du Studio sans développement supplémentaire.

- **Intégrations Externes (Notion, Google, etc.)**
  - **Origine** : Scrappés depuis les composants officiels de Langflow.
  - **Rôle** : Permettent à l'IA d'interagir avec des outils tiers (ex: lire une page Notion, lister des fichiers Google Drive).
- **FAISS (Vector Store)**
  - **Origine** : Librairie de recherche vectorielle de Facebook, intégrée via Langflow.
  - **Rôle** : Une alternative locale à Supabase. Idéal pour des tests rapides ou des recherches vectorielles sur de petits volumes de données sans base de données cloud.
- **Logic & Flow (Helpers)**
  - **Origine** : Moteur logique de Langflow.
  - **Rôle** : Nœuds utilitaires comme le `Prompt Template` (pour formater les questions), les filtres de données, ou les convertisseurs de types (Texte vers Document).
- **Modèles Standards (OpenAI, Anthropic)**
  - **Origine** : Connecteurs LangChain.
  - **Rôle** : Permettent d'utiliser directement les clés API officielles de ces fournisseurs comme alternative à notre passerelle `LiteLLM`.

---

## 🚀 Comment démarrer ?

1. **Lancer le Backend** :
   ```powershell
   .\venv\Scripts\python -m uvicorn backend.app.api.main:app --host 0.0.0.0 --port 8001 --reload
   ```

2. **Lancer le Studio (Frontend)** :
   ```powershell
   cd studio
   npm run dev
   ```

3. **Utilisation** :
   - Ouvrez votre navigateur sur `http://localhost:5173`.
   - Glissez un nœud `File Extraction` et un `Main RAG Agent`.
   - Connectez-les et commencez à discuter avec vos documents !

---

*Développé avec ❤️ pour une IA structurée et puissante.*
