from langflow.custom import Component
from langflow.io import MessageInput, Output
from langflow.schema import Message
import sys
import os

class AvailabilityComponent(Component):
    display_name = "Schedule Availability Agent"
    description = "Real-time calendar analysis to check for open appointment slots and clinic timings."
    icon = "Calendar"
    category = "Models and Agents"

    inputs = [
        MessageInput(
            name="input_value",
            display_name="Query",
            info="Ask about available days/times (e.g., 'Is there any slot tomorrow morning?')",
        ),
    ]

    outputs = [
        Output(display_name="Availability Status", name="response", method="build_response"),
    ]

    def build_response(self) -> Message:
        # Detect project root
        try:
            current_dir = os.path.dirname(__file__)
            project_root = os.path.abspath(os.path.join(current_dir, ".."))
        except NameError:
            project_root = os.getcwd()

        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        try:
            from agent_availability.availability_agent import AvailabilityAgent
            
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            
            agent = AvailabilityAgent()
            response = agent.run(input_text)
            
            return Message(
                text=str(response),
                sender="Machine",
                sender_name="Availability Agent"
            )
        except Exception as e:
            return Message(text=f"⚠️ Availability Error: {e}")
