import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import datetime
import os
import plotly.express as px
from langchain_community.chat_models import ChatZhipuAI
import langchain_core.prompts
import matplotlib.colors as mcolors
import whisper
import csv
import time
import plotly.express as px
import opencc  #简体字

# --- 配置 ---
st.set_page_config(page_title="梦境解析室", page_icon="🌙", layout="wide")
CSV_FILE = 'dream_log.csv'

# --- 工具函数 ---
# 繁体转简体转化器
cc = opencc.OpenCC('t2s')
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

def analyze_dream(dream_text):
    #神秘空间导入api-key
    api_key = st.secrets.get("ZHIPUAI_API_KEY")
    llm = ChatZhipuAI(model="glm-4-flash", zhipuai_api_key=api_key, temperature=0.7, streaming=True)
    prompt = langchain_core.prompts.ChatPromptTemplate.from_messages([
        ("system", """
         你是一位深谙精神分析的心理导师，请以温暖、客观且具洞察力的口吻，从以下四个维度对梦境进行深度解析：：
     1.【情绪透视】：分析梦境中核心的情绪色彩，并尝试连接我近期的现实生活，指出这些情绪可能源自何处。
    2.【意象隐喻】：挑选梦中 1-2 个最深刻的意象（如：追逐、水、高处等），探讨它们在潜意识中可能代表的心理投射（拒绝迷信的算命式解读，而是从个人成长角度分析）。
    3.【潜意识对话】：梦境试图向我传达什么隐藏的信息或未被察觉的需求？
    4.【疗愈建议】：针对梦境折射出的状态，给出一句简单、温柔的心理建设建议或行动指南。

    请用诗意且平实的语言表达，避免冗长枯燥的学术陈述,请采用流式输出。
         请在回复的最后一行，按以下格式输出一个情绪标签：【情绪标签：XX】
XX 只能是以下词汇之一：[愉悦, 焦虑, 平静, 压抑, 困惑, 期待]。
         """),
        ("user", "梦境内容：{dream}")
    ])
    return (prompt | llm).stream({"dream": dream_text})


# 提取情绪函数
def get_mood_label(text):
    import re
    match = re.search(r'【情绪标签：(.*?)】', text)
    return match.group(1) if match else "未知"


