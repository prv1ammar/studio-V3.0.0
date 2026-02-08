# Tyboo Studio : Spécifications Techniques Complètes et Architecture Profonde

Ce document constitue la référence technique ultime pour l'architecture de Tyboo Studio. Il détaille chaque couche du système, du moteur d'exécution des graphes au pipeline RAG de vision avancée.

---

## 1. Résumé Exécutif
Tyboo Studio est un IDE (Integrated Development Environment) visuel "low-code" conçu pour le prototypage rapide et le déploiement d'Agents IA autonomes et de systèmes RAG (Retrieval-Augmented Generation) de pointe. En transformant des infrastructures complexes en interfaces graphiques intuitives, il permet de construire des flux de travail IA capables d'analyser des documents multi-modaux, d'effectuer des recherches vectorielles hybrides et d'orchestrer des bases de données d'entreprise en temps réel.

---

## 2. Architecture Théorique et Flux de Données

### 2.1 Le Modèle de Graphe Acyclique Dirigé (DAG)
Au cœur de Tyboo Studio, chaque flux de travail est traité comme un **Graphe Acyclique Dirigé (DAG)**.
- **Représentation du Flux** : Stocké sous forme d'objet JSON contenant deux tableaux : `nodes` (unités logiques atomiques) et `edges` (chemins de données directionnels).
- **Ordre d'Exécution** : Le backend effectue un **Tri Topologique** sur les liens pour déterminer la séquence exacte d'exécution, garantissant que toutes les dépendances d'un nœud sont satisfaites avant son déclenchement.

### 2.2 L'Objet de Contexte Unifié (Propagation d'État)
L'état dans Tyboo Studio est géré via un **Dictionnaire de Contexte Global**.
- **Injection de Prrécurseurs** : Chaque nœud enregistre sa sortie dans ce dictionnaire, indexée par son `ID de Nœud`.
- **Remplacement Dynamique de Variables** : Les nœuds utilisent une syntaxe en doubles accolades `{{node_id.field}}` pour injecter des données en temps réel dans leurs paramètres d'exécution (ex: injecter le résultat d'une base de données dans un prompt).

---

## 3. Pipeline RAG de Vision (Ingestion Documentaire)

Tyboo Studio implémente un pipeline RAG "Vision-First" unique, capable de préserver la structure documentaire et le contexte visuel là où les systèmes classiques échouent.

### 3.1 Décomposition Structurelle avec Docling
Lors de l'ingestion, chaque document subit une analyse structurelle profonde :
1. **Analyse de Mise en Page (OCR)** : Détecte la position géométrique de chaque élément sur une page.
2. **Classification Sémantique** : Identifie les éléments comme `Titre`, `Paragraphe`, `Tableau` ou `Figure`.
3. **Extraction d'Actifs** : Les images et graphiques sont découpés du fichier original et stockés en tant qu'actifs haute résolution.

### 3.2 Légendage Intelligent et Liage de Proximité
Pour rendre les images consultables, le système utilise un **Algorithme de Buffer de Proximité** :
- **Analyse de Contexte** : Pour chaque figure, le système scanne les 2000 caractères de texte environnants.
- **Découverte de Labels** : Utilise des expressions régulières (Regex) pour identifier les légendes (ex: `Graphique 43 : Projections de revenus`).
- **Tagage des Métadonnées** : Le label découvert est intégré au vecteur de recherche, créant un "pont sémantique" entre l'image et la requête textuelle de l'utilisateur.

### 3.3 Recherche Hybride et Re-ranking Intelligent
La recherche ne se limite pas à des mathématiques vectorielles :
1. **Recherche Vectorielle** : Utilise `pgvector` pour trouver les 10 meilleurs résultats par similarité sémantique.
2. **Boost Numérique/Mots-clés** : Si la requête utilisateur contient un identifiant spécifique (ex: "Figure 43"), le système scanne les résultats et booste mathématiquement tout fragment contenant "Figure 43" en première position.
3. **Seuils Dynamiques** : Un seuil de similarité (par défaut `0.2`) assure un équilibre optimal entre rappel et précision.

---

## 4. Intelligence Agentique et Écosystème d'Outils

### 4.1 Nœuds Agents Autonomes
Le `LangChainAgentNode` fonctionne comme le "cerveau" du graphe. Il ne suit pas simplement un chemin ; il prend des décisions.
- **Transformation en Outils** : Le backend convertit les autres nœuds du graphe (ex: `SupabaseSearch` ou `SmartDB`) en "Outils" exécutables que l'Agent peut appeler à la demande.
- **Cycle ReAct (Raisonnement & Action)** :
  - **Pensée** : L'agent décide quel outil utiliser.
  - **Action** : Il exécute l'appel à l'outil.
  - **Observation** : Il évalue le résultat obtenu pour formuler sa réponse finale.

