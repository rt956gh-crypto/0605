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
    .answer-word {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: 8px;
        background: #2e3820;
        padding: 0.6rem 2rem;
        border-radius: 70px;
        color: #fad974;
        text-align: center;
        font-family: monospace;
    }
    .hint-box {
        background: #ece3d0;
        border-radius: 2rem;
        padding: 1.3rem;
        border-left: 8px solid #f4b942;
    }
    .stButton button { background: #f4b942; color: #1e2c1c; font-weight: bold; border-radius: 3rem; }
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

# 初始化
if "目前分類" not in st.session_state:
    st.session_state.目前分類 = "交通設施"
if "目前題目" not in st.session_state:
    st.session_state.目前題目 = random.choice(题库["交通設施"]["items"]).copy()
if "顯示答案" not in st.session_state:
    st.session_state.顯示答案 = False

# 標題
st.markdown("<h1 style='text-align:center;color:#f4b942'>🎯 點擊分類．隨機謎底</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ffefcf'>點擊左側分類 → 隨機出現該類謎底 → 猜猜看！</p>", unsafe_allow_html=True)

左欄, 右欄 = st.columns([1.2, 2.2], gap="large")

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
                    st.session_state.顯示答案 = False
                    st.rerun()
    
    st.markdown("---")
    st.caption(f"📊 當前分類共 {len(题库[st.session_state.目前分類]['items'])} 題")
    st.caption("🎲 每次點分類或換題都是隨機抽取")

with 右欄:
    icon = 题库[st.session_state.目前分類]["icon"]
    st.markdown(f"<div style='background:#2c5f2d;padding:0.4rem 1.2rem;border-radius:40px;color:#ffefcf;display:inline-block'>📌 目前：{icon} {st.session_state.目前分類}</div>", unsafe_allow_html=True)
    
    # 顯示謎底（問號或答案）
    if st.session_state.顯示答案:
        顯示文字 = st.session_state.目前題目["word"]
    else:
        長度 = len(st.session_state.目前題目["word"])
        if 長度 <= 3:
            顯示文字 = "???"
        elif 長度 <= 6:
            顯示文字 = "????"
        else:
            顯示文字 = "??????"
    
    st.markdown(f"""
    <div class="quiz-card">
        <div style="text-align:center">
            <div class="answer-word">{顯示文字}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 提示
    st.markdown(f"""
    <div class="hint-box">
        <div style="font-size:0.8rem;color:#8b6b3c">💡 AI 提示</div>
        <div style="font-size:1.2rem;font-weight:500">{st.session_state.目前題目["hint"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 按鈕
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 顯示答案", use_container_width=True):
            st.session_state.顯示答案 = True
            st.rerun()
    with col2:
        if st.button("🎲 隨機換一題", use_container_width=True):
            st.session_state.目前題目 = random.choice(题库[st.session_state.目前分類]["items"]).copy()
            st.session_state.顯示答案 = False
            st.rerun()

st.markdown("---")
st.markdown("<p style='text-align:center;color:#cbcdb0;font-size:0.7rem'>✅ 點分類 = 隨機換該類謎底 · 提示也會切換 · 不需要 API Key</p>", unsafe_allow_html=True)
