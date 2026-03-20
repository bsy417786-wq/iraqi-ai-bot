import streamlit as st
import requests

# 1. إعدادات الواجهة (Dark Mode وتصميم بغدادي حديث)
st.set_page_config(page_title="عباس حيدر للابتوبات", page_icon="💻", layout="centered")

# تصميم الـ CSS لإخفاء أدوات ستريمليت وتجميل الفقاعات
design = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stToolbar"] {display: none;}
    
    .stApp {
        background: radial-gradient(circle, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
    }
    
    [data-testid="stChatMessage"] {
        border-radius: 20px !important;
        margin: 10px 0px !important;
    }
    
    [data-testid="stChatMessageUser"] {
        background-color: #1e40af !important;
        border: 1px solid #3b82f6;
    }

    [data-testid="stChatMessageAssistant"] {
        background-color: #334155 !important;
        border: 1px solid #475569;
    }

    .stImage img {
        border-radius: 20px;
        border: 2px solid #38bdf8;
    }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. عرض اللوجو والترحيب
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        # يحاول يقرأ صورتك المرفوعة
        st.image("Gemini_Generated_Image_xhf51axhf51axhf5.jpg")
    except:
        # رابط احتياطي في حال عدم وجود الصورة
        st.image("https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png")

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>💻 عباس حيدر للمبيعات</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>خبير اللابتوبات والذكاء الاصطناعي في بغداد</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #334155;'>", unsafe_allow_html=True)

# 3. المفتاح مالتك (تم وضعه بشكل صحيح كـ نص)
MY_KEY = "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"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطق الدردشة
if prompt := st.chat_input("اسأل عباس حيدر.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MY_KEY}",
        "Content-Type": "application/json"
    }
    
    # تعريف شخصية عباس حيدر (السيستم برومبت)
    context = (
        "أنت عباس حيدر، صاحب محل لابتوبات بالكرادة، بغداد. "
        "رد بلهجة بغدادية محترمة وحارة (هله بيك، عيوني، خادم، تدلل، ما يصير خاطرك إلا طيب). "
        "ممنوع الفصحى نهائياً. بيع لابتوبات بذكاء وانطي مواصفات قوية وأسعار بالدينار العراقي."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": context},
            *st.session_state.messages
        ],
        "temperature": 0.7
    }

    try:
        with st.spinner("لحظة عيوني أشوفلك المخزن..."):
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            if 'choices' in result:
                answer = result['choices'][0]['message']['content']
                with st.chat_message("assistant"):
                    st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("عيوني اكو مشكلة فنية بسيطة، جرب مرة ثانية.")
    except:
        st.error("السيرفر مزدحم حالياً، ثواني وارجع اسألني.")
