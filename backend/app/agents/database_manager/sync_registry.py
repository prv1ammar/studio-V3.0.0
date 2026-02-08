import os
import json
from database_manager.config_manager import get_config_manager
from agent_FAQ.agent_FAQ.prompt_agent_faq import FAQ_SYSTEM_PROMPT
from agent_availability.prompt import AVAILABILITY_PROMPT
from agent_patient.prompt import PATIENT_AGENT_PROMPT
from dotenv import load_dotenv

load_dotenv()

def sync():
    manager = get_config_manager()
    
    agents = {
        "FAQ Agent": {
            "OPENAI_MODEL": os.getenv("OPENAI_MODEL"),
            "SYSTEM_PROMPT": FAQ_SYSTEM_PROMPT
        },
        "Availability Agent": {
            "OPENAI_MODEL": os.getenv("OPENAI_MODEL"),
            "SYSTEM_PROMPT": AVAILABILITY_PROMPT
        },
        "Patient Agent": {
            "OPENAI_MODEL": os.getenv("OPENAI_MODEL"),
            "SYSTEM_PROMPT": PATIENT_AGENT_PROMPT
        },
        "Booking Agent": {
            "OPENAI_MODEL": os.getenv("OPENAI_MODEL"),
            "SYSTEM_PROMPT": "Agent for booking management." 
        }
    }
    
    for agent_name, config in agents.items():
        print(f"Syncing {agent_name}...")
        res = manager.save_config(agent_name, config)
        if res:
            print(f"✅ {agent_name} synced.")
        else:
            print(f"❌ Failed to sync {agent_name}.")

if __name__ == "__main__":
    sync()
