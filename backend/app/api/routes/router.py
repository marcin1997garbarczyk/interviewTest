from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.approval import ApproveActionRequest, ApproveActionResponse
from app.schemas.chat import ChatRequest, ChatResponse, ConversationHistoryResponse
from app.schemas.upload import FileContentResponse, FileUploadResponse
from app.services.agent_chat_service import AgentChatService
from app.services.chat_message_service import ChatMessageService
from app.services.file_service import FileService
from app.services.llm_service import LLMService
from app.services.upload_service import UploadService

router = APIRouter(prefix="/api", tags=["api"])

file_service = FileService()
llm_service = LLMService()
chat_message_service = ChatMessageService()
upload_service = UploadService(file_service=file_service)
agent_chat_service = AgentChatService(
    chat_message_service=chat_message_service,
    llm_service=llm_service,
)


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    return agent_chat_service.process_chat_message(
        session_id=payload.session_id,
        prompt=payload.prompt,
    )


@router.get("/chat/{session_id}/history", response_model=ConversationHistoryResponse)
async def get_history(session_id: str) -> ConversationHistoryResponse:
    return agent_chat_service.get_conversation_history(session_id=session_id)


@router.delete("/chat/{session_id}/history")
async def clear_history(session_id: str) -> dict:
    return agent_chat_service.clear_conversation_history(session_id=session_id)


@router.post("/approve_action", response_model=ApproveActionResponse)
async def approve_action(payload: ApproveActionRequest) -> ApproveActionResponse:
    try:
        return agent_chat_service.apply_action_decision(
            session_id=payload.session_id,
            action_id=payload.action_id,
            decision=payload.decision,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/upload", response_model=FileUploadResponse)
async def upload(file: UploadFile = File(...)) -> FileUploadResponse:
    try:
        return await upload_service.upload_file(file=file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/upload/content", response_model=FileContentResponse)
async def read_uploaded_file(path: str) -> FileContentResponse:
    try:
        return upload_service.read_uploaded_file(path=path)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
