import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="اسأل عباس حيدر", page_icon="🎮", layout="centered")

design = """
    <style>
    /* إخفاء زوائد ستريمليت */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"], div[data-testid="stDecoration"], [data-testid="stStatusWidget"], iframe[title="manage-app"] { 
        visibility: hidden; display: none !important; 
    }

    /* خلفية مريحة للعين */
    .stApp { background: #0f172a; color: #f1f5f9; }

    .main-header {
        color: #38bdf8; font-size: 38px; font-weight: 800;
        text-align: center; margin-top: -30px;
    }
    
    /* سحر الظهور التدريجي (Fade-in Animation) */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stChatMessage"] {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 15px !important;
        margin-bottom: 12px !important;
        animation: fadeIn 0.5s ease-out forwards; /* تطبيق التأثير هنا */
    }

    /* رفع صندوق الكتابة فوق الصور */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 180px !important;
        z-index: 1001 !important;
        background: #1e293b !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 15px !important;
        padding: 5px !important;
    }

    /* تثبيت قسم الصور بالأسفل */
    .fixed-footer-box {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #0f172a;
        padding: 15px 0;
        z-index: 1000;
        border-top: 1px solid #38bdf8;
        text-align: center;
    }

    .footer-images-container {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-bottom: 5px;
    }

    .footer-images-container img {
        width: 130px; height: 80px; object-fit: cover;
        border-radius: 10px; border: 2px solid #38bdf8;
    }

    .stChatContainer { padding-bottom: 320px !important; }

    /* أنيميشن النقاط */
    .typing { display: flex; align-items: center; gap: 5px; padding: 5px; }
    .dot { width: 6px; height: 6px; background: #38bdf8; border-radius: 50%; animation: blink 1.4s infinite both; }
    @keyframes blink { 0% { opacity: 0.2; } 20% { opacity: 1; } 100% { opacity: 0.2; } }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية
st.markdown('<div class="main-header">اسأل عباس حيدر</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#94a3b8; margin-bottom:10px;">خبير الكيمنك والقطع القوية في بغداد</p>', unsafe_allow_html=True)

# 3. المفتاح والذاكرة
MY_KEY = "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"
ABBAS_AVATAR = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"
USER_AVATAR = "👤"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة (مع تأثير الظهور)
for message in st.session_state.messages:
    is_assistant = message["role"] == "assistant"
    avatar = ABBAS_AVATAR if is_assistant else USER_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        label = "عباس حيدر" if is_assistant else "أنت"
        color = "#38bdf8" if is_assistant else "#facc15"
        st.markdown(f"<strong style='color:{color};'>{label}:</strong><br>{message['content']}", unsafe_allow_html=True)

# 5. منطق الإدخال والرد
if prompt := st.chat_input("اكتب سؤالك هنا لـ عباس..."):
    st.session_state.messages.append({"role": "user", "content": prompt
