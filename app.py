import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="عباس حيدر للابتوبات", page_icon="💻", layout="centered")

# 2. تصميم الواجهة (هنا التغيير الحقيقي - CSS احترافي)
design = """
    <style>
    /* إخفاء كل شي يخص ستريمليت */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* خلفية فخمة متدرجة */
    .stApp {
        background: radial-gradient(circle, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* تجميل فقاعات الدردشة */
    [data-testid="stChatMessage"] {
        background-color: #334155 !important;
        border: 1px solid #475569;
        border-radius: 20px !important;
        padding: 15px !important;
        margin: 10px 0px !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    /* تمييز رسائل الزبون */
    [data-testid="stChatMessageUser"] {
        background-color: #1e40af !important;
        border: 1px solid #3b82f6;
    }

    /* تجميل الخطوط */
    .stMarkdown p {
        font-size: 18px !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* اللوجو */
    .stImage img {
        border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        border: 2px solid #38bdf8;
    }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 3. عرض اللوجو مالتك (تأكد من وجود الملف بـ GitHub)
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("Gemini_Generated_Image_xhf51axhf51axhf5.jpg")
    except:
        st.image("https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png")

st.markdown("<h1 style='color: #38bdf8; text-shadow: 2px 2px #000;'>💻 عباس حيدر للمبيعات</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-style: italic;'>خبير اللابتوبات الأول في بغداد - الكرادة</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #334155;'>", unsafe_allow_html=True)

# 4. المفتاح والذاكرة
API_KEY = "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"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق الدردشة
if prompt := st.chat_input("اسأل عباس حيدر عن أي لابتوب.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {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}", "Content-Type": "application/json"}
    
    context = (
        "أنت عباس حيدر، صاحب محل لابتوبات بالكرادة. ردك بغدادي حار (هله بعيوني، تدلل، خادم، ما يصير خاطرك إلا طيب). "
        "احجي بذكاء عن اللابتوبات ولا تستخدم الفصحى نهائياً. بيع لابتوبات وانطي مواصفات قوية."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}, *st.session_state.messages],
        "temperature": 0.8
    }

    try:
        with st.spinner("عباس ديشيك القائمة..."):
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            answer = result['choices'][0]['message']['content']
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except:
        st.error("عيوني اكو ضغط، ارجع اسألني ثواني.")
