from langchain_core.tools import tool


@tool("analyze_data", description="Analyze a file and report potential anomalies.")
def analyze_data(file_id: str) -> str:
    return (
        f"Analyzed file {file_id}. "
        "Potential anomaly detected in transaction pattern; confidence: medium."
    )


@tool("propose_action", description="Prepare an action proposal that requires human approval.")
def propose_action(action_type: str, details: dict) -> dict:
    return {
        "action_type": action_type,
        "details": details,
        "status": "PENDING_HUMAN_APPROVAL",
    }
