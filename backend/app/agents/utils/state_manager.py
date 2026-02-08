from typing import TypedDict, Optional, Dict, List, Any
from langchain_core.messages import BaseMessage

class GlobalState(TypedDict, total=False):
    messages: List[BaseMessage]
    language: Optional[str]
    intent: Optional[str]
    last_routing_reason: Optional[str]
    patient_id: Optional[str]
    phone: Optional[str]
    full_name: Optional[str]
    date: Optional[str]
    time: Optional[str]
    availability_result: Optional[Any]
    faq_handled: bool
    conflict: bool
    logs: List[str]
    current_agent: Optional[str]
    user_message: Optional[str]
    booking_info: Optional[Dict]
    faq_answer: Optional[str]
