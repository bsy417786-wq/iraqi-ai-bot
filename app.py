import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="اسأل عباس حيدر", page_icon="🎮", layout="centered")

design = """
    <style>
    /* إخفاء كل زوائد ستريمليت والـ Manage app */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"], div[data-testid="stDecoration"], [data-testid="stStatusWidget"], iframe[title="manage-app"] { 
        visibility: hidden; display: none !important; 
    }

    /* خلفية مريحة للعين (Deep Navy) */
    .stApp { background: #0f172a; color: #f1f5f9; }

    .main-header {
        color: #38bdf8; font-size: 40px; font-weight: 800;
        text-align: center; margin-top: -30px; letter-spacing: 1px;
    }
    
    [data-testid="stChatMessage"] {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
    }

    /* تثبيت الصور والفوتر بالأسفل */
    .fixed-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #0f172a;
        padding: 10px 0;
        z-index: 999;
        border-top: 2px solid #1e293b;
    }

    .footer-content {
        display: flex;
        justify-content: center;
        gap: 15px;
        padding: 0 10px;
    }

    .footer-img {
        width: 120px;
        height: 70px;
        object-fit: cover;
        border-radius: 8px;
        border: 1px solid #38bdf8;
    }

    /* مسافة أمان للمحادثة حتى لا تختفي وراء الفوتر */
    .stChatContainer { padding-bottom: 200px !important; }
    
    /* أنيميشن النقاط (Typing) */
    .typing { display: flex; align-items: center; gap: 5px; padding: 5px; }
    .dot { width: 6px; height: 6px; background: #38bdf8; border-radius: 50%; animation: blink 1.4s infinite both; }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes blink { 0% { opacity: 0.2; } 20% { opacity: 1; } 100% { opacity: 0.2; } }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية
st.markdown('<div class="main-header">اسأل عباس حيدر</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#94a3b8; margin-bottom:20px;">خبير الكمبيوتر والكيمنك الأول في بغداد</p>', unsafe_allow_html=True)

# 3. المفتاح والذاكرة
MY_KEY = "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"
ABBAS_AVATAR = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"
USER_AVATAR = "👤"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة
for message in st.session_state.messages:
    is_assistant = message["role"] == "assistant"
    avatar = ABBAS_AVATAR if is_assistant else USER_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        label = "عباس حيدر" if is_assistant else "أنت"
        color = "#38bdf8" if is_assistant else "#facc15"
        st.markdown(f"<strong style='color:{color};'>{label}:</strong><br>{message['content']}", unsafe_allow_html=True)

# 5. منطق الإدخال
if prompt := st.chat_input("اسأل عباس عن تجميعات الكيمنك أو اللابتوبات..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(f"<strong style='color:#facc15;'>أنت:</strong><br>{prompt}", unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar=ABBAS_AVATAR):
        st.markdown(f"<strong style='color:#38bdf8;'>عباس حيدر:</strong>", unsafe_allow_html=True)
        typing_placeholder = st.empty()
        typing_placeholder.markdown('<div class="typing"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
        
        context = (
            "أنت عباس حيدر، خبير كمبيوترات وكيمنك في بغداد. لهجتك عراقية بغدادية محترمة. "
            "اختصاصك فقط الكمبيوتر. إذا سألك عن غير شي اعتذر بذكاء وگول اختصاصي بس لابتوبات. "
            "أغري الزبون بعروض الكيمنك والقطع القوية وانصحه كأخ."
        )
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": context}] + st.session_state.messages,
            "temperature": 0.6
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            answer = result['choices'][0]['message']['content']
            typing_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except:
            typing_placeholder.error("السيرفر مشغول شوية عيوني..")

# 6. الفوتر الثابت بالأسفل (الصور)
footer_html = f"""
    <div class="fixed-footer">
        <div style="text-align:center; color:#facc15; font-size:13px; font-weight:bold; margin-bottom:5px;">
            🎮 عروض الكيمنك والاحتراف بانتظارك 🎮
        </div>
        <div class="footer-content">
            <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=200" class="footer-img">
            <img src="https://images.unsplash.com/photo-1603481546238-487240415921?q=80&w=200" class="footer-img">
            <img src="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=200" class="footer-img">
        </div>
        <div style="text-align:center; color:#94a3b8; font-size:10px; margin-top:5px;">
            📍 بغداد - الصناعة | 📞 07700000000 | © 2026 ABBAS HAIDER
        </div>
    </div>
"""
st.markdown(footer_html
