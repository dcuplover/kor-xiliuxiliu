'''
pip install playwright
pip install openai
'''
import os

from langchain_community.document_loaders import PlaywrightURLLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from pydantic import BaseModel, Field, validator
from kor import extract_from_documents, from_pydantic, create_extraction_chain

# openai
from llms.openai_llm import OpenAILLM

# 智谱AI
from llms.zhipu_llm import ZhiPuLLM

# 使用通义千问模型
from llms.tongyiqwen_llm import TongyiLLM

# 使用qianfan
from llms.qianfan_llm import QianFanLLM


import enum

os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['ALL_PROXY'] = ''
os.environ['all_proxy'] = ''
model = 'qwen-72b-chat'
'''
# model = "glm-3-turbo"
model = "glm-3-turbo"

llm = ZhiPuLLM(
    temperature=0.1,
    api_key="dc9141e5280fa99259d9fc186614e466.iaz7285XLLfYM9Zv",
    model=model,
)

llm = OpenAILLM(
    openai_api_key="sk-vbZ36nHdIh6YHXX108C96aD1D2C54a66B446C2A8Ea8a4f3c",
    temperature=0.1,
    model_name=model,
    openai_api_base="https://4.0.wokaai.com/v1/"
)

llm = QianFanLLM(
    temperature=0.1,
    model_name=model,
)
'''

llm = TongyiLLM(
    dashscope_api_key="sk-3cccbc1f76214787af188697575af612",
    temperature=0.1,
    model_name=model,
)

class Action(enum.Enum):
    SAY = "对话"
    THINK = "独白"

# 设置Schema
class PersonDialogue(BaseModel):
    speaker: str = Field(
        description="对话的发起者，说话的人，或者发出内心独白的人。",
        examples=[
            ("黛玉忙止道：“罢了，此刻夜深，明日再看也不迟。”大家又叙了一回，方才安歇。", "黛玉"),
            ("雨村听了大怒道：“岂有这样放屁的事！打死人命就白白的走了，再拿不来的！”因发签差公人立刻将凶犯族中人拿来拷问，令他们实供藏在何处，一面再动海捕文书。", "雨村"),

        ],
    )
    dialogue: str = Field(
        description="对话内容或者内心独白。",
        examples=[
            ("黛玉忙止道：“罢了，此刻夜深，明日再看也不迟。”大家又叙了一回，方才安歇。", "罢了，此刻夜深，明日再看也不迟。大家又叙了一回，方才安歇。"),
            ("雨村听了大怒道：“岂有这样放屁的事！打死人命就白白的走了，再拿不来的！”因发签差公人立刻将凶犯族中人拿来拷问，令他们实供藏在何处，一面再动海捕文书。", "岂有这样放屁的事！打死人命就白白的走了，再拿不来的！因发签差公人立刻将凶犯族中人拿来拷问，令他们实供藏在何处，一面再动海捕文书。"),
        ]
    )
    action: Action = Field(
        description="对话的类型，是对话还是内心独白。",
        examples=[
            ("子兴道：“邪也罢，正也罢，只顾算别人家的帐，你也吃一杯酒才好。”", "对话"),
            ("黛玉心中正疑惑着：“这个宝玉，不知是怎生个惫人物，懵懂顽童？－－倒不见那蠢物也罢了“", "独白"),
        ]
    )

    @validator("speaker")
    def speaker_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("speaker must not be empty")
        return v
    
    @validator("dialogue")
    def dialogue_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("dialogue must not be empty")
        return v

