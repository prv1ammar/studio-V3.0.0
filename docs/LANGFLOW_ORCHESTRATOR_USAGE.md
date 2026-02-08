# How to use the Master Orchestrator Agent (Usagev2)

The **Master Orchestrator** is an intelligent agent that automatically routes your message to the correct specialist (FAQ, Booking, etc.).

1.  **Create a New Flow** in Langflow.
2.  **Add a Custom Component** node.
3.  **Edit the Code** and paste the content below.
4.  **Connect**:
    *   **Chat Input** -> **Input Message**
    *   **Response** -> **Chat Output**
5.  **Run**: Ask it anything! Try "Book an appointment", "When are you open?", or "Create a patient file".

### Orchestrator Component Code

```python
from langflow.custom import Component
from langflow.io import MessageInput, Output
from langflow.schema import Message
import sys
import os

class OrchestratorComponent(Component):
    display_name = "Master Orchestrator Agent"
    description = "Intelligent Router that directs queries to FAQ, Availability, Booking, or Patient agents."
    icon = "network"

    inputs = [
        MessageInput(
            name="input_value",
            display_name="Input Message",
            info="Connect Chat Input here.",
        ),
    ]

    outputs = [
        Output(display_name="Response", name="response", method="build_response"),
    ]

    def build_response(self) -> Message:
        # 1. Setup Path
        # Use hardcoded path for explicit reliability in this environment
        project_root = r"c:\Users\info\Desktop\AI Agent Studio"
        
        # Verify this is correct by checking for a known folder
        if not os.path.exists(os.path.join(project_root, 'agent_orchestrator')):
            # Fallback to CWD if hard path fails (e.g. folder moved)
            project_root = os.getcwd()

        if project_root not in sys.path:
            # Insert at 0 to ensure local 'utils' takes precedence over library 'utils'
            sys.path.insert(0, project_root)

        # 2. Import Orchestrator
        try:
            from agent_orchestrator.orchestrator import OrchestratorAgent
        except ImportError as e:
            return Message(text=f"Import Error: Failed to load Orchestrator. Ensure project root '{project_root}' is valid. Details: {e}")

        # 3. Process
        try:
            user_input = self.input_value

            # Extract text
            if isinstance(user_input, Message):
                input_text = user_input.text
            elif hasattr(user_input, "data") and isinstance(user_input.data, dict):
                input_text = user_input.data.get("text") or str(user_input)
            else:
                input_text = str(user_input)

            # Instantiate and Run
            orchestrator = OrchestratorAgent()
            response = orchestrator.run(input_text)
            
            return Message(text=str(response))

        except Exception as e:
            return Message(text=f"Error running Orchestrator: {str(e)}")
```
