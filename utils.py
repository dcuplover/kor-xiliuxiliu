"""
本页代码为工具类的代码，包括读取配置文件、读取环境变量、读取API_KEY等功能。

读取配置文件： get_conf
读取单个配置文件： get_single_conf_with_lru_cache
读取环境变量： read_env_variable
"""
import importlib # 用于动态导入模块
import inspect # 用于获取函数的参数信息
import os # 用于读取环境变量
from functools import wraps, lru_cache # 用于缓存配置信息

def read_env_variable(name: str, default_ref):
    arg_with_prefix = "GPT_ACADEMIC_" + name 
    if arg_with_prefix in os.environ: 
        env_arg = os.environ[arg_with_prefix]
    elif name in os.environ: 
        env_arg = os.environ[name]
    else:
        raise KeyError
    
    print(f"[ENV_VAR] 尝试加载{name}，默认值：{default_ref} --> 修正值：{env_arg}")

    try:
        if isinstance(default_ref, bool):
            res = env_arg.lower() in ['true', '1', 't']
        elif isinstance(default_ref, int):
            res = int(env_arg)
        elif isinstance(default_ref, float):
            res = float(env_arg)
        elif isinstance(default_ref, str):
            res = env_arg.strip()
        elif isinstance(default_ref, list):
            res = eval(env_arg)
        elif isinstance(default_ref, dict):
            res = eval(env_arg)
        elif default_ref is None:
            assert name == "proxies"
            r = eval(env_arg)
        else:
            print(f"未知的类型{type(default_ref)}") 
            raise TypeError
    except:
        print(f"无法转换{env_arg}为{type(default_ref)}")
        raise ValueError
    return res


@lru_cache(maxsize=128)
def get_single_conf_with_lru_cache(name: str):
    name = name.upper()
    # 读取配置文件
    try:
        # 优先级1 读取环境变量
        default_ref = getattr(importlib.import_module('config'), name) # 读取默认配置，用来判断
        v = read_env_variable(name, default_ref)
    except:
        try:
            # 优先级2 读取config_private.py中的配置
            v = getattr(importlib.import_module('config_private'), name)
        except:
            # 优先级3 读取默认配置
            v = getattr(importlib.import_module('config'), name)

    return v
    

@lru_cache(maxsize=128)
def get_conf(*args):
    res = []
    for arg in args:
        # 根据配置信息名称获取单独的配置信息
        r = get_single_conf_with_lru_cache(arg)
        res.append(r)
    return res


def get_schema(schema_name):
    module = importlib.import_module(f'schemas.{schema_name}')
    schema_class = getattr(module, schema_name)
    description = getattr(module, "description")
    examples = getattr(module, "examples")
    many = getattr(module, "many")
    return schema_class, description, examples, many