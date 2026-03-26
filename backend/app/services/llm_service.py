import os
from typing import Any

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from app.prompts.prompt_manager import PromptManager
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
                    PromptManager.get_agent_system_prompt(),
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
            trigger_keywords = PromptManager.get_mock_action_trigger_keywords()
            if any(keyword in normalized_message for keyword in trigger_keywords):
                action_type = PromptManager.get_mock_propose_action_type()
                action_details = PromptManager.get_mock_propose_action_details()
                proposed_action = propose_action.invoke(
                    {
                        "action_type": action_type,
                        "details": action_details,
                    }
                )
                return {
                    "response": PromptManager.get_mock_pending_action_response(),
                    "tool_outputs": [
                        {
                            "tool_name": "propose_action",
                            "tool_input": {
                                "action_type": action_type,
                                "details": action_details,
                            },
                            "tool_output": proposed_action,
                        }
                    ],
                }
            fallback_response = PromptManager.format_mock_no_api_key_response(
                session_id=session_id,
                user_message=user_message,
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
