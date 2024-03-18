from typing import Any, List, Mapping, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

import openai
from utils import get_conf

class OpenAILLM(LLM):
    temperature: float = 0.1
    model_name: str = ""
    @property
    def _llm_type(self) -> str:
        return "OpenAI"

    def __init__(self, model_name: str, openai_api_key: str, openai_api_base: str):
        super().__init__()
        temperature, api_key, base_url = get_conf("temperature", "openai_api_key", "openai_api_base")
        self.temperature = temperature
        self.model_name = model_name
        openai.api_key = api_key
        openai.base_url = base_url

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        print("开始调用模型")
        system_prompt, = get_conf("system_prompt")
        response = openai.chat.completions.create(
            model=self.model_name,
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "temperature": self.temperature,
            "model_name": self.model_name,
        }
    
    def _get_api_key(self) -> str:
        return self.model_name