from kor import create_extraction_chain
from utils import get_conf
import time
import json

def extract_content(llm, schema, texts, validator, model_name, schema_name):
    chain = create_extraction_chain(
        llm, 
        schema, 
        encoder_or_encoder_class="csv",
        input_formatter="triple_quotes",
        validator=validator,
    )

    print_prompt, extract, reverse_search, filter, save_path = get_conf("print_prompt", "extract", "reverse_search", "filter", "save_path")

    if print_prompt == True:
        print(chain.prompt.format_prompt(text="[user input]").to_string())

    all_data = []
    result_counts = {
        "total": 0,
        "success": 0,
        "fail": 0
    }

    # 判断是否执行提取
    # 如果不执行，就直接返回
    if not extract:
        return
    
    for text in texts:
        text = text.page_content
        res = chain.invoke(text)
        validated_data = res['text']['validated_data']
        for vd in validated_data:
            print(f'提取到的数据: {vd}')

            # 判断是否开启反查
            # 如果开启，就从反查模型中提取数据是否存在于text中
            # 记录反查结果
            if(reverse_search == True):
                if vd.dialogue in text:
                    result_counts["success"] += 1
                else:
                    result_counts["fail"] += 1

                result_counts["total"] += 1


            # 判断是否过滤
            # 如果过滤，就从过滤模不存在于text中的数据
            if(filter == True):
                if vd.dialogue not in text:
                    # 如果不存在，就不添加到all_data中
                    continue

            all_data.append({
                "speaker": vd.speaker,
                "dialogue": vd.dialogue,
                "action": vd.action.value
            })

        # sleep 1秒
        time.sleep(1)

    print(result_counts)

    # 当前日期字符串
    date_str = time.strftime("%Y%m%d", time.localtime())

    # 将提取的数据保存到json文件
    # 判断文件夹是否存在
    import os
    if not os.path.exists(f"{save_path}{date_str}"):
        os.makedirs(f"{save_path}{date_str}")
    
    filename = f"{save_path}{date_str}/{model_name}_{schema_name}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
