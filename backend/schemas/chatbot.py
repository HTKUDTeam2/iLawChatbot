from pydantic import BaseModel


class ChatbotRequest(BaseModel):
    question: str


class ChatbotResponse(BaseModel):
    question: str
    answer: str
    links: list[str]
    titles: list[str]
