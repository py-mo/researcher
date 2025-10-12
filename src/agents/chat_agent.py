from openai import Client
from core import BaseAgent, ChatInput
from pathlib import Path
from dotenv import dotenv_values
from mem0 import Memory, configs


class ChatAgent(BaseAgent):
    """
    Chat Agent
    """

    def __init__(self, env_path: Path):
        self.client: Client = self.__config_client(env_path)

    def __config_client(self, env_path: Path) -> Client:
        data = dotenv_values(env_path)
        return Client(base_url=data["base-url"], api_key=data["open-ai-key"])

    def run(self, chat_input: ChatInput):
        """
        Executes a chat completion based on ChatInput.
        """

        messages = []

        system_prompt = f"""
        You are a helpful AI assistant.
        Intent: {chat_input.intent}.
        Filters: {chat_input.filters}.
        Preferences: {chat_input.user_preferences}.
        Documents: {', '.join(chat_input.documents) if chat_input.documents else 'None'}.
        """
        messages.insert(0, {"role": "system", "content": system_prompt.strip()})
        messages.append({"role": "user", "content": chat_input.query_text})

        reply = self.client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        ).choices[0].message

        return {
            "task_id": chat_input.task_id,
            "intent": chat_input.intent,
            "response": reply,
            "raw_output": reply.content or "",
        }
    

if __name__ == "__main__":
    agent = ChatAgent(env_path=Path(".env"))
    chat_input = ChatInput(
        query_text="Find recent papers on reinforcement learning in robotics",
        context=["User: previous question about RL algorithms"],
        intent="search",
        filters={"year": "2025"},
        user_preferences={"summary_length": "short"}
    )
    response = agent.run(chat_input=chat_input)
    print(response)