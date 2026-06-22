# src/rag.py
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "120"
from openai import OpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from prompt_templates import RAG_PROMPT
# 直接填入你的DeepSeek密钥，不再读取.env文件
client = OpenAI(
    api_key="sk-c3aeeba06d5048ed880bc58d88f1f217",
    base_url="https://api.deepseek.com"
)
# 加载本地向量库（当前终端在ai_course_project目录，使用相对路径）
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh")
vector_db = Chroma(
    persist_directory=r"D:\应用开发技术\ai_course_project\vector_db",
    embedding_function=embeddings
)
def rag_answer(question):
    docs = vector_db.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = RAG_PROMPT.format(context=context, question=question)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
if __name__ == "__main__":
    test_questions = [
        "怎么请病假？",
        "奖学金要多少绩点？",
        "宿舍灯坏了找谁？",
        "一卡通丢了怎么办？",
        "选错了课能退吗？"
    ]
    for idx, query in enumerate(test_questions, 1):
        print(f"\n==================== 测试{idx}：{query} ====================")
        res = rag_answer(query)
        print(f"校园助手回答：{res}")