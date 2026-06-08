import streamlit as st
import requests
import json

# 設定頁面
st.set_page_config(
    page_title="分類問答 AI",
    page_icon="🤖",
    layout="wide"
)

# 自訂 CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(145deg, #1e2b3c 0%, #0f1a24 100%);
    }
    .chat-container {
        background: linear-gradient(135deg, #ffffff 0%, #fef5e6 100%);
        border-radius: 2rem;
        padding: 1.5rem;
        min-height: 400px;
        box-shadow: 0 20px 30px rgba(0,0,0,0.2);
    }
    .user-message {
        background: #4a6e3b;
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        text-align: right;
    }
    .ai-message {
        background: #ece3d0;
        color: #2d3e2b;
        padding: 0.8rem 1.2rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        border-left: 4px solid #f4b942;
    }
    .category-badge {
        background: #2c5f2d;
        padding: 0.5rem 1.2rem;
        border-radius: 40px;
        color: #ffefcf;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .stButton button {
        background: #f4b942;
        color: #1e2c1c;
        border-radius: 3rem;
        font-weight: bold;
    }
    .stTextInput input {
        border-radius: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ======================= 可用分類（去除無用的） =======================
CATEGORIES = [
    "交通設施",
    "場所/地點", 
    "交通相關",
    "日常用品",
    "安全用品",
    "辦公用品",
    "公共設施",
    "自然現象",
    "電子產品",
    "證件文件",
    "廚房用品"
]

# 初始化 session state
if "current_category" not in st.session_state:
    st.session_state.current_category = "交通設施"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# 標題
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #f4b942;">🤖 點擊分類問AI</h1>
    <p style="color: #ffefcf;">選擇分類 → 輸入物品/名詞 → AI 回答是否屬於這個分類</p>
</div>
""", unsafe_allow_html=True)

# 兩欄佈局
left_col, right_col = st.columns([1.2, 2.2], gap="large")

# ======================= 左側：分類選單 =======================
with left_col:
    st.markdown("### 📂 選擇分類")
    st.markdown("點擊分類，AI 會以這個分類為標準來回答")
    
    for cat in CATEGORIES:
        is_active = (st.session_state.current_category == cat)
        button_type = "primary" if is_active else "secondary"
        
        if st.button(cat, key=f"cat_{cat}", use_container_width=True, type=button_type):
            if st.session_state.current_category != cat:
                st.session_state.current_category = cat
                # 切換分類時，加入系統提示訊息
                st.session_state.messages.append({
                    "role": "system",
                    "content": f"現在開始，請根據「{cat}」這個分類來回答使用者的問題。"
                })
                st.rerun()
    
    st.markdown("---")
    st.markdown("### ⚙️ API 設定")
    
    # 選擇 AI 服務商
    api_provider = st.selectbox(
        "選擇 AI 服務",
        ["OpenAI (GPT-3.5/GPT-4)", "Google Gemini", "自訂 API"]
    )
    
    # API Key 輸入
    api_key_input = st.text_input(
        "API Key",
        type="password",
        placeholder="請輸入您的 API Key",
        value=st.session_state.api_key
    )
    if api_key_input:
        st.session_state.api_key = api_key_input
    
    st.caption("💡 提示：需要有效的 API Key 才能使用 AI 回答功能")
    st.caption("📌 分類範圍：交通設施、場所地點、日常用品、安全用品、辦公用品、公共設施、自然現象、電子產品、證件文件、廚房用品")

# ======================= 右側：對話區域 =======================
with right_col:
    st.markdown(f"""
    <div>
        <span class="category-badge">
            🎯 當前分類：{st.session_state.current_category}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # 聊天記錄顯示區域
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if len(st.session_state.messages) == 0:
            st.info(f"💬 歡迎！請輸入一個名詞或物品，我會告訴你是否屬於「{st.session_state.current_category}」分類。")
        else:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-message">👤 {msg["content"]}</div>', unsafe_allow_html=True)
                elif msg["role"] == "assistant":
                    st.markdown(f'<div class="ai-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
                # system 訊息不顯示
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 輸入區域
    st.markdown("---")
    
    user_input = st.text_input(
        "✏️ 輸入名詞或物品",
        placeholder=f"例如：紅綠燈、捷運站、書桌、雨傘...",
        key="user_input",
        label_visibility="collapsed"
    )
    
    col_send, col_clear = st.columns([3, 1])
    with col_send:
        send_button = st.button("🚀 送出詢問", use_container_width=True)
    with col_clear:
        clear_button = st.button("🗑️ 清空對話", use_container_width=True)
    
    if clear_button:
        st.session_state.messages = []
        st.rerun()
    
    # ======================= AI 呼叫函數 =======================
    def call_openai(question, category, api_key):
        """呼叫 OpenAI API"""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        system_prompt = f"""你是一個分類判斷 AI。使用者的問題會問「某個東西是否屬於【{category}】這個分類」。
請直接回答「是」或「否」，並用一句話簡短說明原因。
例如：
- 如果問「紅綠燈」是否屬於【交通設施】，回答：是，紅綠燈是交通設施，用來管制路口行車秩序。
- 如果問「手機」是否屬於【交通設施】，回答：否，手機是電子產品，不屬於交通設施。

請保持回答簡潔、友善、有幫助。"""
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"❌ API 錯誤：{response.status_code} - {response.text[:200]}"
        except Exception as e:
            return f"❌ 連線錯誤：{str(e)}"
    
    def call_gemini(question, category, api_key):
        """呼叫 Google Gemini API"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_prompt = f"""你是一個分類判斷 AI。使用者的問題會問「某個東西是否屬於【{category}】這個分類」。
請直接回答「是」或「否」，並用一句話簡短說明原因。
保持回答簡潔友善。"""
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{system_prompt}\n\n使用者問題：{question}"
                }]
            }]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return f"❌ API 錯誤：{response.status_code}"
        except Exception as e:
            return f"❌ 連線錯誤：{str(e)}"
    
    # 處理送出
    if send_button and user_input:
        if not st.session_state.api_key:
            st.error("⚠️ 請先在上方輸入 API Key")
        else:
            # 加入使用者訊息
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # 顯示 loading
            with st.spinner("🤔 AI 思考中..."):
                # 根據選擇的服務商呼叫 API
                if "OpenAI" in api_provider:
                    ai_response = call_openai(user_input, st.session_state.current_category, st.session_state.api_key)
                elif "Gemini" in api_provider:
                    ai_response = call_gemini(user_input, st.session_state.current_category, st.session_state.api_key)
                else:
                    ai_response = "⚠️ 請選擇有效的 AI 服務並輸入 API Key"
            
            # 加入 AI 回應
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.rerun()

# 頁尾
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #cbcdb0; font-size: 0.7rem;">
    🤖 真正的 AI 分類問答 · 點擊分類後 AI 會判斷是否屬於該類別 · 需要有效 API Key
</div>
""", unsafe_allow_html=True)
