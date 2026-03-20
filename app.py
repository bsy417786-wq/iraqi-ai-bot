import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="اسأل عباس حيدر", page_icon="🎮", layout="centered")

design = """
    <style>
    /* إخفاء زوائد ستريمليت والـ Manage app */
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
        st
