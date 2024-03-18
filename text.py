from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PlaywrightURLLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


import os

def get_text(data_type, data, chunk_size):
    if data_type == "text":
        data = get_text_content(data)
    elif data_type == "file":
        data = read_file(data)
    elif data_type == "url":
        data = data.split(',')
        data = get_url_content(data)
    else:
        raise ValueError(f"未知的数据类型{data_type}")
    
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=chunk_size,
        chunk_overlap=0,
    )

    data = text_splitter.split_documents(data)
    return data


def get_text_content(data):
    return '' 

def read_file(filename):
    # 获取filename的扩展名
    _, ext = os.path.splitext(filename)

    if ext == ".csv":
        return CSVLoader(file_path=filename).load()
    elif ext in [".docx", ".doc"]:
        return Docx2txtLoader(file_path=filename).load()
    elif ext == ".json":
        return JSONLoader(file_path=filename).load()
    elif ext == ".pdf":
        return PyPDFLoader(filename).load()
    elif ext == ".md":
        return UnstructuredMarkdownLoader(filename).load()
    elif ext == ".txt":
        return UnstructuredFileLoader(filename).load()
    else:
        # 提示错误
        raise ValueError(f"未知的文件类型{ext}")


def get_url_content(urls):
    if(len(urls) == 0):
        return ""
    
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
    return loader.load()