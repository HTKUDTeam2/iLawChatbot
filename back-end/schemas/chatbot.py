from pydantic import BaseModel
from typing import List, Dict

class ChatbotRequest(BaseModel):
    conversation: List[Dict[str, str]]
    currentQuestion: str


class ChatbotResponse(BaseModel):
    question: str
    answer: str
    links: list[str]
    titles: list[str]