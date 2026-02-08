from typing import Any, Dict, List, Optional
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from utils.base_agent import BaseAgent
from utils.llms import LLMModel

class ConfigurableAgent(BaseAgent):
    """
    The 'Universal' agent that can be fully configured via JSON inputs.
    Supported configurations: system_prompt, model_name, tools_list.
    """
    
    def __init__(self, agent_name: str = "Configurable Agent", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_name=agent_name, config=config)
        
        self.system_prompt = self.settings.get("system_prompt", "You are a helpful assistant.")
        self.tools = self._initialize_tools(self.settings.get("tools", []))
        self.memory_key = "chat_history"
        
        # Build prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name=self.memory_key),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Initialize Agent Executor
        self._build_executor()

    def _initialize_tools(self, tools_config: List[Any]) -> List[Any]:
        """
        Dynamically loads tools from the central ToolRegistry.
        """
        from backend.tools import tool_registry
        
        # tools_config can be a list of strings (names) or objects
        tool_names = []
        for t in tools_config:
            if isinstance(t, str):
                tool_names.append(t)
            elif isinstance(t, dict) and "name" in t:
                tool_names.append(t["name"])
        
        return tool_registry.get_tools_by_names(tool_names)

    def _build_executor(self):
        """Constructs the LangChain agent executor."""
        if not self.tools:
            # Simple LLM chain if no tools
            self.agent_executor = None
            return

        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt_template
        )
        
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def run(self, user_input: str, state: Optional[Dict[str, Any]] = None) -> str:
        """Executes the agent logic."""
        
        # If no tools, simple invocation
        if not self.agent_executor:
            # Construct messages from history + current input
            messages = [SystemMessage(content=self.system_prompt)]
            messages.extend(self.history)
            messages.append(HumanMessage(content=user_input))
            
            response = self.llm.invoke(messages)
            self.history.append(HumanMessage(content=user_input))
            self.history.append(AIMessage(content=response.content))
            return response.content

        # If tools, use executor
        result = self.agent_executor.invoke({
            "input": user_input,
            "chat_history": self.history
        })
        
        output = result.get("output", "I'm sorry, I couldn't process that.")
        self.history.append(HumanMessage(content=user_input))
        self.history.append(AIMessage(content=output))
        
        # Trim history
        if len(self.history) > 10:
            self.history = self.history[-10:]
            
        return output

    def reset(self):
        super().reset()
        self._build_executor()
