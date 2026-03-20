import streamlit as st
import requests

# 1. إعدادات الصفحة والستايل (كحلي ملكي وأبيض ذهبي)
st.set_page_config(page_title="سولف وي عباس حيدر", page_icon="💻", layout="centered")

design = """
    <style>
    /* إخفاء زوائد ستريمليت */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
    /* الخلفية: كحلي بالأعلى يتدرج للأبيض */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 35%, #f8fafc 100%);
        background-attachment: fixed;
    }
    
    /* المقدمة (سولف وي عباس حيدر) */
    .header-text {
        text-align: center;
        color: #facc15;
        font-size: 50px;
        font-weight: 900;
        padding-top: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .sub-header {
        text-align: center;
        color: #cbd5e1;
        font-size: 18px;
        margin-bottom: 30px;
    }

    /* الدردشة في الجزء العلوي */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.98) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        color: #1e293b !important;
    }

    /* الفوتر (المعلومات بالأسفل) */
    .footer-left {
        position: fixed;
        bottom: 15px;
        left: 20px;
        color: #475569;
        font-size: 13px;
        text-align: left;
        line-height: 1.4;
        z-index: 100;
    }
    
    .footer-right {
        position: fixed;
        bottom: 15px;
        right: 20px;
        color: #b8860b;
        font-size: 15px;
        font-weight: 600;
        font-style: italic;
        z-index: 100;
    }

    /* تحسين صندوق الإدخال */
    .stChatInputContainer {
        padding-bottom: 80px;
    }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. المقدمة (Header)
st.markdown('<div class="header-text">سولف وي عباس حيدر</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">مستشارك التقني الأول في العراق</div>', unsafe_allow_html=True)

# 3. الفوتر (المعلومات والعنوان)
# ملاحظة: غير الأرقام لرقك الحقيقي إذا حبيت
st.markdown("""
    <div class="footer-left">
        📍 بغداد - الكرادة - شارع الصناعة<br>
        📞 07700000000
    </div>
    <div class="footer-right">
        "لابتوبك يمنه.. والضمان بجيبك"
    </div>
""", unsafe_allow_html=True)

# 4. المفتاح والدردشة
MY_KEY = "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"
AVATAR_LINK = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = AVATAR_LINK if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 5. منطق الرد (بالفصحى الرزنة)
if prompt := st.chat_input("تفضل، كيف يمكن لـ عباس حيدر مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
    
    context = (
        "أنت عباس حيدر، خبير لابتوبات محترف. تحدث باللغة العربية الفصحى حصراً. "
        "كن رسمياً، مهذباً، ودقيقاً جداً في وصف الأجهزة."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}, *st.session_state.messages],
        "temperature": 0.3
    }

    try:
        with st.spinner("لحظات من فضلك..."):
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            answer = result['choices'][0]['message']['content']
            
            with st.chat_message("assistant", avatar=AVATAR_LINK):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    except:
        st.error("عذراً، النظام مشغول حالياً.")
