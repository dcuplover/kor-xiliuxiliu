# Kor-xiliuxiliu

Kor-xiliuxiliu is a text extraction tool based on langchain and kor. It is designed to extract text from various sources and provide a clean and structured output.

## Features

- Text extraction from different file formats, including PDF, Word documents, and HTML.
- Support for multiple languages, allowing extraction of text in different languages.
- Automatic language detection for efficient processing.
- Clean and structured output, removing unnecessary formatting and preserving the original document structure.

## Installation

To install Kor-xiliuxiliu, follow these steps:

1. Clone the repository: `git clone https://github.com/dcuplover/kor-xiliuxiliu.git`
2. Navigate to the project directory: `cd kor-xiliuxiliu`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage
1. 编辑config.py文件，填写必要的参数
2. 执行命令：
```bash
python get_data.py --model_name "模型名称，可以参考config" \
--schema_name "选择schema，schema文件放在schemas文件夹下" \
--data_type "url 数据类型是通过url获取"
--data "url地址"
--chunk_size "分割文本时的最大字符数"
```
DEMO
```bash
python get_data.py --model_name "gpt-3.5-turbo" \
--schema_name "PersonDialogue" \
--data_type "url" \
--data "http://www.gudianmingzhu.com/guji/hongloumeng/11369.html" \
--chunk_size 500
```

### 使用api是需要花钱的哟，各位要慎重考虑和使用。

不同模型有不同的提取效果，我测试了一些模型的提取效果，可参考
- [测试不同大模型从非结构化信息中提取结构化信息的能力](https://zhuanlan.zhihu.com/p/686858490)

## TodoList
- 支持更多的文档格式
- api
- webui
- 优化多个url文档的获取方式