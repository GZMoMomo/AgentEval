import csv
import openai

# 使用你的API密钥和基础URL初始化OpenAI客户端
openai.api_key = "fe5f6afae5bfffb5c4fa148b061977a1.9Ep40DMGOnBb3FTo"
openai.base_url = "https://open.bigmodel.cn/api/paas/v4/"

def load_prompts(file_path):
    prompts = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            prompts.append((row['prompt'].strip(), row['expected_output'].strip()))
    return prompts

def evaluate_model(prompt):
    print(1)
    return False

def evaluate_prompt(prompts):
    correct = 0
    total = len(prompts)

    for prompt, expected_output in prompts:
        response = openai.chat.completions.create(
            model="glm-4",  
            messages=[    
                {"role": "system", "content": "你是一个智能助手,用json格式回复"},    
                {"role": "user", "content": f"{prompt}"} 
            ],
            top_p=0.7,
            temperature=0.9,
            max_tokens=50,
            response_format={ "type": "json_object" }
        )
        output = response.choices[0].message.content

        if evaluate_model:
            correct += 1
        
        print(f"提示: {prompt}")
        print(f"期望输出: {expected_output}")
        print(f"实际输出: {output}")
        print()

    accuracy = correct / total
    print(f"准确率: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    prompts = load_prompts('prompts.csv')
    evaluate_prompt(prompts)
