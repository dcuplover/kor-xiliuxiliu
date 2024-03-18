"""
分为4步
1. 根据用户选择的模型，生成llm对象
2. 设置Schema和验证规则
3. 获取需要被提取的内容以及分割字符数
4. 提取内容
"""
from llm import get_llm
from schema import get_schema_and_validator
from text import get_text
from extract import extract_content
import os

import argparse

# 创建解析器
parser = argparse.ArgumentParser(description='Process some data.')

# 添加参数
parser.add_argument('--model_name', type=str, required=True, default='qwen-72b-chat', help='模型名称')
parser.add_argument('--schema_name', type=str, required=True, default='PersonDialogue', help='Schema名称')
parser.add_argument('--data_type', type=str, required=True, default='url', help='数据类型')
parser.add_argument('--data', type=str, required=True, default='', help='数据')
parser.add_argument('--chunk_size', type=int, required=True, default=500, help='分割字符数')

# 解析参数
args = parser.parse_args()

os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['ALL_PROXY'] = ''
os.environ['all_proxy'] = ''

# 1. 根据用户选择的模型，生成llm对象
model_name = args.model_name
llm = get_llm(model_name)

schema_name = args.schema_name

# 2. 设置Schema和验证规则
schema, validator = get_schema_and_validator(schema_name=schema_name)

# 3. 获取需要被提取的内容以及分割字符数
data_type = args.data_type # 选择数据类型, text、 file、 url
data = args.data # 数据
chunk_size = args.chunk_size # 分割字符数
texts = get_text(data_type, data, chunk_size) # 获取需要被提取的内容以及分割字符数

# 4. 提取内容
extract_content(llm=llm, schema=schema, texts=texts, validator=validator, model_name=model_name, schema_name=schema_name)

