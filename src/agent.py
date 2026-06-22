# src/agent.py
import re
# 导入工具函数与RAG问答函数
from tools import get_current_week, calculate_gpa
from rag import rag_answer

def agent_chat(user_input):
    # 1. 意图识别：查询校历周数
    if "周" in user_input and ("几" in user_input or "校历" in user_input):
        return get_current_week()

    # 意图识别：计算绩点GPA
    if "绩点" in user_input or "GPA" in user_input:
        # 提取所有数字
        scores = re.findall(r'\d+', user_input)
        if scores:
            return calculate_gpa(','.join(scores))
        else:
            return "请告诉我您的各科分数，例如：85,90,78"

    # 2. 默认走RAG校园知识库问答
    return rag_answer(user_input)

# 测试入口（可选）
if __name__ == "__main__":
    print(agent_chat("现在是第几周？"))
    print(agent_chat("我的分数90,85,72，算一下绩点"))
    print(agent_chat("选错课能退吗？"))