import streamlit as st
import random

# 設定頁面標題與佈局
st.set_page_config(
    page_title="分類猜謎 AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自訂 CSS 美化
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(145deg, #1e2b3c 0%, #0f1a24 100%);
    }
    .main-header {
        text-align: center;
        padding: 1rem;
        background: rgba(255,255,240,0.1);
        border-radius: 2rem;
        margin-bottom: 2rem;
    }
    .category-btn {
        background: #fff3e0;
        border: none;
        border-radius: 60px;
        padding: 0.7rem 1rem;
        margin: 0.3rem;
        font-weight: 600;
        color: #2d3e2b;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-block;
        text-align: center;
    }
    .quiz-card {
        background: linear-gradient(135deg, #ffffff 0%, #fef5e6 100%);
        border-radius: 2rem;
        padding: 2rem;
        box-shadow: 0 20px 30px rgba(0,0,0,0.2);
    }
    .answer-word {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: 6px;
        background: #2e3820;
        display: inline-block;
        padding: 0.6rem 2rem;
        border-radius: 70px;
        color: #fad974;
        text-align: center;
        width: 100%;
        font-family: monospace;
    }
    .hint-box {
        background: #ece3d0;
        border-radius: 2rem;
        padding: 1.3rem;
        margin: 1.2rem 0;
        border-left: 8px solid #f4b942;
    }
    .stButton button {
        background: #4a6e3b;
        color: white;
        border-radius: 3rem;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        width: 100%;
    }
    .stButton button:hover {
        background: #3a5a2e;
    }
    div[data-testid="column"] {
        padding: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# ======================= 分類資料庫 =======================
# 去除無用分類：抽象概念、生物特徵、生理現象等
categories_data = {
    "交通設施": {
        "icon": "🚦",
        "items": [
            {"word": "紅綠燈", "hint": "站在路口有三色眼睛，車看到它會停或走。"},
            {"word": "測速照相機", "hint": "會幫超速車輛拍紀念照，收到罰單就會想起它。"},
            {"word": "斑馬線", "hint": "黑白條紋鋪在地上，行人過馬路的專屬通道。"},
            {"word": "路燈", "hint": "夜晚照亮街道，像沉默的高個子守護者。"},
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
    "交通相關": {
        "icon": "🚗",
        "items": [
            {"word": "方向盤", "hint": "司機握著它控制車子轉彎。"},
            {"word": "後照鏡", "hint": "幫助駕駛看後方車輛，安全必備。"},
            {"word": "安全帶", "hint": "啪一聲扣上，保護你不會飛出去。"},
            {"word": "油門", "hint": "踩下去車子就會加速奔馳。"},
            {"word": "喇叭", "hint": "叭叭！提醒路人或其他車輛注意。"}
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
    "廚房用品": {
        "icon": "🍳",
        "items": [
            {"word": "鍋鏟", "hint": "翻炒食材的好幫手，煎蛋炒菜都用它。"},
            {"word": "菜刀", "hint": "廚房裡的切割大師，切菜切肉很俐落。"},
            {"word": "砧板", "hint": "墊在下面讓刀子不會傷到檯面。"},
            {"word": "烤箱", "hint": "烤麵包、烤雞翅，讓食物變金黃。"},
            {"word": "洗碗精", "hint": "油膩盤子擠一點，泡泡帶走髒污。"}
        ]
    }
}

# 分類順序
category_keys = [
    "交通設施", "場所/地點", "交通相關", "日常用品",
    "安全用品", "辦公用品", "公共設施", "自然現象",
    "電子產品", "證件文件", "廚房用品"
]

# 初始化 session state
if "current_category" not in st.session_state:
    st.session_state.current_category = "交通設施"
if "current_question" not in st.session_state:
    # 隨機選一個題目
    cat_data = categories_data[st.session_state.current_category]
    st.session_state.current_question = random.choice(cat_data["items"]).copy()
if "answer_revealed" not in st.session_state:
    st.session_state.answer_revealed = False

# 標題區域
st.markdown("""
<div class="main-header">
    <h1 style="color: #f4b942; margin:0;">🎯 點擊分類問AI</h1>
    <p style="color: #ffefcf; margin:0.5rem 0 0 0;">點擊分類 → AI 會從該分類猜謎底，提示也會同步切換</p>
</div>
""", unsafe_allow_html=True)

# 兩欄佈局
left_col, right_col = st.columns([1.2, 2.2], gap="large")

# 左側：分類按鈕
with left_col:
    st.markdown("### 📂 分類選單")
    st.markdown("點擊任一分類，切換謎題範圍")
    
    # 用 row 的方式顯示分類按鈕（較美觀）
    for cat in category_keys:
        if cat in categories_data:
            icon = categories_data[cat]["icon"]
            # 判斷是否為當前選中的分類
            is_active = (st.session_state.current_category == cat)
            button_label = f"{icon} {cat}"
            
            if st.button(button_label, key=f"cat_{cat}", use_container_width=True, 
                         type="primary" if is_active else "secondary"):
                # 切換分類
                if st.session_state.current_category != cat:
                    st.session_state.current_category = cat
                    # 隨機選取新分類的題目
                    new_cat_data = categories_data[cat]
                    st.session_state.current_question = random.choice(new_cat_data["items"]).copy()
                    st.session_state.answer_revealed = False
                    st.rerun()

# 右側：問答區
with right_col:
    # 顯示目前分類標籤
    current_icon = categories_data[st.session_state.current_category]["icon"]
    st.markdown(f"""
    <div style="background: #2c5f2d; padding: 0.4rem 1.2rem; border-radius: 40px; 
                color: #ffefcf; font-weight: 600; width: fit-content; margin-bottom: 1rem;">
        {current_icon} 目前分類：{st.session_state.current_category}
    </div>
    """, unsafe_allow_html=True)
    
    # 謎底顯示區域
    if st.session_state.answer_revealed:
        answer_text = st.session_state.current_question["word"]
    else:
        word_len = len(st.session_state.current_question["word"])
        if word_len <= 3:
            answer_text = "???"
        elif word_len <= 6:
            answer_text = "????"
        else:
            answer_text = "??????"
    
    st.markdown(f"""
    <div class="quiz-card">
        <div style="text-align: center;">
            <div class="answer-word">{answer_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 提示區域
    st.markdown(f"""
    <div class="hint-box">
        <div class="hint-label">✨ AI 提示 ✨</div>
        <div class="hint-text" style="font-size:1.2rem;">{st.session_state.current_question["hint"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 操作按鈕（兩欄）
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔍 顯示答案", use_container_width=True):
            st.session_state.answer_revealed = True
            st.rerun()
    with col_b:
        if st.button("🎲 隨機換一題", use_container_width=True):
            # 從同分類隨機選新題目
            cat_data = categories_data[st.session_state.current_category]
            new_question = random.choice(cat_data["items"]).copy()
            st.session_state.current_question = new_question
            st.session_state.answer_revealed = False
            st.rerun()
    
    # 狀態訊息
    cat_len = len(categories_data[st.session_state.current_category]["items"])
    if not st.session_state.answer_revealed:
        st.info(f"🔎 點擊「顯示答案」可查看謎底 | 目前分類共 {cat_len} 題")
    else:
        st.success(f"📖 答案是「{st.session_state.current_question['word']}」！點「隨機換一題」繼續挑戰同分類。")

# 頁尾
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #cbcdb0; font-size: 0.7rem;">
    🧠 AI 分類謎題庫 · 點分類即切換範圍 | 去除無用分類：抽象概念/生物特徵/生理現象等
</div>
""", unsafe_allow_html=True)
