# Tyboo Studio: Technical Project Overview

## 1. Executive Summary
Tyboo Studio is an advanced, low-code visual IDE designed for building, orchestrating, and deploying enterprise-grade AI Agents and Retrieval-Augmented Generation (RAG) pipelines. It provides a modular, node-based architecture that bridges the gap between complex backend AI logic and intuitive visual workflow design.

## 2. System Architecture

### 2.1 Technical Stack
- **Frontend**: React 19, Vite, Tailwind CSS, and **XYFlow** (React Flow) for the graph-based interface.
- **Backend**: **FastAPI** (Python 3.10+) for high-performance asynchronous API handling.
- **LLM Orchestration**: Custom modular implementation using **LiteLLM** for model-agnostic capabilities (OpenAI, Anthropic, Mistral, etc.).
- **Vector Database**: **Supabase (PostgreSQL + pgvector)** for high-dimensional semantic search.
- **Document Processing**: **Docling** for high-fidelity OCR, table extraction, and structural document analysis.
- **Memory Management**: Multi-backend support (Redis or Local JSON) for persistent conversation state.

### 2.2 Core Architectural Principles
- **DAG-Based Execution**: Workflows are represented as Directed Acyclic Graphs (DAGs) in JSON format.
- **Stateful Management**: Each node execution maintains a context object that propagates through the graph.
- **Asynchronous Execution**: Leveraging Python's `asyncio` for non-blocking I/O operations, specifically for long-running LLM and database calls.

## 3. Key Technical Pillars

### 3.1 Advanced RAG Ingestion Pipeline
Unlike standard RAG systems that only process text, Tyboo Studio implements a **Vision-Aware Ingestion Pipeline**:
- **Structural Analysis**: Uses Docling to decompose PDFs/Docs into hierarchical structures (Headers, Paragraphs, Tables, Figures).
- **Image/Graph Extraction**: Automatically extracts visual assets and generates descriptive metadata (captions) based on surrounding text context.
- **Semantic Chunking**: Documents are split into meaningful chunks while preserving structural integrity and cross-references between text and images.

### 3.2 Intelligent Vector Retrieval
To minimize hallucinations and maximize accuracy, the system uses a multi-stage retrieval process:
- **Vector Search**: Initial retrieval via cosine similarity on pgvector.
- **Smart Re-ranking**: A custom algorithm that prioritizes document chunks based on exact keyword matches (e.g., specific Figure numbers) and semantic relevance.
- **Metadata Filtering**: Filtering by source, document type, or bot-specific identifiers (BotID).

### 3.3 Smart DB Integration
Tyboo Studio features a native "Smart DB" node for direct enterprise data interaction:
- **Dynamic Discovery**: Automatically fetches database schemas, tables, and views via JWT-authenticated REST APIs.
- **CRUD Operations**: Provides a secure interface for Create, Read, Update, and Delete operations without writing SQL code.
- **Generic Adapter**: Supports NocoDB and custom internal database backends through a unified API wrapper.

## 4. Workflow Execution & Security

### 4.1 Node Execution Lifecycle
1. **Validation**: The backend validates the integrity of the graph before execution.
2. **Setup**: Necessary tools (Supabase clients, LLM interfaces) are instantiated per-node.
3. **Execution**: Nodes execute in topological order, passing outputs as inputs to downstream components.
4. **Conclusion**: The final output is aggregated and returned to the UI or via an API endpoint.

### 4.2 Security Architecture
- **JWT Authentication**: Secure interaction with external database APIs.
- **Environment Isolation**: Sensitive credentials (API Keys, DB URLs) are managed via secure environment variables.
- **CORS & Rate Limiting**: Production-ready configurations to prevent unauthorized access.

## 5. Deployment & Scalability
- **Horizontal Scaling**: The FastAPI backend is stateless, allowing it to be deployed in containerized environments (Docker/Kubernetes).
- **Extensibility**: A modular node factory allows developers to create custom nodes by simply extending the `BaseNode` class.

---
**Prepared by**: Technical Engineering Team
**Project Name**: Tyboo Studio
**Version**: 1.0.0
