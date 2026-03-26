from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(default="default-session")
    prompt: str
    context: dict = Field(default_factory=dict)


class ChatResponse(BaseModel):
    session_id: str
    response: str
    pending_action: dict | None = None


class MessagePayload(BaseModel):
    session_id: str
    role: str
    content: str
    metadata: dict = Field(default_factory=dict)


class ConversationHistoryResponse(BaseModel):
    session_id: str
    messages: list[MessagePayload]
