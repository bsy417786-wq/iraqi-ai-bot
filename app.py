import streamlit as st
import requests

# 1. إعدادات الصفحة والستايل الجديد
st.set_page_config(page_title="عباس حيدر للابتوبات", page_icon="💻", layout="centered")

design = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stToolbar"] {display: none;}
    
    /* لون الواجهة الجديد - أزرق غامق ملكي */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* تنسيق النصوص */
    .main-title { color: #38bdf8; font-size: 40px; font-weight: bold; margin-bottom: 5px; text-align: center; }
    .sub-info { color: #94a3b8; font-size: 16px; margin-bottom: 2px; text-align: center; }
    .catch-phrase { color: #facc15; font-size: 18px; font-weight: 500; margin-top: 10px; text-align: center; font-style: italic; }
    
    /* فقاعات الدردشة */
    [data-testid="stChatMessage"] { border-radius: 15px !important; }
    [data-testid="stChatMessageUser"] { background-color: #1d4ed8 !important; }
    [data-testid="stChatMessageAssistant"] { background-color: #334155 !important; }
    
    .stImage img { border-radius: 50%; border: 3px solid #38bdf8; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. قسم الهوية (اللوجو والمعلومات)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("Gemini_Generated_Image_xhf51axhf51axhf5.jpg", width=180)
    except:
        st.image("https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png", width=180)

# الكتابة اللي ردتها
st.markdown('<div class="main-title">عباس حيدر</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-info">📍 بغداد - الكرادة - شارع الصناعة</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-info">📞 07700000000</div>', unsafe_allow_html=True) # غير الرقم لرقك الحقيقي
st.markdown('<div class="catch-phrase">"لابتوبك يمنه.. والضمان بجيبك"</div>', unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #334155; margin: 20px 0;'>", unsafe_allow_html=True)

# 3. المفتاح والرسائل
MY_KEY = "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"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطق الدردشة
if prompt := st.chat_input("اسأل عباس حيدر.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
    
    context = (
        "أنت عباس حيدر، صاحب محل لابتوبات بالكرادة. ردك بغدادي محترم ورزن. "
        "ممنوع الفصحى والرموز الغريبة. بيع بذكاء وبثقة."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}, *st.session_state.messages],
        "temperature": 0.5
    }

    try:
        with st.spinner("ثواني عيوني..."):
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            answer = result['choices'][0]['message']['content']
            
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    except:
        st.error("السيرفر مزدحم، ارجع اسألني عيوني.")
