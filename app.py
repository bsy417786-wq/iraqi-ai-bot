import streamlit as st
import requests

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="عباس حيدر | TECH MASTER", page_icon="🔥", layout="centered")

design = """
    <style>
    /* إخفاء أدوات ستريمليت نهائياً */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"] { visibility: hidden; display: none !important; }
    
    /* خلفية تقنية متحركة (Matrix-Style Blue) */
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #000000 100%);
        color: #ffffff;
    }

    /* تأثير الوهج للعنوان */
    .glitch-title {
        color: #38bdf8;
        font-size: 50px;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
        margin-top: -50px;
    }

    /* فقاعات الدردشة (Glassmorphism & Neon) */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(12px);
        margin-bottom: 20px !important;
        transition: 0.4s;
    }
    
    [data-testid="stChatMessage"]:hover {
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    }

    /* لون الخط داخل الفقاعات (أبيض ساطع للوضوح) */
    [data-testid="stChatMessage"] p {
        color: #f1f5f9 !important;
        font-size: 17px !important;
        line-height: 1.6;
    }

    /* صورة البروفايل (تأثير دائري مضيء) */
    [data-testid="stChatMessageAvatar"] img {
        border: 2px solid #38bdf8;
        box-shadow: 0 0 10px #38bdf8;
    }

    /* الفوتر (العناوين بالزوايا) */
    .footer-box {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: rgba(15, 23, 42, 0.9);
        padding: 10px 0;
        border-top: 1px solid #38bdf8;
        z-index: 1000;
    }
    .f-left { position: fixed; bottom: 15px; left: 20px; color: #38bdf8; font-size: 13px; font-weight: bold; }
    .f-right { position: fixed; bottom: 15px; right: 20px; color: #38bdf8; font-size: 13px; font-weight: bold; }
    
    /* تصميم صندوق الإدخال */
    .stChatInputContainer { padding-bottom: 80px; }
    input { background-color: #0f172a !important; color: white !important; border: 1px solid #38bdf8 !important; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهيدر (صور اللابتوبات الاحترافية)
st.image("https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
st.markdown('<div class="glitch-title">اسئل عباس حيدر</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>EXPERT LAPTOP SOLUTIONS | BAGHDAD</p>", unsafe_allow_html=True)

# 3. الفوتر والمعلومات
st.markdown(f"""
    <div class="f-left">📍 بغداد - الكرادة - شارع الصناعة<br>📞 07700000000</div>
    <div class="f-right">🚀 لابتوبك يمنه.. والضمان بجيبك<br>© 2026 ABBAS HAIDER</div>
""", unsafe_allow_html=True)

# 4. الروابط والمفاتيح
MY_KEY = "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"
ABBAS_AVATAR = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"
USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/3177/3177440.png"

if "messages" not in st.
