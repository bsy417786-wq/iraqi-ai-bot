import streamlit as st
import requests

# 1. إعدادات الصفحة والستايل الجديد (Anti-Black Design)
st.set_page_config(page_title="عباس حيدر | Tech Advisor", page_icon="💻", layout="centered")

design = """
    <style>
    /* إخفاء كل أدوات ستريمليت واليوزر تماماً */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
    /* خلفية بيضاء لؤلؤية مع تدرج معدني - لا يوجد أسود نهائياً */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        color: #2c3e50;
    }
    
    /* تنسيق العنوان بالذهب الملكي */
    .main-title { 
        background: linear-gradient(90deg, #b8860b, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px; font-weight: 900; text-align: center; margin-bottom: 5px;
    }
    
    .sub-info { color: #7f8c8d; font-size: 14px; text-align: center; font-weight: 500; letter-spacing: 1px; }
    .catch-phrase { color: #b8860b; font-size: 16px; text-align: center; margin-top: 8px; font-weight: 600; }

    /* تصميم الفقاعات بستايل Glassmorphism فاتح */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
        color: #2c3e50 !important;
    }
    
    /* تمييز رسالة المستخدم بلون ذهبي ناعم */
    [data-testid="stChatMessageUser"] {
        background: rgba(212, 175, 55, 0.1) !important;
        border-right: 5px solid #d4af37 !important;
    }

    /* تنسيق صندوق الإدخال ليكون أبيض وأنيق */
    .stChatInputContainer {
        background-color: transparent !important;
        padding-bottom: 40px;
    }
    
    input {
        background-color: white !important;
        color: #2c3e50 !important;
        border: 1px solid #d4af37 !important;
    }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية البصرية (بدون صورة اللابتوبات اللي بالبداية)
st.markdown('<div class="main-title">عباس حيدر</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-info">📍 BAGHDAD | TECHNOLOGY CONSULTANT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-info">📞 07700000000</div>', unsafe_allow_html=True)
st.markdown('<div class="catch-phrase">"نحو رؤية تقنية متجددة"</div>', unsafe_allow_html=True)
st.markdown("<hr style='border: 0.1px solid rgba(212,175,55,0.3); margin: 30px 0;'>", unsafe_allow_html=True)

# 3. المفتاح ورابط الأفاتار (استخدام رابط اللوجو كأفاتار)
MY_KEY = "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"
AVATAR_LINK = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar=AVATAR_LINK):
            st.markdown(message["content"])
    else:
        with st.chat_message("user"):
            st.markdown(message["content"])

# 4. منطق الدردشة (فصحى رسمية جداً)
if prompt := st.chat_input("بمَ يمكننا خدمتكم اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
    
    context = (
        "أنت عباس حيدر، خبير استراتيجي في تقنيات الحاسوب. "
        "تحدث باللغة العربية الفصحى الراقية. كن صريحاً، دقيقاً، واحترافياً لأقصى درجة. "
        "قدم النصائح التقنية بناءً على أحدث معايير السوق العالمي."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}, *st.session_state.messages],
        "temperature": 0.3
    }

    try:
        with st.spinner("جاري التحليل الفني..."):
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            answer = result['choices'][0]['message']['content']
            
            with st.chat_message("assistant", avatar=AVATAR_LINK):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    except:
        st.error("عذراً، تعذر الاتصال بالنظام حالياً.")
