import os
from typing import Any

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from app.schemas.chat import MessagePayload
from app.tools.agent_tools import analyze_data, propose_action


class LLMService:
    def __init__(self) -> None:
        self._tools = [analyze_data, propose_action]
        self._agent_executor = self._create_agent_executor()

    def _create_agent_executor(self) -> AgentExecutor | None:
        if not os.getenv("OPENAI_API_KEY"):
            return None

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a modular AI agent. Use tools when relevant. "
                    "If user asks for an operation that needs approval, call propose_action tool.",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_tools_agent(llm=llm, tools=self._tools, prompt=prompt)
        return AgentExecutor(agent=agent, tools=self._tools, verbose=False, return_intermediate_steps=True)

    def _to_langchain_messages(self, history: list[MessagePayload]) -> list[Any]:
        messages: list[Any] = []
        for message in history:
            if message.role == "user":
                messages.append(HumanMessage(content=message.content))
            elif message.role == "ai":
                messages.append(AIMessage(content=message.content))
            elif message.role == "tool":
                messages.append(ToolMessage(content=message.content, tool_call_id=message.metadata.get("tool_call_id", "tool")))
            else:
                messages.append(SystemMessage(content=message.content))
        return messages

    def process_message(self, session_id: str, user_message: str, history: list[MessagePayload]) -> dict:
        if self._agent_executor is None:
            normalized_message = user_message.lower()
            if "approve" in normalized_message or "action" in normalized_message:
                proposed_action = propose_action.invoke(
                    {
                        "action_type": "credit_memo",
                        "details": {"reason": "detected anomaly from uploaded data"},
                    }
                )
                return {
                    "response": "I prepared an action proposal that needs your approval.",
                    "tool_outputs": [
                        {
                            "tool_name": "propose_action",
                            "tool_input": {
                                "action_type": "credit_memo",
                                "details": {"reason": "detected anomaly from uploaded data"},
                            },
                            "tool_output": proposed_action,
                        }
                    ],
                }
            fallback_response = (
                "Agent is running in mock mode because OPENAI_API_KEY is not set. "
                f"Session {session_id} received: {user_message}"
            )
            return {"response": fallback_response, "tool_outputs": []}

        chain_input = {
            "input": user_message,
            "chat_history": self._to_langchain_messages(history),
        }
        result = self._agent_executor.invoke(chain_input)
        return {
            "response": result.get("output", ""),
            "tool_outputs": [
                {
                    "tool_name": step[0].tool,
                    "tool_input": step[0].tool_input,
                    "tool_output": step[1],
                }
                for step in result.get("intermediate_steps", [])
            ],
        }
