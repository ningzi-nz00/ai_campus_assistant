# src/agent.py
import re
from tools import get_current_week, calculate_gpa
from rag import rag_answer

# 全局列表保存完整对话历史
conversation_history = []

def agent_chat(user_input, context=None):
    # 1. 意图识别：查询校历周数（工具调用，无需历史）
    if "周" in user_input and ("几" in user_input or "校历" in user_input):
        return get_current_week()

    # 2. 意图识别：计算绩点GPA（工具调用，无需历史）
    if "绩点" in user_input or "GPA" in user_input:
        scores = re.findall(r'\d+', user_input)
        if scores:
            return calculate_gpa(','.join(scores))
        else:
            return "请告诉我您的各科分数，例如：85,90,78"

    # 3. RAG知识库问答，带上对话上下文记忆
    if context is not None and len(context) > 0:
        # 拼接历史对话给提示词，实现多轮记忆
        history_text = ""
        for msg in context:
            history_text += f"{msg['role']}: {msg['content']}\n"
        full_query = f"历史对话：\n{history_text}\n当前用户问题：{user_input}"
        return rag_answer(full_query)
    else:
        return rag_answer(user_input)

# 带对话记忆的封装函数（实训步骤3要求）
def chat_with_memory(user_input):
    # 存入用户提问
    conversation_history.append({"role": "user", "content": user_input})
    # 只保留最近5轮对话上下文
    recent_context = conversation_history[-5:]
    # 调用智能体，传入历史上下文
    response = agent_chat(user_input, context=recent_context)
    # 存入模型回答
    conversation_history.append({"role": "assistant", "content": response})
    return response

# 多轮对话测试入口
if __name__ == "__main__":
    print("===== 多轮对话记忆测试 =====")
    print("第一轮提问：现在第几周？")
    print(chat_with_memory("现在第几周？"))

    print("\n第二轮提问：我分数85,90,78，算绩点")
    print(chat_with_memory("我分数85,90,78，算绩点"))

    print("\n第三轮提问：选错课能退吗？（读取前两轮历史记忆）")
    print(chat_with_memory("选错课能退吗？"))