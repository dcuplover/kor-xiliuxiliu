from typing import Any, List, Mapping, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

import os
import qianfan
from utils import get_conf

class QianFanLLM(LLM):
    temperature: float = 0.1
    model_name: str = ""
    chat_comp: qianfan.ChatCompletion = None

    @property
    def _llm_type(self) -> str:
        return "QianFan"

    def __init__(self, model_name: str):
        super().__init__()
        self.temperature, = get_conf("temperature")
        self.model_name = model_name

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        print("开始调用模型")
        qianfan_access_key, qianfan_secret_key = get_conf("qianfan_access_key", "qianfan_secret_key")
        os.environ["QIANFAN_ACCESS_KEY"] = qianfan_access_key
        os.environ["QIANFAN_SECRET_KEY"] = qianfan_secret_key
        chat_comp = qianfan.Completion()
        messages = [
            {"role": "user", "content": prompt},
        ]

        response = chat_comp.do(
            model=self.model_name,
            prompt=prompt,
            temperature=self.temperature,
        )
        
        return response["body"]['result'] # response.output.choices[0].message.content

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "temperature": self.temperature,
            "model_name": self.model_name,
        }
    
    def _get_api_key(self) -> str:
        return self.model_name