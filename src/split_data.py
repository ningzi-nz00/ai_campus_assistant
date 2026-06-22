# src/split_data.py
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 1. 读取之前整理好的校园问答CSV
df = pd.read_csv(r"D:\应用开发技术\ai_course_project\data\campus_data.csv", encoding="utf-8")

# 2. 拼接每条问答为完整文本（question+answer作为待切分原文）
text_list = []
for idx, row in df.iterrows():
    full_text = f"【分类】{row['category']}\n问题:{row['question']}\n答复:{row['answer']}\n资料来源:{row['source']}"
    text_list.append(full_text)
# 合并所有问答为一整段长文本
long_text = "\n=====分割线=====\n".join(text_list)

# 3. 初始化递归文本切分器（实训给定参数）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,        # 每个文本块最大200字符
    chunk_overlap=20       # 相邻块重叠20字符，防止上下文断裂丢失信息
)

# 4. 执行切分，得到分块列表
chunks = text_splitter.split_text(long_text)

# 5. 打印测试：输出分块数量与前3块内容，验证切分效果
print(f"文本切分完成，共生成 {len(chunks)} 个文本块")
print("=====前3个文本块示例=====")
for i, chunk in enumerate(chunks[:3]):
    print(f"块{i+1}：\n{chunk}\n------------------------")