# --- 主界面 ---
tab1, tab2 = st.tabs(["✨ 梦境解析室", "📂 我的梦境库"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("✍️ 记录你的梦")
        model = load_whisper_model()
        audio_file = st.audio_input("🎙️ 点击录音")
        
        # 使用 session_state 来存储临时文本，保证可被手动清空
        if "temp_text" not in st.session_state:
            st.session_state.temp_text = ""


        if audio_file:
            with open("temp.wav", "wb") as f: f.write(audio_file.read())
            with st.spinner("识别中..."): 
                # 1. 获取原始结果
                raw_text = model.transcribe("temp.wav", language="zh")["text"]
        
                # 2. 将繁体转换为简体
                st.session_state.temp_text = cc.convert(raw_text)


        os.remove("temp.wav")
        
        # 将 value 绑定到 session_state.temp_text
        dream_input = st.text_area("梦境详情：", value=st.session_state.temp_text, height=200)
        
        # 同步更新状态（为了手动修改后也能保存）
        st.session_state.temp_text = dream_input

        if st.button("开始解析 ✨"):
            if dream_input:
                stream_generator = analyze_dream(dream_input)
                st.session_state.last_dream = dream_input
                
                # 触发 UI 更新：利用 session_state 标记解析中
                st.session_state.analysis_loading = True
                if "analysis" in st.session_state:
                    del st.session_state.analysis
                
                # 立即进入显示逻辑
            else:
                st.warning("请输入梦境内容")

    with col2:
        st.subheader("✨ 深度解析")
        with st.container(height=350, border=True):
            
            st.markdown("""<style>
                [data-testid="stVerticalBlockBorderWrapper"] { background-color: #FFF0F3; 
                        border-radius: 15px; border-color: #FFC8DD; }
            </style>""", unsafe_allow_html=True)
            
            #解析中 vs 解析后 vs 等待中
            if "analysis_loading" in st.session_state and st.session_state.analysis_loading:
                # 触发流式输出
                full_response = st.write_stream(analyze_dream(st.session_state.last_dream))
                st.session_state.analysis = full_response
                st.session_state.analysis_loading = False
                st.rerun() # 触发一次刷新以显示底下的操作按钮
            elif "analysis" in st.session_state:
                st.write(st.session_state.analysis)
            else:
                st.markdown('<div style="text-align: center; color: #FF85A1; ' \
                'padding-top: 80px;">🌙 梦境等待中...</div>', unsafe_allow_html=True)


        if "analysis" in st.session_state and not st.session_state.get("analysis_loading", False):
            st.markdown("""<div style="background-color: #FFF5F7; padding: 15px; 
                        border-radius: 15px; border: 1px dashed #FF85A1; margin-top: 10px;">
                        <p style="color: #FF758F; font-size: 0.9em; margin-bottom: 5px;">
                        <b>💡 心情定格</b></p>
                        <p style="font-size: 0.8em; color: #888;">
                        记录这一刻的情绪，让 AI 更好地理解你的梦境轨迹。</p>
                    </div>""", unsafe_allow_html=True)

            if "analysis" in st.session_state:
                st.divider()
                st.subheader("💬 与导师对话")
    
                # 初始化聊天历史
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = [{"role": "assistant", "content": "关于这个梦，你还有什么想深入聊聊的吗？"}]

                # 显示聊天记录
                for msg in st.session_state.chat_history:
                    st.chat_message(msg["role"]).write(msg["content"])

                # 聊天输入框
                if prompt := st.chat_input("追问一下你的导师..."):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    st.chat_message("user").write(prompt)
        
                    with st.chat_message("assistant"):
                    # 注意传入上下文（梦境原文 + AI解析结果 + 追问）
                        context = f"梦境原文：{st.session_state.last_dream}\nAI之前的解析：{st.session_state.analysis}"
                        # 流式调用
                        api_key = st.secrets.get("ZHIPUAI_API_KEY")
                        llm=ChatZhipuAI(model="glm-4-flash", zhipuai_api_key=api_key, temperature=0.7, streaming=True)
                        response = st.write_stream(llm.stream(f"{context}\n用户追问：{prompt} 字数控制在100字以内。"))
                        st.session_state.chat_history.append({"role": "assistant", "content": response})

            mood = st.slider("这一刻，心情如何？", 0, 10, 5)
            if st.button("💾 归档此梦"):
                new_data = pd.DataFrame([{"时间": datetime.datetime.now(), 
                                          "梦境": st.session_state.last_dream, 
                                          "AI解析": st.session_state.analysis, 
                                          "情绪得分": mood}])
                new_data.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False, quoting=csv.QUOTE_ALL)
                st.success("已归档！")
                st.session_state.temp_text = ""
                del st.session_state.analysis
                del st.session_state.last_dream
                time.sleep(1)
                st.rerun()

with tab2:
    st.header("📂 梦境历史档案")
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, engine='python', on_bad_lines='skip')
        df['时间'] = pd.to_datetime(df['时间'], format='mixed')
        df["删除?"] = False
        # 只在表格显示部分核心信息
        display_df = df[['时间', '梦境', '情绪得分']].copy()
        display_df["删除?"] = False
        
        #选择一行
        edited_df = st.data_editor(
            display_df, 
            column_config={
                "梦境": st.column_config.TextColumn("梦境", width="medium"),
                "时间": st.column_config.DatetimeColumn("时间", format="YYYY/MM/DD HH:mm")
            },
            hide_index=True, 
            use_container_width=True
        )
        
        #获取用户选中的行（如果有点击选择）
        #selectbox 选择查看
        selected_index = st.selectbox("选择一条梦境查看完整解析：", df.index, format_func=lambda x: f"{df.loc[x, '时间']} - {df.loc[x, '梦境'][:15]}...")
        
        if selected_index is not None:
            st.divider()
            st.subheader("📖 梦境深度解析预览")
            # 使用带有边框的容器，美化显示
            with st.container(border=True):
                st.markdown(f"**时间**：{df.loc[selected_index, '时间']}")
                st.markdown(f"**梦境**：{df.loc[selected_index, '梦境']}")
                st.markdown("---")
                #渲染详细的解析内容
                st.markdown(df.loc[selected_index, 'AI解析'].replace(chr(10), 
                '<br>'), unsafe_allow_html=True)
        
        if st.button("🚀 保存删除操作"):
            remaining_df = df[edited_df["删除?"] == False]
            remaining_df.to_csv(CSV_FILE, index=False, quoting=csv.QUOTE_ALL)
            st.rerun()
        
        st.divider()
        st.subheader("📊 情绪波动轨迹")
        st.line_chart(df.set_index('时间')['情绪得分'], color="#FF85A1")
    else:
        st.info("暂无历史记录。")
        st.divider()
    st.subheader("☁️ 潜意识关键词云")
    
    if len(df) > 0:
        # 将梦境内容和解析内容合并
        all_text = " ".join(df['梦境'].astype(str)) + " " + " ".join(df['AI解析'].astype(str))
        
        try:
            wc = WordCloud(
                font_path=r"C:\Windows\Fonts\msyh.ttc", 
                width=800, height=400, 
                background_color="white",
                colormap="magma"
            ).generate(all_text)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        except Exception:
            st.warning("词云生成失败，请确认系统是否有中文字体文件。")
    else:
        st.write("暂无足够数据生成词云。")


    if len(df) > 0:
        df['情绪标签'] = df['AI解析'].apply(get_mood_label)
        mood_counts = df['情绪标签'].value_counts()
        fig = px.pie(values=mood_counts, names=mood_counts.index, title="近期梦境情绪分布", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)