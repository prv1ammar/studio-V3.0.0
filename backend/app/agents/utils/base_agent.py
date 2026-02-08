from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from utils.llms import LLMModel
from database_manager.config_manager import get_config_manager

class BaseAgent(ABC):
    """
    Base abstract class for all AI agents in the Studio.
    Ensures a consistent interface for orchestration and management.
    """
    
    def __init__(self, agent_name: str, config: Optional[Dict[str, Any]] = None):
        self.agent_name = agent_name
        
        # Load external config (from Studio) or fall back to DB/Environment
        self.config_manager = get_config_manager()
        db_settings = self.config_manager.get_config(self.agent_name)
        
        # Merge: Inject Studio config -> DB Settings -> Empty Dict
        self.settings = {**(db_settings or {}), **(config or {})}
        
        # Set up Model (dynamic choice from config/settings)
        model_name = self.settings.get("model_name") or self.settings.get("OPENAI_MODEL")
        self.llm = LLMModel().get_model(model_name=model_name)
        
        self.history = []
        source = "studio injection" if config else "database settings"
        print(f"[{self.agent_name}] initialized via {source}.")

    @abstractmethod
    def run(self, user_input: str, state: Optional[Dict[str, Any]] = None) -> str:
        """
        Main execution method for the agent.
        :param user_input: The message from the user.
        :param state: Optional global state or context.
        :return: Agent's response as a string.
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Resets the agent's internal state and history.
        """
        self.history = []
        print(f"[{self.agent_name}] state reset.")

    def get_info(self) -> Dict[str, Any]:
        """
        Returns metadata about the agent.
        """
        return {
            "name": self.agent_name,
            "type": self.__class__.__name__
        }
