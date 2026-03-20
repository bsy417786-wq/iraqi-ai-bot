import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="سولف وي عباس حيدر", page_icon="💻", layout="centered")

design = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 35%, #f8fafc 100%);
        background-attachment: fixed;
    }
    
    .header-text {
        text-align: center;
        color: #facc15;
        font-size: 45px;
        font-weight: 900;
        padding-top: 10px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        color: #1e293b !important;
    }

    /* الفوتر أسفل اليسار واليمين */
    .footer-left { position: fixed; bottom: 20px; left: 20px; color: #475569; font-size: 13px; z-index: 100; }
    .footer-right { position: fixed; bottom: 20px; right: 20px; color: #b8860b; font-size: 15px; font-weight: 600; font-style: italic; z-index: 100; }

    /* جعل صندوق الإدخال ثابت بالأسفل */
    .stChatInputContainer { padding-bottom: 70px; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. المقدمة والفوتر
st.markdown('<div class="header-text">سولف وي عباس حيدر</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="footer-left">
        📍 بغداد - الكرادة - شارع الصناعة<br>
        📞 07700000000
    </div>
    <div class="footer-right">
        "لابتوبك يمنه.. والضمان بجيبك"
    </div>
""", unsafe_allow_html=True)

# 3. المفتاح والذاكرة
MY_KEY = "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"
AVATAR_LINK = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. منطق الإدخال (قبل عرض الرسائل حتى تطلع الرسالة الجديدة أول وحدة)
if prompt := st.chat_input("تفضل، اسأل عباس حيدر.."):
    # إضافة رسالة المستخدم للذاكرة
    st.session_state.messages.insert(0, {"role": "user", "content": prompt})
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
    
    context = (
        "أنت عباس حيدر، مستشار تقني محترف في بغداد. تحدث باللغة العربية الفصحى حصراً. "
        "كن رسمياً ومختصراً ودقيقاً."
    )
    
    # نرسل الرسائل بالترتيب الصحيح للذكاء الاصطناعي (من الأقدم للأحدث)
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages[::-1],
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        answer = result['choices'][0]['message']['content']
        # إضافة رد عباس في بداية القائمة لتظهر بالأعلى
        st.session_state.messages.insert(0, {"role": "assistant", "content": answer})
    except:
        st.error("عذراً، حدث خطأ في الاتصال.")

# 5. عرض المحادثة (الرسائل تظهر من الأحدث للأقدم - يعني الجديدة فوك)
for message in st.session_state.messages:
    avatar = AVATAR_LINK if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
