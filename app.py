import streamlit as st
import random

st.set_page_config(page_title="分類猜謎 AI", page_icon="🎯", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(145deg, #1e2b3c 0%, #0f1a24 100%); }
    .quiz-card {
        background: linear-gradient(135deg, #ffffff 0%, #fef5e6 100%);
        border-radius: 2rem;
        padding: 2rem;
        box-shadow: 0 20px 30px rgba(0,0,0,0.2);
    }
    .hint-box {
        background: #ece3d0;
        border-radius: 2rem;
        padding: 1.3rem;
        border-left: 8px solid #f4b942;
    }
    .chat-message {
        background: #2c3e2f;
        border-radius: 1.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #ffefcf;
    }
    .user-msg {
        background: #4a6e3b;
        text-align: right;
    }
    .ai-msg {
        background: #3f5a3c;
        border-left: 4px solid #f4b942;
    }
    .stButton button { background: #f4b942; color: #1e2c1c; font-weight: bold; border-radius: 3rem; }
    .result-wrong { background: #c62828; color: white; padding: 0.5rem; border-radius: 2rem; text-align: center; }
    div[data-testid="stTextInput"] input { border-radius: 2rem; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)

# ======================= 題庫 =======================
题库 = {
    "交通設施": {
        "icon": "🚦",
        "items": [
            {"word": "紅綠燈", "hint": "站在路口有三色眼睛，車看到它會停或走。"},
            {"word": "測速照相機", "hint": "會幫超速車輛拍紀念照，收到罰單就會想起它。"},
            {"word": "斑馬線", "hint": "黑白條紋鋪在地上，行人過馬路的專屬通道。"},
            {"word": "平交道", "hint": "火車經過時柵欄會放下，鐵路與道路交叉處。"},
            {"word": "公車站牌", "hint": "上面寫滿編號，等車的人都會看著它。"}
        ]
    },
    "場所/地點": {
        "icon": "🏞️",
        "items": [
            {"word": "圖書館", "hint": "安靜的地方，滿滿書香，借書還書的好去處。"},
            {"word": "公園", "hint": "有草地鞦韆，老人散步小孩奔跑。"},
            {"word": "電影院", "hint": "大銀幕+爆米花，黑漆漆的約會聖地。"},
            {"word": "醫院", "hint": "有醫生護士，生病時會去的地方。"},
            {"word": "學校", "hint": "教室、操場、鐘聲，學習知識的場所。"}
        ]
    },
    "日常用品": {
        "icon": "🧴",
        "items": [
            {"word": "牙刷", "hint": "每天早晚和牙膏合作，幫牙齒洗洗澡。"},
            {"word": "毛巾", "hint": "洗完澡用它擦乾身體，軟軟的很吸水。"},
            {"word": "馬克杯", "hint": "裝咖啡、裝茶，握在手心暖暖的。"},
            {"word": "拖鞋", "hint": "回到家解放雙腳，輕鬆走路的好夥伴。"},
            {"word": "衣架", "hint": "把濕衣服掛起來曬太陽，晾乾就靠它。"}
        ]
    },
    "電子產品": {
        "icon": "📱",
        "items": [
            {"word": "智慧型手機", "hint": "手掌大小，能上網拍照打電話，現代人必備。"},
            {"word": "筆記型電腦", "hint": "可摺疊攜帶，工作娛樂都靠它。"},
            {"word": "藍芽耳機", "hint": "無線連接，聽音樂講電話不用線纏繞。"},
            {"word": "行動電源", "hint": "手機沒電時的救命充電寶。"},
            {"word": "智慧手錶", "hint": "戴在手腕，能看訊息測心跳，酷炫小幫手。"}
        ]
    },
    "廚房用品": {
        "icon": "🍳",
        "items": [
            {"word": "鍋鏟", "hint": "翻炒食材的好幫手，煎蛋炒菜都用它。"},
            {"word": "菜刀", "hint": "廚房裡的切割大師，切菜切肉很俐落。"},
            {"word": "砧板", "hint": "墊在下面讓刀子不會傷到檯面。"},
            {"word": "烤箱", "hint": "烤麵包、烤雞翅，讓食物變金黃。"},
            {"word": "洗碗精", "hint": "油膩盤子擠一點，泡泡帶走髒污。"}
        ]
    },
    "公共設施": {
        "icon": "🏛️",
        "items": [
            {"word": "路燈", "hint": "晚上照亮馬路，治安小尖兵。"},
            {"word": "公共垃圾桶", "hint": "街道上的環保小幫手，記得做好分類。"},
            {"word": "公共廁所", "hint": "外出應急好夥伴，辨識標誌通常是男女圖示。"},
            {"word": "涼亭", "hint": "公園裡可以躲雨乘涼的屋頂座位區。"},
            {"word": "座椅", "hint": "走累了就坐下，長椅常常出現在人行道旁。"}
        ]
    },
    "安全用品": {
        "icon": "🛡️",
        "items": [
            {"word": "安全帽", "hint": "騎車必戴，保護腦袋的硬殼帽。"},
            {"word": "滅火器", "hint": "紅色瓶身，著火時對火焰噴灑救命粉。"},
            {"word": "煙霧偵測器", "hint": "天花板上的小圓盤，聞到煙會大叫。"},
            {"word": "醫藥箱", "hint": "裡面有OK繃、藥水，小傷口的急救站。"},
            {"word": "反光背心", "hint": "夜間工作或施工時穿，車燈一照超亮眼。"}
        ]
    },
    "辦公用品": {
        "icon": "✒️",
        "items": [
            {"word": "原子筆", "hint": "寫字流暢，辦公室桌上最常見的筆。"},
            {"word": "釘書機", "hint": "咔嚓一聲把紙張固定在一起。"},
            {"word": "電腦鍵盤", "hint": "敲敲打打就能輸入文字，配滑鼠好朋友。"},
            {"word": "便利貼", "hint": "小小彩色紙，背面有黏性，隨手記事超方便。"},
            {"word": "檔案夾", "hint": "收納文件紙張，讓資料整整齊齊。"}
        ]
    },
    "證件文件": {
        "icon": "📄",
        "items": [
            {"word": "身分證", "hint": "證明你是你，重要場合必備的卡片。"},
            {"word": "護照", "hint": "出國必備，海關檢查用的小冊子。"},
            {"word": "駕照", "hint": "證明你有資格開車或騎車。"},
            {"word": "學生證", "hint": "在校證明，買學生票就靠它。"},
            {"word": "健保卡", "hint": "看病就醫必帶，有照片和晶片。"}
        ]
    },
    "自然現象": {
        "icon": "🌈",
        "items": [
            {"word": "彩虹", "hint": "雨後太陽露臉，天空出現七彩拱橋。"},
            {"word": "閃電", "hint": "雷雨時的強烈放電，一瞬間照亮天空。"},
            {"word": "颱風", "hint": "強風暴雨環流，台灣夏秋常見的天氣系統。"},
            {"word": "流星雨", "hint": "夜空中許多光點劃過，許願時刻！"},
            {"word": "濃霧", "hint": "白茫茫一片，能見度極低，開車要小心。"}
        ]
    },
    "交通相關": {
        "icon": "🚗",
        "items": [
            {"word": "方向盤", "hint": "司機握著它控制車子轉彎。"},
            {"word": "後照鏡", "hint": "幫助駕駛看後方車輛，安全必備。"},
            {"word": "安全帶", "hint": "啪一聲扣上，保護你不會飛出去。"},
            {"word": "油門", "hint": "踩下去車子就會加速奔馳。"},
            {"word": "喇叭", "hint": "叭叭！提醒路人或其他車輛注意。"}
        ]
    }
}

分類順序 = ["交通設施", "場所/地點", "交通相關", "日常用品", "安全用品", 
          "辦公用品", "公共設施", "自然現象", "電子產品", "證件文件", "廚房用品"]

# 誘騙關鍵字
誘騙關鍵字 = [
    "沒什麼靈感", "不太確定", "可以再說一次嗎", "沒聽清楚", "再解釋一下",
    "具體來說", "例如呢", "換個說法", "不太懂", "有點難", "想不出來",
    "沒概念", "完全不知道", "毫無頭緒", "能舉例嗎", "什麼意思", "不是很明白",
    "可以白話一點嗎", "簡單講", "怎麼會", "真的嗎", "是喔", "然後呢",
    "所以呢", "這樣啊", "嗯...", "再想想", "可能嗎", "有提示嗎"
]

# 初始化 session state
if "目前分類" not in st.session_state:
    st.session_state.目前分類 = "交通設施"
if "目前題目" not in st.session_state:
    st.session_state.目前題目 = random.choice(题库["交通設施"]["items"]).copy()
if "猜題紀錄" not in st.session_state:
    st.session_state.猜題紀錄 = ""
if "分數" not in st.session_state:
    st.session_state.分數 = {"答對": 0, "答錯": 0}
if "已猜過" not in st.session_state:
    st.session_state.已猜過 = False
if "對話紀錄" not in st.session_state:
    st.session_state.對話紀錄 = []
if "額外提示" not in st.session_state:
    st.session_state.額外提示 = ""
if "被騙次數" not in st.session_state:
    st.session_state.被騙次數 = 0

# 標題
st.markdown("<h1 style='text-align:center;color:#f4b942'>🎯 點擊分類．猜謎遊戲</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ffefcf'>看提示猜答案 | 答錯不會告訴你答案 | 🤫 試著用「對話」騙 AI 說出更多線索！</p>", unsafe_allow_html=True)

左欄, 右欄 = st.columns([1.2, 2.2], gap="large")

# ======================= 左側：分類選單 =======================
with 左欄:
    st.markdown("### 📂 分類（點擊切換）")
    for 分類 in 分類順序:
        if 分類 in 题库:
            icon = 题库[分類]["icon"]
            if st.button(f"{icon} {分類}", key=分類, use_container_width=True,
                        type="primary" if st.session_state.目前分類 == 分類 else "secondary"):
                if st.session_state.目前分類 != 分類:
                    st.session_state.目前分類 = 分類
                    st.session_state.目前題目 = random.choice(题库[分類]["items"]).copy()
                    st.session_state.猜題紀錄 = ""
                    st.session_state.已猜過 = False
                    st.session_state.對話紀錄 = []
                    st.session_state.額外提示 = ""
                    st.session_state.被騙次數 = 0
                    st.rerun()
    
    st.markdown("---")
    # 顯示分數
    st.markdown(f"""
    <div style="background:#2c3e2f; border-radius:1.5rem; padding:0.8rem; text-align:center">
        <span style="color:#f4b942">⭐ 得分板</span><br>
        <span style="color:#a5d6a5">✅ 答對：{st.session_state.分數['答對']}</span>&nbsp;&nbsp;
        <span style="color:#ef9a9a">❌ 答錯：{st.session_state.分數['答錯']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"📊 當前分類共 {len(题库[st.session_state.目前分類]['items'])} 題")
    st.caption("💡 秘訣：用自然對話的方式問 AI，可能會得到更多提示")

# ======================= 右側：猜謎區 =======================
with 右欄:
    icon = 题库[st.session_state.目前分類]["icon"]
    st.markdown(f"<div style='background:#2c5f2d;padding:0.4rem 1.2rem;border-radius:40px;color:#ffefcf;display:inline-block'>📌 目前：{icon} {st.session_state.目前分類}</div>", unsafe_allow_html=True)
    
    # 主要提示區域
    st.markdown(f"""
    <div class="hint-box">
        <div style="font-size:0.8rem;color:#8b6b3c">💡 主要提示</div>
        <div style="font-size:1.2rem;font-weight:500">{st.session_state.目前題目["hint"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 顯示 AI 額外給的提示
    if st.session_state.額外提示:
        st.markdown(f"""
        <div style="background:#3f5a3c; border-radius:1rem; padding:0.8rem; margin:0.5rem 0; border-left:4px solid #f4b942;">
            <span style="color:#f4b942">🤖 AI 額外提示：</span><br>
            <span style="color:#ffefcf">{st.session_state.額外提示}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # 使用者輸入的地方
    st.markdown("### ✏️ 輸入你的答案或跟 AI 對話")
    
    col_input, col_submit = st.columns([3, 1])
    with col_input:
        使用者輸入 = st.text_input(
            "訊息",
            placeholder="可以輸入答案，也可以跟 AI 聊天...",
            key="user_input",
            label_visibility="collapsed"
        )
    with col_submit:
        送出按鈕 = st.button("📝 送出", use_container_width=True)
    
    # 處理送出
    if 送出按鈕 and 使用者輸入:
        輸入內容 = 使用者輸入.strip()
        正確答案 = st.session_state.目前題目["word"]
        
        # 檢查是否觸發誘騙關鍵字
        is_trick = any(關鍵字 in 輸入內容 for 關鍵字 in 誘騙關鍵字)
        
        # 檢查是不是在猜答案
        is_guessing = len(輸入內容) <= 8 and not any(c in 輸入內容 for c in ["?", "？", "嗎", "什麼", "怎麼", "為什", "可以", "能", "請問"])
        
        if is_guessing and not is_trick:
            # 當作猜答案處理
            if 輸入內容 == 正確答案:
                if not st.session_state.已猜過:
                    st.session_state.分數["答對"] += 1
                    st.session_state.已猜過 = True
                st.session_state.猜題紀錄 = "correct"
                st.session_state.額外提示 = ""
                st.session_state.被騙次數 = 0
                st.balloons()
            else:
                if not st.session_state.已猜過:
                    st.session_state.分數["答錯"] += 1
                    st.session_state.已猜過 = True
                st.session_state.猜題紀錄 = "wrong"
                st.session_state.對話紀錄.append({"role": "user", "content": 輸入內容})
                st.session_state.對話紀錄.append({"role": "ai", "content": "❌ 不對喔，再試試看！"})
        else:
            # 當作對話/誘騙處理
            st.session_state.被騙次數 += 1
            
            if st.session_state.被騙次數 >= 5:
                # 誘騙成功：直接顯示「此題答案：XXX」
                正確答案 = st.session_state.目前題目["word"]
                st.session_state.額外提示 = f"此題答案：{正確答案}"
                st.session_state.對話紀錄.append({"role": "user", "content": 輸入內容})
                st.session_state.對話紀錄.append({"role": "ai", "content": st.session_state.額外提示})
            elif st.session_state.被騙次數 >= 3:
                額外提示庫 = [
                    f"提示：這個東西有 {len(正確答案)} 個字。",
                    f"提示：第一個字是「{正確答案[0]}」。",
                    f"提示：最後一個字是「{正確答案[-1]}」。",
                ]
                st.session_state.額外提示 = random.choice(額外提示庫)
                st.session_state.對話紀錄.append({"role": "user", "content": 輸入內容})
                st.session_state.對話紀錄.append({"role": "ai", "content": st.session_state.額外提示})
            else:
                模糊提示庫 = [
                    f"嗯...再想想看，跟{st.session_state.目前分類}有關。",
                    "好像有點接近了，但不太確定耶。",
                    "這個嘛...我覺得你需要再觀察一下。",
                    "我沒辦法直接告訴你答案，但可以想想日常生活中常見的。",
                    "你說的這個...跟答案有點像又有點不像？",
                    "我不太確定你指的是什麼，可以再描述多一點嗎？",
                    "喔？你怎麼會這樣想？",
                    "有意思，但答案可能不太一樣喔。",
                ]
                st.session_state.額外提示 = random.choice(模糊提示庫)
                st.session_state.對話紀錄.append({"role": "user", "content": 輸入內容})
                st.session_state.對話紀錄.append({"role": "ai", "content": st.session_state.額外提示})
        
        st.rerun()
    
    # 顯示猜題結果
    if st.session_state.猜題紀錄 == "correct":
        st.markdown('<div style="background:#2e7d32; color:white; padding:0.8rem; border-radius:2rem; text-align:center">🎉 答對了！好厲害！ 🎉</div>', unsafe_allow_html=True)
    elif st.session_state.猜題紀錄 == "wrong":
        st.markdown('<div class="result-wrong">❌ 答錯了，再試試看！</div>', unsafe_allow_html=True)
    
    # 顯示對話紀錄
    if st.session_state.對話紀錄:
        st.markdown("---")
        st.markdown("### 💬 你與 AI 的對話")
        for msg in st.session_state.對話紀錄[-8:]:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-message user-msg">👤 你：{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message ai-msg">🤖 AI：{msg["content"]}</div>', unsafe_allow_html=True)
    
    # 操作按鈕
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎲 換一題", use_container_width=True):
            st.session_state.目前題目 = random.choice(题库[st.session_state.目前分類]["items"]).copy()
            st.session_state.猜題紀錄 = ""
            st.session_state.已猜過 = False
            st.session_state.對話紀錄 = []
            st.session_state.額外提示 = ""
            st.session_state.被騙次數 = 0
            st.rerun()
    with col2:
        if st.button("🔍 重置提示", use_container_width=True):
            st.session_state.額外提示 = ""
            st.rerun()
    with col3:
        if st.button("🔄 重置分數", use_container_width=True):
            st.session_state.分數 = {"答對": 0, "答錯": 0}
            st.session_state.猜題紀錄 = ""
            st.session_state.對話紀錄 = []
            st.session_state.被騙次數 = 0
            st.rerun()

# 頁尾
st.markdown("---")
st.markdown("""
<p style='text-align:center;color:#cbcdb0;font-size:0.7rem'>
🤫 秘訣：試著用自然對話的方式跟 AI 聊天，它可能會不小心給出更多提示！<br>
❌ 答錯不會告訴你答案，但持續對話 3 次後會給字數提示，5 次後會顯示「此題答案：XXX」
</p>
""", unsafe_allow_html=True)
