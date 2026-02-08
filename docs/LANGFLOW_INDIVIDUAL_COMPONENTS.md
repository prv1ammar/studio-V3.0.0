# How to Add Individual Agents to Langflow Studio

You requested to have each agent (`FAQ`, `Availability`, `Booking`, `Patient`) as its own separate node in Langflow. Follow these steps to set them up and save them for reuse.

## 1. FAQ Agent Component

1.  **Add a Custom Component** node to your flow.
2.  **Edit Code** and paste the following:

```python
from langflow.custom import Component
from langflow.io import MessageInput, Output
from langflow.schema import Message
from agent_FAQ.agent_FAQ.faq_agent import FAQAgent

class FAQComponent(Component):
    display_name = "FAQ Agent"
    description = "Handles general questions about the clinic (hours, address, services)."
    icon = "info"

    inputs = [
        MessageInput(
            name="input_value",
            display_name="Input Message",
            info="User question",
        ),
    ]

    outputs = [
        Output(display_name="Response", name="response", method="build_response"),
    ]

    def build_response(self) -> Message:
        try:
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            
            agent = FAQAgent()
            response = agent.run(input_text)
            return Message(text=str(response))
        except Exception as e:
            return Message(text=f"Error: {e}")
```

3.  Click **Check & Save**.
4.  *(Optional)* To keep it available, you can copy this node to other flows or save the flow as a "Project" template.

---

## 2. Booking Agent Component

1.  **Add a Custom Component** node.
2.  **Edit Code** and paste:

```python
from langflow.custom import Component
from langflow.io import MessageInput, Output
from langflow.schema import Message
from agent_booking.booking_agent import BookingAgent

class BookingComponent(Component):
    display_name = "Booking Agent"
    description = "Handles appointment booking, updates, and cancellations."
    icon = "bookmark"

    inputs = [
        MessageInput(
            name="input_value",
            display_name="Input Message",
            info="Booking request",
        ),
    ]

    outputs = [
        Output(display_name="Response", name="response", method="build_response"),
    ]

    def build_response(self) -> Message:
        try:
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            
            agent = BookingAgent()
            response = agent.run(input_text)
            return Message(text=str(response))
        except Exception as e:
            return Message(text=f"Error: {e}")
```
3.  Click **Check & Save**.

---

## 3. Availability Agent Component

1.  **Add a Custom Component** node.
2.  **Edit Code** and paste:

```python
from langflow.custom import Component
from langflow.io import MessageInput, Output
from langflow.schema import Message
from agent_availability.availability_agent import AvailabilityAgent

class AvailabilityComponent(Component):
    display_name = "Availability Agent"
    description = "Checks doctor availability and slots."
    icon = "calendar"

    inputs = [
        MessageInput(
            name="input_value",
            display_name="Input Message",
            info="Query about availability",
        ),
    ]

    outputs = [
        Output(display_name="Response", name="response", method="build_response"),
    ]

    def build_response(self) -> Message:
        try:
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            
            agent = AvailabilityAgent()
            response = agent.run(input_text)
            return Message(text=str(response))
        except Exception as e:
            return Message(text=f"Error: {e}")
```
3.  Click **Check & Save**.

---

## 4. Patient Agent Component

1.  **Add a Custom Component** node.
2.  **Edit Code** and paste:

```python
from langflow.custom import Component
from langflow.io import MessageInput, Output
from langflow.schema import Message
from agent_patient.patient_agent import PatientAgent

class PatientComponent(Component):
    display_name = "Patient Agent"
    description = "Manages patient records and identification."
    icon = "user"

    inputs = [
        MessageInput(
            name="input_value",
            display_name="Input Message",
            info="Patient details or retrieval request",
        ),
    ]

    outputs = [
        Output(display_name="Response", name="response", method="build_response"),
    ]

    def build_response(self) -> Message:
        try:
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            
            agent = PatientAgent()
            response = agent.run(input_text)
            return Message(text=str(response))
        except Exception as e:
            return Message(text=f"Error: {e}")
```
3.  Click **Check & Save**.

---

## How to use them?

You can now connect a **Chat Input** to any of these agents independently to test them, or build your own custom orchestration flow visually by connecting a Router (Classifier) to these nodes!
