# Strategic Refactoring Plan: Universal Agent Architecture

## 1. Problem Statement
The current Tyboo Studio backend utilizes **task-specific agent classes** (e.g., `FAQAgent`, `BookingAgent`, `RealEstateAgent`). This architecture creates several inhibitors to scaling:
- **Redundancy**: Core logic (LLM invocation, history management, tool calling) is duplicated across multiple packages.
- **Maintenance**: Updates to the orchestration engine must be manually applied to every individual agent.
- **Fragility**: High-level agents often break due to specific relative import dependencies that don't scale with the project structure.
- **Inflexibility**: Creating a new type of agent (e.g., "Customer Support" or "Technical Assistant") requires backend code changes rather than simple Studio configuration.

## 2. The Universal Agent Philosophy
We are moving from a "One Class per Task" model to a **"One Core Engine, Dynamic Roles"** model. 

### Core Principles:
- **Agents are Generic**: An agent is simply a loop that connects an LLM to a set of Tools.
- **Roles are Injected**: The "Role" (FAQ, Booking, etc.) is defined by the **System Prompt** and the **Tools** connected to the agent in the Studio graph.
- **Zero-Code Scaling**: Adding a new functional agent should only involve dragging a `UniversalAgent` node and connecting it to the desired tools.

## 3. Core LangChain Agent Templates
We have consolidated all specialized agents into three highly optimized LangChain patterns:

| Agent Pattern | Purposed Implementation | Example Tasks |
| :--- | :--- | :--- |
| **Simple Agent** | **LangChain LCEL Chain** (Prompt \| LLM \| Parser) | FAQ, Greeting, Sentiment Analysis. |
| **Standard Agent** | **Tool-Calling Agent** (Native JSON tool calling) | Booking, Order Tracking, CRM updates. |
| **Planner / Orchestrator**| **ReAct Agent** (Reasoning and Acting Loop) | Complex Business Workflows, Multi-Agent Swarms. |

## 4. Implementation Roadmap

### Phase 1: Consolidation (COMPLETED ✅)
1.  **Promote the Universal Node**: Refactored `backend/app/nodes/agents/langchain_agent.py` into `backend/app/nodes/agents/universal_agent.py`.
2.  **Generic Routing**: Updated `NodeFactory.py` and `NodeRegistry` to route legacy agent IDs (`faq_node`, `booking_node`, `easySpaceAgent`, etc.) to the `UniversalAgentNode`.
3.  **Inject Configuration**: `UniversalAgentNode` now reads behavior from `config` and includes **Smart Defaults** for legacy roles.

### Phase 2: Tool Standardisation (COMPLETED ✅)
1.  **Tool Discovery**: Implemented automatic tool detection in `UniversalAgentNode` via graph edges.
2.  **Schema Enforcement**: Updated `UniversalAPIConnectorNode` to provide standard LangChain `Tool` objects via `get_langchain_object`.

### Phase 3: Cleanup & Deprecation (COMPLETED ✅)
1.  **Remove Specialized Packages**: Deleted redundant nodes and logic in `backend/app/nodes/agents/` and `backend/app/agents/`.
2.  **Library Alignment**: The system is now ready to support 100% of the node library via a single, robust orchestration engine.

## 5. Benefits
- **Architecture**: Cleaner, more professional codebase.
- **Scalability**: Support for 1,000+ different agent roles without adding a single line of backend code.
- **Speed**: Drastically reduced development time for new AI features.
- **Stability**: Improvements to the core `UniversalAgent` automatically benefit every agent in the platform.
