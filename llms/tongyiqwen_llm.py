from typing import Any, List, Mapping, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
import dashscope
from http import HTTPStatus
from utils import get_conf

class TongyiLLM(LLM):
    dashscope_api_key: str = ""
    temperature: float = 0.1
    model_name: str = ""

    @property
    def _llm_type(self) -> str:
        return "Tongyi"

    def __init__(self, model_name: str):
        super().__init__()
        dashscope_api_key, temperature = get_conf("tongyiqwen_api_key", "temperature")
        self.dashscope_api_key = dashscope_api_key
        self.temperature = temperature
        self.model_name = model_name

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        dashscope.api_key = self.dashscope_api_key
        system_prompt, = get_conf("system_prompt")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        response = dashscope.Generation.call(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            result_format='message'
        )

        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content
        else:
            print(response)
            return ""

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "dashscope_api_key": self.dashscope_api_key,
            "temperature": self.temperature,
            "model_name": self.model_name,
        }