from typing import Any, List, Mapping, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from zhipuai import ZhipuAI
from utils import get_conf

class ZhiPuLLM(LLM):
    api_key: str = ""
    temperature: float = 0.0
    model: str = ""
    client: ZhipuAI = None

    @property
    def _llm_type(self) -> str:
        return "ZhipuAI"

    def __init__(self, model_name: str):
        super().__init__()
        api_key, temperature = get_conf("zhipu_api_key", "temperature")
        self.api_key = api_key
        self.temperature = temperature
        self.model = model_name
        self.client = ZhipuAI(api_key=self.api_key) 
        print('初始化zhipu api')
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        print("开始调用模型")
        system_prompt, = get_conf("system_prompt")
        messages = [
            {"role":"system", "content": system_prompt},
            {"role":"user", "content": prompt},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            do_sample=True,
            temperature=self.temperature,
        )  

        return response.choices[0].message.content
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "api_key": self.api_key,
            "temperature": self.temperature,
            "model": self.model,
        }
    

        
    
