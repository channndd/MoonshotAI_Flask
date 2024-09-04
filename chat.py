from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key = "sk-4vTwJRJOEQsuA0AHUQB7ICHuC6XMNvwNt06Db4vpdUPG3KgW",
    base_url = "https://api.moonshot.cn/v1",
)

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

# 只保留最近几轮对话
def manage_history(history):
    if len(history) > 25:
        history = history[:1] + history[-20:]  # 保留最近的20轮对话
    return history

# 确保总输入内容不超过20万字
def check_content_length(history):
    max_length = 200000  # 20万字
    total_length = sum(len(entry["content"]) for entry in history)
    if total_length > max_length:
        # 从最早的对话开始删除，直到总长度小于等于20万字
        for entry in history[:-1]:  # 保留最近的一轮对话
            total_length -= len(entry["content"])
            history.remove(entry)
            if total_length <= max_length:
                break
    return history

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
    history = check_content_length(history)
    response, history = chat(user_message, history)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run()