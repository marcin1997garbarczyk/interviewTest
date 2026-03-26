MOCK_ACTION_TRIGGER_KEYWORDS = ("approve", "action")

MOCK_PROPOSE_ACTION_TYPE = "credit_memo"
MOCK_PROPOSE_ACTION_DETAILS = {"reason": "detected anomaly from uploaded data"}

MOCK_PENDING_ACTION_RESPONSE = "I prepared an action proposal that needs your approval."
MOCK_NO_API_KEY_RESPONSE_TEMPLATE = (
    "Agent is running in mock mode because OPENAI_API_KEY is not set. "
    "Session {session_id} received: {user_message}"
)

PENDING_ACTION_SYSTEM_MESSAGE_TEMPLATE = "Action {action_type} requires approval."
ACTION_DECISION_SYSTEM_MESSAGE_TEMPLATE = "Action {action_type} was {status} by human."
