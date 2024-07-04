import csv
import openai
import json
import re 
import requests

# 使用你的API密钥和基础URL初始化OpenAI客户端
openai.api_key = "fe5f6afae5bfffb5c4fa148b061977a1.9Ep40DMGOnBb3FTo"
openai.base_url = "https://open.bigmodel.cn/api/paas/v4/"
model = "glm-4"
host = "https://uat.agentspro.cn"
uuid = "6c3408b7f41946b4bb4a3e1095ac12c6"
auth_key = "6c3408b7f41946b4bb4a3e1095ac12c6"
auth_secret = "PygRQ2d5sUOOHxqt5VToeIVDA4N9Nh1H"

def load_prompts(file_path):
    prompts = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            prompts.append((row['prompt'].strip(), row['expected_output'].strip()))
    return prompts

def extract_json(text):
    if "```json" in text:
        pattern = re.compile(r'```json(.*?)\```', re.DOTALL)
        match = pattern.search(text.replace('\n',''))
        if match:
            return match.group(1)  # 返回匹配的JSON字符串
        else:
            return text  # 如果没有找到匹配的模式，则返回None
    else:
        return text

def evaluate_model(actual_output,expected_output):
    system_prompt = """
    # Role：文本内容一致性分析师

    ## Background：
    在自然语言处理领域，文本内容的对比分析是一个常见的任务，用于判断两个文本是否表达相同的信息。

    ## Attention：
    成功的文本匹配不仅需要对比直接的文字相似性，还要能够识别语义的一致性，即便面对语法或表达形式的差异。这是一项挑战但同时也非常关键的任务。

    ## Profile：
    - Language: 中文
    [描述]: 作为一个文本内容一致性分析师，专门帮助解决文本相似度判别问题，使用自然语言处理技术评估两段文本在语义上的相关性。

    ### Skills:
    - 丰富的自然语言处理知识，包括但不限于文本挖掘、语义分析和机器学习。
    - 能够处理和分析大量的文本数据，并从中提取有用信息。
    - 熟练操作多种文本相似度测试方法，包括余弦相似性、Jaccard相似性等。

    ## Goals:
    - 分析给定的两段文本，确定它们是否在内容上相符。
    - 输出一个结构化的json格式结果，明确表示文本一致性判定。

    ## Constrains:
    - 必须仅仅基于提供的文本内容来做出判断，不得引入外部信息。
    - 输出结果必须是json格式，确保数据的可用性和一致性。

    ## Workflow:
    1. 接收并读取两段文本输入,<文本1> </文本1>和<文本2> </文本2>。
    2. 应用文本相似度对比两段文本。
    3. 根据结果判定两文本是否内容相符。
    4. 封装判定结果到json格式，输出。

    ## OutputFormat:
    - 所有输出必须为json格式，确保数据结构的正确性和兼容性。
    - 明确指出result字段为最终判定结果。
    { "result": "True" } 或 { "result": "False" }
    """

    user_prompt = f"""
    <文本1>{actual_output}</文本1>
    <文本2>{expected_output}</文本2>
    """
    response = openai.chat.completions.create(
        model= model,
        messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content":user_prompt}
        ],
        top_p=0.7,
        temperature=0.9,
        response_format= { "type": "json_object" }
    )
    meassage = response.choices[0].message.content

    json_str = extract_json(meassage)
    try:
        bollean = json.loads(json_str)['result']
    except Exception as e:
        print(f"模型没有正确输出json格式，模型输出：{json_str}")
        return False
    return bollean

def chat_model(prompt,model):
    response = openai.chat.completions.create(
        model= model,
        messages=[
            {"role":"system", "content":"i am llm model"},
            {"role":"user", "content":prompt}
        ],
        top_p=0.7,
        temperature=0.9
    )
    return response.choices[0].message.content

def api_model(host,uuid,authKey,authSecret,prompt):
    url = host+"/openapi/agent/chat/completions/v1"
    headers = {
        "Authorization": f"Bearer {authKey}.{authSecret}"
    }
    body = {
        "agentId": f"{uuid}",
        "chatId": None,
        "userChatInput": f"{prompt}",
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, json=body)

    # 检查响应状态码
    if response.status_code == 200:
        print("Request successful")
        data = response.json()
        str = data["choices"][0]["content"]
        print("Response data:", str)
    else:
        print("Request failed")
        print("Status code:", response.status_code)
        print("Response:", response.text)

def evaluate_prompt(prompts, model):
    correct = 0
    total = len(prompts)

    with open('evaluation_results.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入CSV文件的头部
        writer.writerow(["提示", "期望输出", "实际输出", "模型评估"])
        
        for prompt, expected_output in prompts:
            output = chat_model(prompt, model)
            boolean = evaluate_model(output, expected_output)
            if boolean == "True":
                correct += 1
            
            # 写入每一行数据到CSV文件
            writer.writerow([prompt, expected_output, output, boolean])
            
            # 打印到控制台
            print("------------------------------------")
            print(f"提示: {prompt}")
            print(f"期望输出: {expected_output}")
            print(f"实际输出: {output}")
            print(f"模型评估: {boolean}")
            print()

    accuracy = correct / total
    print(f"准确率: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    prompts = load_prompts('prompts.csv')
    # evaluate_prompt(prompts,model)
    api_model(host,uuid,auth_key,auth_secret,prompt="1")
