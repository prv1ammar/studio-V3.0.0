from langflow.custom import Component
from langflow.io import MessageInput, Output
from langflow.schema import Message
import sys
import os

class PatientComponent(Component):
    display_name = "Patient Records Agent"
    description = "Secure access to patient profiles, history, and status updates within the clinic database."
    icon = "User"
    category = "Models and Agents"

    inputs = [
        MessageInput(
            name="input_value",
            display_name="Patient Detail/Query",
            info="Enter patient name, ID, or details to retrieve or update records.",
        ),
    ]

    outputs = [
        Output(display_name="Patient Data", name="response", method="build_response"),
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
            from agent_patient.patient_agent import PatientAgent
            
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            
            agent = PatientAgent()
            response = agent.run(input_text)
            
            return Message(
                text=str(response),
                sender="Machine",
                sender_name="Patient Agent"
            )
        except Exception as e:
            return Message(text=f"⚠️ Patient Records Error: {e}")
