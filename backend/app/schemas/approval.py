from pydantic import BaseModel, Field


class PendingAction(BaseModel):
    action_id: str
    session_id: str
    action_type: str
    details: dict = Field(default_factory=dict)
    status: str = "PENDING_HUMAN_APPROVAL"


class ApproveActionRequest(BaseModel):
    session_id: str
    action_id: str
    decision: str


class ApproveActionResponse(BaseModel):
    action_id: str
    session_id: str
    status: str
    decision: str
