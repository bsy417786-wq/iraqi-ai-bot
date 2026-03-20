import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="اسئل عباس", page_icon="💻", layout="centered")

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
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 35%, #ffffff 100%);
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
        background-color: rgba(255, 255, 255, 1.0) !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        margin-bottom: 15px !important;
    }
    
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] div {
        color: #000000 !important;
        font-weight: 500 !important;
        font-size: 17px !important;
    }

    .footer-left { position: fixed; bottom: 20px; left: 20px; color: #1e293b; font-size: 13px; font-weight: bold; z-index: 100; }
    .footer-right { position: fixed; bottom: 20px; right: 20px; color: #b8860b; font-size: 15px; font-weight: 900; font-style: italic; z-index: 100; }

    .stChatInputContainer { padding-bottom: 80px; }
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

# 3. المفتاح والروابط
MY_KEY = "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"
ABBAS_AVATAR = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"
USER_AVATAR = "👤"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. منطق الدردشة (الرسالة بالأعلى والرد تحتها)
if prompt := st.chat_input("تفضل، اسأل عباس حيدر.."):
    # إضافة رسالة المستخدم في نهاية الذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
    
    context = (
        "أنت عباس حيدر، مستشار تقني محترف في بغداد. تحدث باللغة العربية الفصحى حصراً. "
        "كن رسمياً ومختصراً ودقيقاً جداً في وصف الأجهزة."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages,
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        if 'choices' in result:
            answer = result['choices'][0]['message']['content']
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("عذراً، تأكد من مفتاح API.")
    except Exception as e:
        st.error(f"خطأ في الاتصال: {str(e)}")

# 5. عرض المحادثة بالترتيب الطبيعي
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar=ABBAS_AVATAR):
            st.markdown(f"**عباس حيدر:** {message['content']}")
    else:
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(f"**أنت:** {message['content']}")
