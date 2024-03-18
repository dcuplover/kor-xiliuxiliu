from langchain_core.language_models.llms import LLM
from utils import get_conf

from llms import InterLM2LLM, TongyiLLM, OpenAILLM, QianFanLLM, ZhiPuLLM

def get_llm(model_name: str) -> LLM:
    # 根据模型名字判断使用的哪个平台
    model_name = model_name.lower()
    platform_list, = get_conf("platform_list")
    print(platform_list)
    if model_name in platform_list['tongyi']:
        return TongyiLLM(model_name)
    elif model_name in platform_list['zhipu']:
        return ZhiPuLLM(model_name)
    elif model_name in platform_list['qianfan']:
        return QianFanLLM(model_name)
    elif model_name in platform_list['openai']:
        return OpenAILLM(model_name)
    elif model_name in platform_list['internlm2']:
        return InterLM2LLM(model_name)
    else:
        raise ValueError(f"Unsupported model name: {model_name}")

