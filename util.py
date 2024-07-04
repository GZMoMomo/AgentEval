import re 

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