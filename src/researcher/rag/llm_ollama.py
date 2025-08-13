from ollama import Client
from typing import Optional
from researcher.rag import LLMInference


class LLMOllama(LLMInference):
    def __init__(self, model: str = "phi4-mini"):
        self.client = Client()
        self.model = model

    def ask(self, prompt: str, system_prompt: Optional[str] = None, options: dict = None) -> str:
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat(
            model=self.model,
            messages=messages,
            stream=False,
            options=options
        )
        return response['message']['content']

if __name__ == "__main__":
    llm = LLMInference()
    result = llm.ask("Summarize contrastive learning.")
    print(result)
