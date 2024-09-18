from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)




def get_api_key():
    # 1. 首先尝试从环境变量获取API密钥
    api_key = os.getenv("MOONSHOT_API_KEY")
    
    # 2. 如果环境变量中没有找到，则尝试加载.env文件并再次获取
    if api_key is None:
        load_dotenv()
        api_key = os.getenv("MOONSHOT_API_KEY")
    
    # 3. 如果仍然没有找到API密钥，抛出异常
    if api_key is None:
        raise ValueError("MOONSHOT_API_KEY not found in environment variables or .env file")
    
    return api_key

try:
    client = OpenAI(
        api_key=get_api_key(),
        base_url="https://api.moonshot.cn/v1"
    )
except ValueError as e:
    print(f"Error: {e}")
    exit(1)

# client = OpenAI(
#     # 你可以直接设置api_key
#     # api_key = "$MOONSHOT_API_KEY",
#     # or
#     # 我们会从环境变量中获取 MOONSHOT_DEMO_API_KEY 的值作为 API Key，
#     # 请确保你已经在环境变量中正确设置了 MOONSHOT_DEMO_API_KEY 的值
#     api_key=os.environ["MOONSHOT_API_KEY"],
#     base_url = "https://api.moonshot.cn/v1",
# )

first_prompt = """
▎角色扮演
你是一个AI助手，名字为Moon-Chan，擅长从基本原理和常识出发，推演问题解决思路。

▎基本信息
- 作者: chan
- 版本: 0.2
- LLM: Moon-Chan
- 描述: 利用AI的强大分析能力，帮助用户解决问题。

▎激灵起来
你作为AI助手，拥有广泛的知识和信息处理能力。你会利用这些能力，帮助用户进行问题分析和解决。

▎限制条件
- 每次思考之前，先理解用户的需求
- 思考时不要着急，一步步思考，慢慢来，想透彻
- 只输出与用户问题相关的内容，不要输出多余的解释说明语句

▎擅长技能
- 逻辑推理：从问题出发，运用逻辑推理找到解决方案
- 数据分析：利用数据分析技能，提取关键信息
- 跨学科知识：结合不同学科的知识，提供全面的解决方案
- 简洁表达：用简洁明了的语言，向用户解释复杂问题

▎表述语气
理性、清晰、专业

▎价值观念
1. 用户至上：始终以用户的需求为中心
2. 效率优先：提供快速、有效的解决方案
3. 持续学习：不断学习新知识，提升解决问题的能力
4. 创新思维：鼓励创新，不断寻找更好的解决方案

▎工作流程
你会遵守以下流程来和用户交互：
1. 理解：仔细理解用户的问题和需求
2. 分析：运用逻辑推理和数据分析技能，分析问题
3. 解决：提供解决方案或建议
4. 反馈：根据用户的反馈，调整解决方案

▎开场对白
以如下开场白和用户开启对话：
"你好，我是Moon-Chan，我可以帮你解决问题，请问有什么可以帮到你？"
"""

history = [{"role": "system", "content": f"{first_prompt}"}]

def manage_history(history):
    """
    仅保留最近几轮对话。
    
    :param history: 对话历史记录列表
    :return: 处理后的对话历史记录列表
    """
    try:
        if not isinstance(history, list):
            raise ValueError("history must be a list")
        
        if len(history) > 25:
            history = history[-21:]  # 保留最近的20轮对话
        elif len(history) == 0:
            history = []  # 显式处理空列表的情况
        
        return history
    except Exception as e:
        print(f"Error: {e}")
        return []

def chat(query, history):
    history.append({
        "role": "user",
        "content": query
    })
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=history,
        temperature=0.3,
    )
    result = completion.choices[0].message.content
    history.append({
        "role": "assistant",
        "content": result
    })
    return result, history

# 渲染聊天界面
@app.route('/')
def chat_page():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_with_ai():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    global history
    history = manage_history(history)
    response, history = chat(user_message, history)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run()