# src/app.py
import streamlit as st
# 导入智能体对话函数
from agent import agent_chat

# 页面基础配置
st.set_page_config(page_title="校园百事通", page_icon="🏫")
st.title("🏫 校园生活百事通助手")

# 初始化会话存储聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 循环渲染历史所有聊天消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 底部聊天输入框
if prompt := st.chat_input("问点校园问题..."):
    # 保存并展示用户提问
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 调用智能体获取回答
    with st.chat_message("assistant"):
        response = agent_chat(prompt)
        st.markdown(response)
    # 保存助手回复到会话历史
    st.session_state.messages.append({"role": "assistant", "content": response})