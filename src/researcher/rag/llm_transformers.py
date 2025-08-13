from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed, BitsAndBytesConfig
import torch
from typing import Optional
from researcher.rag import LLMInference


class LLMTransformers(LLMInference):
    def __init__(self, model: str = "ibm-granite/granite-3.3-2b-instruct"
                 , bnb_config: BitsAndBytesConfig = None):
        self.model = AutoModelForCausalLM.from_pretrained(
            model,
            device_map="auto",
            quantization_config=bnb_config,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model
        )

    def ask(self, prompt: str, system_prompt: Optional[str] = None, options: dict = None) -> str:
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        input_ids = self.tokenizer.apply_chat_template(
            messages, return_tensors="pt"
            , thinking=True
            , return_dict=True
            , add_generation_prompt=True
            , options=options)

        set_seed(42)
        output = self.model.generate(
            **input_ids,
            max_new_tokens=8192,
        )

        prediction = self.tokenizer.decode(output[0, input_ids["input_ids"].shape[1]:]
                                           , skip_special_tokens=True)
        return prediction

if __name__ == "__main__":
    llm = LLMTransformers()
    result = llm.ask("Summarize contrastive learning.")
    print(result)
