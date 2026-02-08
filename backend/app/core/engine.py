import sys
import os
from typing import Dict, Any, List, Optional
import traceback
from app.nodes.factory import NodeFactory

# Root path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# Backend path to support 'app.' imports
backend_path = os.path.join(project_root, "backend")
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Agents directory for legacy/utility support
agents_dir = os.path.join(project_root, "backend", "app", "agents")
if agents_dir not in sys.path:
    sys.path.append(agents_dir)

class AgentEngine:
    """
    Modular Agent Engine that follows a LangChain-style architecture.
    Nodes are delegated to specialized classes in app/nodes/.
    """
    
    def __init__(self):
        self.node_factory = NodeFactory()

    async def execute_node(self, node_type: str, input_text: Any, config: Dict[str, Any] = None, context: Dict[str, Any] = None) -> Any:
        """
        Loads and executes a node based on its type.
        """
        node = self.node_factory.get_node(node_type, config)
        if not node:
             return f"Error: Node type '{node_type}' not found in registry."
        
        try:
            return await node.execute(input_text, context)
        except Exception as e:
            print(f"Node Execution Error ({node_type}): {e}")
            traceback.print_exc()
            return f"Execution Error: {str(e)}"

    async def process_workflow(self, graph_data: Dict[str, Any], message: str, broadcaster=None) -> str:
        """
        Core workflow execution engine.
        Traverses the graph and invokes nodes.
        """
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])
        
        if not nodes: return "Graph is empty."

        # 1. Identify Entry Point (Chat Input)
        current_node = next((n for n in nodes if n.get('data', {}).get('id') == 'chatInput'), nodes[0] if nodes else None)
        if not current_node: return "No valid entry point found."
        
        current_input = message
        visited = set()
        
        # Max hops to prevent infinite loops
        for _ in range(20):
            node_id = current_node['id']
            if node_id in visited: break
            visited.add(node_id)
            
            node_type = current_node.get('type')
            node_data = current_node.get('data', {})
            reg_id = node_data.get('id')
            
            # Prepare execution context
            context = {
                "graph_data": graph_data,
                "node_id": node_id,
                "visited": list(visited),
                "engine": self
            }
            
            # Broadcast node start
            if broadcaster: await broadcaster("node_start", node_id)
            
            # Execute Node Logic
            target_type = reg_id if reg_id and reg_id != 'chatInput' else node_type
            
            if reg_id == 'chatInput':
                result = current_input
            else:
                # Add routes for branching nodes (like Router)
                outgoing = [e for e in edges if e['source'] == node_id]
                context["routes"] = [{"target_id": e['target'], "condition": e.get('label', 'Default')} for e in outgoing]
                
                # Dynamic Execution via Factory
                result = await self.execute_node(target_type, current_input, config=node_data, context=context)

            # Broadcast node completion
            if broadcaster: await broadcaster("node_end", node_id, {"output": str(result)[:200]})
            
            # 2. Determine Next Node (Traversal)
            all_node_ids = [n.get('id') for n in nodes]
            next_node_id = None
            
            # Use result if it's a specific node ID (Explicit Routing)
            if result in all_node_ids:
                print(f"🔀 Engine: Branching to node {result}")
                next_node_id = result
            else:
                # Fallback to standard sequential traversal
                next_edge = next((e for e in edges if e['source'] == node_id), None)
                next_node_id = next_edge['target'] if next_edge else None
            
            if not next_node_id: break
            
            # PREPARE INPUT FOR NEXT NODE (Handle-Aware Mapping)
            edge_to_next = next((e for e in edges if e['source'] == node_id and e['target'] == next_node_id), None)
            
            if result in all_node_ids:
                # Coming from a Router/Jump: Keep original input (propagate the trigger)
                pass 
            else:
                # Sequential data flow
                if edge_to_next and (edge_to_next.get('sourceHandle') or edge_to_next.get('targetHandle')):
                    s_handle = edge_to_next.get('sourceHandle')
                    t_handle = edge_to_next.get('targetHandle') or "input"
                    
                    mapped_value = result
                    if s_handle and isinstance(result, dict) and s_handle in result:
                        mapped_value = result[s_handle]
                    
                    # Structure as a dict for the target node
                    current_input = {t_handle: mapped_value}
                    print(f"🧬 Engine: Mapped handle '{s_handle}' -> '{t_handle}'")
                else:
                    current_input = result
            
            current_node = next((n for n in nodes if n['id'] == next_node_id), None)
            if not current_node: break
            
        return str(result)

# Instantiate and export the engine
engine = AgentEngine()

# Add registry property for compatibility with main.py
# (It expects engine.registry to exist)
from app.nodes.factory import NODE_MAP
engine.registry = NODE_MAP