# 生成schema, validator
schema, validator = from_pydantic(
    PersonDialogue,
    description="红楼梦对话提取，提取红楼梦中的对话和独白，输出说话人，对话内容，对话类型。",
    many=True,
    examples=[(
        """雨村笑道：“我如何得知。”门子冷笑道：“这人算来还是老爷的大恩人呢！
        他就是葫芦庙旁住的甄老爷的小姐，名唤英莲的。”雨村罕然道：“原来就是他！闻得养至五岁被人拐去，却如今才来卖呢？”
        雨村听了，亦叹道：“这也是他们的孽障遭遇，亦非偶然。不然这冯渊如何偏只看准了这英莲？这英莲受了拐子这几年折磨，才得了个头路，且又是个多情的，若能聚合了，倒是件美事，偏又生出这段事来。这薛家纵比冯家富贵，
        想其为人，自然姬妾众多，淫佚无度，未必及冯渊定情于一人者。这正是梦幻情缘，恰遇一对薄命儿女。且不要议论他，只目今这官司，如何剖断才好？”
        门子笑道：“老爷当年何其明决，今日何反成了个没主意的人了！小的闻得老爷补升此任，亦系贾府王府之力，此薛蟠即贾府之亲，老爷何不顺水行舟，作个整人情，
        将此案了结，日后也好去见贾府王府。”
        """,
        [
            {
                "speaker": "雨村",
                "dialogue": "我如何得知。",
                "action": "对话"
            },
            {
                "speaker": "门子",
                "dialogue": "这人算来还是老爷的大恩人呢！他就是葫芦庙旁住的甄老爷的小姐，名唤英莲的。",
                "action": "对话"
            },
            {
                "speaker": "雨村",
                "dialogue": "原来就是他！闻得养至五岁被人拐去，却如今才来卖呢？",
                "action": "对话"
            },
            {
                "speaker": "雨村",
                "dialogue": "这也是他们的孽障遭遇，亦非偶然。不然这冯渊如何偏只看准了这英莲？这英莲受了拐子这几年折磨，才得了个头路，且又是个多情的，若能聚合了，倒是件美事，偏又生出这段事来。这薛家纵比冯家富贵，想其为人，自然姬妾众多，淫佚无度，未必及冯渊定情于一人者。这正是梦幻情缘，恰遇一对薄命儿女。且不要议论他，只目今这官司，如何剖断才好？",
                "action": "对话"
            },
            {
                "speaker": "门子",
                "dialogue": "老爷当年何其明决，今日何反成了个没主意的人了！小的闻得老爷补升此任，亦系贾府王府之力，此薛蟠即贾府之亲，老爷何不顺水行舟，作个整人情，将此案了结，日后也好去见贾府王府。",
                "action": "对话"
            },
        ]
    )],
)

# 获取文章内容
urls = [
    "http://www.gudianmingzhu.com/guji/hongloumeng/11369.html"
]

# 设置过滤器
loader = PlaywrightURLLoader(urls, remove_selectors=[
    "#topbanner", 
    "#menu",
    ".weizhi", 
    ".right", 
    ".djpagecon", 
    ".footer", 
    ".pre", 
    ".ml", 
    ".next",
    ".rblock",
    ".rblock",
    ".guide"
])

data = loader.load()

# 将文章分割成段落
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=500,
    chunk_overlap=0,
)

data = text_splitter.split_documents(data)

# 从每个段落中提取文本
chain = create_extraction_chain(
    llm, 
    schema, 
    encoder_or_encoder_class="csv",
    input_formatter="triple_quotes",
    validator=validator,
)

'''
print(chain.prompt.format_prompt(text="[user input]").to_string())
print(data[0])
'''

all_data = []

'''
res = chain.invoke(data[0].page_content)

validated_data = res['text']['validated_data']
print(validated_data)
'''

for d in data:
    res = chain.invoke(d.page_content)
    validated_data = res['text']['validated_data']
    print(res)
    print(validated_data)
    for vd in validated_data:
        all_data.append({
            "speaker": vd.speaker,
            "dialogue": vd.dialogue,
            "action": vd.action.value
        })
    
    # sleep 1秒
    import time
    time.sleep(1)
    

# 将提取的数据保存到json文件
import json
filename = f"person_dialogue_{model}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

