'''
interlm2的llm类
'''
from typing import Any, List, Mapping, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

from modelscope import snapshot_download, AutoTokenizer, AutoModelForCausalLM

from langchain_core.messages import HumanMessage, SystemMessage
from utils import get_conf

class InterLM2LLM(LLM):
    tokenizer : AutoTokenizer = None
    model : AutoModelForCausalLM = None

    @property
    def _llm_type(self) -> str:
        return "interlm2"
    
    def __init__(self, model_name :str):
        super().__init__()
        print("正在从本地加载模型...")
        cache_dir, = get_conf("model_cache_dir")
        model_dir = snapshot_download(model_id=model_name, local_files_only=True, cache_dir=cache_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True)
        # 将代码设置为评估模式
        self.model = self.model.eval()
        print("完成本地模型的加载")
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        print("开始调用模型")
        # 重写调用函数
        system_prompt, = get_conf("system_prompt")
        messages = [(system_prompt, '')]
        response, history = self.model.chat(self.tokenizer,prompt,history=messages)
        print(response)
        return response
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": self.model, "tokenizer": self.tokenizer}