### 4.2 Orchestration LLM (LiteLLM)
Nous utilisons une **Passerelle Universelle** via LiteLLM.
- **Moteur Agnostique** : Supporte plus de 100 modèles (OpenAI, Claude, Mistral) via une API unique.
- **Logique de Repli (Fallback)** : Capacité de basculer automatiquement d'un modèle à l'autre en cas de panne d'une API.

---

## 5. Persistance et Connectivité Entreprise

### 5.1 Nœud Smart DB (Le Pont vers les Données Structurées)
Le nœud Smart DB agit comme un proxy sécurisé pour les bases de données externes (NocoDB / TybotFlow).
- **Découverte Dynamique de Schéma** : Interroge les API en temps réel pour peupler les menus déroulants du Studio.
- **Transactions Sécurisées JWT** : Utilise des jetons porteurs (Bearer tokens) signés pour garantir l'intégrité des données d'entreprise.
- **Couche REST-to-CRUD** : Traduit les configurations visuelles en méthodes REST standards (`GET`, `POST`, `PATCH`, `DELETE`).

### 5.2 Mémoire de Conversation
- **Backends** : Supporte **Redis** pour les performances de production et le **JSON Local** pour les déploiements légers.
- **Gestion de Fenêtre** : Gère automatiquement la longueur du contexte en élaguant les anciens messages tout en conservant l'historique pertinent.

---

## 6. Écosystème de Nœuds et Scalabilité Immense

L'une des forces majeures de Tyboo Studio réside dans la richesse et la diversité de sa bibliothèque de composants, offrant une versatilité sans précédent.

### 6.1 Une Bibliothèque de 355+ Nœuds
Le projet intègre un écosystème de **plus de 355 nœuds pré-configurés**, permettant de couvrir la quasi-totalité des besoins d'une entreprise moderne sans développement supplémentaire :
- **Intégrations Réseaux Sociaux** : YouTube, LinkedIn, Instagram, etc.
- **Connecteurs de Données** : NocoDB, SmartDB, Google Sheets, PostgreSQL, Airtable.
- **Intelligence Artificielle** : Support de tous les LLM majeurs, Vision, OCR, et Recherche Vectorielle.
- **Outils de Productivité** : Gmail, Slack, Drive, Webhooks personnalisés.
- **Moteurs de Traitement** : Scripts Python personnalisés, formatage JSON, analyse sémantique.

### 6.2 Architecture de Découverte Dynamique
Malgré ce volume massif de composants, le système reste léger et performant grâce à son **Architecture de Découverte Dynamique** :
- **Auto-Génération de l'Interface** : Le Studio n'embarque pas les nœuds en dur. Il interroge l'endpoint `/nodes` au démarrage.
- **Mapping Backend-Frontend** : Chaque nœud Python expose ses propres métadonnées (nom, icône, paramètres requis). Le frontend React génère alors dynamiquement le formulaire de configuration dans l'inspecteur.
- **Scalabilité Limitée uniquement par l'Imagination** : Ajouter un 356ème nœud ne prend que quelques minutes en étendant la classe `BaseNode`, rendant le système virtuellement infini dans son extension.

---

## 7. Résumé du Stack Technique

| Couche | Technologie |
| :--- | :--- |
| **Interface Visuelle** | React 19, XYFlow, Tailwind CSS |
| **Moteur Backend** | Python 3.10+, FastAPI (Asynchrone) |
| **Base de Données** | Supabase (PostgreSQL + pgvector) |
| **Ingestion** | Docling (Vision-based OCR & Analysis) |
| **Intelligence** | LiteLLM + LangChain Framework |
| **Mémoire** | Redis / Stockage Local |

---

## 8. Workflow Développeur (Extensibilité)
Tyboo Studio est conçu pour la modularité. Pour ajouter une fonctionnalité :
1. **Définir la Logique** : Hériter de la classe `BaseNode` dans le backend.
2. **Exposition UI** : Le backend lit automatiquement la classe et l'envoie à l'interface via l'endpoint `/nodes`.
3. **Interaction** : Glissez-déposez le nouveau nœud et connectez-le à vos agents.

---
**Version du Document** : 1.2.0  
**Confidentialité** : Technique Interne / Présentation Client  
**Note** : Ce document est destiné à l'évaluation technique et à la préparation des démonstrations.
