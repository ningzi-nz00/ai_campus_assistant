# ========== 最顶部 基础导入与容错 ==========
import streamlit as st
import os

# 容错导入向量库构建函数
try:
    from build_vector_db import build_vector_store
except Exception:
    def build_vector_store():
        pass

# 自动创建向量库（相对路径，本地云端通用）
if not os.path.exists(r"D:\应用开发技术\ai_course_project\vector_db"):
    with st.spinner("正在初始化校园知识库，首次加载稍慢..."):
        build_vector_store()

# 密钥读取（标准正确写法）
if "DEEPSEEK_API_KEY" in st.secrets:
    DEEPSEEK_API_KEY = st.secrets["sk-c3aeeba06d5048ed880bc58d88f1f217"]
else:
    DEEPSEEK_API_KEY = os.getenv("sk-c3aeeba06d5048ed880bc58d88f1f217")

# ========== 页面全局美化配置 ==========
st.set_page_config(
    page_title="校园生活百事通助手",
    page_icon="🏫",
    layout="wide",  # 宽屏布局，更大显示区域
    initial_sidebar_state="expanded"
)

# 自定义全局CSS美化：圆角、阴影、配色、输入框样式
st.markdown("""
<style>
/* 整体页面背景 */
.main {
    background-color: #f8f9fa;
}
/* 标题样式 */
h1 {
    color: #2b54aa;
    text-align: center;
    padding: 10px 0;
}
/* 聊天消息卡片 */
.stChatMessage {
    border-radius: 16px !important;
    padding: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
/* 用户气泡浅蓝色 */
.stChatMessage.user {
    background-color: #e8f0fe !important;
}
/* 助手气泡浅绿 */
.stChatMessage.assistant {
    background-color: #f0fdf4 !important;
}
/* 底部输入框美化 */
.stChatInput {
    border-radius: 24px !important;
    padding: 8px 16px !important;
}
/* 侧边栏卡片 */
.sidebar-card {
    background: white;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ========== 侧边栏（美化功能面板） ==========
with st.sidebar:
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.subheader("🏫 校园百事通 使用说明")
    st.divider()
    st.markdown("""
    你可以咨询以下校园相关问题：
    - 食堂、宿舍、教学楼位置
    - 选课、考试、教务流程
    - 社团、活动、校园设施
    - 快递、医务室、图书馆开放时间
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.subheader("💡 小提示")
    st.info("首次打开会加载知识库，请耐心等待几秒再提问！")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.caption("AI校园问答助手 | 基于DeepSeek大模型")

# ========== 主页面标题与分割线 ==========
st.title("🏫 校园生活百事通助手")
st.divider()
st.markdown("<p style='text-align:center;color:#666'>一站式解答校园生活、教务、设施各类问题</p>", unsafe_allow_html=True)
st.divider()

# ========== 聊天会话初始化 ==========
if "messages" not in st.session_state:
    st.session_state.messages = [
        # 开场欢迎话术
        {"role": "assistant", "content": "你好！我是校园百事通🏫，有任何校园相关问题都可以问我～"}
    ]

# 渲染历史聊天记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========== 底部聊天输入框 ==========
if prompt := st.chat_input("输入你的校园问题，例如：图书馆几点关门？"):
    # 保存并展示用户提问
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 加载动画 + 调用AI回答
    with st.chat_message("assistant"):
        with st.spinner("正在检索校园知识库，思考回答中..."):
            from agent import agent_chat
            response = agent_chat(prompt)
        st.markdown(response)
    # 保存助手回复
    st.session_state.messages.append({"role": "assistant", "content": response})
