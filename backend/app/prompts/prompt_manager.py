from app.prompts.agent_prompts import (
    ACTION_DECISION_SYSTEM_MESSAGE_TEMPLATE,
    MOCK_ACTION_TRIGGER_KEYWORDS,
    MOCK_NO_API_KEY_RESPONSE_TEMPLATE,
    MOCK_PENDING_ACTION_RESPONSE,
    MOCK_PROPOSE_ACTION_DETAILS,
    MOCK_PROPOSE_ACTION_TYPE,
    PENDING_ACTION_SYSTEM_MESSAGE_TEMPLATE,
)
from app.prompts.system_prompts import AGENT_SYSTEM_PROMPT


class PromptManager:
    @staticmethod
    def get_agent_system_prompt() -> str:
        return AGENT_SYSTEM_PROMPT

    @staticmethod
    def get_mock_action_trigger_keywords() -> tuple[str, ...]:
        return MOCK_ACTION_TRIGGER_KEYWORDS

    @staticmethod
    def get_mock_propose_action_type() -> str:
        return MOCK_PROPOSE_ACTION_TYPE

    @staticmethod
    def get_mock_propose_action_details() -> dict:
        return MOCK_PROPOSE_ACTION_DETAILS

    @staticmethod
    def get_mock_pending_action_response() -> str:
        return MOCK_PENDING_ACTION_RESPONSE

    @staticmethod
    def format_mock_no_api_key_response(session_id: str, user_message: str) -> str:
        return MOCK_NO_API_KEY_RESPONSE_TEMPLATE.format(
            session_id=session_id,
            user_message=user_message,
        )

    @staticmethod
    def format_pending_action_system_message(action_type: str) -> str:
        return PENDING_ACTION_SYSTEM_MESSAGE_TEMPLATE.format(action_type=action_type)

    @staticmethod
    def format_action_decision_system_message(action_type: str, status: str) -> str:
        return ACTION_DECISION_SYSTEM_MESSAGE_TEMPLATE.format(
            action_type=action_type,
            status=status,
        )
