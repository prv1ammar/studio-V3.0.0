from langflow.custom import Component
from langflow.io import MessageInput, DropdownInput, Output
from langflow.schema import Message
import sys
import os

class StandardAgentComponent(Component):
    display_name = "Specialized Agent Selector"
    description = "A versatile component that allows you to manually select and deploy any specialized domain agent."
    icon = "LayoutGrid"
    category = "Models and Agents"

    inputs = [
        DropdownInput(
            name="agent_type",
            display_name="Select Agent Role",
            options=["FAQ Agent", "Availability Agent", "Booking Agent", "Patient Agent"],
            value="FAQ Agent",
            info="Choose the specific specialist agent you want to interact with.",
        ),
        MessageInput(
            name="input_value",
            display_name="Input Message",
            info="Ask a question or provide instructions for the selected agent.",
        ),
    ]

    outputs = [
        Output(display_name="Role Response", name="response", method="build_response"),
    ]

    async def build_response(self) -> Message:
        # Detect project root
        try:
            current_dir = os.path.dirname(__file__)
            project_root = os.path.abspath(os.path.join(current_dir, ".."))
        except NameError:
            project_root = os.getcwd()

        if project_root not in sys.path:
            sys.path.append(project_root)

        try:
            from app.nodes.factory import NodeFactory
            factory = NodeFactory()
            
            agent_type = self.agent_type
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)

            # Map the UI selection to the Universal Agent with specific IDs
            node_id_map = {
                "FAQ Agent": "faq_node",
                "Availability Agent": "availability_node",
                "Booking Agent": "booking_node",
                "Patient Agent": "patient_node",
            }
            
            target_id = node_id_map.get(agent_type, "universalAgent")
            
            # Use factory to get the universal agent instance
            agent = factory.get_node(target_id, config={"id": target_id, "agent_pattern": "standard"})
            
            if not agent:
                return Message(text=f"Error: Could not initialize Universal Agent for {agent_type}")
                
            # Execute (using a dummy context for the component)
            response = await agent.execute(input_text, context={"chat_history": []})
            
            return Message(
                text=str(response),
                sender="Machine",
                sender_name=agent_type
            )
        except Exception as e:
            return Message(text=f"⚠️ Selection Error: {str(e)}")
