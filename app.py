import streamlit as st
import requests

# 1. إخفاء كل أدوات Streamlit (التشفير البصري)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            div[data-testid="stToolbar"] {display: none;}
            </style>
            """
st.set_page_config(page_title="عباس حيدر للابتوبات", page_icon="💻", layout="centered")

# هنا التصحيح: استخدمنا unsafe_allow_html بدل config
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. عرض اللوجو (حاول ترفع صورتك على موقع مثل imgbb وتحط الرابط هنا)
st.image("https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png", width=150)
st.title("💻 عباس حيدر للمبيعات")
st.markdown("<p style='text-align: center; color: gray;'>خبير اللابتوبات الأول في بغداد</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. الأمان (استخدام Secrets للتشفير)
# ملاحظة: إذا ردت تشفر المفتاح، حطه بالـ Secrets بموقع Streamlit
# هسة راح أحطه مباشرة بس تأكد تبدله بمفتاحك الشغال
API_KEY = "gsk_حط_مفتاح_GROQ_هنا"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة (الذاكرة)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تفضل عيوني اسألني.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # إعداد الطلب لسيرفر Groq
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {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}",
        "Content-Type": "application/json"
    }
    
    # شخصية عباس حيدر البغدادي (السيستم برومبت)
    context = (
        "أنت عباس حيدر، صاحب محل لابتوبات بالكرادة، بغداد. "
        "رد بلهجة بغدادية قوية ومرحة (هله بيك، عيوني، خادم، تدلل، ما يصير خاطرك إلا طيب). "
        "ممنوع تحجي فصحى نهائياً. "
        "الأسعار تبدأ من 150 ألف صعوداً والتوصيل مجاني لبغداد. "
        "إذا سألوك عن شي خارج اللابتوبات، اعتذر بلطافة وكولهم 'أنا اختصاصي بس لابتوبات عيوني'."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": context},
            *st.session_state.messages # الذاكرة
        ],
        "temperature": 0.6
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if 'choices' in result:
            answer = result['choices'][0]['message']['content']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("عيوني، اكو مشكلة بالمفتاح أو السيرفر.")
    except Exception as e:
        st.error("ثواني وارجع اسألني، السيرفر عليه لود.")
