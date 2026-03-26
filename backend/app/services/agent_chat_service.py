from app.schemas.approval import ApproveActionResponse
from app.schemas.chat import ChatResponse, ConversationHistoryResponse, MessagePayload
from app.services.chat_message_service import ChatMessageService
from app.services.llm_service import LLMService


class AgentChatService:
    def __init__(self, chat_message_service: ChatMessageService, llm_service: LLMService) -> None:
        self.chat_message_service = chat_message_service
        self.llm_service = llm_service

    def process_chat_message(self, session_id: str, prompt: str) -> ChatResponse:
        history = self.chat_message_service.get_conversation_history(session_id)
        user_message = MessagePayload(session_id=session_id, role="user", content=prompt)
        self.chat_message_service.save_message(user_message)
        result = self.llm_service.process_message(
            session_id=session_id,
            user_message=prompt,
            history=history,
        )
        pending_action = self._register_pending_action_if_needed(session_id=session_id, tool_outputs=result["tool_outputs"])
        llm_text = result["response"]
        ai_message = MessagePayload(session_id=session_id, role="ai", content=llm_text)
        self.chat_message_service.save_message(ai_message)
        return ChatResponse(session_id=session_id, response=llm_text, pending_action=pending_action)

    def get_conversation_history(self, session_id: str) -> ConversationHistoryResponse:
        messages = self.chat_message_service.get_conversation_history(session_id=session_id)
        return ConversationHistoryResponse(session_id=session_id, messages=messages)

    def clear_conversation_history(self, session_id: str) -> dict:
        self.chat_message_service.clear_history(session_id=session_id)
        return {"session_id": session_id, "status": "cleared"}

    def apply_action_decision(self, session_id: str, action_id: str, decision: str) -> ApproveActionResponse:
        if decision not in {"approve", "reject"}:
            raise ValueError("Decision must be approve or reject")
        action = self.chat_message_service.resolve_pending_action(
            action_id=action_id,
            decision=decision,
        )
        if action is None or action.session_id != session_id:
            raise LookupError("Pending action not found")
        self.chat_message_service.save_message(
            MessagePayload(
                session_id=session_id,
                role="system",
                content=f"Action {action.action_type} was {action.status.lower()} by human.",
                metadata={"action_id": action.action_id, "decision": decision},
            )
        )
        return ApproveActionResponse(
            action_id=action.action_id,
            session_id=action.session_id,
            status=action.status,
            decision=decision,
        )

    def _register_pending_action_if_needed(self, session_id: str, tool_outputs: list[dict]) -> dict | None:
        for tool_output in tool_outputs:
            if tool_output["tool_name"] != "propose_action":
                continue
            output_payload = tool_output["tool_output"]
            if not isinstance(output_payload, dict):
                continue
            if output_payload.get("status") != "PENDING_HUMAN_APPROVAL":
                continue
            action = self.chat_message_service.add_pending_action(
                session_id=session_id,
                action_type=output_payload.get("action_type", "generic_action"),
                details=output_payload.get("details", {}),
            )
            pending_action = action.model_dump()
            self.chat_message_service.save_message(
                MessagePayload(
                    session_id=session_id,
                    role="system",
                    content=f"Action {action.action_type} requires approval.",
                    metadata={"pending_action": pending_action},
                )
            )
            return pending_action
        return None
