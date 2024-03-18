PLATFORM_LIST = {
    "tongyi": ["qwen-max", "qwen-max-1201", "qwen-plus", "qwen-turbo", "qwen-72b-chat"],
    "zhipu": ["glm-3-turbo", "glm-4"],
    "qianfan": ["Mixtral-8x7B-Instruct", "Yi-34B-Chat"],
    "openai": ["gpt-3.5-turbo", "gpt-4"],
    "internlm2": [""],
}

# 是否反查提取的内容是否存在于原文中
REVERSE_SEARCH = True

# 是否过滤不存在于原文中的内容
FILTER = True

# 是否打印Prompt
PRINT_PROMPT = True

# 是否执行提取
EXTRACT = True

# 保存生成的文件的路径
SAVE_PATH = "./output/"

# temperature
TEMPERATURE = 0.1

# system prompt
SYSTEM_PROMPT = "你作为一个文本信息提取系统，你的任务是从下面的对话中提取出对话者和对话内容。"

# tongyiQwen
TONGYIQWEN_API_KEY = ""

# zhipu config
ZHIPU_API_KEY = ""

# qianfan config
QIANFAN_ACCESS_KEY = ""
QIANFAN_SECRET_KEY = ""

# openai config
OPENAI_API_KEY = ""
OPENAI_API_BASE = ""

# internlm2 config
# cache_dir
MODEL_CACHE_DIR = "/data/models/"




