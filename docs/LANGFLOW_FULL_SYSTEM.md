# Langflow Components Guide (Full System)

This guide provides the premium code for every component in your AI Agent Studio. These components are designed with Langflow 1.1 logic and features.

## 1. Core Strategy Orchestrator (The "Brain")
The central routing engine that analyzes user intent and dispatches to specialized domain agents (FAQ, Availability, Booking, Patient). Use this as your primary chatbot entry point.

- **Display Name**: Core Strategy Orchestrator
- **Category**: Models and Agents
- **Icon**: Cpu

```python
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
            from agent_orchestrator.orchestrator import OrchestratorAgent
            
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)

            if not input_text:
                return Message(text="No input provided. Please enter a request.")

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
            error_trace = traceback.format_exc()
            print(f"Orchestrator Error:\n{error_trace}")
            return Message(text=f"⚠️ Orchestration Error: {str(e)}")
```

---

## 2. Specialized Specialist Agents
Use these components for isolated testing or specialized flows.

### A. Knowledge Base Agent (FAQ)
- **Icon**: BookOpen
- **Logic**: Connects to the FAQ knowledge repository.

```python
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
        try:
            from agent_FAQ.agent_FAQ.faq_agent import FAQAgent
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            agent = FAQAgent()
            response = agent.run(input_text)
            return Message(text=str(response), sender="Machine", sender_name="FAQ Agent")
        except Exception as e:
            return Message(text=f"⚠️ Knowledge Base Error: {e}")
```

### B. Schedule Availability Agent
- **Icon**: Calendar

```python
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
            info="Ask about available days/times.",
        ),
    ]

    outputs = [
        Output(display_name="Availability Status", name="response", method="build_response"),
    ]

    def build_response(self) -> Message:
        try:
            from agent_availability.availability_agent import AvailabilityAgent
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            agent = AvailabilityAgent()
            response = agent.run(input_text)
            return Message(text=str(response), sender="Machine", sender_name="Availability Agent")
        except Exception as e:
            return Message(text=f"⚠️ Availability Error: {e}")
```

### C. Appointment Booking Agent
- **Icon**: CheckCircle

```python
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
        try:
            from agent_booking.booking_agent import BookingAgent
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            agent = BookingAgent()
            response = agent.run(input_text)
            return Message(text=str(response), sender="Machine", sender_name="Booking Agent")
        except Exception as e:
            return Message(text=f"⚠️ Booking Error: {e}")
```

### D. Patient Records Agent
- **Icon**: User

```python
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
        try:
            from agent_patient.patient_agent import PatientAgent
            user_input = self.input_value
            input_text = user_input.text if isinstance(user_input, Message) else str(user_input)
            agent = PatientAgent()
            response = agent.run(input_text)
            return Message(text=str(response), sender="Machine", sender_name="Patient Agent")
        except Exception as e:
            return Message(text=f"⚠️ Patient Records Error: {e}")
```
