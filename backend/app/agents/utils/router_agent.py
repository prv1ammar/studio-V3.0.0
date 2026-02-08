from typing import Any, Dict, List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from utils.base_agent import BaseAgent

class RouterDecision(BaseModel):
    """Schema for the router's decision."""
    next_node_id: str = Field(description="The ID of the node to route to.")
    reasoning: str = Field(description="Why this path was chosen.")

class RouterAgent(BaseAgent):
    """
    A specialized agent that decides which path to take in a graph.
    It evaluates the input against a set of condition descriptions associated with connected nodes.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_name="Router Logic", config=config)
        self.routes = config.get("routes", []) if config else [] # List of {target_id: "description"}

    def set_routes(self, routes: List[Dict[str, str]]):
        """Called by the engine to inject the connected paths dynamically."""
        self.routes = routes

    def run(self, user_input: str, state: Optional[Dict[str, Any]] = None) -> str:
        """
        Evaluates the input and returns the ID of the next node.
        """
        if not self.routes:
            return "NO_ROUTE"

        # Construct a routing prompt
        route_options = "\n".join([f"- Path to Node '{r['target_id']}': {r['condition']}" for r in self.routes])
        
        system_prompt = (
            "You are a Logic Router. Your ONLY job is to select the best path for the user's request.\n"
            "Analyze the input and match it to one of the following conditions:\n\n"
            f"{route_options}\n\n"
            "Return the Result in JSON format: { \"next_node_id\": \"...\", \"reasoning\": \"...\" }\n"
            "If no condition matches well, pick the most generic one."
        )
        
        try:
            parser = JsonOutputParser(pydantic_object=RouterDecision)
            chain = self.llm | parser
            
            response = chain.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ])
            
            # We return a special signal that the Engine intercepts
            return f"__ROUTING_LEADER__{response['next_node_id']}"
            
        except Exception as e:
            print(f"Router Error: {e}")
            # Fallback to first route
            return f"__ROUTING_LEADER__{self.routes[0]['target_id']}"

    def reset(self):
        pass
