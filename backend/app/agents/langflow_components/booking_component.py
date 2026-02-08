from langflow.custom import Component
from langflow.io import MessageInput, Output
from langflow.schema import Message
import sys
import os

class BookingComponent(Component):
    display_name = "Appointment Booking Agent"
    description = "Facilitates the creation, confirmation, and scheduling of patient appointments."
    icon = "CheckCircle"
    category = "Models and Agents"

    inputs = [
        MessageInput(
            name="input_value",
            display_name="Request",
            info="Request to book, reschedule, or cancel an appointment.",
        ),
    ]

    outputs = [
        Output(display_name="Booking Response", name="response", method="build_response"),
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
            from agent_booking.booking_agent import BookingAgent
            
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            
            agent = BookingAgent()
            response = agent.run(input_text)
            
            return Message(
                text=str(response),
                sender="Machine",
                sender_name="Booking Agent"
            )
        except Exception as e:
            return Message(text=f"⚠️ Booking Error: {e}")
