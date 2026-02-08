# Langflow Integration Guide

Langflow is now running! You can access it at: **http://127.0.0.1:7860**

## How to use the Standard Agent Component

To use your standardized agents (`FAQAgent`, `AvailabilityAgent`, `BookingAgent`, `PatientAgent`) inside Langflow, follow these steps:

1.  **Open Langflow**: Go to [http://127.0.0.1:7860](http://127.0.0.1:7860) in your browser.
2.  **Create a New Flow**: Click "New Project" (or "Blank Flow").
3.  **Add a Custom Component**:
    *   In the sidebar, scroll down to **Custom** or search for **Custom Component**.
    *   Drag and drop the **Custom Component** node onto the canvas.
4.  **Edit the Code**:
    *   Click the "Code" icon (</>) on the Custom Component node.
    *   **Delete** all the existing code in the editor.
    *   **Copy** the code from `langflow_components/standard_agent.py` (see below) and **Paste** it into the editor.
    *   Click **Check & Save** (or "Build").
5.  **Configure the Agent**:
    *   The node should now be renamed to **Standard Agent Studio**.
    *   Select the **Agent Type** from the dropdown (e.g., "FAQ Agent").
    *   Connect a **Chat Input** component to the **Input Message** field.
    *   Connect the **Response** output to a **Chat Output** or **Text Output** component.
6.  **Run**: Click the lightning bolt icon or the "Play" button to interact with your agent!

### Component Code (`langflow_components/standard_agent.py`)

Copy this code:

```python
from langflow.custom import Component
from langflow.io import MessageInput, DropdownInput, Output
from langflow.schema import Message
import sys
import os

class StandardAgentComponent(Component):
    display_name = "Standard Agent Studio"
    description = "Wraps our standardized AI Agents (FAQ, Availability, Booking, Patient)"
    icon = "bot"

    inputs = [
        DropdownInput(
            name="agent_type",
            display_name="Agent Type",
            options=["FAQ Agent", "Availability Agent", "Booking Agent", "Patient Agent"],
            value="FAQ Agent",
        ),
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
        try:
            # If running from file
            current_dir = os.path.dirname(__file__)
            project_root = os.path.abspath(os.path.join(current_dir, ".."))
        except NameError:
            # If pasted into UI, __file__ might not exist.
            # Fallback to CWD or specific path
            project_root = os.getcwd()
            
            # Check if we are in the root by looking for 'utils' or 'agent_FAQ'
            if not os.path.exists(os.path.join(project_root, 'agent_FAQ')):
                # Try a hardcoded path as last resort for this specific user environment
                hardcoded_path = r"c:\Users\info\Desktop\AI Agent Studio"
                if os.path.exists(hardcoded_path):
                     project_root = hardcoded_path

        if project_root not in sys.path:
            sys.path.append(project_root)

        # 2. Import Agents (Lazy Import)
        try:
            from agent_FAQ.agent_FAQ.faq_agent import FAQAgent
            from agent_availability.availability_agent import AvailabilityAgent
            from agent_booking.booking_agent import BookingAgent
            from agent_patient.patient_agent import PatientAgent
        except ImportError as e:
            return Message(text=f"Import Error: Failed to load agents. Ensure project root '{project_root}' is valid. Details: {e}")

        # 3. Process
        agent_type = self.agent_type
        user_input = self.input_value

        # Extract text from input based on its type
        if isinstance(user_input, Message):
            input_text = user_input.text
        elif hasattr(user_input, "data") and isinstance(user_input.data, dict):
            input_text = user_input.data.get("text") or str(user_input)
        else:
            input_text = str(user_input)

        # Map display names to classes
        agent_map = {
            "FAQ Agent": FAQAgent,
            "Availability Agent": AvailabilityAgent,
            "Booking Agent": BookingAgent,
            "Patient Agent": PatientAgent,
        }
        
        agent_class = agent_map.get(agent_type)
        if not agent_class:
            return Message(text=f"Error: Unknown agent type {agent_type}")
            
        try:
            # Instantiate the agent
            agent = agent_class()
            # Run the agent
            response = agent.run(input_text)
            return Message(text=str(response))
        except Exception as e:
            return Message(text=f"Error running {agent_type}: {str(e)}")
```


