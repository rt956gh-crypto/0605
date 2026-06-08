<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>分類猜謎 AI · 點擊分類換謎底與提示</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none; /* 避免選取文字干擾點擊，但無傷大雅 */
        }

        body {
            background: linear-gradient(145deg, #1e2b3c 0%, #0f1a24 100%);
            font-family: 'Segoe UI', 'Roboto', 'Noto Sans TC', system-ui, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }

        /* 主卡片 */
        .game-container {
            max-width: 1300px;
            width: 100%;
            background: rgba(255,255,240,0.1);
            backdrop-filter: blur(2px);
            border-radius: 3.5rem;
            padding: 1.8rem;
            box-shadow: 0 25px 45px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.1);
            transition: all 0.2s;
        }

        /* 兩欄佈局: 左分類 / 右謎題區 */
        .split-layout {
            display: flex;
            flex-wrap: wrap;
            gap: 1.8rem;
        }

        /* 左側分類面板 */
        .categories-panel {
            flex: 1.2;
            min-width: 240px;
            background: #fef9e8;
            border-radius: 2rem;
            padding: 1.6rem 1.2rem;
            box-shadow: 0 12px 24px rgba(0,0,0,0.2);
            backdrop-filter: blur(0px);
            transition: all 0.2s;
        }

        .categories-panel h2 {
            font-size: 1.7rem;
            margin-top: 0;
            margin-bottom: 1.2rem;
            font-weight: 700;
            color: #2c3e2f;
            border-left: 7px solid #f4b942;
            padding-left: 1rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .categories-panel h2:before {
            content: "🔖";
            font-size: 1.6rem;
        }

        .category-grid {
            display: flex;
            flex-direction: column;
            gap: 0.7rem;
        }

        .cat-btn {
            background: #fff3e0;
            border: none;
            border-radius: 60px;
            padding: 0.9rem 1rem;
            font-size: 1.2rem;
            font-weight: 600;
            text-align: center;
            color: #2d3e2b;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            font-family: inherit;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .cat-btn span:first-child {
            font-size: 1.3rem;
        }

        .cat-btn:hover {
            background: #ffe2b5;
            transform: translateY(-2px);
            box-shadow: 0 10px 18px rgba(0,0,0,0.1);
        }

        .cat-btn.active {
            background: #f4b942;
            color: #1e2c1c;
            box-shadow: 0 4px 12px rgba(244,185,66,0.5);
            border: 1px solid #e0a82b;
        }

        /* 右側遊戲區 */
        .quiz-panel {
            flex: 2.2;
            min-width: 280px;
            background: #ffffffdd;
            backdrop-filter: blur(12px);
            background: linear-gradient(135deg, #ffffff 0%, #fef5e6 100%);
            border-radius: 2rem;
            padding: 2rem 1.8rem;
            box-shadow: 0 20px 30px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column;
        }

        .current-category-badge {
            display: inline-block;
            background: #2c5f2d;
            padding: 0.4rem 1.2rem;
            border-radius: 40px;
            color: #ffefcf;
            font-weight: 600;
            font-size: 0.9rem;
            width: fit-content;
            margin-bottom: 1rem;
            letter-spacing: 1px;
        }

        .mystery-area {
            text-align: center;
            margin: 1rem 0 1.4rem 0;
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
            box-shadow: inset 0 -2px 0 #6a5c3a, 0 8px 18px rgba(0,0,0,0.1);
            font-family: monospace;
        }

        .hint-box {
            background: #ece3d0;
            border-radius: 2rem;
            padding: 1.3rem;
            margin: 1.2rem 0;
            border-left: 8px solid #f4b942;
            transition: all 0.2s;
        }

        .hint-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            font-weight: bold;
            color: #8b6b3c;
            letter-spacing: 1px;
        }

        .hint-text {
            font-size: 1.35rem;
            font-weight: 500;
            color: #2a3b24;
            margin-top: 6px;
            line-height: 1.4;
        }

        .action-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin: 0.5rem 0 1rem;
        }

        .btn-secondary {
            background: #e7dbbc;
            border: none;
            padding: 0.7rem 1.5rem;
            border-radius: 3rem;
            font-weight: bold;
            font-size: 1rem;
            cursor: pointer;
            transition: 0.1s linear;
            font-family: inherit;
        }

        .btn-secondary:active {
            transform: scale(0.97);
        }

        .reveal-btn {
            background: #4a6e3b;
            color: white;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }

        .next-btn {
            background: #3f6e8c;
            color: white;
        }

        .status-message {
            font-size: 0.9rem;
            text-align: center;
            color: #5a4a2a;
            background: #f9efda;
            border-radius: 2rem;
            padding: 0.5rem;
            margin-top: 0.5rem;
        }

        footer {
            font-size: 0.7rem;
            text-align: center;
            margin-top: 1.8rem;
            color: #cbcdb0;
        }

        @media (max-width: 750px) {
            .game-container {
                padding: 1rem;
            }
            .answer-word {
                font-size: 2rem;
                letter-spacing: 3px;
            }
            .hint-text {
                font-size: 1.1rem;
            }
            .cat-btn {
                font-size: 1rem;
                padding: 0.6rem 0.8rem;
            }
        }
    </style>
