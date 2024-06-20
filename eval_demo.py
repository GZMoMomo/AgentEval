from openai import OpenAI 

client = OpenAI(
    api_key="fe5f6afae5bfffb5c4fa148b061977a1.9Ep40DMGOnBb3FTo",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
) 

my_assistant = client.beta.assistants.create(
    instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    name="Math Tutor",
    tools=[{"type": "code_interpreter"}],
    model="glm-4",
)
print(my_assistant)