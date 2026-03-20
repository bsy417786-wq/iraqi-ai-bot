import streamlit as st
import requests

# 1. إعدادات الصفحة والتصميم الجمالي (CSS)
st.set_page_config(page_title="عباس حيدر للابتوبات", page_icon="💻", layout="centered")

custom_css = """
    <style>
    /* إخفاء القوائم المزعجة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* تغيير خلفية الموقع */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }
    
    /* تنسيق فقاعات الدردشة */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
        padding: 10px;
    }
    
    /* تجميل خطوط الكتابة */
    h1, h2, h3, p {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
    }
    
    /* تنسيق صندوق الإدخال */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 2. عرض اللوجو مالتك (تأكد من اسم الملف بالـ GitHub يكون logo.jpg)
# ملاحظة: إذا رفعت الصورة بنفس المجلد، استخدم اسمها مباشرة
try:
    st.image("Gemini_Generated_Image_xhf51axhf51axhf5.jpg", width=250)
except:
    st.image("https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png", width=250) # رابط احتياطي

st.markdown("<h2 style='color: #38bdf8;'>أهلاً بيك في عالم اللابتوبات</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>عباس حيدر - خبيرك التقني في بغداد</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. الأمان (المفتاح مالتك)
API_KEY = "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"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة بستايل حلو
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطق الدردشة
if prompt := st.chat_input("اسأل عباس حيدر عن أي لابتوب.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {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}",
        "Content-Type": "application/json"
    }
    
    context = (
        "أنت عباس حيدر، صاحب محل لابتوبات بالكرادة. "
        "ردك لازم يكون بغدادي حار ومحترم (هله بعيوني، تدلل، خادم، ما يصير خاطرك إلا طيب). "
        "ممنوع الفصحى. خليك شاطر بالمبيعات وانطي عروض مغرية."
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
        with st.spinner("عباس ديشيك المخزن..."):
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            answer = result['choices'][0]['message']['content']
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except:
        st.error("عيوني السيرفر شوية تعبان، ثواني وارجع.")
