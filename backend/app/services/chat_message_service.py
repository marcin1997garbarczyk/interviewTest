from collections import defaultdict
from uuid import uuid4

from app.schemas.approval import PendingAction
from app.schemas.chat import MessagePayload


class ChatMessageService:
    def __init__(self) -> None:
        self._session_messages: dict[str, list[MessagePayload]] = defaultdict(list)
        self._pending_actions: dict[str, PendingAction] = {}

    def save_message(self, msg: MessagePayload) -> MessagePayload:
        self._session_messages[msg.session_id].append(msg)
        return msg

    def get_conversation_history(self, session_id: str) -> list[MessagePayload]:
        return self._session_messages.get(session_id, [])

    def clear_history(self, session_id: str | None = None) -> None:
        if session_id is None:
            self._session_messages.clear()
            self._pending_actions.clear()
            return
        self._session_messages.pop(session_id, None)
        pending_ids = [
            action_id
            for action_id, action in self._pending_actions.items()
            if action.session_id == session_id
        ]
        for action_id in pending_ids:
            self._pending_actions.pop(action_id, None)

    def add_pending_action(self, session_id: str, action_type: str, details: dict) -> PendingAction:
        action = PendingAction(
            action_id=str(uuid4()),
            session_id=session_id,
            action_type=action_type,
            details=details,
        )
        self._pending_actions[action.action_id] = action
        return action

    def get_pending_action(self, action_id: str) -> PendingAction | None:
        return self._pending_actions.get(action_id)

    def resolve_pending_action(self, action_id: str, decision: str) -> PendingAction | None:
        action = self._pending_actions.get(action_id)
        if action is None:
            return None
        action.status = "APPROVED" if decision == "approve" else "REJECTED"
        return action
