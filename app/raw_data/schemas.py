from pydantic import BaseModel


class ChatbotSchema(BaseModel):
    query: str
