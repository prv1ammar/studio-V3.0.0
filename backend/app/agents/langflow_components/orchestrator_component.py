from langflow.custom import Component
from langflow.io import MessageInput, Output
from langflow.schema import Message
import sys
import os
import traceback

class OrchestratorComponent(Component):
    display_name = "Core Strategy Orchestrator"
    description = "The central routing engine that analyzes user intent and dispatches to specialized domain agents (FAQ, Availability, Booking, Patient)."
    icon = "Cpu"
    category = "Models and Agents"

    inputs = [
        MessageInput(
            name="input_value",
            display_name="Input Message",
            info="The user's message to be processed by the orchestrator. Connect your Chat Input here.",
        ),
    ]

    outputs = [
        Output(display_name="Outcome", name="response", method="build_response"),
    ]

    def build_response(self) -> Message:
        # Detect project root
        try:
            current_dir = os.path.dirname(__file__)
            project_root = os.path.abspath(os.path.join(current_dir, ".."))
        except NameError:
            project_root = os.getcwd()

        # Fallback if we're not in the right place
        if not os.path.exists(os.path.join(project_root, 'agent_orchestrator')):
            hardcoded_path = r"c:\Users\info\Desktop\AI Agent Studio"
            if os.path.exists(hardcoded_path):
                project_root = hardcoded_path

        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        try:
            # Import Orchestrator lazily to avoid startup issues
            from agent_orchestrator.orchestrator import OrchestratorAgent
            
            user_input = self.input_value
            input_text = ""
            
            if isinstance(user_input, Message):
                input_text = user_input.text
            elif hasattr(user_input, "data") and isinstance(user_input.data, dict):
                input_text = user_input.data.get("text") or str(user_input)
            else:
                input_text = str(user_input)

            if not input_text:
                return Message(text="No input provided. Please enter a request.")

            # Instantiate and Run
            orchestrator = OrchestratorAgent()
            response_text = orchestrator.run(input_text)
            
            return Message(
                text=str(response_text),
                sender="Machine",
                sender_name="Orchestrator"
            )

        except ImportError as e:
            return Message(text=f"⚙️ System Error: Failed to load Orchestrator modules. Path: {project_root}. Error: {e}")
        except Exception as e:
            # Detailed error logging for premium debugging
            error_trace = traceback.format_exc()
            print(f"Orchestrator Error:\n{error_trace}")
            return Message(text=f"⚠️ Orchestration Error: {str(e)}")
