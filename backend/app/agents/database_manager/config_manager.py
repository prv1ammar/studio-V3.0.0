import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class ConfigManager:
    def __init__(self):
        self._supabase = None
        self._current_url = None
        self._current_key = None

    @property
    def supabase(self) -> Client:
        url = os.getenv("MANAGEMENT_SUPABASE_URL")
        key = os.getenv("MANAGEMENT_SUPABASE_KEY")
        
        if not url or not key:
            return None
        
        if self._supabase is None or url != self._current_url or key != self._current_key:
            self._supabase = create_client(url, key)
            self._current_url = url
            self._current_key = key
            
        return self._supabase

    def save_config(self, chatbot_id: str, config_dict: dict):
        """
        Save environment variables for a chatbot in a SINGLE ROW.
        chatbot_id will be used as the Agent Name/ID (e.g., 'FAQ Agent').
        """
        if not self.supabase:
            return None
            
        try:
            data = {
                "chatbot_id": chatbot_id,
                "env_key": "full_config",
                "env_value": json.dumps(config_dict),
                "is_secret": False
            }
            
            res = self.supabase.table("chatbot_env_configs").upsert(data, on_conflict="chatbot_id, env_key").execute()
            
            if res.data:
                return res.data[0]
            return {}
        except Exception as e:
            print(f"[ConfigManager] Error saving config for {chatbot_id}: {e}")
            return None

    def get_config(self, chatbot_id: str) -> dict:
        """Retrieve the configuration for an agent."""
        if not self.supabase:
            return {}
            
        try:
            response = self.supabase.table("chatbot_env_configs").select("*").eq("chatbot_id", chatbot_id).eq("env_key", "full_config").execute()
            if response.data:
                item = response.data[0]
                return json.loads(item['env_value'])
            return {}
        except Exception as e:
            print(f"[ConfigManager] Error retrieving config for {chatbot_id}: {e}")
            return {}

    def list_agents(self):
        """List all agents registered in the system."""
        if not self.supabase:
            return []
        try:
            response = self.supabase.table("chatbot_env_configs").select("chatbot_id").eq("env_key", "full_config").execute()
            return [item['chatbot_id'] for item in response.data]
        except Exception as e:
            print(f"[ConfigManager] Error listing agents: {e}")
            return []

    def test_connection(self):
        """Verify connection and check if the required table exists."""
        if not self.supabase:
            return False, "Supabase credentials missing."
        try:
            self.supabase.table("chatbot_env_configs").select("id").limit(1).execute()
            return True, "Connection successful and table found!"
        except Exception as e:
            error_msg = str(e)
            if "not find the table" in error_msg:
                return False, "Table 'chatbot_env_configs' NOT found."
            return False, f"Connection error: {error_msg}"

_manager = None
def get_config_manager():
    global _manager
    if _manager is None:
        _manager = ConfigManager()
    return _manager