</head>
<body>
<div class="game-container">
    <div class="split-layout">
        <!-- 左側分類區塊 : 保留實用的具體分類，去除抽象/生理/生物特徵等不好猜謎的類別 -->
        <div class="categories-panel">
            <h2>📂 點擊分類．AI 猜謎</h2>
            <div class="category-grid" id="categoryList">
                <!-- 動態生成按鈕，分類資料由 JS 控制 -->
            </div>
            <div style="font-size: 0.7rem; margin-top: 1.2rem; text-align: center; color:#8f7a55;">
                💡 點擊分類 → 謎底 & 提示切換為該類別
            </div>
        </div>

        <!-- 右側問答區 -->
        <div class="quiz-panel">
            <div class="current-category-badge" id="activeCategoryLabel">🏷️ 未選擇</div>
            <div class="mystery-area">
                <div class="answer-word" id="answerDisplay">????</div>
            </div>
            <div class="hint-box">
                <div class="hint-label">✨ AI 提示 ✨</div>
                <div class="hint-text" id="hintText">
                    點選左側分類，AI 會從該分類中挑選謎底，並顯示專屬提示
                </div>
            </div>
            <div class="action-buttons">
                <button class="btn-secondary reveal-btn" id="revealBtn">🔍 顯示答案</button>
                <button class="btn-secondary next-btn" id="nextBtn">🎲 隨機換一題 (同分類)</button>
            </div>
            <div class="status-message" id="statusMsg">
                ✅ 當前分類內隨機出題
            </div>
        </div>
    </div>
    <footer>
        🧠 AI 分類謎題庫 · 點分類即切換範圍 | 去除無用分類：抽象概念/生物特徵/生理現象等
    </footer>
</div>

