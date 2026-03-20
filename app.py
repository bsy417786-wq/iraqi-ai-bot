import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="دردشة عباس حيدر", page_icon="🎮", layout="centered")

design = """
    <style>
    /* إخفاء زوائد ستريمليت */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"], div[data-testid="stDecoration"], [data-testid="stStatusWidget"], iframe[title="manage-app"] { 
        visibility: hidden; display: none !important; 
    }

    /* خلفية الدارك مود الفخمة */
    .stApp { background: #0b141a; color: #e9edef; }

    /* أنيميشن الظهور التدريجي */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* تنسيق فقاعات الدردشة (مثل الواتساب) */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        animation: fadeIn 0.4s ease-in-out;
    }

    /* فقاعة المستخدم (يسار) */
    div[data-testid="stChatMessage"]:has(img[alt="user-avatar"]), 
    div[data-testid="stChatMessage"]:nth-child(even) {
        flex-direction: row-reverse;
        text-align: left;
    }
    
    /* ستايل الكلام داخل الفقاعة */
    .stMarkdown {
        padding: 10px 15px;
        border-radius: 15px;
        display: inline-block;
        max-width: 80%;
    }

    /* صندوق الكتابة (ثابت فوق الصور) */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 140px !important;
        z-index: 1000 !important;
        background: #202c33 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 10px !important;
    }

    /* الصور الثابتة (أسفل الكل) */
    .footer-fixed {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0b141a;
        padding: 10px 0;
        z-index: 999;
        border-top: 1px solid #202c33;
        text-align: center;
    }

    .footer-imgs {
        display: flex; justify-content: center; gap: 8px;
    }

    .footer-imgs img {
        width: 100px; height: 60px; object-fit: cover;
        border-radius: 5px; border: 1px solid #38bdf8;
    }

    /* مسافة حتى المحادثة ما تندفن */
    .stChatContainer { padding-bottom: 250px !important; }

    /* النقاط اللي ترمش */
    .typing { display: flex; gap: 4px; padding: 10px; }
    .dot { width: 6px; height: 6px; background: #38bdf8; border-radius: 50%; animation: blink 1.4s infinite; }
    @keyframes blink { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية
st.markdown("<h2 style='text-align:center; color:#38bdf8;'>🎮 عباس حيدر - واتساب الكيمنك</h2>", unsafe_allow_html=True)

# 3. المفتاح والذاكرة
MY_KEY = "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"
ABBAS_AVATAR = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة (يسار ويمين)
for msg in st.session_state.messages:
    side = "assistant" if msg["role"] == "assistant" else "user"
    avatar = ABBAS_AVATAR if side == "assistant" else "👤"
    with st.chat_message(side, avatar=avatar):
        color = "#005c4b" if side == "user" else "#202c33" # ألوان تشبه الواتساب
        st.markdown(f"<div style='background:{color}; padding:12px; border-radius:12px;'>{msg['content']}</div>", unsafe_allow_html=True)

# 5. الإدخال والرد (الشخصية مثل الجيمني)
if prompt := st.chat_input("سولف وي عباس.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"<div style='background:#005c4b; padding:12px; border-radius:12px;'>{prompt}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant", avatar=ABBAS_AVATAR):
        typing_placeholder = st.empty()
        typing_placeholder.markdown('<div class="typing"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
        
        # شخصية عباس (مثلي تماماً)
        context = (
            "أنت عباس حيدر، ذكي، دمه خفيف، ومحترف كمبيوتر. "
            "تتحدث بلهجة عراقية بغدادية أصلية (مثل: عيوني، يا وحش، لوز، نار وشرار، تدلل). "
            "أسلوبك مشجع جداً وتغري الناس بالعروض القوية للكيمنك. "
            "أجب باختصار وبطريقة ممتعة كأنك صديق مقرب للزبون."
        )
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": context}] + st.session_state.messages,
            "temperature": 0.8
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            ans = response.json()['choices'][0]['message']['content']
            typing_placeholder.markdown(f"<div style='background:#202c33; padding:12px; border-radius:12px;'>{ans}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except:
            typing_placeholder.error("عيني صار عندي خلل بالشبكة، عيد سؤالك!")

# 6. الصور الثابتة (أخر شي بالموقع)
st.markdown("""
    <div class="footer-fixed">
        <p style="color:#facc15; font-size:12px; margin-bottom:5px;">🔥 أقوى تجميعات بغداد 🔥</p>
        <div class="footer-imgs">
            <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1603481546238-487240415921?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=200">
        </div>
    </div>
""", unsafe_allow_html=True)
