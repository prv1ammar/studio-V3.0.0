from langflow.custom import Component
from langflow.io import MessageInput, Output
from langflow.schema import Message
import sys
import os

class FAQComponent(Component):
    display_name = "Knowledge Base Agent (FAQ)"
    description = "Handles common inquiries and provides instant information from the clinic's knowledge repository."
    icon = "BookOpen"
    category = "Models and Agents"

    inputs = [
        MessageInput(
            name="input_value",
            display_name="Query",
            info="Ask a question about clinic hours, location, services, or general information.",
        ),
    ]

    outputs = [
        Output(display_name="Answer", name="response", method="build_response"),
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
            from agent_FAQ.agent_FAQ.faq_agent import FAQAgent
            
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            
            agent = FAQAgent()
            response = agent.run(input_text)
            
            return Message(
                text=str(response),
                sender="Machine",
                sender_name="FAQ Agent"
            )
        except Exception as e:
            return Message(text=f"⚠️ Knowledge Base Error: {e}")