<script>
    // ======================= 分類資料庫 =======================
    // 只保留「具體可猜、適合當謎底」的分類，去掉：抽象概念、生物特徵、生理現象、重複冗贅
    // 依照原始清單但整理後實用分類 + 建立各自豐富的題庫與對應提示風格
    const categoriesData = {
        "交通設施": {
            icon: "🚦",
            items: [
                { word: "紅綠燈", hint: "站在路口有三色眼睛，車看到它會停或走。" },
                { word: "測速照相機", hint: "會幫超速車輛拍紀念照，收到罰單就會想起它。" },
                { word: "斑馬線", hint: "黑白條紋鋪在地上，行人過馬路的專屬通道。" },
                { word: "路燈", hint: "夜晚照亮街道，像沉默的高個子守護者。" },
                { word: "公車站牌", hint: "上面寫滿編號，等車的人都會看著它。" }
            ]
        },
        "場所/地點": {
            icon: "🏞️",
            items: [
                { word: "圖書館", hint: "安靜的地方，滿滿書香，借書還書的好去處。" },
                { word: "公園", hint: "有草地鞦韆，老人散步小孩奔跑。" },
                { word: "電影院", hint: "大銀幕+爆米花，黑漆漆的約會聖地。" },
                { word: "醫院", hint: "有醫生護士，生病時會去的地方。" },
                { word: "學校", hint: "教室、操場、鐘聲，學習知識的場所。" }
            ]
        },
        "交通相關": {
            icon: "🚗",
            items: [
                { word: "方向盤", hint: "司機握著它控制車子轉彎。" },
                { word: "後照鏡", hint: "幫助駕駛看後方車輛，安全必備。" },
                { word: "安全帶", hint: "啪一聲扣上，保護你不會飛出去。" },
                { word: "油門", hint: "踩下去車子就會加速奔馳。" },
                { word: "喇叭", hint: "叭叭！提醒路人或其他車輛注意。" }
            ]
        },
        "日常用品": {
            icon: "🧴",
            items: [
                { word: "牙刷", hint: "每天早晚和牙膏合作，幫牙齒洗洗澡。" },
                { word: "毛巾", hint: "洗完澡用它擦乾身體，軟軟的很吸水。" },
                { word: "馬克杯", hint: "裝咖啡、裝茶，握在手心暖暖的。" },
                { word: "拖鞋", hint: "回到家解放雙腳，輕鬆走路的好夥伴。" },
                { word: "衣架", hint: "把濕衣服掛起來曬太陽，晾乾就靠它。" }
            ]
        },
        "安全用品": {
            icon: "🛡️",
            items: [
                { word: "安全帽", hint: "騎車必戴，保護腦袋的硬殼帽。" },
                { word: "滅火器", hint: "紅色瓶身，著火時對火焰噴灑救命粉。" },
                { word: "煙霧偵測器", hint: "天花板上的小圓盤，聞到煙會大叫。" },
                { word: "醫藥箱", hint: "裡面有OK繃、藥水，小傷口的急救站。" },
                { word: "反光背心", hint: "夜間工作或施工時穿，車燈一照超亮眼。" }
            ]
        },
        "辦公用品": {
            icon: "✒️",
            items: [
                { word: "原子筆", hint: "寫字流暢，辦公室桌上最常見的筆。" },
                { word: "釘書機", hint: "咔嚓一聲把紙張固定在一起。" },
                { word: "電腦鍵盤", hint: "敲敲打打就能輸入文字，配滑鼠好朋友。" },
                { word: "便利貼", hint: "小小彩色紙，背面有黏性，隨手記事超方便。" },
                { word: "檔案夾", hint: "收納文件紙張，讓資料整整齊齊。" }
            ]
        },
        "公共設施": {
            icon: "🏛️",
            items: [
                { word: "路燈", hint: "晚上照亮馬路，治安小尖兵。" },
                { word: "公共垃圾桶", hint: "街道上的環保小幫手，記得做好分類。" },
                { word: "公共廁所", hint: "外出應急好夥伴，辨識標誌通常是男女圖示。" },
                { word: "涼亭", hint: "公園裡可以躲雨乘涼的屋頂座位區。" },
                { word: "座椅", hint: "走累了就坐下，長椅常常出現在人行道旁。" }
            ]
        },
        "自然現象": {
            icon: "🌈",
            items: [
                { word: "彩虹", hint: "雨後太陽露臉，天空出現七彩拱橋。" },
                { word: "閃電", hint: "雷雨時的強烈放電，一瞬間照亮天空。" },
                { word: "颱風", hint: "強風暴雨環流，台灣夏秋常見的天氣系統。" },
                { word: "流星雨", hint: "夜空中許多光點劃過，許願時刻！" },
                { word: "濃霧", hint: "白茫茫一片，能見度極低，開車要小心。" }
            ]
        },
        "電子產品": {
            icon: "📱",
            items: [
                { word: "智慧型手機", hint: "手掌大小，能上網拍照打電話，現代人必備。" },
                { word: "筆記型電腦", hint: "可摺疊攜帶，工作娛樂都靠它。" },
                { word: "藍芽耳機", hint: "無線連接，聽音樂講電話不用線纏繞。" },
                { word: "行動電源", hint: "手機沒電時的救命充電寶。" },
                { word: "智慧手錶", hint: "戴在手腕，能看訊息測心跳，酷炫小幫手。" }
            ]
        },
        "證件文件": {
            icon: "📄",
            items: [
                { word: "身分證", hint: "證明你是你，重要場合必備的卡片。" },
                { word: "護照", hint: "出國必備，海關檢查用的小冊子。" },
                { word: "駕照", hint: "證明你有資格開車或騎車。" },
                { word: "學生證", hint: "在校證明，買學生票就靠它。" },
                { word: "健保卡", hint: "看病就醫必帶，有照片和晶片。" }
            ]
        },
        "廚房用品": {
            icon: "🍳",
            items: [
                { word: "鍋鏟", hint: "翻炒食材的好幫手，煎蛋炒菜都用它。" },
                { word: "菜刀", hint: "廚房裡的切割大師，切菜切肉很俐落。" },
                { word: "砧板", hint: "墊在下面讓刀子不會傷到檯面。" },
                { word: "烤箱", hint: "烤麵包、烤雞翅，讓食物變金黃。" },
                { word: "洗碗精", hint: "油膩盤子擠一點，泡泡帶走髒污。" }
            ]
        }
    };

    // 額外確保每個分類至少有三個題目，若有重疊(例如路燈同時在交通設施與公共設施)沒關係，允許不同分類提示不同
    // 修補交通設施避免跟公共設施完全一樣但可接受（豐富度）
    if(categoriesData["交通設施"].items.length<3){
        categoriesData["交通設施"].items.push({word:"平交道", hint:"火車經過時柵欄會放下，鐵路與道路交叉處。"});
    }
    if(categoriesData["公共設施"].items.length<3){
        categoriesData["公共設施"].items.push({word:"電話亭", hint:"公共空間中的小亭子，可以打電話(雖然現在少見)"});
    }

    // 分類按鈕順序 (依照實用且去除「抽象/生物/生理」)
    const categoryKeys = [
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
    ];

    // 狀態管理
    let currentCategory = "交通設施";      // 預設第一個
    let currentQuestion = null;            // 存放當前 {word, hint}
    let isAnswerRevealed = false;           // 是否顯示答案 (控制顯示 ??? 或 真實單詞)
    let currentItemList = [];               // 當前分類的題庫陣列

    // DOM 元素
    const categoryListDiv = document.getElementById("categoryList");
    const activeCategoryLabelSpan = document.getElementById("activeCategoryLabel");
    const answerDisplaySpan = document.getElementById("answerDisplay");
    const hintTextDiv = document.getElementById("hintText");
    const revealBtn = document.getElementById("revealBtn");
    const nextBtn = document.getElementById("nextBtn");
    const statusMsgSpan = document.getElementById("statusMsg");

    // 輔助: 根據分類名稱取得 icon
    function getCategoryIcon(catName){
        return categoriesData[catName]?.icon || "📌";
    }

    // 重新整理當前分類的內部資料 (更換謎底時使用)
    function loadQuestionsForCategory(categoryName){
        if(!categoriesData[categoryName]){
            // 若萬一不存在退回首個分類
            categoryName = categoryKeys[0];
        }
        const catData = categoriesData[categoryName];
        if(catData && catData.items.length > 0){
            currentItemList = [...catData.items];
        } else {
            // fallback 臨時題庫
            currentItemList = [{word:"預設謎題", hint:"請檢查分類資料庫"}];
        }
    }

    // 從 currentItemList 隨機挑選一題 (不改變揭露狀態)
    function pickRandomQuestion(){
        if(!currentItemList.length) return {word:"???", hint:"暫無謎題"};
        const randomIndex = Math.floor(Math.random() * currentItemList.length);
        return {...currentItemList[randomIndex]};
    }

    // 刷新畫面: 更新謎底文字 (根據是否顯示答案)、更新提示、更新分類標籤
    function refreshUI(){
        if(!currentQuestion){
            // 若無則隨機產生
            currentQuestion = pickRandomQuestion();
        }
        // 更新顯示的謎底文字
        if(isAnswerRevealed){
            answerDisplaySpan.textContent = currentQuestion.word;
        } else {
            // 隱藏答案顯示問號 (長度比例展現)
            let hiddenStr = "???";
            if(currentQuestion.word && currentQuestion.word.length <= 6){
                hiddenStr = "????".substring(0, currentQuestion.word.length);
                if(hiddenStr.length<2) hiddenStr="??";
            } else {
                hiddenStr = "??????";
            }
            answerDisplaySpan.textContent = hiddenStr;
        }
        // 提示永遠顯示當前問題的提示
        hintTextDiv.textContent = currentQuestion.hint || "AI 正在思考這個分類的線索...";
        // 更新左上角分類標籤
        const icon = getCategoryIcon(currentCategory);
        activeCategoryLabelSpan.innerHTML = `${icon} 目前分類：${currentCategory}`;
        // 狀態列更新
        if(!isAnswerRevealed){
            statusMsgSpan.innerHTML = `🔎 點擊「顯示答案」可查看謎底 | 目前分類共 ${currentItemList.length} 題`;
        } else {
            statusMsgSpan.innerHTML = `📖 答案已揭曉：${currentQuestion.word} | 再按「隨機換題」會繼續同分類`;
        }
    }

    // 更換當前分類 (重點功能: 使用者點分類時觸發)
    function switchCategory(newCategory){
        if(!categoriesData[newCategory]) return;
        // 更新當前分類
        currentCategory = newCategory;
        // 載入此分類題庫
        loadQuestionsForCategory(currentCategory);
        // 重置揭露狀態
        isAnswerRevealed = false;
        // 重新隨機挑選一個謎底
        currentQuestion = pickRandomQuestion();
        // 刷新UI
        refreshUI();
        // 更新按鈕 active 樣式
        updateActiveButtonStyle(newCategory);
        // 另外產生一個輕提示(可選)
        statusMsgSpan.innerHTML = `✨ 已切換至【${currentCategory}】分類，AI 從該類隨機出題 ✨`;
        setTimeout(()=>{
            if(!isAnswerRevealed && statusMsgSpan.innerHTML.includes("已切換")){
                // 避免蓋掉重要訊息但兩秒後可恢復一點
                if(!isAnswerRevealed)
                    statusMsgSpan.innerHTML = `🔎 點擊「顯示答案」查看謎底 | 目前分類共 ${currentItemList.length} 題`;
            }
        },1800);
    }

    // 隨機更換同分類的謎底 (下一題)
    function nextQuestionInSameCategory(){
        // 更換題目
        currentQuestion = pickRandomQuestion();
        // 若先前答案已揭露，換題後強制隱藏答案 (符合直覺)
        isAnswerRevealed = false;
        refreshUI();
        statusMsgSpan.innerHTML = `🔄 同分類【${currentCategory}】已更換新謎底，試試看！`;
        setTimeout(()=>{
            if(!isAnswerRevealed && statusMsgSpan.innerHTML.includes("已更換")){
                statusMsgSpan.innerHTML = `🔎 提示有效！點「顯示答案」觀看解答 (${currentCategory})`;
            }
        },2000);
    }

    // 顯示答案 (不更換分類)
    function revealAnswer(){
        if(isAnswerRevealed){
            // 已經顯示答案就簡單提示
            statusMsgSpan.innerHTML = `📢 答案已經是「${currentQuestion.word}」了，點下一題吧！`;
            return;
        }
        isAnswerRevealed = true;
        refreshUI();
        statusMsgSpan.innerHTML = `🔓 答案是「${currentQuestion.word}」！點「隨機換一題」繼續挑戰同分類。`;
    }

    // 更新按鈕 active 樣式
    function updateActiveButtonStyle(activeCat){
        const allBtns = document.querySelectorAll(".cat-btn");
        allBtns.forEach(btn => {
            const catValue = btn.getAttribute("data-cat");
            if(catValue === activeCat){
                btn.classList.add("active");
            } else {
                btn.classList.remove("active");
            }
        });
    }

    // 建立左側分類按鈕 (過濾掉不實用的類別，我們只用了 categoryKeys 內定義好的)
    function buildCategoryButtons(){
        categoryListDiv.innerHTML = "";
        for(let cat of categoryKeys){
            if(categoriesData[cat]){
                const iconSym = categoriesData[cat].icon || "📌";
                const btn = document.createElement("button");
                btn.className = "cat-btn";
                btn.setAttribute("data-cat", cat);
                btn.innerHTML = `<span>${iconSym}</span><span>${cat}</span>`;
                btn.addEventListener("click", (e) => {
                    e.preventDefault();
                    switchCategory(cat);
                });
                categoryListDiv.appendChild(btn);
            }
        }
        // 預設高亮第一個分類
        if(categoryKeys.length){
            updateActiveButtonStyle(currentCategory);
        }
    }

    // 初始化加載
    function initGame(){
        buildCategoryButtons();
        // 設置預設分類 = 交通設施 (存在)
        currentCategory = "交通設施";
        loadQuestionsForCategory(currentCategory);
        currentQuestion = pickRandomQuestion();
        isAnswerRevealed = false;
        refreshUI();
        // 綁定按鈕監聽
        revealBtn.addEventListener("click", revealAnswer);
        nextBtn.addEventListener("click", nextQuestionInSameCategory);
    }

    // 執行初始化
    initGame();
</script>
</body>
</html>
