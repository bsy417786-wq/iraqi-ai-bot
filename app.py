import streamlit as st
import requests

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="عباس حيدر | TECH MASTER", page_icon="🔥", layout="centered")

design = """
    <style>
    /* إخفاء أدوات ستريمليت نهائياً */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"] { visibility: hidden; display: none !important; }
    
    /* خلفية تقنية (Midnight Blue Gradient) */
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
        margin-top: -20px;
    }

    /* فقاعات الدردشة (Neon Cyber) */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(12px);
        margin-bottom: 20px !important;
    }
    
    [data-testid="stChatMessage"] p {
        color: #f1f5f9 !important;
        font-size: 17px !important;
        line-height: 1.6;
    }

    /* الفوتر بالزوايا */
    .f-left { position: fixed; bottom: 20px; left: 20px; color: #38bdf8; font-size: 13px; font-weight: bold; z-index: 100; }
    .f-right { position: fixed; bottom: 20px; right: 20px; color: #38bdf8; font-size: 13px; font-weight: bold; z-index: 100; text-align: right; }
    
    .stChatInputContainer { padding-bottom: 80px; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهيدر (صورة احترافية وعنوان)
st.image("https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
st.markdown('<div class="glitch-title">سولف وي عباس حيدر</div>', unsafe_allow_html=True)

# 3. الفوتر (المعلومات)
st.markdown("""
    <div class="f-left">📍 بغداد - الكرادة - شارع الصناعة<br>📞 07700000000</div>
    <div class="f-right">🚀 لابتوبك يمنه.. والضمان بجيبك<br>© 2026 ABBAS HAIDER</div>
""", unsafe_allow_html=True)

# 4. روابط الأفاتار والمفتاح
MY_KEY = "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"
ABBAS_AVATAR = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"
USER_AVATAR = "👤"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. منطق الدردشة
if prompt := st.chat_input("اسأل عباس حيدر عن اللابتوبات..."):
    # ترتيب طبيعي: رسالتك تضاف للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
    
    context = (
        "أنت عباس حيدر، المستشار التقني الأول في العراق. تحدث بالفصحى الراقية. "
        "قدم مواصفات دقيقة بأسلوب احترافي جداً."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages,
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        answer = result['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except:
        st.error("خطأ في الاتصال بالسيرفر..")

# 6. العرض بالترتيب الطبيعي (رسالتك ثم رد عباس)
for message in st.session_state.messages:
    is_assistant = message["role"] == "assistant"
    avatar = ABBAS_AVATAR if is_assistant else USER_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        label = "عباس حيدر" if is_assistant else "أنت"
        color = "#38bdf8" if is_assistant else "#facc15"
        st.markdown(f"<strong style='color:{color};'>{label}:</strong>", unsafe_allow_html=True)
        st.markdown(message["content"])
